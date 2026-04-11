---
name: query
description: 搜索 Obsidian vault 中的已有知识来回答问题。CC 主动读取 MOC 索引和相关 Cards，综合 vault 知识 + 模型知识回答，标注来源。当用户说"query"、"查一下 vault"、"vault 里有什么"、"从笔记里找"时触发。
invocation: user
arguments:
  - name: question
    description: 要查询的问题或主题
    required: true
---

# /query — 带 Vault 上下文的知识查询

> 让 CC 不只靠模型记忆回答，而是主动搜索 vault 中的已有知识。

## 执行流程

### Step 1: 解析查询意图

从用户问题中提取：
- 关键概念（用于搜索）
- 涉及的 domain（用于定位 MOC）
- 查询类型：事实查找 / 综合分析 / 对比 / 探索

### Step 2: 搜索 Vault

```bash
# 1. 读取相关 MOC 索引
obsidian read path="Cards/MOC-{Domain}.md"

# 2. 搜索关键词
obsidian search query="{关键概念1}"
obsidian search query="{关键概念2}"

# 3. 带上下文搜索（更精确）
obsidian search:context query="{关键短语}"
```

### Step 3: 读取命中的 Cards

```bash
# 批量读取搜索结果
for card in {搜索结果}; do
  obsidian read path="$card"
done
```

优先读取：
1. 研究摘要（type/research, type/reading）— 综合信息密度最高
2. 概念卡（type/concept）— 定义和关键要点
3. 洞察卡（type/insight）— 独特见解
4. 原子卡片（type/atomic）— 精炼知识点

### Step 4: 综合回答

回答原则：
- **Vault 知识优先**：vault 中有的信息，标注来源 `[[Card名]]`
- **模型知识补充**：vault 中没有的，用模型知识补充，明确标注"（模型知识，vault 中暂无）"
- **诚实告知**：如果搜索后 vault 中确实没有相关内容，说"vault 中暂无此主题的笔记"

回答格式：
```markdown
## 回答

{综合回答，穿插 [[Card名]] 引用}

---
📚 引用了 {N} 张 Cards：[[Card1]] [[Card2]] [[Card3]]
💡 模型补充：{有/无}
```

### Step 5: 回写提议（可选）

如果回答产出了有价值的综合分析：

```
这个回答包含了跨 Card 的综合分析，值得存为新的对比/综合卡片吗？
→ 说 "note" 走 /note 流程回写
→ 说 "不用" 跳过
```

不自动回写，用户觉得好才走 /note。

## 与普通提问的区别

| | 普通提问 | /query |
|---|---------|--------|
| 知识来源 | 模型记忆 | vault Cards + 模型 |
| 溯源 | 无 | 标注来自哪张 Card |
| 搜索范围 | 无 | MOC → Cards → 全文搜索 |
| 沉淀 | 留在对话里 | 可通过 /note 回写 |

## 注意事项

- 搜索结果多时，先读 MOC 索引缩小范围，不要盲目全文搜索
- 单次查询读取的 Cards 控制在 10 张以内，避免 context 溢出
- 如果问题跨多个 domain，先搜索各自 MOC 再综合
