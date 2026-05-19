---
title: AGENTS.md — Project Governance Agent Rules
version: 3.0
updated: 2026-05-10
---

# AGENTS.md — Rules for AI Agents Operating the Project Vault

> **Install**: 把本文件复制到你的 Obsidian vault 根目录。
>
> **Scope**: 本文件约束 AI agent（Claude Code / Codex / 其他）**操作 vault** 时的行为。
>
> **与 SCHEMA.md 的关系**: `SCHEMA.md` 定义**什么是什么**（项目结构、文档类型、标签体系、权限矩阵），`AGENTS.md` 定义 agent **怎么操作**（CLI 命令、铁律、写入纪律）。两者互补，缺一不可。
>
> **适用角色**: 本系统为**单人使用**设计，用户同时承担项目经理（交付运营）和业务经理（前端经营）职责。Agent 是助手，不是协作者。

---

## Schema 优先

操作 vault 前先读取 vault 根目录的 `SCHEMA.md`（`obsidian read path="SCHEMA.md"`），了解当前目录结构、文档类型、权限矩阵和写入规则。

---

## 工具：Obsidian CLI（默认）+ MCP（回退）

**默认使用 CLI**（通过 Bash 工具调用 `obsidian` 命令）。仅当 Obsidian 应用未运行且 CLI 报 connection refused 时，回退使用 MCP（`mcp__obsidian__*`）。

> **架构**：CLI 是 IPC 遥控器，通过 socket 与运行中的 Obsidian GUI 通信。v1.12.4 起官方内置，100+ 命令。优势：移动文件自动更新 wikilinks、访问 backlinks/插件/同步状态。

### CLI 能力速查

| 操作 | CLI 命令 | MCP 回退 |
|------|----------|----------|
| 创建笔记 | `obsidian create path="..." content="..."` | `write_note` |
| 追加内容 | `obsidian append path="..." content="..."` | `write_note` (mode=append) |
| 前插内容 | `obsidian prepend path="..." content="..."` | `write_note` (mode=prepend) |
| 读取笔记 | `obsidian read path="..."` | `read_note` |
| 搜索 | `obsidian search query="..."` | `search_notes` |
| 带上下文搜索 | `obsidian search:context query="..."` | `search_notes` |
| 设置属性 | `obsidian property:set path="..." name="..." value="..." type=list` | `update_frontmatter` |
| 读取属性 | `obsidian property:read path="..." name="..."` | `get_frontmatter` |
| 标签列表 | `obsidian tags path="..."` | `manage_tags` |
| 移动/重命名 | `obsidian move path="..." to="..."` | `move_note` |
| 反向链接 | `obsidian backlinks path="..."` | _(MCP 无此功能)_ |
| 目录浏览 | `obsidian files folder="..."` / `obsidian folders` | `list_directory` |
| Vault 统计 | `obsidian vault` | `get_vault_stats` |
| 删除笔记 | `obsidian delete path="..."` | `delete_note` |

### 批量读取

CLI 无原生批量读取命令，使用 for 循环：

```bash
for doc in $(obsidian search query="type/milestone"); do
  obsidian read path="$doc"
done
```

> 一个项目下通常 20-50 个文档，批量读取效率足够。

---

## 铁律（FATAL）— 违反等于不可接受的灾难

> AI 最危险的时刻，不是它犯错的时候。是它觉得自己在帮你的时候。

### FATAL-001：禁止擅自重组文件结构

AI 天生有整理强迫症。它看到文件夹结构"不够整齐"，就浑身难受，恨不得帮你归归类、建建层级。但用户的文件结构是用户心智模型的外化。用户觉得它乱，其实什么都找得到。AI 觉得它整齐了，但用户什么都找不到了。

**绝对禁止**：移动文件夹、重命名目录、批量迁移文件。除非用户明确指示。

项目目录结构（`项目库/PJ-YYYY-NNN-xxx/`）是项目治理的骨架。AI 不能凭"整齐"的直觉改动它。

### FATAL-002：删除用户内容必须归档，禁止直接删

信息不可逆。删除是单向门——推开了就回不来。归档是暂停键，东西还在，只是换了个位置。所有不要的内容，归档，不删除。这条规则的本质是敬畏。对信息的敬畏，对用户记忆的敬畏。

项目档案具有法律和审计价值。删除是单向门，归档是暂停键。

### FATAL-003：禁止强加分类体系

用户自己的项目组织逻辑，比任何分类体系都重要。AI 替用户决定分类，就像一个新来的助理帮老板重新整理项目档案——你觉得在帮忙，用户觉得你在添乱。

### FATAL-004：禁止破坏现有链接和标签

