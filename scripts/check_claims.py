#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""作品集口径自动校验 (portfolio claims checker).

为什么要有这个东西
------------------
作品集跨 8 个仓库、几十份文档 + 一个线上看板，口径靠人肉对齐必然出错。
已真实发生过的三类事故：
  1) 公开仓库(bench)被写成「私有仓库 · 需授权访问」（与事实相反，且中英文 README 自相矛盾）
  2) bench 陷阱题数写成 23（真值 29）
  3) gh-pages 线上看板回退成 30 题 / 12 周（真值 112 题 / 14 周），差点推上去

设计原则
--------
1. **真实数字一律从源头文件反推**（questions.json / statutes.jsonl / status.json），
   绝不硬编码。源头变了，校验自动跟着变。
2. **只报确定错的**，不替人裁决 nuanced 表述（比如 KB 的 2327 vs 2337 都合理）。
3. **零第三方依赖**，Python 3.8+，CI 与本地都能跑。
4. **缺仓则跳过**——CI 里只挂 hub 也能跑，不会误报红。
5. 违规 -> exit 1，可直接阻断 CI / pre-commit。

用法
----
    python3 scripts/check_claims.py                    # 自动探测仓库
    python3 scripts/check_claims.py --root ~/WorkBuddy # 指定工作区根
    python3 scripts/check_claims.py --repo watch=/x/legal-ai-watch
    python3 scripts/check_claims.py --list-facts       # 只打印推导出的真实数字
    python3 scripts/check_claims.py --strict           # WARN 也当失败
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------- 仓库识别

REPO_KEYS = ("hub", "watch", "bench", "triangle", "kb", "lcb", "showcase")

REPO_DIR_NAMES = {
    "hub": "vickywu97-profile",
    "watch": "legal-ai-watch",
    "bench": "legal-hallucination-bench",
    "triangle": "compliance-triangle",
    "kb": "verified-chinese-law-kb",
    "lcb": "law-citation-bench",
    "showcase": "portfolio-showcase",
}

# 不在代码里写死任何本机绝对路径（这是公开仓库）。
# 仓库定位靠：① --repo key=path 显式指定；② --root 下自动发现（支持
# <root>/<repo> 与 <root>/<date>/<repo> 两种布局）；③ CI 下 root 本身即仓库。
# 找不到就跳过对应规则，不会误报红——见 discover()。

# 对外门面文档：题数/口径类规则只扫这些，避免扫到 changelog / 历史数据说明。
CLAIM_SURFACES = {
    "hub": ("README.md", "cv.html"),
    "watch": ("README.md",),
    "triangle": ("README.md", "README_EN.md"),
    "bench": ("README.md",),
    "showcase": ("index.html", "README.md"),
}


# ---------------------------------------------------------------- 工具

def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def read_json(path: Path):
    """读 json。文件不存在或内容非法一律返回 None——调用方依赖 None 做回退判断。"""
    if not path.is_file():
        return None
    try:
        return json.loads(read_text(path) or "{}")
    except (ValueError, TypeError):
        return None


def count_lines(path: Path) -> int:
    if not path.is_file():
        return -1
    n = 0
    with path.open("r", encoding="utf-8", errors="replace") as fh:
        for _ in fh:
            n += 1
    return n


def iter_text_files(root: Path):
    """遍历仓库里的 md / html（跳过 .git / 缓存 / 三方目录）。"""
    skip = {".git", "node_modules", "__pycache__", ".venv", "venv", "site-packages"}
    for p in sorted(root.rglob("*")):
        if not p.is_file():
            continue
        if any(part in skip for part in p.parts):
            continue
        if p.suffix.lower() in (".md", ".html", ".htm"):
            yield p


# ---------------------------------------------------------------- 事实推导

