---
name: lint
description: "项目治理体检。扫描断链、项目结构缺失、客户档案未关联、里程碑无合同对应、数据不一致、跨项目命名冲突。产出健康报告。当用户说'lint'、'体检'、'vault检查'、'健康检查'时触发。"
invocation: user
arguments:
  - name: scope
    description: "'all'（全 vault）、'project'（仅项目库）、'links'（仅链接检查）。默认 'all'"
    required: false
---

# /lint — 项目治理体检

全 vault 体检，确保项目档案的完整性和一致性。

## 定位

| Skill | 职责 | 输出 |
|-------|------|------|
| `/monitor` | 运营监控 | 项目健康度（业务层面） |
| `/lint` | **项目治理体检（结构层面）** | Vault 健康报告 |
| `/query` | 跨项目查询 | 知识检索 |

---

## Behavior

### Step 1: 读取 Schema

```bash
obsidian read path="SCHEMA.md"
```

确认当前检查项清单和规则定义。

### Step 2: 全量扫描

并行执行以下检查：

#### 2a: 链接检查

```bash
# 断链：搜索所有 wikilink，检查目标是否存在
obsidian search query="[["

# 对每个项目检查内部链接
obsidian files folder="项目库"
```

#### 2b: 项目结构检查

```bash
# 扫描每个项目文件夹
obsidian folders folder="项目库"
```

检查每个项目是否包含必需文档：
- `00-项目章程.md`
- `01-合同/主合同关键条款.md`
- `04-监控/风险登记册.md`
- `04-监控/预算执行表.md`
- `04-监控/问题跟踪.md`

#### 2c: 关联检查

```bash
# 检查项目章程的 client 字段
obsidian search query="type/project"
```

逐个读取项目章程，检查：
- `client` 字段是否对应存在的客户档案
- `project_id` 是否与文件夹名一致

#### 2d: 里程碑对齐检查

```bash
obsidian search query="type/milestone"
```

检查：
- 里程碑是否有对应的合同付款节点（如 `payment_pct > 0`）
- 里程碑状态是否与完成率一致
- `planned_date < today` 且 `status` 不是 `done` 的里程碑，是否有关联的变更记录（CR）说明延期原因

> 交叉检查方法：对每个逾期里程碑，搜索 `变更记录/` 下所有 CR 的正文和 frontmatter，检查是否有 `[[里程碑-{name}]]` 引用。无引用则报告。

#### 2e: 变更检查

```bash
obsidian files folder="项目库" pattern="*/变更记录/*"
```

检查：
- 变更记录是否有影响评估
- 已批准变更是否已更新里程碑/预算

#### 2f: 会议纪要检查

```bash
obsidian files folder="项目库" pattern="*/会议纪要/*"
```

检查：
- 会议纪要是否有决议项
- 决议项是否有责任人+截止日期

#### 2g: 风险检查

```bash
obsidian search query="type/risk"
```

检查：
- 高风险项是否超过 7 天未更新
- 风险是否有应对措施和责任人
- 是否存在未被任何会议纪要或变更记录引用的孤儿风险

> 孤儿风险判断：扫描该 `type/risk` 条目（风险登记册中的行），检查是否有任何 `会议纪要/` 或 `变更记录/` 文档通过 wikilink 引用该风险。无引用则标记为孤儿。

#### 2h: 数据一致性检查

```bash
# 预算执行表 vs 支出记录
obsidian search query="type/cost-report"
```

检查：
- 预算执行表的总支出是否等于各支出记录之和
- 里程碑完成率 100% 的文档状态是否为 done
- 项目状态 closed 的是否还有 active 里程碑

#### 2i: 命名一致性检查

```bash
obsidian search query="客户档案"
```

检查：
- 同一客户在不同项目中名称是否一致
- 项目编号是否符合 `PJ-YYYY-NNN` 格式

#### 2j: 空链统计

```bash
obsidian search query="[["
```

收集所有指向不存在页面的 wikilink，按项目分组统计。

#### 2k: 看板检查

```bash
# 检查交付看板是否存在
obsidian search query="type/kanban"
obsidian read path="项目库/{project}/03-执行/交付看板.md"
```

检查：
- 项目 status 为 executing 但交付看板不存在
- REQ 条目缺少 `milestone` 字段关联
- REQ 预计日期超过关联里程碑计划日期但无对应 CR
- TMP done 超过 7 天未移动到归档区