每个 `[[wikilink]]` 都是一条项目关联连接。每个 tag 都是一个筛选维度。这些不是格式，是资产。是用户一条一条手动建立的关系网络，日积月累，越来越值钱。断链等于项目信息断层。一次鲁莽的文件移动，可能让项目章程中的引用全部失效。

### FATAL-005：结构性变更必须走审批流

任何涉及文件移动、目录调整、批量重命名的操作，必须走流程：
1. **SCAN** — 只读模式，扫描现状
2. **PLAN** — 提出最小化变更方案，附安全叙事（哪些文件会动、怎么回滚、有没有链接会断）
3. **CONFIRM** — 展示 before/after 对照，等用户确认
4. **EXECUTE** — 审批通过才动手
5. **VERIFY** — 检查链接完整性，确认没有断链

质量标准三个字：**最少步骤**。不是帮你做最多的事，是做最少但最有效的事。

---

## 写入质量（SEVERE）— 违反需修正

### 笔记必须有 frontmatter

没有 frontmatter 的笔记是孤岛。搜不到，分不了类，进不了知识图谱。一个 vault 里有上千个 .md 文件，如果其中两百个没有 tags，你的知识图谱就缺了两百个节点。不是内容不存在，是系统看不见它。

最低要求：
- `tags` 字段（遵循三维标签体系：`type/` + `status/` + `priority/`）
- `date` 或 `created` 字段
- 项目相关文档必须有 `project` 字段

### 先搜再写，禁止创建冗余笔记

写入新笔记前，先搜索 vault 中是否已有同主题内容。一个项目里不需要三份一样的预算执行表。能追加就追加，能链接就链接，确认没有才新建。

### 不破坏 frontmatter 格式

元数据是 AI 可读性的基础，格式一乱，所有自动化全崩。修改笔记时必须保持现有 frontmatter 结构完整。

### 文件夹嵌套不超过 3 层

三层以上的目录结构，人类自己都记不住路径。项目内部已设计为最大 2 层嵌套。

### raw/ 和产出/ 目录规则

各阶段（线索、售前、执行、验收、收尾）的 `raw/` 和 `产出/` 目录是**收纳箱**，不是知识卡片库：

- **raw/**：存放外部来源的原始素材（聊天记录、客户发来的 PPT/Word/PDF、截图等）。文件**不改名**（保持原始文件名，可按日期加前缀如 `2026-05-10-王局聊天记录.txt`），**不要求 frontmatter**，**不要求结构化**。AI 不主动往 raw/ 写文件，只在用户要求时操作。
- **产出/**：存放我们产出的附件（PPT、Word、Excel、PDF 等），按版本命名（如 `方案汇报-v2-20260515.pptx`），不强制 frontmatter。AI 不主动往产出/ 写文件，只在用户要求时操作。
- 售前阶段的 `售前材料/` 即产出/ 的特例（负责版本化 PPT/Word/Excel），名称保留不动。
- AI 在 `/prospect` `/presales` `/initiate` 等 Skill 中自动创建这两个空目录，不在此处做额外决策。

---

## 行为纪律

### 大批量操作必须先出 plan

涉及 5 个以上文件的操作（批量更新里程碑状态、批量录入支出记录），必须先列出完整方案，等用户确认再执行。**AI 提议，人类拍板。**

### 不确定归哪就放 inbox，不硬塞

如果不确定一篇笔记该归到哪个项目或目录，不要猜。放进 `Inbox/`，生成选项让用户选。**不确定就说不确定。** 宁可多问一句，不可乱做一步。

### 移动文件前必须检查反向链接

移动任何 .md 文件前，先用 `obsidian backlinks path="..."` 检查有无其他笔记链接到它。有链接的文件移动后必须更新所有引用（CLI `move` 会自动更新 wikilinks），或告知用户影响范围。

### 项目数据修改必须留痕

涉及预算、工期、合同条款的修改，必须在文档中记录：
- 修改日期
- 修改原因
- 修改前 → 修改后

项目数据具有审计价值，修改必须可追溯。

---

## 八荣八耻

> 承认不知道，比假装懂了有用一万倍。

| 荣 | 耻 |
|---|---|
| 深入查阅现有项目档案和结构 | 猜测 vault 目录和文件位置 |
| 主动确认再动手 | 模糊理解就执行 |
| 交给用户验证 | 假设用户的组织意图 |
| 复用已有笔记和 `[[链接]]` | 凭空新建重复内容 |
| 修改预算/工期时留痕 | 静默修改关键项目数据 |
| 不确定时列出选项问用户 | 替用户做项目决策 |

---

> **Customization**: 这份文件定义的是**项目治理的底线纪律**。你 fork 时可以根据你的领域调整 —— 但请保留 FATAL 五条铁律。它们不是个人偏好，是防止 AI 毁掉项目档案的底线。
