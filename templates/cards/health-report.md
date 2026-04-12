---
title: "Vault Health Report YYYY-MM-DD"
tags:
  - type/health-report
  - domain/meta
date: YYYY-MM-DD
---

<!--
⚠️ 这是 Knowledge MEMO 作者的个人模板样本。
Health Report 由 /lint 自动生成，一般不需要你手写 —— 这份模板只是参考结构。
请 fork 改造，而不是原样使用。
参见: docs/philosophy.md § "知识管理是高度个人化的"
-->

# Vault Health Report — YYYY-MM-DD

## 总览
- **总 Card 数**: {{N}}
- **健康评分**: {{A / B / C / D}}
- **上次 Lint**: YYYY-MM-DD

## 🔴 高严重度（必须处理）
### 断链
- [[不存在的 Card 1]] ← 被 [[某卡]] 引用
- ...

### 缺 frontmatter
- {{文件路径 1}}
- ...

## 🟡 中严重度（建议处理）
### 孤岛 Card（零 backlink）
- [[孤岛卡 1]]

### MOC 遗漏新 Card
- {{domain}} MOC 漏了 [[新卡 1]]

## 🔵 信息
### Clippings 库存
- 待研究: {{N}} 张
- 已研究: {{N}} 张
- 超过 30 天未研究: {{N}} 张

### 知识缺口（按 domain 排序空链密度）
- {{domain 1}}: {{N}} 个空链 → 建议研究方向
- {{domain 2}}: {{N}} 个空链

## 建议
{{lint 不自动修复，只列建议。你决定先处理哪些。}}
