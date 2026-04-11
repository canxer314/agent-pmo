---
name: lint
description: Obsidian Vault 全量体检。扫描断链、孤岛、缺标签、噪声标签、Clipping 库存、MOC 完整性，产出健康报告。当用户说"lint"、"体检"、"vault 检查"、"健康检查"时触发。
invocation: user
---

# /lint — Vault 健康体检

> 参考规则：先读取 vault 根目录 `SCHEMA.md` 获取完整检查项定义。

## 执行流程

### Step 1: 读取 Schema

```bash
obsidian read path="SCHEMA.md"
```

确认当前检查项清单和标签体系定义。

### Step 2: 全量扫描

并行执行以下检查（使用 Obsidian CLI + subagent 加速）：

#### 2a: 链接检查
```bash
# 断链：搜索所有 wikilink，检查目标是否存在
obsidian search query="[["
# 孤岛：检查 Cards/ 下零 backlink 的文件
# 对每个 Card: obsidian backlinks path="Cards/{name}.md"
```

#### 2b: 标签检查
```bash
# 扫描所有 Cards，检查 frontmatter 中是否有 type/ 和 domain/ 标签
# 扫描所有标签，找出不属于四维体系的噪声标签
obsidian tags path="Cards/"
```

#### 2c: 格式检查
```bash
# 扫描所有 .md 文件，检查是否有 frontmatter（以 --- 开头）
obsidian files folder="Cards"
# 逐个读取检查 frontmatter
```

#### 2d: Clipping 库存
```bash
# 统计待研究 / 已研究数量（按文件夹区分）
obsidian files folder="Clippings"       # 待研究（根目录下的 .md 文件）
obsidian files folder="Clippings/已研究"  # 已研究
# 检查超过 30 天未研究的（按 created 字段判断）
```

#### 2e: MOC 完整性
```bash
# 读取每个 MOC 文件
# 检查是否有 Card 被遗漏（有 domain 标签但不在对应 MOC 中）
# 检查 MOC 中的链接是否有效
```

#### 2f: 空链统计（知识缺口）
```bash
# 收集所有指向不存在页面的 [[wikilink]]
# 按 domain 分组统计
```

### Step 3: 安全写入

Lint 可自动执行的（无需用户确认）：
1. 生成健康报告

Lint **不能自动执行的**（只报告）：
- 修复断链、补标签、建 Card、修改/删除任何内容

### Step 4: 生成健康报告

产出格式：

```markdown
---
title: "Vault Health Report YYYY-MM-DD"
tags:
  - type/health-report
date: YYYY-MM-DD
---

## 总览

- 健康评分: XX/100
- Cards: {总数} | Clippings: {unread数} unread / {read数} read
- 断链: {数量} | 孤岛: {数量} | 噪声标签: {数量}

## 🔴 需要修复（高严重度）

{断链清单、缺标签 Card 清单、缺 frontmatter 文件清单、MOC 链接失效}

## 🟡 建议改善（中严重度）

{孤岛 Card、噪声标签、超 30 天 unread Clippings、MOC 遗漏}

## 🟢 信息

{Clipping 库存统计、空链统计}

## 📚 研究缺口建议

{按 domain 分组的空链热点，建议研究方向}
```

### Step 5: 存入 Vault

```bash
obsidian create path="Cards/Vault Health Report YYYY-MM-DD.md" content="..." overwrite
```

### Step 6: 输出摘要

向用户展示报告核心数据和需要关注的高优先级项目。

## 评分规则

| 扣分项 | 每个扣分 |
|--------|----------|
| 断链 | -3 |
| 缺 frontmatter | -2 |
| 缺四维标签 | -1 |
| 孤岛 Card | -0.5 |
| 噪声标签 | -1 |
| MOC 遗漏 | -0.5 |

满分 100，扣完为止，最低 0 分。

## Cron 模式

被 cron 调用时（非用户手动触发），行为与手动相同，但：
- 报告自动写入 `Journal/Vault Health Report YYYY-MM-DD.md`（而非 Cards/）
- 不输出到对话（无用户在场）
- 安全写入照常执行（补 unread status）
