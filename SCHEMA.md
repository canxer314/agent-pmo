---
title: Knowledge MEMO Schema
version: 2.0
tags:
  - type/schema
updated: 2026-04-11
---

# SCHEMA.md — Knowledge MEMO Vault Schema

> ⚠️ **这是 Knowledge MEMO 作者的个人 vault schema 样本。**
> 你的领域可能需要不同的 Card 类型、不同的标签体系、不同的权限矩阵。
> **请 fork 改造，不要原样使用。** 见 `docs/philosophy.md` 里的 "知识管理是高度个人化的"。
>
> **Install**: 把本文件复制到你的 Obsidian vault 根目录。AI agent（Claude Code / Codex / 其他）操作 vault 前会自动读取它。
>
> **对齐 Karpathy LLM Wiki**: 这是 Karpathy gist 里提到的 "The Schema" 层 —— 规则层，随使用不断迭代。

---

## 1. 三层架构

| 层 | 目录 | 所有权 | 说明 |
|----|------|--------|------|
| Raw Sources | `Clippings/` | 用户拥有，AI 只读 | Web Clipper 剪藏的原始文章。AI 唯一可做的操作：学完后 move 到 `Clippings/已研究/` |
| Raw Sources | `Clippings/已研究/` | 用户拥有，AI 只读 | 已通过 `/note` 完成学习沉淀的文章 |
| Wiki | `Cards/` | AI 编译维护，用户验证 | 编译后的知识层：摘要、概念、洞察、对比、原子卡片、MOC 索引 |
| Schema | 本文件 | 双方共同迭代 | 规则层，随使用不断优化 |
| 支撑层 | `Journal/` · `Archive/` · `Attachments/` · `Canvas/` | 各自独立 | 不参与编译流程 |

> **关于目录名 "已研究"**: 作者保留中文命名，因为这体现"真实个人系统"的可信度。你 fork 时可以改成 `Clippings/studied/` 或任何你喜欢的名字 —— 同步更新 `/note` skill 里的对应引用即可。

---

## 2. Card 模板体系

`/note` 是 vault **唯一写入通道**。所有对话类 skill（`/read`, `/insights`, `/query` 等）只负责对话，不写 vault。

### 类型定义

| type 标签 | 存储位置 | 说明 |
|-----------|----------|------|
| `type/reading` | `Cards/Reading/` | 从 Clipping 编译的阅读摘要 |
| `type/research` | `Cards/Research/` | 深度研究报告 |
| `type/insight` | `Cards/Insights/` | 对话中沉淀的洞察 |
| `type/concept` | `Cards/` | 独立概念卡 |
| `type/comparison` | `Cards/` | 跨来源对比分析 |
| `type/atomic` | `Cards/` | 原子卡片，用于 `/review` 间隔重复 |
| `type/moc` | `Cards/` | MOC 索引页，按 domain 聚合 |
| `type/health-report` | `Cards/` | Lint 体检报告 |

### 通用 Frontmatter 规则

- 所有 Card 必须有**四维标签**：`type/` + `domain/` + `category/`（可选）+ `mastery/`（可选）
- 研究摘要必须有 `source` 字段回链原 Clipping
- 原子卡片必须有 `source` 字段回链研究摘要
- **原子卡片识别标准**：`type/atomic` 标签为**唯一标准**（v2 起。v1 曾用 `【】-in-H1`，已废弃）
- **溯源链**：`Clipping ← 研究摘要 ← 原子卡片`

---

## 3. Clipping 状态流转

| 位置 | 含义 |
|------|------|
| `Clippings/` | 剪藏了但还没学习（库存） |
| `Clippings/已研究/` | 已通过 `/note` 完成学习沉淀 |

- 新 Clipping 由 Web Clipper 剪入 `Clippings/` 根目录
- `/note` 完成时，AI 用 `obsidian move` 将来源 Clipping 移至 `Clippings/已研究/`（仅当 `/note` 来源于特定 Clipping）
- 纯对话产生的 `/note` 不移动任何 Clipping
- 导航栏一眼可见：`Clippings/` = 待研究库存，`已研究/` = 已消化

---

## 4. Ingest 编译规则

Ingest 是 **用户驱动的学习过程**，不是自动流水线。**人必须在 loop 里**。

### 流程

1. 用户手动剪藏 → `Clippings/`
2. 用户选择学习 → 对话 skill（`/read`, `/insights` 等）
3. 用户说 "note" → `/note` 执行写入

### `/note` 双提议（Human-in-the-loop 强制点）

`/note` 回顾对话后同时提出两类建议：

**提议 1 — Wikilink 建议**（链接到已有 Card）
- AI 搜索 vault 中已有 Cards，找到相关的列出
- 重要概念无对应 Card → 建议建空链标记知识缺口
- **用户逐条确认**

**提议 2 — Atomic Card 建议**（创建新卡片）
- AI 从对话中提取值得反复记忆的知识点
- **用户选择要创建哪些**

### 涟漪更新

| 操作 | 权限 |
|------|------|
| 新 Card 内加 wikilink（用户已确认的） | AI 执行 |
| 更新 MOC 索引 | AI 自主 |
| 已有 Card 正文补链 | 列出建议，用户确认 |

