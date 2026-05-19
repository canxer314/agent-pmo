---
name: bid
description: "投标管理。创建售前项目、管理技术方案与商务报价、记录投标结果。当用户说'bid'、'投标'、'报价'、'投标结果'时触发。售前需求分析和方案迭代请用 /presales。"
invocation: user
arguments:
  - name: prospect
    description: "关联的线索名称（可选）。如不提供，会列出现有线索供选择，或询问客户信息。"
    required: false
  - name: action
    description: "'new'（新建售前项目）、'update'（更新技术方案/商务报价）、'result'（记录投标结果）。默认 'new'"
    required: false
---

# /bid — 投标管理

创建售前项目骨架，管理技术方案与商务报价，记录投标结果。

## 定位

| Skill | 职责 | 输出 |
|-------|------|------|
| `/prospect` | 线索管理 | 线索文档 |
| `/bid` | **售前项目 + 技术方案 + 商务报价 + 投标结果** | 售前项目骨架 |
| `/presales` | 售前工作台 — 需求分析 + 方案迭代 + 材料管理 + 需求冻结 | 需求分析 + 解决方案 + 材料清单 |
| `/initiate` | 项目立项 — 中标后创建项目 | 项目结构 |

**典型工作流**:

```
/prospect 跟进线索直到用户决定升级
    ↓
/bid action=new（创建售前项目骨架）
    ↓
/presales（首次需求对接 → 更新客户需求分析）
/presales（方案成形 → 更新解决方案）
/presales action=material（材料版本管理）
/presales action=tech-exchange（技术交流）
    ↓（循环迭代）↓
/presales action=lock（锁定需求）
    ↓
/bid action=update（更新商务报价）
    ↓
/bid action=result（记录投标结果）
    ↓
【中标】→ /initiate 立项
```

---

### 投标状态推导（投标阶段）

`/presales` 负责售前阶段的状态推导（`needs-analysis` → `requirement-locked`），`/bid` 负责投标阶段的状态推导（`priced` → `won`/`lost`）。

| 状态 | 含义 | 触发条件 | 负责 Skill |
|------|------|----------|------------|
| `needs-analysis` | 需求调研中 | `/bid action=new` 后 | — |
| `solution-drafting` | 方案编写中 | 首次更新 `解决方案.md` | `/presales` |
| `solution-communicating` | 方案已发客户 | 材料标记已发客户后 | `/presales` |
| `tech-exchange-loop` | 技术交流迭代中 | 技术交流完成后 | `/presales` |
| `requirement-locked` | 需求已冻结 | 需求冻结确认书创建后 | `/presales` |
| `priced` | 已定价 | 更新 `商务报价.md`（lock 之后） | `/bid` |
| `submitted` | 已递交标书 | 用户确认标书已递交 | `/bid` |
| `won` / `lost` | 中标/未中标 | `/bid action=result` 完成后 | `/bid` |

**推导方法**：每次操作前，AI 读取售前项目中已有文件判断当前状态；操作完成后，在双提议中建议下一状态。AI 不静默修改状态字段。

---

## Behavior

### Step 0: 确定动作

| action | 行为 |
|--------|------|
| `new`（默认）| 创建售前项目骨架（项目概览 + 招标要求 + 技术方案 + 商务报价 + 投标结果 + 共享子目录） |
| `update` | 更新「技术方案」或「商务报价」|
| `result` | 记录投标结果 |

---

### Step 1: 新建售前项目（action=new）

#### 1a. 关联线索

如提供 `prospect` 参数：

```bash
obsidian read path="线索池/活跃线索/线索-{客户}-{主题}/线索-{客户}-{主题}.md"
```

未提供时，搜索线索池：

```bash
obsidian search query="type/prospect"
obsidian files folder="线索池/活跃线索"
```

列出状态为"跟进中"的线索供选择（用户自主判断是否升级）。

#### 1b. 创建售前项目结构

创建文件夹：`售前项目/{客户}-{主题}-{日期}/`

**投标核心文档**（由 `/bid` 创建）：

