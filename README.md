# Knowledge MEMO

> **把 Karpathy 的 LLM Wiki 装进你的 Obsidian —— 但请允许我们反对他一件事：人不能退出 loop**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

---

## Why this exists

这几天 Andrej Karpathy 在推特点燃了一把火 —— 他发了一份 [`llm-wiki.md` gist](https://gist.github.com/karpathy)，提出 "LLM Wiki" 的理念：让 LLM 像程序员维护代码库一样，持续编译一个 Markdown 知识库。Gary Tan 也加入讨论（他的 gbrain 系统）。Karpathy 明确说这是 "idea file"，**不是实现** —— "在 Agent 时代，你分享思路，别人让各自的 Agent 去搭。"

**Knowledge MEMO 就是那个"别人搭的一版"**，而且它不是从 gist 看完灵光一闪凑出来的 —— 它是作者 6 个月个人知识系统 + 三天整改（Phase 1-6）跑通的完整落地版本，碰巧和 Karpathy 的三层架构高度重合。

```bash
# 一行装好 SCHEMA / Ingest / Query / Lint / Retain
# Claude Code:
cp -r read insights note review query lint "$HOME/.claude/skills/"

# Codex:
cp -r read insights note review query lint "$HOME/.agents/skills/"

cp SCHEMA.md AGENTS.md /path/to/your/vault/
```

> 💡 完整的哲学立场（为什么"人必须在 loop 里"，以及"为谁积累"的经济学论证），短版中英对照见 [`docs/philosophy.md`](./docs/philosophy.md)。长文《实现人的四个未来化之知识 memo 化》正在撰写，发布后在此补中文链接。

### Karpathy LLM Wiki → Knowledge MEMO 实现对照表

| Karpathy Gist 概念 | Knowledge MEMO 实现 |
|---|---|
| Raw Sources | `Clippings/` + Obsidian Web Clipper |
| The Wiki | `Cards/` + 8 种 Card 类型 + Domain MOCs |
| The Schema | `SCHEMA.md` + `AGENTS.md`（根目录，Karpathy 惯例）|
| Ingest | `/read` + `/insights` + `/note`（双提议）|
| Query | `/query` |
| Lint | `/lint` |
| 🆕 **Retain** | **`/review` + FSRS-6**（Karpathy 没写的第四步）|

---

## The Six Skills

| Skill | Layer | Role | Output |
|-------|-------|------|--------|
| [`/read`](./read/) | Flywheel | Deep reading of papers, articles, PDFs | Structured analysis report |
| [`/insights`](./insights/) | Flywheel | Extract patterns from business content | Actionable insights report → `/note` |
| [`/note`](./note/) | Flywheel | Distill conversation into Map + Stones | Summary + atomic cards (dual-proposal) |
| [`/review`](./review/) | Flywheel | FSRS-6 spaced repetition | Quiz + mastery tracking |
| [`/query`](./query/) | Governance | Query vault knowledge via MOC + search | Grounded answer with sources |
| [`/lint`](./lint/) | Governance | Scan vault health (broken links, islands, gaps) | Vault Health Report |

### 三层架构

```
┌──────────────────────────────────────────────┐
│  L1 Schema Layer (宪法)                       │
│  SCHEMA.md · AGENTS.md                        │
│  三层架构 / 8 种 Card / 四维标签 / 权限矩阵   │
├──────────────────────────────────────────────┤
│  L2 Flywheel Layer (动作闭环)                 │
│  /read → /insights → /note → /review          │
│         (Ingest)       (Retain)               │
├──────────────────────────────────────────────┤
│  L3 Governance Layer (治理)                   │
│  /query · /lint                               │
└──────────────────────────────────────────────┘
             ↓ all write to
       📓 Obsidian Vault
```

对齐 Karpathy 的三层架构（Raw Sources / The Wiki / The Schema），但多了一个治理层和一个 Retain 环节。

---

## Quick Start

### 0. Pick your agent runtime

Knowledge MEMO currently supports both:

- **Claude Code** — install skills into `~/.claude/skills/`
- **Codex** — install skills into `~/.agents/skills/` (Codex official user-level skill directory)

`SCHEMA.md` and `AGENTS.md` are shared. For Codex, launch it from your vault root (or a subdirectory inside that vault) so `AGENTS.md` is in scope. If you use Claude Code, add a tiny vault-level `CLAUDE.md` that tells Claude Code to follow the rules in `AGENTS.md`.

### 1. Clone

```bash
git clone https://github.com/owenliang60-ship-it/knowledge-mgmt.git
cd knowledge-mgmt
```

### 2. Install the six skills into your agent runtime

**Claude Code**

```bash
mkdir -p "$HOME/.claude/skills"
cp -r read insights note review query lint "$HOME/.claude/skills/"
```

**Codex**

```bash
mkdir -p "$HOME/.agents/skills"
cp -r read insights note review query lint "$HOME/.agents/skills/"
```

### 3. Install SCHEMA + AGENTS to your Obsidian vault root

```bash
cp SCHEMA.md AGENTS.md /path/to/your/obsidian/vault/
```

If you use **Claude Code**, add a bridge file once:

```bash
cat > /path/to/your/obsidian/vault/CLAUDE.md <<'EOF'
Read AGENTS.md before operating this vault.
EOF
```

### 4. (Optional) Install card templates

```bash
cp -r templates /path/to/your/obsidian/vault/
```

### 5. Do the fastest possible first run

If you want the shortest path from “clone” to “I saw this work”, follow [`docs/first-15-minutes.md`](./docs/first-15-minutes.md). It is written for both Claude Code and Codex and aims for one concrete success in under 15 minutes.

Invoke the same workflow in either runtime:

**Claude Code**

```
/read https://arxiv.org/abs/...     # deep-read a paper
/insights <url-or-pasted-text>      # analyze a business/source article
/note                               # distill this conversation
/query "what do I know about X?"    # ask your vault
/lint                               # weekly health check
/review                             # today's spaced repetition
```

**Codex** (explicit skill invocation; natural-language prompting also works)

```
$read https://arxiv.org/abs/...     # deep-read a paper
$insights <url-or-pasted-text>      # analyze a business/source article
$note                               # distill this conversation
$query "what do I know about X?"    # ask your vault
$lint                               # weekly health check
$review                             # today's spaced repetition
```

---

## Demo Gallery

真实运行中的样本卡片，来自作者个人领域（认知神经科学 / 投资 / 哲学 / 游戏设计）：

👉 [`demo/README.md`](./demo/README.md)

> ⚠️ 这些**不是通用模板**。它们是"一个跑通的系统长什么样"的样本。请 fork 改造，长成你自己的那一个。

---

## How the Six Skills Work Together

### `/read` — Understand Deeply
模拟专家读者过程：结构扫描 → 论点追溯 → 方法评估 → 逻辑批判。支持 URL / PDF / Obsidian 笔记 / 纯文本，`quick`（5 分钟概览）或 `deep`（完整分析）两种模式。输出一份结构化报告，可直接喂给 `/note`。

### `/insights` — See What Others Miss
像分析师一样读商业内容：表面信息 → 深层逻辑 → 可迁移模式。每个洞察有三层（证据 → 逻辑 → 可迁移模式），优先收集反直觉、非显然的发现。`/insights` 本身不写 vault；它输出一份结构化洞察报告，再交给 `/note` 走双提议沉淀。

### `/note` — Crystallize Knowledge (Dual-Proposal)
把对话压缩成两层：**Map**（叙事摘要，保留推理链）+ **Stones**（独立原子卡片，每张一个 idea）。**人在 loop 的关键强制点** —— 不自动写卡，而是提出两个提议：(1) Wikilink 建议，你逐条确认；(2) Atomic Card 建议，你挑选。

### `/review` — Make It Stick
FSRS-6 间隔重复覆盖 Obsidian 里所有 `type/atomic` 标签的卡片。AI 出题、评分、安排下次复习。两种题型：recall（凭记忆复述）和 question（回答具体问题）。Mastery 通过 Obsidian 标签追踪：`mastery/new → mastery/again → mastery/good → mastery/easy`。

### `/query` — Ask Your Vault
先读 domain MOC（地图）→ 再做关键词搜索 → 综合 vault 知识 + 模型知识，给出带来源的答案。不是全文检索，是**利用你自己编织的知识图谱**作答。

### `/lint` — Vault Health Check
扫描断链 / 孤岛卡片 / 缺标签 / MOC 不完整 / 知识缺口。输出 Vault Health Report（写入 Cards/ 作为 type/health-report 卡），你决定修复什么。

---

## Human-in-the-loop: 一个关键约束

Karpathy 的方向里有一句话很诱人：**"维护成本趋近于零。"** 他设想的是 LLM 作为"不知疲倦的知识工程师"，持续编译 wiki，让人基本退出。

我们在这一点上**故意不一样**。Knowledge MEMO 有三条硬性纪律：

1. **没有自动信息流** —— 没有 auto-ingest、没有 scheduled scraping。你必须自己浏览、自己剪藏、自己决定今天读什么。
2. **`/note` 是对话中的双提议** —— 它不替你写卡，它提议。Wikilink 要你确认，atomic card 要你挑选。
3. **Agent 不独自改写 Wiki** —— 所有写入 `Cards/` 的动作必须经过 `/note` 的双提议通道，没有绕开它的 API。

为什么坚持这样？一句话：**"给 Agent 准备的 context 会被下一代模型淘汰，只有推进人脑的知识才是保值资产。"** 完整论证见长文。

---

## Upgrading from v1

v1 用户注意：v2 `/review` 用 `type/atomic` 标签识别原子卡，替代原来的 `【】-in-H1` 约定。**在升级前运行迁移脚本**：

```bash
python3 review/scripts/migrate_v1_to_v2.py /path/to/your/vault
```

完整指南见 [`docs/upgrade-from-v1.md`](./docs/upgrade-from-v1.md)。

---

## Prerequisites

- **[Claude Code](https://docs.anthropic.com/claude-code)** — Anthropic's CLI for Claude
- **Codex** — OpenAI Codex / Codex desktop，custom skills 默认安装到 `$HOME/.agents/skills/`
- **[Obsidian 1.12.4+](https://obsidian.md/)** — 首选 `obsidian` CLI；或者任意 Obsidian MCP server 作为 fallback
- **Python 3.9+** — `/review` 的 FSRS-6 引擎（stdlib only，无任何第三方依赖）

---

## Design Decisions

| Decision | Choice | Why |
|---|---|---|
| Knowledge backend | Obsidian（local + markdown）| Local-first, no vendor lock-in, excellent bi-directional linking |
| Schema location | Vault 根目录 `SCHEMA.md` + `AGENTS.md` | 对齐 Karpathy 惯例，Agent 读 vault 前自动加载 |
| Atomic card identification | `type/atomic` tag | 和 markdown 语法解耦，比 `【】-in-H1` 更可靠 |
| `/note` workflow | Dual-proposal (interactive) | 强制 human-in-the-loop |
| `/review` algorithm | FSRS-6 | State-of-the-art open-source SRS, stdlib only |
| State storage | Local JSON | Simple, portable, env var `KM_REVIEW_STATE_PATH` 可覆盖默认路径 |
| Templates | 8 minimal templates with "fork me" disclaimer | 降低复现门槛但强制可改性 |

---

## Contributing

核心原则：**Fork, Don't Consume**。Knowledge MEMO 不是一个通用产品 —— 它是作者个人（认知神经科学/哲学/投资/游戏设计）的知识管理系统。我们开源它，是让你看到一个真实跑通的样本，然后去长出**你自己的那一个**。详见 [CONTRIBUTING.md](./CONTRIBUTING.md)。

---

## License

MIT — see [LICENSE](./LICENSE). Fork 随便改。
