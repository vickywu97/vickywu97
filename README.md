# Hi, I'm Vicky Wu 👋

**律师 + 税务师 + 专利代理师 ｜ 在做 AI 法律产品**
**Lawyer · Tax Adviser · Patent Attorney → building AI legal-product & compliance tooling: both *measuring* LLM quality and *doing* compliance work.**

我把六年的法律 / 税务 / 知识产权实务经验，翻译成两条互补的产品线：

- **① 可量化、可复现的 AI 质量评测与防护** —— 不是只会调 prompt，而是能把"模型错了"变成"可度量、可修复的规格"。
- **② 直接干活的生产力型合规工具** —— 开源许可证合规 / 隐私政策体检 / 代币监管定性；离线零依赖、可进 CI 门禁，是法务岗日常能直接用的东西，而不是演示品。

I turn six years of legal / tax / IP practice into two complementary product lines:

- **① quantifiable, reproducible AI-quality evaluation & guardrails** — turning vague "the model is wrong" into a measured, fixable specification.
- **② productivity compliance tools that actually do the work** — OSS licensing / privacy-policy review / token classification; offline, zero-dependency, CI-gateable — tools a legal team can run daily, not demos.

> 📖 作品集总括叙事（为什么做这些、怎么被审计出来）：[PORTFOLIO_NARRATIVE.md](./PORTFOLIO_NARRATIVE.md)

---

## 📦 作品集（11 个仓库 · 全部公开）· Portfolio — 11 repos (all public)

### 🧰 生产力型合规工具 · Productivity compliance tools

> 直接对应法务岗日常工作的三个工具：**离线 · 零第三方依赖 · 可进 CI 门禁**。
> Three tools that map directly to in-house legal work: **offline · zero third-party deps · CI-gateable**.

