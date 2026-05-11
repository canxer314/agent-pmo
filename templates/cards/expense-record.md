---
title: "支出记录 EXP-{{编号}}"
type: expense
project: "{{project_id}}"
exp_id: "EXP-{{编号}}"
amount: {{金额}}
category: 人力成本 | 采购成本 | 管理费用 | 风险储备 | 其他
expense_date: YYYY-MM-DD
approval_status: pending | approved | rejected
invoice_status: 已开票 | 未开票 | 不需要
tags:
  - type/expense
  - status/{{状态}}
---

<!--
⚠️ 这是项目全生命周期系统的个人模板样本。
请 fork 改造，而不是原样使用。
-->

# 支出记录 EXP-{{编号}}

> 项目：[[00-项目章程]] | 日期：YYYY-MM-DD

## 基本信息

| 项 | 内容 |
|----|------|
| 支出编号 | EXP-{{编号}} |
| 金额 | {{金额}}万 |
| 类别 | {{类别}} |
| 日期 | YYYY-MM-DD |
| 审批状态 | {{状态}} |
| 发票状态 | {{发票状态}} |

## 用途说明

{{这笔支出的用途和原因}}

## 关联文档

- 来源依据：[[变更记录-CR-xxx]] / [[会议纪要-xxx]] / 其他
- 所属里程碑：[[里程碑-xxx]]

## 审批记录

| 审批人 | 意见 | 日期 |
|--------|------|------|
| | | |

## 付款信息

- 付款方式：
- 付款日期：
- 收款方：