1. `项目概览.md` — 售前项目入口笔记（导航枢纽 + 状态追踪）
2. `招标要求.md`
3. `技术方案.md`
4. `商务报价.md`
5. `投标结果.md`

**共享子目录**（由 `/bid` 创建，`/presales` 使用）：

```
售前项目/{客户}-{主题}-{日期}/
├── 项目概览.md          ← 售前项目入口笔记
├── raw/                   ← 客户发来的原始素材
│   └── .gitkeep
├── 售前材料/              ← /presales 使用（我们产出的材料）
│   └── .gitkeep
├── 技术交流记录/          ← /presales 使用
│   └── .gitkeep
├── 需求冻结/              ← /presales 使用
│   └── .gitkeep
├── 招标要求.md
├── 技术方案.md
├── 商务报价.md
└── 投标结果.md
```

> 客户需求分析.md 和 解决方案.md 由 `/presales` 首次操作时创建。

#### 1c. 项目概览.md

```markdown
---
title: "项目概览 — {客户} {主题}"
type: bid
client: "{{客户}}"
project: "{{主题}}"
bid_date: YYYY-MM-DD
status: needs-analysis
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags:
  - type/bid
  - status/active
---

# 项目概览 — {客户} {主题}

> 售前项目入口 | 创建日期：YYYY-MM-DD | 最后更新：YYYY-MM-DD
> 当前状态：needs-analysis

## 基本信息

- 客户：[[客户档案/{客户}]]
- 项目：{主题}
- 投标类型：公开招标 / 邀请招标 / 竞争性谈判
- 预算限价：{{金额}}万
- 投标截止：YYYY-MM-DD

## 文档导航

- [[招标要求]] — 招标方要求原文
- [[技术方案]] — 我方技术方案
- [[商务报价]] — 报价明细与版本
- [[投标结果]] — 中标/未中标结果
- {由 /presales 创建后自动出现}
  - [[客户需求分析]]
  - [[解决方案]]
  - [[售前材料清单]]

## 状态时间线

| 日期 | 状态变更 | 备注 |
|------|----------|------|
| YYYY-MM-DD | → needs-analysis | 售前项目创建 |

## 关键决策记录

[记录售前过程中的关键决策]

## 关联资源

- 来源线索：{如从线索升级} [[线索池/活跃线索/线索-{客户}-{主题}/线索-{客户}-{主题}]]
```

#### 1d. 招标要求.md

```markdown
---
title: "招标要求"
type: bid
bid_type: 公开招标 | 邀请招标 | 竞争性谈判
bid_date: YYYY-MM-DD
budget_limit: {{预算限价}}
client: "{{客户}}"
project: "{{主题}}"
tags:
  - type/bid
  - status/active
---

# 招标要求 — {客户} {主题}

## 招标基本信息

- 招标编号：
- 发布时间：
- 投标截止：
- 开标时间：
- 预算限价：{{金额}}万

## 资质要求

[对投标人资质的要求]

## 技术需求要点

[核心技术需求]

## 评分标准

| 评分项 | 权重 | 说明 |
|--------|------|------|
| 技术方案 | 40% | |
| 商务报价 | 30% | |
| 项目经验 | 20% | |
| 服务承诺 | 10% | |

## 关键时间节点

- [ ] YYYY-MM-DD：购标书
- [ ] YYYY-MM-DD：现场踏勘
- [ ] YYYY-MM-DD：提疑截止
- [ ] YYYY-MM-DD：投标截止
```

#### 1e. 技术方案.md

```markdown
---
title: "技术方案"
type: bid
tags:
  - type/bid
---

# 技术方案 — {客户} {主题}

## 总体架构

[技术架构描述]

## 实施方案

[实施计划]

## 团队配置

| 角色 | 人数 | 资质要求 |
|------|------|----------|
| 项目经理 | 1 | PMP |

## 关键技术点

[与竞争对手的差异化技术点]
```

#### 1f. 商务报价.md