def derive_facts(repos: dict) -> dict:
    """从源头文件反推真实数字。缺仓则对应字段为 None。"""
    facts = {}

    # ---- watch ----
    watch = repos.get("watch")
    if watch:
        qj = read_json(watch / "config" / "questions.json") or {}
        qlist = qj.get("questions") or []
        facts["watch_questions"] = len(qlist)

        aj = read_json(watch / "config" / "article_texts.json") or {}
        arts = aj.get("article_texts") or {}
        facts["watch_articles"] = len(arts)
        facts["watch_uncovered"] = len(aj.get("_uncovered") or [])

        # 线上看板数据（gh-pages 分支的 status.json）
        st = read_json(watch / "status.json")
        if st is None:
            # 本地 main 上没有该目录时，尝试从 git 读 gh-pages 分支
            st = _git_show_json(watch, "origin/gh-pages:status.json")
        if isinstance(st, dict) and "questions" in st:
            facts["site_questions"] = st.get("questions")
            facts["site_weeks"] = st.get("history_weeks")

    # ---- bench ----
    bench = repos.get("bench")
    if bench:
        bq = read_json(bench / "questions.json") or {}
        facts["bench_questions"] = len(bq.get("questions") or [])
        facts["bench_verifications"] = count_lines(
            bench / "benchmark" / "reports" / "verifications.jsonl"
        )
        # bench 自带一份法条 KB（knowledge_base/laws/statutes.jsonl）。
        # 注意：这与 verified-chinese-law-kb 是两份不同的 KB，条数不同
        # （bench=2327/8 部法；kb 仓库=2337/9 模块含未发布的著作权法）。
        # 文档里引用的「2327 节点」指的都是 bench 这份，别拿 kb 仓库的数去比对。
        kb_file = bench / "knowledge_base" / "laws" / "statutes.jsonl"
        if kb_file.is_file():
            facts["bench_kb_nodes"] = count_lines(kb_file)

    # ---- kb ----
    kb = repos.get("kb")
    if kb:
        total = 0
        modules = 0
        for f in sorted(kb.rglob("*.jsonl")):
            if any(s in f.parts for s in ("__pycache__", ".git")):
                continue
            n = count_lines(f)
            if n > 0:
                total += n
                modules += 1
        facts["kb_nodes"] = total
        facts["kb_modules"] = modules

    # ---- lcb ----
    lcb = repos.get("lcb")
    if lcb:
        ds = lcb / "dataset" / "smoke_500.jsonl"
        if ds.is_file():
            facts["lcb_questions"] = count_lines(ds)

    return facts


def _git_show_json(repo: Path, spec: str):
    """用 git show 读某个 ref 下的 json（本地没有该分支工作区时）。"""
    import subprocess

    try:
        out = subprocess.run(
            ["git", "-C", str(repo), "show", spec],
            capture_output=True, text=True, timeout=30,
        )
        if out.returncode == 0 and out.stdout.strip():
            return json.loads(out.stdout)
    except Exception:
        pass
    return None


# ---------------------------------------------------------------- 规则

# 历史/演进语境标记：出现这些词说明该行在讲"从旧到新"，允许出现 legacy 数字。
HIST_MARKER = re.compile(
    r"→|->|=>|从\s*\d|由\s*\d|原|旧|历史|曾|扩|增至|升级|扩库|第二批|第三批"
    r"|baseline|基线|previously|prior|was\s+\d|legacy|v1\.\d",
    re.I,
)

# legacy 数字：只有在 HIST_MARKER 语境下才被容忍。
LEGACY = {
    "watch_questions": {31, 39, 63, 88},
    "bench_questions": {23},
    "kb_nodes": set(),
    "lcb_questions": set(),
}

NUM = r"(\d[\d,]*)"


def _nums(raw: str) -> list:
    out = []
    for m in re.findall(NUM, raw):
        try:
            out.append(int(m.replace(",", "")))
        except ValueError:
            pass
    return out


def rule_visibility(repos: dict) -> list:
    """R1: bench 为公开仓（LICENSE MIT），任何把它写成
    『私有 / 需授权访问 / Private』的"当前口径"表述都是错的。

    豁免：
    - CHANGELOG* 历史文件（记录的是各时间点的决策，非当前口径）
    - 同一行已写明"开源/open source/公开"，属对比或修正语境
    """
    bad = []
    bench_alias = re.compile(r"legal[-_]?hallucination[-_]?bench|hallucination[-_]?bench", re.I)
    private_re = re.compile(r"私有|需授权访问|access\s+on\s+request|Private\s*[—-]", re.I)
    public_re = re.compile(r"开源|open[\s\-]?source|公开|public", re.I)

    for key, repo in repos.items():
        if not repo:
            continue
        for f in iter_text_files(repo):
            # CHANGELOG 记录历史决策，不视为当前口径
            if str(f).split("/")[-1].upper().startswith("CHANGELOG"):
                continue
            for ln, line in enumerate(read_text(f).splitlines(), 1):
                mb = bench_alias.search(line)
                if not mb:
                    continue
                if not private_re.search(line):
                    continue
                # 同一行已写明正确口径(开源/公开) => 对比或修正语境，不算违规
                if public_re.search(line):
                    continue
                bad.append((
                    "FAIL", f, ln,
                    "bench(公开仓)被写成私有/需授权访问: ...%s..." % line.strip()[:110],
                ))
    return bad