| 仓库 Repo | 合规领域 Domain | 一句话 One-liner |
| --- | --- | --- |
| [🧾 oss-license-checker](https://github.com/vickywu97/oss-license-checker) | **知产 / 开源法务 IP · OSS** | 解析 npm / pip / go 依赖清单，逐依赖判定**商用可行性 · 传染性（5 档）· 需履行义务 · 冲突组合**；四态兼容矩阵（兼容 / 单向 / 有条件 / 不兼容，争议项显式标注不装"确定"），内置 22 个 license 事实库（附来源 URL + 核验日期），支持 SPDX `OR`/`AND` 表达式，可导出 **CycloneDX SBOM**，`--fail-on` 可作流水线门禁 / parses npm·pip·go manifests → per-dependency verdicts on commercial use, copyleft (5 tiers), obligations & conflicts; four-state compatibility matrix (disputed pairs flagged, never faked as certain); 22-license fact base with sources & verification dates; SPDX expressions; **CycloneDX SBOM** export; `--fail-on` CI gate. |
| [🔏 privacy-policy-checker](https://github.com/vickywu97/privacy-policy-checker) | **数据 / 隐私合规 Data · Privacy** | 对照 **PIPL 31 项 + GDPR 42 项**检查项逐条核验隐私政策，四态判定（satisfied / partial / missing / **not_applicable**）；带语境条件的检查项（如跨境传输、敏感信息）在全文无相关语境时自动判"不适用"，避免对纯境内 / 非敏感产品误报；每条附**法条原文 + 来源 URL + 核验日期** / audits a privacy policy against **31 PIPL + 42 GDPR** checks with four-state verdicts; context-gated items auto-marked `not_applicable` to avoid false positives on domestic-only / non-sensitive products; every item cites article text + source URL + verification date. |
| [🪙 token-classifier](https://github.com/vickywu97/token-classifier) | **Web3 / 加密法务 Crypto** | 输入代币机制描述 → **Howey 四要素**逐要素四态判定（strong / weak / absent / unknown）+ 置信度 + **香港 SFC / 新加坡 MAS 分法域**分别定性（不做统一全球结论）；证据片段锚定命中词原文，争议项显式标注（如"购买"可能仅为消费而非投资）；**只输出分析线索，绝不输出二元法律结论** / token mechanism description → Howey four-factor four-state scoring + confidence + **separate HK SFC / SG MAS verdicts** (no single global conclusion); evidence anchored to matched wording; disputed points flagged (e.g. "purchase" may be mere consumption); **analysis leads only — never a binary legal conclusion**. |

### 🧪 评测与数据地基 · Evaluation & data foundation

| 仓库 Repo | 角色 Role | 一句话 One-liner |
| --- | --- | --- |
| [🧱 verified-chinese-law-kb](https://github.com/vickywu97/verified-chinese-law-kb) | **数据地基 · Data foundation** | 8 部法律、**2,327 条**逐字核验法条（M1 民法典 **1,260 条**全文，其中 27 条为律师抽核逐条签核初版，其余由 AI 核验）、可独立下载模块 / 2,327 line-by-line verified articles (M1 Civil Code: 1,260 full-text; 27 attorney spot-checked & line-by-line signed in the initial batch, the rest AI-verified) across 8 laws, independently downloadable（著作权法模块内部整理中）/ across 8 laws, independently downloadable — a Copyright Law module is in internal prep. |
| [🔬 law-citation-bench](https://github.com/vickywu97/law-citation-bench) | **评测地基 · Eval foundation** | 离线零依赖基准，500 题量化法条引用准确率；一行提示词修复回收 **+97 分** / offline stdlib benchmark, 500 Q, a one-line prompt fix recovered +97 pts. |
| [🗂️ law-cli](https://github.com/vickywu97/law-cli) | **法条数据 CLI · Statute-data CLI** | 中文法条「数据层最小闭环」——合法获取 / 固定来源 / 可复现证明；`fetch`·`show`·`verify`，零依赖；AI 审核终核（219/219 `ai_verified`）/ the smallest closed loop for Chinese statutes: lawful fetch, pinned source, reproducible proof; zero-dep; AI final-review (219/219 `ai_verified`). |
| [📉 legal-hallucination-bench](https://github.com/vickywu97/legal-hallucination-bench) _(开源仓库 · MIT)_ | **量化基准 · Quantification** | 5 国产模型 × 29 陷阱题，HVI **33.3%–54.2%**，8 法域逐字 EXACT 全 0%；ground truth **2,327** 节点含 **212** 个 Tier A 专家逐条签核节点 / 5 models × 29 traps, HVI 33.3–54.2%, 8 laws EXACT all 0%; ground truth 2,327 nodes incl. 212 Tier A attorney-signed. |
| [🛡️ compliance-triangle](https://vickywu97.github.io/compliance-triangle/) · [repo](https://github.com/vickywu97/compliance-triangle) | **产品 · Product** | 同一套 verify 引擎给每条 AI 引注盖 🟢🟡🔴 章（法律·税务·IP 三域）/ same verify engine → 🟢🟡🔴 stamps across legal·tax·IP. |
| [📡 legal-ai-watch](https://github.com/vickywu97/legal-ai-watch) | **公开榜单 · Public leaderboard** | 112 题公开评测 + [gh-pages 看板](https://vickywu97.github.io/legal-ai-watch)（演示数据 · github.io 国内可能不可达 / may be unreachable in mainland China），跟踪主流模型法条引用表现 / 112-Q public eval + [live dashboard](https://vickywu97.github.io/legal-ai-watch) (demo data · github.io may be unreachable in CN). |
| [⏱️ lawyer-timesheet](https://vickywu97.github.io/lawyer-timesheet/) · [repo](https://github.com/vickywu97/lawyer-timesheet) | **实务工具 · Practice tooling** | 本地优先 / 零依赖的中国律师**计时·计费 CLI**；审计哈希链可回放、中国税法原生（价税分离/免税/跨境预提）、事项智能归类 + 移动端快速捕获 / local-first, zero-dep legal time-billing CLI; replayable audit hash chain, China-tax native, intelligent task categorization + mobile quick-capture. |
| [⚙️ TASK-DD-007](https://github.com/vickywu97/TASK-DD-007) | **Agent · 工程 · Engineering** | 离线·零依赖·依赖 pin（纯 Python vendored，规避 lxml）的**确定性规则引擎**；读取 52 项尽调清单 + 资料室，产出 4 件可机器校验交付物；隐藏 B 卷迁移安全（不写死实例答案、不捆绑预生成成果）/ offline, dependency-pinned (vendored pure-Python, no lxml) **deterministic rule engine**; reads 52-item checklist + data room → 4 machine-verifiable deliverables; hidden-B-volume migration-safe (no hardcoded answers, no pre-bundled outputs). |

![作品集架构](./portfolio_architecture.svg)

> 🛡️ **产品实测截图**（compliance-triangle · 给每条 AI 引注盖 🟢🟡🔴 章）：
> ![合规三角 AI 引注三层校验演示](https://raw.githubusercontent.com/vickywu97/compliance-triangle/master/docs/dashboard_preview.png)

---

## 🛡️ 护城河（三证合一）· Moat — triple qualification

- **律师 Lawyer** —— 懂"引用法条"在法律实务里有多严肃 → 定下逐字二元判定。 / understands how serious citation is in practice → defines the exact-match binary criterion.
- **税务师 Tax Adviser** —— 把增值税法 / 企税 / 个税优先纳入（多数法律 AI 评测不碰税法）。 / prioritizes tax law (most legal-AI evals avoid it).
- **专利代理师 Patent Attorney** —— 职业习惯是"精确比对文本" → 与基准"一个字都不能差"同一思维。 / habit of precise text comparison → same mindset as "not one character off".

同一人设计校验规则、定义陷阱、签署每一条 KB——这是任何纯工程 / 纯算法团队无法复制的壁垒。
One person designs the rules, defines the traps, and signs every KB entry — a barrier no pure-engineering team can replicate.

---

## 📊 关键数字（无可辩驳）· Key numbers

两套互补量尺，口径不同、不可混为一谈：

**A. 量化基准 `legal-hallucination-bench`（对抗陷阱集）**
- 规模 Scale：**5 国产模型 × 29 陷阱题 = 145 条**有效回答 / 145 valid responses.
- 引注幻觉率 HVI（最宽松尺度）：**33.3%–54.2%**（连付费旗舰都不过半）/ even paid flagships fail half.
- 内容级 EXACT（逐字合规率）：**8 法域全部 0%** / 8 laws all 0% exact match.
- 知识库 KB：**2,327 条**逐字核验法条 · **8 部法律** / KB: 2,327 verified articles · 8 laws.
- 评测地基 `law-citation-bench`：离线零依赖、**500 题**确定性生成基准（一行提示词修复回收 +97 分）/ offline stdlib, 500 Q.

**B. 公开榜单 `legal-ai-watch`（常规引注监测集 · 周更）**
- **112 题**常规引注评测，当前参评 **3 模型**（DeepSeek-R1 / Qwen-Max / GLM-4）/ 112-Q routine eval, 3 models.
- 引注幻觉率 HVI：看板当前为**演示数据**，配置模型密钥后自动刷新真实 HVI/CRFI（详见 [gh-pages 看板](https://vickywu97.github.io/legal-ai-watch) · github.io 国内可能不可达）/ HVI: dashboard currently **demo data**; real HVI/CRFI auto-refresh once API keys are set — see live dashboard (github.io may be unreachable in mainland China).
- 法域覆盖民法 / 刑法 / 公司法 / 专利 / 税法，并新增数据合规（PIPL / 数据安全法）、竞争法（反不正当竞争法），共 **7 个法域** / spans 7 domains incl. data-compliance & competition law.

> 口径说明：A 是**故意挖坑**的对抗集（旧法陷阱 / 张冠李戴 / 不存在条号），专测难例可靠性；B 是**常规事实引注**监测，测日常可用性。模型在 B 上尚可，≠ 在 A 的陷阱前安全——二者互补。

---

## 🧩 其他作品 · Other builds

- **Excel 大师系列** —— 单一权威生成入口 `regen_*.py`，覆盖**公司治理模板生成**与**增值税进项税抵扣审核**；沉淀"找错纠错 + 逐行正确值"范式（平台合规检测"数学正确 / 场景设定"内核）。
  Excel Master series — single canonical `regen_*.py` generator for **corporate-governance templates** & **VAT input-tax deduction audit**; the "find-the-error + per-row correct value" pattern.
- **GDPR / 欧盟数据保护研习** —— 系统研习 IAPP CIPP/E 知识体系与 GDPR 框架（自研刷题题库不公开）。
  GDPR / EU data protection — working knowledge of the GDPR / EU data-protection framework (systematically studied the IAPP CIPP/E body of knowledge); question bank not public.

---

## 🧰 技术标签 · Skills

`Python 标准库` · `离线零依赖` · `可复现评测` · `LLM 评测` · `法律 AI` · `税务合规` · `知识产权` · `产品设计` · `开源许可证合规` · `隐私合规 (PIPL/GDPR)` · `Web3 合规` · `SBOM` · `CI 门禁`
`Python stdlib` · `offline-zero-dep` · `reproducible eval` · `LLM evaluation` · `legal AI` · `tax compliance` · `IP` · `product design` · `OSS license compliance` · `privacy (PIPL/GDPR)` · `Web3 compliance` · `SBOM` · `CI gating`

---

## 📄 简历 / Resume

<details>
<summary>展开查看完整简历 · Click to expand the full resume</summary>

**Vicky Wu · 律师 / 税务师 / 专利代理师（中国）**
目标方向：互联网 / AI / 科技公司 法务岗（in-house legal counsel）· 法律合规 · 税务合规 · 知识产权（远程优先）

**专业概述**
六年法律 / 税务 / 知识产权实务经验，现聚焦 AI 法律产品与合规工具。开源作品证明两件事：一是不只是会调 prompt，更能**定义并量化 AI 在法律场景的质量**——从逐字核验的法条真值库，到离线评测基准（一个提示词改动把模型幻觉盲区从 0 拉到 0.97），再到每周自动监测排行榜与带门禁的合规产品；二是能**把法律判断直接做成工具**——开源许可证合规、隐私政策体检、代币监管定性，三个工具均离线零依赖、可进 CI 门禁，法务岗日常能直接用。

**核心项目**

*生产力型合规工具 —— 直接对应法务岗日常工作 / Productivity compliance tools*
- **oss-license-checker**（知产 · 开源法务）：解析 npm / pip / go 依赖清单，逐依赖判定商用可行性、传染性（5 档）、需履行义务与冲突组合；四态兼容矩阵（争议项显式标注）；22 个 license 事实库附来源 URL + 核验日期；支持 SPDX `OR`/`AND`；可导出 CycloneDX SBOM；`--fail-on` 可作 CI 门禁。
- **privacy-policy-checker**（数据 · 隐私合规）：对照 PIPL 31 项 + GDPR 42 项逐条核验，四态判定（含语境感知的 `not_applicable`，避免对纯境内 / 非敏感产品误报）；每条附法条原文 + 来源 URL + 核验日期。
- **token-classifier**（Web3 · 加密法务）：Howey 四要素逐要素四态判定 + 置信度 + 香港 SFC / 新加坡 MAS 分法域定性（不做统一全球结论）；证据锚定命中词原文，争议项显式标注；只输出分析线索，绝不输出二元法律结论。

*评测与数据地基 / Evaluation & data foundation*
- **verified-chinese-law-kb**（数据地基）：8 部法律、2,327 条逐字核验法条，模块化、带版本轴、可独立下载；M1 民法典由执业律师具名签署。
- **law-citation-bench**（评测地基）：离线零依赖、500 题确定性基准，量化 LLM 法条引用准确率；一行提示词修复为 Qwen 回收 **+97 分**。
- **legal-hallucination-bench**（量化基准 · 开源）：5 国产模型 × 29 陷阱题，HVI **33.3%–54.2%**，8 法域逐字 EXACT 全 0%。
- **compliance-triangle**（产品）：同一 verify 引擎给每条 AI 引注盖 🟢🟡🔴 章（法律·税务·IP 三域）。
- **legal-ai-watch**（公开榜单）：112 题周更评测 + 看板（演示数据）。
- **law-cli**（法条数据 CLI）：中文法条「数据层最小闭环」——合法获取 / 固定来源 / 可复现证明；零依赖，`fetch`/`show`/`verify`，AI 审核终核（219/219 `ai_verified`）。
- **lawyer-timesheet**（实务工具）：本地优先·零依赖的中国律师计时与计费 CLI；审计哈希链可回放、中国税法原生（价税分离/免税/跨境预提）、事项智能归类 + 移动端快速捕获（V2）。
- **TASK-DD-007**（Agent·工程）：离线·零依赖·依赖 pin（纯 Python vendored，规避 lxml）的确定性规则引擎；读取 52 项尽调清单 + 资料室，产出 4 件可机器校验交付物；隐藏 B 卷迁移安全（不写死实例答案、不捆绑预生成成果）。

**其他作品**
- Excel 大师系列：公司治理模板生成 + 增值税进项税抵扣审核（单一 `regen_*.py` 生成入口）。
- GDPR / 欧盟数据保护研习：系统研习 IAPP CIPP/E 知识体系与 GDPR 框架（自研刷题题库不公开）。

**技能**
Python 标准库 · 离线零依赖 · 可复现评测 · LLM 评测 · 法律 AI · 税务合规 · 知识产权 · 产品设计。

**联系**
LinkedIn：[in/wuyitong](https://www.linkedin.com/in/wuyitong) · 邮箱：[vickywu97@163.com](mailto:vickywu97@163.com)

</details>

也可下载排版版简历：[cv.html](./cv.html)（打印友好 / print-friendly）。

---

## 📫 联系 · Reach me

欢迎 AI 法律 / 合规方向的团队交流 —— **LinkedIn** [linkedin.com/in/wuyitong](https://www.linkedin.com/in/wuyitong) · **邮箱** [vickywu97@163.com](mailto:vickywu97@163.com) · 或在任意仓库开 Issue。
**Open to:** 互联网 / AI / 科技公司 法务岗（in-house legal counsel）· 法律合规 · 税务合规 · 知识产权（远程优先）— LinkedIn [in/wuyitong](https://www.linkedin.com/in/wuyitong) · [vickywu97@163.com](mailto:vickywu97@163.com) · 或开 Issue。

> 注：评测结果与数字随版本演进，最新以各仓库 README 为准；本页仅作作品集导航，不构成法律 / 税务 / 专利意见。
> Numbers evolve with versions; latest per-repo READMEs are authoritative. This page is navigation only, not legal / tax / patent advice.