#### 2l: 专项工作检查

```bash
obsidian search query="type/work-item"
```

对每个 `type/work-item` 文档检查：
- `source=meeting` 但 `source_doc` 指向的会议纪要文件不存在（断链）
- `deadline < today` 且 `status` 不是 `done`（过期未完成）
- 该文档未被任何看板的 TMP 行通过 wikilink 引用（孤儿工作 — 有文档但无跟踪）

> 判断"未被看板引用"的方法：从交付看板中提取所有 `[[专项工作/...]]` 链接，与 `专项工作/` 下实际文件做差集。

### Step 3: 安全写入

Lint 可自动执行的（无需用户确认）：
1. 生成健康报告

Lint **不能自动执行的**（只报告）：
- 修复断链
- 补标签
- 建文档
- 修改/删除任何内容

### Step 4: 生成健康报告

产出格式：

```markdown
---
title: "Vault Health Report YYYY-MM-DD"
type: cost-report
date: YYYY-MM-DD
tags:
  - type/cost-report
---

# Vault Health Report YYYY-MM-DD

## 总览

- 健康评分: XX/100
- 项目数: {N} | 活跃: {N} | 已关闭: {N}
- 断链: {N} | 结构缺失: {N} | 命名冲突: {N}

## 🔴 需要修复（高严重度）

| 项目 | 问题 | 建议 |
|------|------|------|
| PJ-001 | 断链：`[[李四]]` 不存在 | 创建干系人档案或修正姓名 |
| PJ-002 | 项目结构缺失：无风险登记册 | 补充创建 |

## 🟡 建议改善（中严重度）

| 项目 | 问题 | 建议 |
|------|------|------|
| PJ-001 | 里程碑"系统上线"无合同付款节点对应 | 核对合同条款 |
| 跨项目 | 客户名不一致：`某市政府` vs `市政府` | 统一命名 |

## 🟢 信息

| 类别 | 统计 |
|------|------|
| 线索池 | {N} 条待跟进 |
| 售前项目 | {N} 个，中标 {N} 个 |
| 项目库 | {N} 个，活跃 {N} 个 |
| 知识库 | {N} 条经验教训 |

## 数据一致性

| 检查项 | 结果 |
|--------|------|
| 预算汇总一致性 | ✓ / ✗ |
| 里程碑状态一致性 | ✓ / ✗ |
| 项目状态一致性 | ✓ / ✗ |
```

### Step 5: 存入 Vault

```bash
obsidian create path="个人工作台/Vault Health Report YYYY-MM-DD.md" content="..." overwrite
```

### Step 6: 输出摘要

向用户展示报告核心数据和需要关注的高优先级项目。

## 评分规则

| 扣分项 | 每个扣分 |
|--------|----------|
| 断链 | -3 |
| 项目结构缺失 | -5 |
| 客户档案未关联 | -5 |
| 项目状态 closed 但有 active 里程碑 | -5 |
| 里程碑无合同对应 | -2 |
| 变更无影响评估 | -2 |
| 会议纪要无决议跟踪 | -1 |
| 高风险项超期未更新 | -3 |
| 孤儿风险（未被会议纪要/变更引用）| -2 |
| 预算汇总不一致 | -5 |
| 里程碑状态不一致 | -3 |
| 里程碑逾期未关联变更记录 | -2 |
| 跨项目命名冲突 | -2 |
| 空链 | -0.5 |
| 看板缺失（executing 项目无看板） | -5 |
| REQ 无 milestone 关联 | -2 |
| REQ 日期溢出里程碑且无 CR | -5 |
| TMP done 未归档 | -1 |
| 专项工作 source_doc 断链 | -2 |
| 专项工作 deadline 过期未 done | -2 |
| 专项工作孤儿（未被看板引用） | -1 |

满分 100，扣完为止，最低 0 分。

## Cron 模式

被 cron 调用时（非用户手动触发），行为与手动相同，但：
- 报告自动写入 `个人工作台/Vault Health Report YYYY-MM-DD.md`
- 不输出到对话（无用户在场）
- **不做任何"顺手修复"**

---

## Notes

- `/lint` 是项目档案的**结构体检**，与 `/monitor` 的业务健康度互补
- 建议每周运行一次 `/lint`
- 所有修复建议必须经过用户确认后执行
- 评分规则可根据实际情况调整
