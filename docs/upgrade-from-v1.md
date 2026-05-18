# 从上游仓库同步更新

> 本指南适用于从 `owenliang60-ship-it/knowledge-mgmt` fork 并做了定制修改的用户。

---

## 背景

本仓库 fork 自 [owenliang60-ship-it/knowledge-mgmt](https://github.com/owenliang60-ship-it/knowledge-mgmt)，并针对 **售前 + 解决方案 + 项目管理** 场景做了适配。上游仓库会持续更新（新增 Skills、修复 bug、优化 Schema），本指南说明如何将上游更新合并到你的 fork 中。

---

## 前置检查

### 确认 remote 配置

```bash
git remote -v
```

应包含：
- `origin` → 你的 fork（`canxer314/knowledge-mgmt`）
- `upstream` → 上游仓库（如尚未添加，见下方）

### 添加上游 remote（如尚未配置）

```bash
git remote add upstream https://github.com/owenliang60-ship-it/knowledge-mgmt.git
git fetch upstream
```

---

## 同步流程

### 1. 确保本地工作区干净

```bash
git status
```

如有未提交的修改，先 stash 或 commit。

### 2. 拉取上游更新

```bash
git fetch upstream
git checkout main
git merge upstream/main
```

### 3. 处理冲突

上游更新可能与你的定制修改产生冲突。以下是常见的冲突场景及处理建议：

| 冲突文件 | 上游可能做了什么 | 你的处理策略 |
|----------|-----------------|-------------|
| `SCHEMA.md` | 新增 Card 类型、调整状态流转 | 仔细对比，保留你的定制部分（命名规范、目录结构），合并上游新增的类型定义 |
| `AGENTS.md` | 新增铁律、调整写入纪律 | 通常直接采用上游更新，铁律是底线规范 |
| `README.md` | 更新 Skill 列表、工作流说明 | 保留你的角色描述和 URL，合并上游新增的 Skill 说明 |
| `templates/cards/*.md` | 新增模板或修改 frontmatter | 对比差异，选择性合并——模板是你已经定制过的 |
| 新 Skill 目录 | 上游新增了独立 Skill | 直接合并，然后根据你的场景决定是否启用 |
| `docs/*.md` | 上游更新文档 | 你已重写了 docs/，需要手动阅读上游新文档，选择性采纳内容 |
| `*.SKILL.md` 内部 | 上游修改了 Skill 行为逻辑 | **重点审查**——这是核心执行逻辑，合并后需要重新测试 |

### 4. 重新安装 Skills

上游更新了 Skill 文件后，需要重新复制到 Claude Code 的 skills 目录：

```bash
cp -r prospect bid presales initiate plan contract meeting change acceptance work-item monitor payment query lint "$HOME/.claude/skills/"
```

### 5. 验证同步后的系统健康

```bash
# 在 Claude Code 中运行体检
/lint
```

确认没有因合并引入的结构性问题。

---

## 冲突预防策略

### 最小化定制文件的范围

以下文件是你**应该定制**的（上游不太可能改，或改了你也应该覆盖）：
- `CLAUDE.md`、`CLAUDE-bridge.md`、`AGENTS.md` 中的个人偏好部分
- `SCHEMA.md` 中的命名规范和目录结构

以下文件**尽量保持与上游一致**（减少合并冲突）：
- 各 `SKILL.md` 核心执行逻辑
- Card 类型定义体系
- 状态流转规则

### 记录你的定制决策

建议在每次同步后记录：

```markdown
## 同步记录

- YYYY-MM-DD：从 upstream/main 合并至 {commit-hash}
  - 采纳：新增 /work-item Skill、验收状态流转优化
  - 保留我的版本：docs/philosophy.md（已完全重写为项目治理哲学）
  - 冲突处理：SCHEMA.md 中合同状态定义有冲突，合并后以我的版本为主
```

---

## 常见问题

### Q: 上游的更新和我的定制冲突太多怎么办？

A: 选择性合并而非全量 merge。用 `git cherry-pick` 只拿你需要的 commit。或者阅读上游的变更 diff，手动将逻辑应用到你的版本中。

### Q: 我的 docs/ 已经全部重写了，上游 docs/ 更新怎么处理？

A: 阅读上游新的 docs/ 内容（不直接 merge），手动提取对你有用的部分，写入你的版本。

### Q: 上游新增了一个 Skill 但我用不上？

A: 仍然合并代码（保持 git 历史干净），但不复制到 `~/.claude/skills/`。Skill 未安装就不会被触发。

---

## 回退

如果同步后系统行为异常：

```bash
git reflog                    # 找到合并前的 commit
git reset --hard <commit>     # 回退到合并前
```

重新安装回退后的 Skills：

```bash
cp -r prospect bid presales initiate plan contract meeting change acceptance work-item monitor payment query lint "$HOME/.claude/skills/"
```