```markdown
---
title: "商务报价"
type: bid
total_price:
cost_breakdown:
profit_margin:
tags:
  - type/bid
---

# 商务报价 — {客户} {主题}

## 报价汇总

| 项目 | 金额（万） |
|------|-----------|
| 人力成本 | |
| 分包成本 | |
| 管理成本 | |
| 其他成本 | |
| **合计成本** | |
| 利润 | |
| **报价** | |

## 付款条件

[与招标要求的对照]

## 报价版本记录

| 版本 | 日期 | 金额 | 利润率 | 审批状态 |
|------|------|------|--------|----------|
| v1 | YYYY-MM-DD | | | 待审批 |
```

#### 1g. 投标结果.md

```markdown
---
title: "投标结果"
type: bid
status: pending
result:
tags:
  - type/bid
---

# 投标结果 — {客户} {主题}

## 结果

- [ ] 中标
- [ ] 未中标

## 中标信息

- 中标金额：
- 中标单位：

## 未中标分析

- 中标单位：
- 中标金额：
- 我方排名：
- 未中标原因：

## 经验教训

[本次投标的经验教训]
```

#### 1h. 创建子目录

```bash
obsidian create path="售前项目/{客户}-{主题}-{日期}/raw/.gitkeep" content=""
obsidian create path="售前项目/{客户}-{主题}-{日期}/售前材料/.gitkeep" content=""
obsidian create path="售前项目/{客户}-{主题}-{日期}/技术交流记录/.gitkeep" content=""
obsidian create path="售前项目/{客户}-{主题}-{日期}/需求冻结/.gitkeep" content=""
```

#### 1i. 写入文档

```bash
obsidian create path="售前项目/{客户}-{主题}-{日期}/项目概览.md" content="..."
obsidian create path="售前项目/{客户}-{主题}-{日期}/招标要求.md" content="..."
obsidian create path="售前项目/{客户}-{主题}-{日期}/技术方案.md" content="..."
obsidian create path="售前项目/{客户}-{主题}-{日期}/商务报价.md" content="..."
obsidian create path="售前项目/{客户}-{主题}-{日期}/投标结果.md" content="..."
```

#### 1j. 双提议

```markdown
✓ 确定性链接已自动建立：
- [[线索池/活跃线索/线索-{客户}-{主题}/线索-{客户}-{主题}]] — 来源线索（prospect 参数已指定）
- [[客户档案/{客户}]] — 客户档案（如存在）

提议 1 — 关联建议：
1. `知识库/合同范本/` — 历史同类项目合同参考

提议 2 — 后续行动：
1. 是否立即进入售前阶段？
   → /presales 开始需求分析对接
2. 是否关联下游合作团队？（如需联合投标）

🏷️ 投标状态建议：→ needs-analysis（售前项目已创建）

请回复编号确认，或纠正状态，或"跳过"
```

#### 1k. 更新售前看板

操作完成后，自动更新售前管道看板：

```bash
obsidian read path="售前项目/售前看板.md"
obsidian files folder="售前项目"
```

扫描所有 `售前项目/{客户}-{主题}-{日期}/` 目录，对每个项目：
1. 读已有文件推导当前状态（见 SCHEMA.md §4 投标状态定义）
2. `stat` 关键文件取 mtime 计算最近活动距今天数
3. 读对应文件提取最紧急的下一步行动（截断至 15 字）
4. 标记 >30 天无活动的项目到停滞预警
5. 项目列 wikilink 必须指向入口笔记，禁止将文件夹名作为链接目标。格式：`[[售前项目/{客户}-{主题}-{日期}/00-项目概览\|{主题}]]`，客户列填纯文本 `{客户}`

```bash
obsidian create path="售前项目/售前看板.md" content="[全量重新生成的内容]"
```

看板不存在时用 `templates/cards/presales-kanban.md` 创建。

---

### Step 2: 更新技术方案 / 商务报价（action=update）

#### 2a. 选择售前项目

```bash
obsidian files folder="售前项目"
```

列出售前项目供选择。

#### 2b. 选择要更新的文档

```
要更新哪个文档？
1. 技术方案.md
2. 商务报价.md
```

#### 2c. 读取并更新

```bash
obsidian read path="售前项目/{客户}-{主题}-{日期}/{选择的文档}.md"
```

