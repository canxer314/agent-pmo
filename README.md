# Knowledge MEMO — Project Lifecycle Management System

> **个人项目全生命周期绩效运营系统**
>
> 适用角色：项目经理（交付运营）+ 业务经理（前端经营）+ 售前技术工程师（解决方案）+ 解决方案工程师
>
> 本系统覆盖从售前对接 → 投标 → 立项 → 执行 → 收尾的全流程，同时支持售前材料管理和需求锁定。

---

## 系统定位

| 原有定位（v1-v2） | 新定位（v3+）|
|---|---|
| LLM Wiki + 间隔重复 | 项目全生命周期管理 |
| 个人知识积累 | 售前→投标→合同→执行→回款 |
| /read /insights /note /review | /prospect /bid /presales /initiate /plan /meeting /change /payment /monitor /close |

---

## 核心概念

### 三层架构

```
┌─────────────────────────────────────────────────────────┐
│  L1 Schema Layer（规则层）                               │
│  SCHEMA.md · AGENTS.md                                  │
│  三层架构 / 14+ Card 类型 / 状态流转 / 权限矩阵         │
├─────────────────────────────────────────────────────────┤
│  L2 Flywheel Layer（生命周期飞轮）                       │
│  /prospect → /bid → /presales → /initiate → /plan          │
│  /meeting → /change → /payment → /close                    │
│  （AI 执行，人验证）                                     │
├─────────────────────────────────────────────────────────┤
│  L3 Governance Layer（治理层）                           │
│  /query · /lint                                         │
│  （AI 扫描，人决策）                                     │
└─────────────────────────────────────────────────────────┘
```

### 目录结构

```
Vault/
├── SCHEMA.md                    # 本文件
├── AGENTS.md                    # Agent 操作规则
├── 线索池/                       # 业务经理：售前线索
├── 投标档案/                     # 投标过程留痕（/bid + /presales + /meeting）
├── 项目库/                       # 正式立项后的项目（核心）
│   └── {PJ-YYYY-NNN}/
│       ├── 00-项目章程.md
│       ├── 01-合同/
│       ├── 02-计划/
│       ├── 03-执行/
│       ├── 04-监控/
│       ├── 05-验收/
│       └── 06-收尾/
├── 客户档案/                     # 客户维护
├── 供应商库/                     # 采购管理
├── 知识库/                       # 可复用经验
└── 个人工作台/                   # 每日仪表盘
```

---

## 十二个 Skills

### 生命周期飞轮

| Skill | 职责 | 输出 |
|-------|------|------|
| `/prospect` | 线索管理 | 线索文档 |
| `/bid` | 投标管理（建档 + 技术方案 + 商务报价 + 结果）| 投标档案骨架 |
| `/presales` | 售前工作台（需求分析 + 方案迭代 + 材料管理 + 需求冻结）| 售前文档 |
| `/initiate` | 项目立项（唯一创建项目结构的通道） | 项目文件夹 + 章程 |
| `/plan` | 计划制定 | WBS + 里程碑 |
| `/meeting` | 会议纪要（售前技术交流 / 执行阶段会议） | 会议文档 |
| `/change` | 变更管理 | 变更记录 |
| `/payment` | 回款跟踪 | 回款汇总 + 催款跟踪 |
| `/close` | 项目收尾 | 决算 + 复盘 |

### 治理层

| Skill | 职责 | 输出 |
|-------|------|------|
| `/monitor` | 运营监控（站会跟踪 + 健康度诊断） | 看板更新 + 健康报告 + 工作台 |
| `/query` | 查询项目知识 | 带来源的答案 |
| `/lint` | Vault 体检 | 健康报告 |

---

## 典型工作流

### 售前→投标流程

```
/prospect 线索推进到方案沟通
    ↓
/bid action=new（创建投标档案骨架）
    ↓
↓ 售前阶段（循环迭代）↓
/presales 更新「客户需求分析」（首次需求对接）
/presales 更新「解决方案」（方案成形）
/presales action=material（材料版本管理）
/meeting 记录技术交流（售前阶段）
    ↓
/presales action=lock（锁定合同内容）
    ↓
/bid action=update（更新商务报价）
    ↓
/bid action=result（记录投标结果）
    ↓
【中标】→ /initiate 立项
```

### 项目执行流程

```
/initiate 立项
    ↓
/plan 制定 WBS 和里程碑
    ↓
/meeting 记录启动会
    ↓
↓ 执行阶段（循环）↓
/meeting 记录周例会/评审会
/monitor 定期健康检查
/change 处理变更需求
/payment 跟踪回款节点
    ↓
/close 项目收尾
```

---

## 安装

### 1. 克隆

```bash
git clone https://github.com/owenliang60-ship-it/knowledge-mgmt.git
cd knowledge-mgmt
```

### 2. 安装 Skills 到 Agent Runtime

**Claude Code**

```bash
mkdir -p "$HOME/.claude/skills"
cp -r prospect bid presales initiate plan meeting change monitor payment query lint "$HOME/.claude/skills/"
```

**Codex**

```bash
mkdir -p "$HOME/.agents/skills"
cp -r prospect bid initiate plan meeting change monitor query lint "$HOME/.agents/skills/"
```

### 3. 安装 SCHEMA + AGENTS 到 Obsidian Vault

```bash
cp SCHEMA.md AGENTS.md /path/to/your/obsidian/vault/
```

**Claude Code** 用户需要添加桥接文件：

```bash
cat > /path/to/your/obsidian/vault/CLAUDE.md <<'EOF'
Read AGENTS.md before operating this vault.
EOF
```

### 4. 安装模板（可选）

```bash
cp -r templates /path/to/your/obsidian/vault/
```

---

## 关键设计

### 双提议机制（Human-in-the-loop 强制点）

所有项目相关写入动作必须经过双提议：

**提议 1 — 关联建议**：新文档关联哪些已有文档（客户档案、线索、合同等）

**提议 2 — 后续行动**：建议下一步操作（更新其他文档、通知相关方等）

用户逐条确认后，AI 才执行写入。

### 状态标签体系

所有 Card 必须有三维标签：`type/` + `status/` + `priority/`

```
type:   prospect | bid | project | milestone | meeting | change | risk | ...
status: active | done | blocked | cancelled | pending | ...
priority: p0 | p1 | p2 | p3
```

### 确定性链接（自动建立，无需提议）

| 场景 | 自动操作 |
|------|----------|
| `/initiate` 创建项目 | 自动在项目章程中链接 `[[客户档案-{client}]]` |
| `/plan` 创建里程碑 | 自动在里程碑中链接 `[[00-项目章程]]` |
| `/meeting` 创建纪要 | 自动链接 `[[00-项目章程]]` |
| `/change` 创建变更 | 自动链接 `[[预算执行表]]` 和受影响里程碑 |
| 线索中标转化 | 自动 move 线索到 `已转化/`，并链接到项目章程 |

---

## 与旧版差异

| 功能 | 旧版（v1-v2） | 新版（v3+）|
|------|---------------|-------------|
| 核心理念 | LLM Wiki + 知识积累 | 项目全生命周期管理 |
| 核心用户 | 个人知识管理者 | 项目经理 + 业务经理 + 售前 |
| 存储内容 | 论文/文章/笔记 | 线索/投标/合同/里程碑/变更 |
| 典型操作 | /read /note /review | /prospect /bid /initiate /monitor |
| 复习方式 | FSRS-6 间隔重复 | 回款跟踪 + 里程碑进度 |
| 治理检查 | 断链/孤岛 | 项目健康度（进度/预算/质量/风险）|

---

## License

MIT — see [LICENSE](./LICENSE).