def _scan_numbers(repos, fact_key, canonical, pattern, context_re, label,
                  scope, exclude_re=None):
    """通用数字口径扫描。

    scope      : 只扫哪些仓库的门面文档（避免拿 A 的规则去扫 B 的自述）
    context_re : 该行必须命中，才认为在讲这件事
    exclude_re : 命中则跳过（防止 hub 里 LCB 的 500 题被当成 watch 的题数）
    """
    bad = []
    pat = re.compile(pattern, re.I)
    ctx = re.compile(context_re, re.I)
    exc = re.compile(exclude_re, re.I) if exclude_re else None
    legacy = LEGACY.get(fact_key, set())
    if canonical is None:
        return bad

    for key in scope:
        repo = repos.get(key)
        if not repo:
            continue
        for name in CLAIM_SURFACES.get(key, ()):
            f = repo / name
            if not f.is_file():
                continue
            for ln, line in enumerate(read_text(f).splitlines(), 1):
                if not ctx.search(line):
                    continue
                if exc is not None and exc.search(line):
                    continue
                for m in pat.finditer(line):
                    for n in _nums(m.group(1)):
                        if n == canonical:
                            continue
                        if n in legacy and HIST_MARKER.search(line):
                            continue
                        bad.append((
                            "FAIL", f, ln,
                            "%s 口径错误: 文档写 %s，源头真值 %s（%s）"
                            % (label, n, canonical, line.strip()[:90]),
                        ))
    return bad


# 题/Questions 的数字模式。Q 后不能再跟数字，否则会把 "Q7 引已废止" 的 7 当成题数。
QTY = NUM + r"\s*(?:题|questions?|-Q|Q(?![0-9]))"


def rule_watch_questions(repos, facts):
    """watch 题数。只扫会声称 watch 题数的地方，并排除在讲别的制品的行。"""
    return _scan_numbers(
        repos, "watch_questions", facts.get("watch_questions"), QTY,
        context_re=r"watch|题库|常规引注|公开评测|引注评测|周更",
        label="watch 题库数",
        scope=("hub", "watch", "triangle"),
        # 这一行在讲 bench / LCB / 陷阱题 时不归本规则管
        exclude_re=r"陷阱题|trap\s*questions?|law-citation|LCB|引用准确率|legal-hallucination-bench",
    )


def rule_bench_questions(repos, facts):
    """bench 陷阱题数。真值 29；23 只在明确写了 baseline/基线等历史语境下容忍。"""
    return _scan_numbers(
        repos, "bench_questions", facts.get("bench_questions"),
        NUM + r"\s*(?:陷阱题|trap\s*questions?|traps?)",
        context_re=r"陷阱题|trap",
        label="bench 陷阱题数",
        scope=("hub", "triangle", "bench"),
    )


def rule_lcb_questions(repos, facts):
    return _scan_numbers(
        repos, "lcb_questions", facts.get("lcb_questions"), QTY,
        context_re=r"law-citation|citation|LCB|引文|引用准确率",
        label="LCB 题库数",
        scope=("hub", "lcb"),
        # "citation-evaluation" 这类词在 watch 语境里也常见，别把 watch 的 112 当成 LCB 的题数
        exclude_re=r"watch|legal-ai-watch|周更|weekly|dashboard|看板|常规引注",
    )