根据用户输入，append 或 overwrite 对应内容。

#### 2d. 双提议

读售前项目已有文件，推导当前状态后：

```markdown
提议 1 — 关联建议：
1. 本次更新是否影响关联文档？

提议 2 — 后续行动：
1. 如更新了商务报价，是否已通过内部审批？
2. 是否已具备投标递交条件？
3. 🏷️ 投标状态建议：当前 {derived_state} → 建议 {next_state}（基于本次更新内容）

请回复编号确认，或纠正状态，或"跳过"
```

#### 2e. 更新售前看板

同 Step 1j — 全量扫描 `售前项目/` 重新生成 `售前项目/售前看板.md`。

---

### Step 3: 记录投标结果（action=result）

#### 3a. 选择售前项目

```bash
obsidian files folder="售前项目"
```

#### 3b. 填写结果

与用户对话收集：
- 中标/未中标
- 中标金额
- 中标单位（如未中标）
- 我方排名（如未中标）
- 未中标原因分析

#### 3c. 更新投标结果文档

```bash
obsidian read path="售前项目/{客户}-{主题}-{日期}/投标结果.md"
```

更新 frontmatter 和正文。

#### 3d. 双提议

```markdown
🏷️ 投标状态建议：→ won（中标）/ → lost（未中标）

提议 1 — 关联更新：
1. 更新关联的 [[线索池/活跃线索/线索-{客户}-{主题}/线索-{客户}-{主题}]]（中标 → 已转化 / 未中标 → lost）
2. 是否更新 [[客户档案/{客户}]] 中的合作历史？

提议 2 — 后续行动：
{如中标}
1. → 输入 /initiate 正式立项
2. 报价单关键数字将同步到项目预算
{如未中标}
1. 是否将经验教训沉淀到知识库/经验教训/？
2. 是否将竞品"{中标单位}"的信息沉淀到 知识库/竞品/？
   → 如确认，创建 知识库/竞品/{中标单位}.md（自动链接来源 [[售前项目/{客户}-{主题}-{日期}/投标结果]]）
3. 该竞品是否在历史其他投标中也出现过？搜索 vault 中关联投标

请回复编号确认，或纠正状态，或"跳过"
```

#### 3e. 后续处理

如中标且用户确认：
```
🎉 恭喜中标！

下一步：
→ /initiate 正式立项
→ 线索自动 move 到 已转化/
→ 报价单关键数字同步到项目预算
```

如未中标且用户确认沉淀经验教训：
- 创建 `知识库/经验教训/{项目}-投标复盘.md`

如未中标且用户确认沉淀竞品信息：
```bash
obsidian create path="知识库/竞品/{中标单位}.md" content="..."
# 自动链接来源 [[售前项目/{客户}-{主题}-{日期}/投标结果]]（确定性链接）
# 如用户确认历史关联投标，在竞品档案中列出
```

#### 3f. 更新售前看板

同 Step 1j — 全量扫描 `售前项目/` 重新生成 `售前项目/售前看板.md`。

---

## 与其他 Skill 的协作

| 场景 | 组合 |
|------|------|
| 投标建档后进入售前 | `/bid action=new` → `/presales` |
| 需求锁定后报价 | `/presales action=lock` → `/bid action=update` |
| 中标后立项 | `/bid action=result` → `/initiate` |
| 投标前了解客户 | `/bid` → `/query "客户X的历史合作"` |
| 未中标沉淀知识 | `/bid action=result` → 知识库经验教训 + 竞品 |

---

## Notes

- `/bid action=new` 创建售前项目骨架（4 个核心文档 + 3 个共享子目录），不创建售前文档
- 售前文档（客户需求分析、解决方案、售前材料清单）由 `/presales` 管理
- 技术交流记录由 `/presales action=tech-exchange` 管理
- 需求锁定由 `/presales action=lock` 完成，锁定后回到 `/bid` 进入商务报价阶段
- 一个线索可能对应多次投标（如初投未中，二次招标）
- 报价关键数字将在 `/initiate` 立项时同步到项目预算
