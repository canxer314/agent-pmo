# Contributing to Knowledge MEMO

## 核心原则: Fork, Don't Consume

Knowledge MEMO 不是一个通用产品。这是作者个人（认知神经科学 / 哲学 / 投资 / 游戏设计 领域）的知识管理系统。

我们把它开源，**不是让你当产品用，是让你看到一个真实跑通的样本**，然后去长出**你自己的那一个**。

Gary Tan 的 gbrain 会考虑让 idea 怎么生长（因为他做创业），我们的系统会考虑让概念怎么交叉（因为我们做跨域思考），你的系统会考虑什么？只有你自己知道。

---

## 建议的 Fork 流程

1. **Clone 到本地**
   ```bash
   git clone https://github.com/owenliang60-ship-it/knowledge-mgmt.git
   cd knowledge-mgmt
   ```

2. **用你自己的 domain 替换作者的 domain**
   `demo/cards/` 里展示的是作者的样本。你的领域可能完全不同。删掉不相关的，保留可借鉴的结构。

3. **改写 `SCHEMA.md` § 2 的 Card 类型**
   去掉你不需要的，加上你需要的。作者有 `type/insight`（投资洞察）、`type/research`（深度研究），你的领域可能需要 `type/experiment`（实验记录）或 `type/sketch`（设计草图）。

4. **改写 `templates/cards/` 下的模板**
   符合你的 frontmatter 偏好、你的标签体系、你的写作习惯。

5. **跑一周，观察哪里不顺手，迭代 SCHEMA**
   知识管理不是 "装好就好"，是 "持续调优"。每次调整都要记录理由和日期（这本身就是 "知识管理是过程而非产品" 的证据）。

---

## 如果你想回流贡献

- **Bug fix / 文档改进**: 直接 PR 到 main
- **新 skill 或新 Card 类型**: 先开 issue 讨论，避免破坏现有叙事
- **哲学立场变更**: 不接受（这是作者的立场，不是民主投票）

---

## 不接受的 PR

这些不是 "看不上"，是和这个 repo 的灵魂冲突：

- ❌ **"auto-ingest feeds" / "scheduled scraping" 等自动化信息流**
  违背 "人必须在 loop 里" 原则。Knowledge MEMO 的第一条纪律是：你必须自己浏览、剪藏、决定今天读什么。

- ❌ **删除 `/review` 或任何 "retain" 环节**
  这是我们和 Karpathy LLM Wiki 的核心差异点。没有 Retain 的 wiki 是 "给 Agent 准备的 context"，会被下一代模型淘汰。我们做的是 "给人脑准备的脚手架"。

- ❌ **把作者的个人 demo 换成 "通用示例"**
  失去真实性。`demo/` 的价值恰恰在于它是真实个人系统 —— 有偏见、有领域、有取舍。一旦变成通用示例就平庸了。

- ❌ **给 `/note` 加 "auto-confirm" 模式**
  双提议机制是故意的摩擦。它确保每一张写入 vault 的 card 都经过人的确认。绕开它就失去了 "人在 loop" 的强制点。

---

## 我们特别欢迎的贡献

- ✅ **翻译**: README / SCHEMA / AGENTS 的英译版、日译版、其他语言版
- ✅ **测试覆盖**: `review/scripts/migrate_v1_to_v2.py` 的更多 edge case fixture
- ✅ **Skill 改进**: 提升现有 6 个 skill 的 prompt 质量、修 bug、补 error handling
- ✅ **Platform 兼容**: 让 skills 在非 Claude Code 环境能跑（OpenAI Codex、本地 LLM 等）
- ✅ **Fork 案例分享**: 你改造后的版本 —— 即使不 PR 回来，把 link 发 issue 让我们看看，会帮助其他人想象可能性

---

## 关于 "作者" 这个词

你会发现这个 repo 里有很多 "作者" 或 "the user" 这类指代。它指的是 `owenliang60-ship-it` —— 这套系统的第一个使用者。你 fork 之后，"作者" 就是你。

把 README 里的领域列表（神经科学 / 哲学 / 投资 / 游戏设计）换成你的领域，把 SCHEMA 里的 Card 类型换成你需要的，把 `demo/` 里的样本换成你真实写过的 —— 这个 repo 就变成你自己的 "个人知识管理样板 repo"。

---

## MIT License

一切内容 MIT。Fork 随便改。不用署名，不用分享回来，不用感谢。

但如果你真的做出了一个你自己用得顺手的版本，**记得给自己鼓一下掌** —— 因为那意味着你完成了这份 repo 最想传递的一件事：**别人跑通的样本可以启发你，但只有你自己能长出你自己的那一个**。