def rule_kb_nodes(repos, facts):
    """KB 节点数校验。

    关键事实（曾踩坑）：bench 自带的法条 KB（knowledge_base/laws/statutes.jsonl）
    是 2327 条 / 8 部法；verified-chinese-law-kb 是另一份、2337 条 / 9 模块
    （含未发布的著作权法 10 条）。对外文档里的「2327 节点」指的都是 bench 这份。
    因此本规则以 bench 的 KB 为准——写 2337 才是拿错了源。
    """
    bad = []
    total = facts.get("bench_kb_nodes")
    if total is None:
        return bad
    pat = re.compile(NUM + r"\s*(?:节点|nodes)", re.I)
    for key, names in CLAIM_SURFACES.items():
        repo = repos.get(key)
        if not repo:
            continue
        for name in names:
            f = repo / name
            if not f.is_file():
                continue
            for ln, line in enumerate(read_text(f).splitlines(), 1):
                for m in pat.finditer(line):
                    for n in _nums(m.group(1)):
                        if n == total:
                            continue
                        # 只有明显是 KB 规模(4 位数)才管，避免误伤 212 / 203 之类
                        if n < 1000:
                            continue
                        bad.append((
                            "WARN", f, ln,
                            "KB 节点写 %s，但 bench 自带 KB 真值 %s（8 部法）。"
                            "若写的是 %s，那是 verified-chinese-law-kb 仓库的全模块合计"
                            "（含未发布著作权法），与 bench 非同一份，别混用。"
                            % (n, total, facts.get("kb_nodes", "?")),
                        ))
    return bad


def rule_data_integrity(repos, facts):
    """数据类硬校验：线上看板 / bench 证据 / 参考库覆盖。"""
    bad = []

    # 线上看板题数不得落后于题库（曾差点回退成 30 题）
    wq = facts.get("watch_questions")
    sq = facts.get("site_questions")
    if wq and sq and sq != wq:
        bad.append((
            "FAIL", Path("gh-pages:status.json"), 0,
            "线上看板 questions=%s，但题库真值=%s —— 站点已落后/回退" % (sq, wq),
        ))

    # watch 参考库不得有未覆盖条目
    unc = facts.get("watch_uncovered")
    if unc is None:
        pass
    elif unc != 0:
        bad.append((
            "FAIL", Path("config/article_texts.json"), 0,
            "_uncovered=%s，参考库存在未覆盖条目" % unc,
        ))

    # bench 真实评测报告必须存在且非空（HVI 33.3%-54.2% 的唯一证据）
    ver = facts.get("bench_verifications")
    if ver is not None and ver <= 0:
        bad.append((
            "FAIL", Path("benchmark/reports/verifications.jsonl"), 0,
            "真实评测报告为空(%s 行) —— 证据被清空，须立即从 git 恢复" % ver,
        ))

    return bad


RULES = (
    ("R1 bench 可见性禁语", rule_visibility, False),   # (name, fn, needs_facts)
    ("R2 watch 题库数", rule_watch_questions, True),
    ("R3 bench 陷阱题数", rule_bench_questions, True),
    ("R4 LCB 题库数", rule_lcb_questions, True),
    ("R5 KB 节点数", rule_kb_nodes, True),
    ("R6 数据完整性", rule_data_integrity, True),
)


# ---------------------------------------------------------------- 发现仓库

def _commit_ts(repo: Path) -> int:
    """仓库 HEAD 的提交时间戳。用于在同一仓库的多个克隆里挑最新的那个。"""
    import subprocess

    try:
        out = subprocess.run(
            ["git", "-C", str(repo), "log", "-1", "--format=%ct"],
            capture_output=True, text=True, timeout=15,
        )
        if out.returncode == 0 and out.stdout.strip().lstrip("-").isdigit():
            return int(out.stdout.strip())
    except Exception:
        pass
    return -1


def _candidates(root: Path) -> dict:
    """在 root 及 root 的直接子目录里找各仓库的所有克隆。

    支持两种布局：<root>/<repo>（CI / 单目录克隆）与
    <root>/<date>/<repo>（WorkBuddy 工作区布局）。
    """
    cands = {k: [] for k in REPO_KEYS}
    bases = [root]
    try:
        bases += [p for p in root.iterdir() if p.is_dir()]
    except OSError:
        pass
    for key in REPO_KEYS:
        name = REPO_DIR_NAMES[key]
        for base in bases:
            cand = base / name
            if (cand / ".git").exists():
                cands[key].append(cand)
        # CI 场景：仓库被 checkout 到以仓库名命名的目录（就是 root 本身）
        if root.name == name and (root / ".git").exists() and root not in cands[key]:
            cands[key].append(root)
    return cands


