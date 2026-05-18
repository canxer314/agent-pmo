---
name: plan
description: "计划制定。基于项目章程和合同约束，分解WBS、制定里程碑计划。当用户说'plan'、'排计划'、'WBS'、'里程碑'、'工作分解'时触发。"
invocation: user
arguments:
  - name: project
    description: "项目编号或名称。如不提供，列出活跃项目供选择。"
    required: false
---

# /plan — 计划制定

基于项目章程和合同约束，分解工作结构（WBS）并制定里程碑计划。

## 定位

| Skill | 职责 | 输出 |
|-------|------|------|
| `/initiate` | 项目立项 | 项目结构 + 章程 + 合同条款 |
| `/plan` | **计划制定 — 唯一创建里程碑的通道** | WBS + 里程碑计划 |
| `/monitor` | 运营监控 | 进度跟踪 + 健康报告 |

**典型工作流**: `/initiate` 立项 → `/plan` 制定计划 → `/monitor` 跟踪执行

---

## Behavior

### Step 1: 获取项目信息

#### 1a. 选择项目

如提供 `project` 参数：

```bash
obsidian read path="项目库/{project}/00-项目章程.md"
```

未提供时：

```bash
obsidian search query="type/project"
```

列出 `status: initiated` 或 `status: planning` 的项目供选择。

#### 1b. 读取约束条件

```bash
obsidian read path="项目库/{project}/01-合同/主合同关键条款.md"
```

提取关键约束：
- 合同起止日期
- 付款节点及对应条件
- 验收条件
- 延期违约金条款

### Step 2: 与用户对话分解 WBS

#### 2a. WBS 分解

引导用户分解工作包：

```markdown
请分解项目工作结构（WBS）：

1. 项目有哪些主要阶段？（如：需求 → 设计 → 开发 → 测试 → 上线 → 验收）
2. 每个阶段下有哪些工作包？
3. 每个工作包的交付物是什么？
4. 工作包之间的依赖关系？
```

#### 2b. 生成 WBS 文档

```markdown
---
title: "WBS-工作分解"
type: project
project: "{project_id}"
tags:
  - type/project
---

# WBS-工作分解

## 项目阶段

### 1. 需求阶段

| 工作包 | 交付物 | 负责人 | 工期 |
|--------|--------|--------|------|
| 1.1 需求调研 | 《需求调研报告》 | | 2周 |
| 1.2 需求分析 | 《需求规格说明书》 | | 2周 |
| 1.3 需求确认 | 《需求确认书》 | | 1周 |

### 2. 设计阶段

...

## 依赖关系

```mermaid
gantt
title 项目甘特图（概要）
dateFormat YYYY-MM-DD
section 需求
需求确认 :a1, 2026-05-15, 5w
section 设计
系统设计 :a2, after a1, 4w
...
```
```

### Step 3: 制定里程碑计划

#### 3a. 里程碑定义

基于 WBS 和合同付款节点，定义里程碑（此处仅为规划内容，待用户确认后写入）：

```markdown
---
title: "里程碑计划"
type: milestone
project: "{project_id}"
tags:
  - type/milestone
---

# 里程碑计划

| 编号 | 里程碑 | 计划日期 | 付款节点 | 完成标准 | 负责人 | 状态 |
|------|--------|----------|----------|----------|--------|------|
| M1 | 需求确认 | 2026-06-15 | 30% | 客户签署《需求确认书》 | | not-started |
| M2 | 系统设计完成 | 2026-07-15 | — | 通过设计评审 | | not-started |
| M3 | 系统上线 | 2026-10-01 | 30% | 通过上线验收 | | not-started |
| M4 | 终验 | 2026-12-01 | 10% | 通过终验 | | not-started |
```

#### 3b. 里程碑文档内容（待确认后写入）

每个里程碑单独成文档，存于 `02-计划/`。内容模板如下：

```markdown
---
title: "里程碑-{名称}"
type: milestone
project: "{project_id}"
planned_date: YYYY-MM-DD
actual_date:
payment_pct: 30
completion_pct: 0
status: not-started
deliverables:
  - 《需求调研报告》
  - 《需求规格说明书》
  - 《需求确认书》
tags:
  - type/milestone
  - status/not-started
---

# 里程碑-{名称}

> 计划日期：YYYY-MM-DD | 付款节点：X%

## 完成标准

- [ ] 客户签署《需求确认书》
- [ ] 内部评审通过

## 前置条件

- [[WBS-工作分解]] 中对应任务完成

## 下游影响

- [[里程碑-{下游名称}]] 依赖此里程碑
```

### Step 4: 双提议

```markdown
✓ 确定性链接已自动建立：
- [[00-项目章程]] — 已自动关联（每个里程碑）
- [[02-计划/里程碑计划]] — 已自动关联（索引页）
- {payment_pct > 0 的里程碑} [[01-合同/主合同关键条款]] — 已自动关联（付款节点来源）

提议 1 — 合同对齐检查：
1. {如有} 里程碑 X 无对应付款节点 — 建议确认是否为内部里程碑
2. 各里程碑的完成标准是否与验收条件对齐？

提议 2 — 风险/依赖建议：
1. 是否从历史项目读取同类里程碑的实际工期作为参考？
2. 里程碑之间是否有关键路径风险？建议检查
3. 是否需要为每个里程碑预设验收检查清单？

请回复编号确认，或"跳过"
```

### Step 5: 写入里程碑文档并更新项目章程

#### 5a. 写入里程碑文档（如用户确认）

```bash
# 创建里程碑计划总文档
obsidian create path="项目库/{project}/02-计划/里程碑计划.md" content="..."

# 创建各里程碑单独文档
obsidian create path="项目库/{project}/02-计划/里程碑-需求确认.md" content="..."
obsidian create path="项目库/{project}/02-计划/里程碑-系统设计完成.md" content="..."
obsidian create path="项目库/{project}/02-计划/里程碑-系统上线.md" content="..."
obsidian create path="项目库/{project}/02-计划/里程碑-终验.md" content="..."
```

#### 5b. 更新项目章程

```bash
obsidian read path="项目库/{project}/00-项目章程.md"
```

在项目章程的"快速状态 → 里程碑总览"表格中填入里程碑信息。

更新项目状态：

```bash
obsidian property:set path="项目库/{project}/00-项目章程.md" name="tags" value="type/project,status/planning,priority/p0" type=list
```

### Step 6: 输出确认

```markdown
---
计划已制定：{project}

📋 WBS：{N} 个阶段，{M} 个工作包
📅 里程碑：{K} 个
   - 含付款节点：{X} 个
   - 内部里程碑：{Y} 个

📎 已关联：
- 合同付款节点已对齐
- 项目章程已更新里程碑总览

下一步：
→ /meeting 召开项目启动会，确认计划
→ /monitor 开始跟踪里程碑进度
```

---

## 与其他 Skill 的协作

| 场景 | 组合 |
|------|------|
| 计划后开启动会 | `/plan` → `/meeting` |
| 计划后监控进度 | `/plan` → `/monitor` |
| 检查历史工期参考 | `/plan` 中 → `/query "同类项目里程碑实际工期"` |
| 里程碑延期需变更 | `/monitor` 发现 → `/change` |

---

## Notes

- `/plan` 是 vault **唯一创建里程碑的通道**
- 里程碑必须与合同付款节点对齐（如有）
- 每个里程碑的 `payment_pct` 字段用于 `/monitor` 的收款跟踪
- 里程碑延期时，`/monitor` 会提示是否走 `/change`
