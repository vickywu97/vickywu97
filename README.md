# Hi, I'm Vicky Wu 👋

**律师 + 税务师 + 专利代理师 ｜ 在做 AI 法律产品**
**Lawyer · Tax Adviser · Patent Attorney → building AI legal-product & compliance tooling that *measures* LLM quality.**

我把六年的法律 / 税务 / 知识产权实务经验，翻译成一套**可量化、可复现的 AI 质量评测与防护产品**——不是只会调 prompt，而是能把"模型错了"变成"可度量、可修复的规格"。
I turn six years of legal / tax / IP practice into AI-quality evaluation and guardrail tooling that is *quantifiable and reproducible* — turning vague "the model is wrong" into a measured, fixable specification.

---

## 📦 作品集（5 个仓库 · 4 公开 1 私有）· Portfolio — 5 repos (4 public · 1 private)

| 仓库 Repo | 角色 Role | 一句话 One-liner |
| --- | --- | --- |
| [🧱 verified-chinese-law-kb](https://github.com/vickywu97/verified-chinese-law-kb) | **数据地基 · Data foundation** | 8 部法律、**2,327 条**逐字核验法条（M1 民法典 **1,260 条**全文，其中 27 条为律师抽核逐条签核初版，其余由 AI 核验）、可独立下载模块 / 2,327 line-by-line verified articles (M1 Civil Code: 1,260 full-text; 27 attorney spot-checked & line-by-line signed in the initial batch, the rest AI-verified) across 8 laws, independently downloadable. |
| [🔬 law-citation-bench](https://github.com/vickywu97/law-citation-bench) | **评测地基 · Eval foundation** | 离线零依赖基准，500 题量化法条引用准确率；一行提示词修复回收 **+97 分** / offline stdlib benchmark, 500 Q, a one-line prompt fix recovered +97 pts. |
| [📉 legal-hallucination-bench](https://github.com/vickywu97/legal-hallucination-bench) *(私有 · private)* | **量化基准 · Quantification** | 5 国产模型 × 23 陷阱题，HVI **33.3%–54.2%**，8 法域逐字 EXACT 全 0%；ground truth **2,327** 节点含 **212** 个 Tier A 专家逐条签核节点 / 5 models × 23 traps, HVI 33.3–54.2%, 8 laws EXACT all 0%; ground truth 2,327 nodes incl. 212 Tier A attorney-signed. |
| [🛡️ compliance-triangle](https://github.com/vickywu97/compliance-triangle) | **产品 · Product** | 同一套 verify 引擎给每条 AI 引注盖 🟢🟡🔴 章（法律·税务·IP 三域）/ same verify engine → 🟢🟡🔴 stamps across legal·tax·IP. |
| [📡 legal-ai-watch](https://github.com/vickywu97/legal-ai-watch) | **公开榜单 · Public leaderboard** | 31 题公开评测 + [gh-pages 看板](https://vickywu97.github.io/legal-ai-watch)（演示数据），跟踪主流模型法条引用表现 / 31-Q public eval + [live dashboard](https://vickywu97.github.io/legal-ai-watch) (demo data). |

![作品集架构](./portfolio_architecture.svg)

---

## 🛡️ 护城河（三证合一）· Moat — triple qualification

- **律师 Lawyer** —— 懂"引用法条"在法律实务里有多严肃 → 定下逐字二元判定。 / understands how serious citation is in practice → defines the exact-match binary criterion.
- **税务师 Tax Adviser** —— 把增值税法 / 企税 / 个税优先纳入（多数法律 AI 评测不碰税法）。 / prioritizes tax law (most legal-AI evals avoid it).
- **专利代理师 Patent Attorney** —— 职业习惯是"精确比对文本" → 与基准"一个字都不能差"同一思维。 / habit of precise text comparison → same mindset as "not one character off".

同一人设计校验规则、定义陷阱、签署每一条 KB——这是任何纯工程 / 纯算法团队无法复制的壁垒。
One person designs the rules, defines the traps, and signs every KB entry — a barrier no pure-engineering team can replicate.

---

## 📊 关键数字（无可辩驳）· Key numbers

- 测试规模 Scale：**5 国产模型 × 23 陷阱题 = 115 条**有效回答 / 115 valid responses.
- 引注幻觉率 HVI（最宽松尺度）：**33.3%–54.2%**（连付费旗舰都不过半）/ even paid flagships fail half.
- 内容级 EXACT（逐字合规率）：**8 法域全部 0%** / 8 laws all 0% exact match.
- 知识库 KB：**2,327 条**逐字核验法条 · **8 部法律** / KB: 2,327 verified articles · 8 laws.
- 评测基准 Benchmark：**500 题**确定性生成，T1 接地 / T2 检索 / T3 幻觉 / 500 deterministic questions.

---

## 🧩 其他作品 · Other builds

- **Excel 大师系列** —— 单一权威生成入口 `regen_*.py`，覆盖**公司治理模板生成**与**增值税进项税抵扣审核**；沉淀"找错纠错 + 逐行正确值"范式（平台合规检测"数学正确 / 场景设定"内核）。
  Excel Master series — single canonical `regen_*.py` generator for **corporate-governance templates** & **VAT input-tax deduction audit**; the "find-the-error + per-row correct value" pattern.
- **CIPP/E 备考体系** —— 已系统学习 IAPP **CIPP/E（欧盟数据保护）** 体系；相关真题 / 刷题题库不公开。
  CIPP/E prep — studied IAPP **CIPP/E (EU data protection)** system; question bank not public.

---

## 🧰 技术标签 · Skills

`Python 标准库` · `离线零依赖` · `可复现评测` · `LLM 评测` · `法律 AI` · `税务合规` · `知识产权` · `产品设计`
`Python stdlib` · `offline-zero-dep` · `reproducible eval` · `LLM evaluation` · `legal AI` · `tax compliance` · `IP` · `product design`

---

## 📫 联系 · Reach me

欢迎 AI 法律 / 合规方向的团队交流 —— **LinkedIn** [linkedin.com/in/wuyitong](https://www.linkedin.com/in/wuyitong) · **邮箱** [vickywu97@163.com](mailto:vickywu97@163.com) · 或在任意仓库开 Issue。
**Open to:** AI 法律产品经理 / 法律合规 / 税务 / 专利（远程优先）— LinkedIn [in/wuyitong](https://www.linkedin.com/in/wuyitong) · [vickywu97@163.com](mailto:vickywu97@163.com) · 或开 Issue。

> 注：评测结果与数字随版本演进，最新以各仓库 README 为准；本页仅作作品集导航，不构成法律 / 税务 / 专利意见。
> Numbers evolve with versions; latest per-repo READMEs are authoritative. This page is navigation only, not legal / tax / patent advice.
