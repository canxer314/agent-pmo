# Knowledge MEMO — Project Lifecycle Management System

> **面向售前 + 解决方案 + 项目管理的全生命周期运营系统**
>
> 适用角色：售前技术工程师（解决方案）+ 项目经理（交付运营）+ 业务经理（前端经营）
>
> 本系统覆盖从售前对接 → 投标 → 方案迭代 → 立项 → 合同 → 执行 → 验收 → 回款 → 收尾的全流程，以 AI Agent 为执行引擎、Obsidian Vault 为数据中枢。

---

## 系统定位

| 原有定位（v1-v2） | 新定位（v3+）|
|---|---|
| LLM Wiki + 间隔重复 | 项目全生命周期管理 |
| 个人知识积累 | 售前→投标→合同→执行→回款 |
| /read /insights /note /review | /prospect /bid /presales /initiate /plan /contract /meeting /work-item /change /acceptance /payment /monitor /close |

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
│  /prospect → /bid → /presales → /initiate → /plan → /contract  │
│  /meeting → /change → /acceptance → /payment → /close      │
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
├── 售前项目/                     # 投标过程留痕（/bid + /presales + /meeting）
├── 项目库/                       # 正式立项后的项目（核心）
│   └── {PJ-YYYY-NNN}/
│       ├── 00-项目章程.md
│       ├── 01-合同/
│       │   ├── 主合同关键条款.md
│       │   ├── 签订记录.md
│       │   ├── 履行义务清单.md
│       │   └── 补充协议/
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

## 十五个 Skills

### 生命周期飞轮

| Skill | 职责 | 输出 |
|-------|------|------|
| `/prospect` | 线索管理（新线索 → 跟进中 → 升级/关闭） | 线索卡片 + 线索看板 + raw素材 |
| `/bid` | 投标管理（建档 + 技术方案 + 商务报价 + 结果）| 售前项目骨架 |
| `/presales` | 售前工作台（需求分析 + 方案迭代 + 材料管理 + 技术交流 + 需求冻结）| 售前文档 + 技术交流记录 |
| `/initiate` | 项目立项（唯一创建项目结构的通道） | 项目文件夹 + 章程 |
| `/plan` | 计划制定 | WBS + 里程碑 |
| `/contract` | 合同管理（审查 + 签订 + 补充协议 + 履约跟踪） | 履行清单 + 签订记录 + 补充协议 |
| `/meeting` | 会议纪要（执行阶段会议：周例会/启动会/评审会等）| 会议文档 |
| `/change` | 变更管理 | 变更记录 |
| `/acceptance` | 验收管理（阶段验收 + 终验 + 不符合项跟踪）| 验收报告 |
| `/payment` | 回款跟踪 | 回款汇总 + 催款跟踪 |
| `/close` | 项目收尾 | 决算 + 复盘 |

### 横向工具

| Skill | 职责 | 输出 |
|-------|------|------|
| `/work-item` | 专项工作管理（创建、推进、完成，在看板同步） | 专项工作文档 + 看板 TMP 行 |

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
/prospect 跟进线索，收集 raw 素材，判断机会质量
    ↓   （用户拍板：这个线索值得投入 → 升级）
/bid action=new（创建售前项目骨架）
    ↓
↓ 售前阶段（循环迭代）↓
/presales 更新「客户需求分析」（首次需求对接）
/presales 更新「解决方案」（方案成形）
/presales action=material（材料版本管理）
/presales action=tech-exchange 记录技术交流（售前阶段）
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
/contract action=review 审查合同条款，生成履行清单
    ↓
/contract action=sign 记录合同签订
    ↓
/plan 制定 WBS 和里程碑
    ↓
/meeting 记录启动会
    ↓
↓ 执行阶段（循环）↓
/meeting 记录周例会/评审会
  ├─ 会议决议 → /work-item action=new source=meeting（创建专项工作）
/monitor 定期健康检查 + action=track 每日站会
  ├─ 站会发现 → /work-item action=new source=standup（创建专项工作）
/work-item action=update 推进工作（步骤完成、备注补充）
/change 处理变更需求
/contract action=track 履约跟踪
/payment 跟踪回款节点
    ↓
/work-item action=close 专项工作完成归档
    ↓
↓ 验收阶段 ↓
/acceptance action=stage 里程碑达到，启动阶段验收
    ↓（不符合项整改后重新验收）↓
/acceptance action=final 全部里程碑完成，启动终验
    ↓
/close 项目收尾
```

---

## 安装

### 1. 克隆

```bash
git clone https://github.com/canxer314/knowledge-mgmt.git
cd knowledge-mgmt
```

### 2. 安装 Skills 到 Agent Runtime

**Claude Code**

```bash
mkdir -p "$HOME/.claude/skills"
cp -r prospect bid presales initiate plan contract meeting change acceptance work-item monitor payment query lint "$HOME/.claude/skills/"
```

**Codex**

```bash
mkdir -p "$HOME/.agents/skills"
cp -r prospect bid initiate plan contract meeting change acceptance work-item monitor query lint "$HOME/.agents/skills/"
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
| `/contract` action=review | 自动链接 `[[00-项目章程]]` + `[[主合同关键条款]]` |
| `/contract` action=sign | 自动链接 `[[主合同关键条款]]` + `[[履行义务清单]]` |
| `/plan` 创建里程碑 | 自动在里程碑中链接 `[[00-项目章程]]` |
| `/meeting` 创建纪要 | 自动链接 `[[00-项目章程]]` |
| `/change` 创建变更 | 自动链接 `[[预算执行表]]` 和受影响里程碑 |
| `/work-item` action=new | 自动链接 `[[03-执行/交付看板]]`（在看板同步 TMP 行） |
| `/work-item` source=meeting | 自动链接 `[[会议纪要-{date}]]`（来源会议） |
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