def _repos_under(base: Path) -> int:
    """base 下能找到几个已知仓库（用于挑工作区根）。"""
    return sum(1 for v in _candidates(base).values() if v)


def default_root() -> Path:
    """向上找包含作品集仓库最多的那一层作为工作区根。

    脚本放在 <hub>/scripts/ 下，需要上溯到 WorkBuddy 那一层才能同时看到
    分布在不同日期目录里的各仓库；逐层比较取最多者，可适应不同摆放方式。
    """
    p = Path(__file__).resolve().parent
    best, best_n = p, -1
    for _ in range(6):
        n = _repos_under(p)
        if n > best_n:
            best, best_n = p, n
        p = p.parent
        if not str(p) or str(p) == str(p.parent):
            break
    return best


def discover(root: Path, overrides: dict) -> dict:
    repos = {}
    cands = _candidates(root)
    for key in REPO_KEYS:
        if key in overrides:
            p = Path(overrides[key]).expanduser()
            if p.is_dir():
                repos[key] = p
            continue
        cs = cands.get(key) or []
        if not cs:
            continue
        # 同名克隆可能有很多个（其中有冻结的旧克隆）。按最新提交时间挑，
        # 避免拿陈旧副本当真值——这类坑真实发生过。
        repos[key] = max(cs, key=_commit_ts)
    return repos


# ---------------------------------------------------------------- 主流程

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="作品集口径自动校验")
    ap.add_argument("--root", default=None, help="工作区根目录（自动探测各仓库）")
    ap.add_argument("--repo", action="append", default=[],
                    metavar="KEY=PATH", help="显式指定仓库路径，可重复")
    ap.add_argument("--list-facts", action="store_true", help="只打印推导出的真实数字")
    ap.add_argument("--strict", action="store_true", help="WARN 也视为失败")
    args = ap.parse_args(argv)

    overrides = {}
    for item in args.repo:
        if "=" in item:
            k, v = item.split("=", 1)
            overrides[k.strip()] = v.strip()

    if args.root:
        root = Path(args.root).expanduser()
    else:
        root = default_root()

    repos = discover(root, overrides)
    facts = derive_facts(repos)

    if args.list_facts:
        print("=== 推导出的真实数字（全部来自源头文件）===")
        for k in sorted(facts):
            print("  %-22s = %s" % (k, facts[k]))
        print("\n=== 纳入校验的仓库 ===")
        for k in REPO_KEYS:
            print("  %-10s %s" % (k, repos.get(k) or "(缺失，跳过)"))
        return 0

    print("=== 作品集口径校验 ===")
    print("仓库: " + ", ".join(
        "%s=%s" % (k, "OK" if repos.get(k) else "缺失") for k in REPO_KEYS))
    print("真值: " + ", ".join("%s=%s" % (k, facts[k]) for k in sorted(facts)))
    print("-" * 70)

    issues = []
    for name, fn, needs_facts in RULES:
        try:
            args_for_rule = (repos, facts) if needs_facts else (repos,)
            got = fn(*args_for_rule)
        except Exception as exc:  # 单条规则炸了不能拖垮整体
            got = [("FAIL", Path("?"), 0, "规则 %s 执行异常: %s" % (name, exc))]
        if got:
            print("[%s] %s -> %d 处" % ("命中", name, len(got)))
        else:
            print("[通过] %s" % name)
        issues.extend(got)

    print("-" * 70)
    fails = [i for i in issues if i[0] == "FAIL"]
    warns = [i for i in issues if i[0] == "WARN"]

    for level, f, ln, msg in issues:
        loc = "%s:%s" % (f, ln) if ln else str(f)
        print("%-4s %s\n     %s" % (level, loc, msg))

    if not issues:
        print("\n✅ 全部通过：口径一致，无违规。")
        return 0

    print("\n汇总: %d FAIL / %d WARN" % (len(fails), len(warns)))
    if fails:
        print("❌ 口径校验失败，禁止合入。")
        return 1
    if warns and args.strict:
        print("❌ --strict 模式：WARN 视为失败。")
        return 1
    print("⚠️  仅有 WARN，不阻断（加 --strict 可设为阻断）。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
