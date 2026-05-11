---
title: "变更请求 CR-{{编号}}"
type: change
project: "{{project_id}}"
cr_id: "CR-{{编号}}"
change_type: 范围变更 | 需求变更 | 工期调整 | 成本追加 | 其他
proposed_by: "{{提出人}}"
proposed_date: YYYY-MM-DD
impact_cost: +{{追加成本}}
impact_schedule: +{{追加天数}}
approval_status: draft | submitted | under-review | approved | rejected | implemented
tags:
  - type/change
  - status/draft
---

<!--
⚠️ 这是项目全生命周期系统的个人模板样本。
请 fork 改造，而不是原样使用。
-->

# 变更请求 CR-{{编号}}

> 项目：[[00-项目章程]] | 提出人：{{提出人}} | 日期：YYYY-MM-DD

## 变更内容

{{具体变更描述}}

## 变更原因

{{为什么需要变更}}

## 影响评估

### 工期影响

- 影响天数：+{{N}} 天
- 受影响里程碑：
  - [[里程碑-xxx]] — 计划从 {{原日期}} 调整为 {{新日期}}

### 成本影响

- 追加成本：+{{N}} 万
- 成本类别：
- 新预算总额：{{原预算}} + {{追加}} = {{新总额}}

### 质量影响

{{对交付物质量的影响}}

### 合同影响

- 是否涉及合同条款变更：
- 客户书面确认：已获取 / 待获取 / 不需要

## 审批记录

| 审批人 | 意见 | 日期 | 状态 |
|--------|------|------|------|
| | | | |

## 实施状态

- [ ] 已批准
- [ ] 已实施
- [ ] 已验证