### 双输出原则

每次 `/note` 操作产出两份东西：一份给用户看的确认输出，一份回写 vault 的更新。

---

## 5. Wikilink 规则

### 质量标准

- 只链 **同 domain 或有实质关联** 的 Card，不是提到就链
- 优先链接概念卡（`type/concept`）— 它们是知识图谱的枢纽节点
- 一张 Card 的 wikilink 控制在 **5-15 个**
- `aliases` 字段帮助匹配同义词

### 空链含义

`[[未创建的概念]]` 在 Obsidian 中显示为紫色，表示知识缺口。**这是有意义的标记，不是错误。**

---

## 6. MOC 索引规则

MOC（Map of Content）按 domain 聚合，AI 自主维护。

### 结构

- 文件名：`Cards/MOC-{Domain}.md`
- 标签：`type/moc` + `domain/{domain}`
- Section 分区：概念 / 阅读 / 洞察 / 研究 / 知识缺口

### 权限细分

| MOC 操作 | 权限 |
|----------|------|
| 添加新条目 | AI 自主 |
| 创建新 MOC 文件 | AI 自主 |
| 修改已有条目 | 用户确认 |
| 删除条目 | 用户确认 |

---

## 7. Lint 检查项

### 全 vault 体检项

| 类别 | 检查项 | 严重度 |
|------|--------|--------|
| 链接 | 断链（wikilink 指向不存在页面） | 高 |
| 链接 | 孤岛 Card（零 backlink） | 中 |
| 链接 | 空链统计（知识缺口汇总） | 信息 |
| 标签 | Card 缺四维标签 | 高 |
| 标签 | 非四维体系的噪声标签 | 中 |
| 格式 | 缺 frontmatter 的 .md 文件 | 高 |
| 库存 | `Clippings/` 待研究 vs `已研究/` 统计 | 信息 |
| 库存 | 超过 30 天未研究的 Clippings | 中 |
| 索引 | MOC 遗漏新 Card | 中 |
| 索引 | MOC 中链接失效 | 高 |
| 缺口 | 按 domain 分析空链密度，建议研究方向 | 信息 |

### Lint 写入语义

| Lint 可以自动做的 | Lint 只报告不做的 |
|-------------------|-------------------|
| 生成健康报告写入 `Cards/` | 修复断链 |
| | 给 Card 补标签 |
| | 建新 Card 填补缺口 |
| | 修改/删除任何 Card |

---

## 8. Query 规则

`/query` 让 AI 带 vault 上下文回答问题。

- 先读 MOC 索引 → 搜索相关 Cards → 读取内容 → 综合回答
- 回答中引用 vault 内容时用 `[[Card名]]` 标注来源
- vault 中无相关内容时**诚实告知**
- 好的回答可通过 `/note` 回写（用户决定）

---

## 9. 权限矩阵

| 操作 | 权限 |
|------|------|
| 创建研究摘要 Card | AI 执行（`/note` 流程内） |
| 创建 Atomic Card | 用户从提议中选择 |
| 新 Card 内加 wikilink | 用户从提议中确认 |
| 已有 Card 正文补链 | 用户确认 |
| MOC 添加新条目 | AI 自主 |
| MOC 修改/删除已有条目 | 用户确认 |
| Clipping 移至 `已研究` | AI 自动（仅 `/note` 来源于 Clipping 时） |
| Lint 报告生成/写入 | AI 自动 |
| Lint 修复建议 | 用户拍板执行 |
| `SCHEMA.md` 修改 | 双方讨论后更新 |

---

## 10. 命名规范

| 类型 | 命名规则 | 示例 |
|------|----------|------|
| 阅读编译卡 | `{来源标题} — 阅读编译` | `Reading/Karpathy 知识库方法论 — 阅读编译.md` |
| 研究摘要 | `{主题} — 研究摘要` | `多巴胺奖励系统 — 研究摘要.md` |
| 概念卡 | `{概念名}` | `奖励预测误差.md` |
| 洞察卡 | `{洞察主题}` | `交易系统的反脆弱性.md` |
| 原子卡片 | `{概念名}` | `RLHF.md` |
| MOC | `MOC-{Domain}` | `MOC-Neuroscience.md` |
| 健康报告 | `Vault Health Report YYYY-MM-DD` | `Vault Health Report 2026-04-09.md` |

### 标签命名

- 使用小写英文 + 连字符：`domain/cognitive-science`
- 层级用斜杠：`domain/research/biology`
- **不创建四维体系外的标签前缀**

---

## 11. 验证责任

**人拍板，AI 建议。**

- AI 可以自主做的：MOC 新增条目、Clipping 移至已研究、Lint 报告生成
- AI 必须提议等确认的：wikilink 建链、atomic 卡片创建、已有 Card 修改
- 用户不需要看懂代码也能判断：所有提议用自然语言列出

---

> 本 Schema 随使用不断迭代。修改需双方讨论后更新。
> Fork 你自己的版本时，建议记录每次修改的理由和日期 —— 这本身就是"知识管理是过程而非产品"的证据。
