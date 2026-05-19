# 15 分钟快速上手

> 目标：从 "刚 clone 这个 repo" 到 "第一个项目已立项，跑通了 /initiate → /monitor → /query 闭环"。

本指南面向 **Claude Code** 用户。假设你：
- 已经在用 Obsidian
- 已经安装并配置了 Claude Code
- 想要最快见到效果，而非一次性完美配置

---

## 第 0-3 分钟：安装 Skills + 规则文件

### 1. Clone 仓库

```bash
git clone https://github.com/canxer314/knowledge-mgmt.git
cd knowledge-mgmt
```

### 2. 安装 Skills 到 Claude Code

```bash
mkdir -p "$HOME/.claude/skills"
cp -r prospect bid presales initiate plan contract meeting change acceptance work-item monitor payment query lint "$HOME/.claude/skills/"
```

### 3. 安装 Schema 和 Agent 规则到 Obsidian Vault

```bash
cp SCHEMA.md AGENTS.md /path/to/your/obsidian/vault/
```

添加桥接文件，让 Claude Code 在操作 vault 时自动加载规则：

```bash
cat > /path/to/your/obsidian/vault/CLAUDE.md <<'EOF'
Read AGENTS.md before operating this vault.
EOF
```

### 4. （可选）安装模板

```bash
cp -r templates /path/to/your/obsidian/vault/
```

---

## 第 3-5 分钟：验证 Obsidian CLI 连通

打开你的 vault 在 Obsidian 中，然后验证 CLI 可连通：

```bash
obsidian vault
```

如果报 connection refused，确保 Obsidian 正在运行且 vault 已打开。

---

## 第 5-10 分钟：创建第一个项目

不需要先建线索、先建售前项目。直接从 `/initiate` 开始——用你最近在跟的一个项目做实验。

在 Claude Code 中，输入：

```text
/initiate
```

Claude 会与你对话，收集以下信息：
- 项目名称
- 客户名称
- 合同金额
- 合同起止日期
- 付款节点
- 总体预算

对话完成后，`/initiate` 会在你的 Obsidian Vault 中创建完整项目结构：

```
项目库/PJ-2026-001-{项目名}/
├── 00-项目章程.md          ← 项目总览 + 导航
├── 01-合同/主合同关键条款.md
├── 02-计划/
├── 03-执行/
├── 04-监控/
│   ├── 风险登记册.md
│   ├── 预算执行表.md
│   ├── 问题跟踪.md
│   └── 回款跟踪.md
├── 05-验收/
└── 06-收尾/
```

**成功标志**：在 Obsidian 中看到完整的项目文件夹结构，项目章程的 frontmatter 包含正确的 `project_id`、`client`、`contract_value`。

---

## 第 10-13 分钟：制定计划 + 健康检查

### 制定里程碑计划

```text
/plan project=PJ-2026-001
```

Claude 会帮你创建 WBS 工作分解和里程碑计划。里程碑的付款节点会自动关联到合同关键条款。

### 运行健康检查

```text
/monitor project=PJ-2026-001 action=health
```

Claude 会读取项目章程、里程碑计划、风险登记册、预算执行表，计算四维健康度（进度 / 预算 / 质量 / 风险），输出健康报告。

**成功标志**：健康报告展示了项目的综合健康度分数和各维度状态。

---

## 第 13-15 分钟：查询验证

测试治理层查询能力：

```text
/query "PJ-2026-001 的健康状态如何？"
```

```text
/query "我有哪些活跃项目？"
```

成功标志：回答引用了 vault 中的实际文档（用 `[[文档名]]` 标注来源）。

---

## 15 分钟后你拥有了什么

- `SCHEMA.md` + `AGENTS.md` 在 vault 根目录
- 一个完整的项目结构（`项目库/PJ-2026-001-xxx/`），包含章程、合同条款、风险登记册
- 至少一份里程碑计划
- `/monitor` 和 `/query` 能够正确读取项目数据

---

## 接下来做什么

1. **跑通完整链路**：从 `/prospect` 建一个线索 → `/bid` 创建投标 → `/initiate` 立项 → `/plan` 排计划 → `/monitor` 跟踪
2. **定制 SCHEMA.md**：根据你的实际项目类型调整 Card 类型和命名规范
3. **修改模板**：`templates/cards/` 中的模板改为你自己的写作习惯
4. **日常使用一周**：每天 `/monitor action=track` 做站会跟踪，积累真实数据后跑 `/lint` 做体检
5. **积累经验教训**：项目收尾时用 `/close` 生成复盘，沉淀到 `知识库/经验教训/`

---

## 常见踩坑

- **Obsidian CLI 连不上**：确保 Obsidian 已打开目标 vault，CLI 通过 socket 与运行中的 Obsidian 通信
- **Skills 加载不到**：检查 `~/.claude/skills/` 目录结构，每个 skill 目录下必须有 `SKILL.md`
- **首次 `/initiate` 信息不全**：没关系，后续可通过各 Skill 补全——合同条款用 `/contract`，计划用 `/plan`
- **想一次性配完美**：不用。先用默认配置跑完一个项目周期，再回来改 SCHEMA 和模板
