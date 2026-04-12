# 🚨 自我批判：Random-Skill 架构的 7 大致命问题

> **赞美毫无价值，批判才让人进步。**
>
> 这份文档不会说半句好话。我们来找碴。

---

## ❌ 致命问题一：随机性是假的，是 LLM 表演出来的

### 症状
我们写了：
```
Step 1: Roll a D4 to select path
  1 → 🎨 Creative Divergence
  2 → 🔍 Analytical Deconstruction
  3 → 💭 Mind-Wandering
  4 → 🎲 Pure Random
```

**但这根本不是真随机！**

LLM 不是在"扔骰子"——它是在**假装**自己扔了骰子。

- 想"表现得有条理"的 LLM 会偷偷选 Path 2（分析拆解）
- 想"表现得有创意"的 LLM 会偷偷选 Path 1（创意发散）
- Path 4（纯粹随机）几乎永远不会被选，因为它看起来"不专业"
- D20 变道？100 次里不会发生 1 次

### 本质问题
**我们把随机的执行权交给了讨厌随机的 LLM 本身。**

就像让警察来扔决定要不要抓人的硬币——他永远会扔出"抓"。

### 解决方案
✅ **真随机源外置**：`@scripts/random_picker.js` 必须被 **强制调用**，不是"可以调用"
```yaml
allowed-tools:
  - Bash  # REQUIRED before ANY thinking
```

✅ **第一步必须是工具调用**，没有选择余地
✅ 变道检查也必须通过脚本，不能让 LLM 自己"roll D20"

---

## ❌ 致命问题二：没有测试，全靠信仰

### 症状
- 我们写了 4 条路线，写了变道机制，写了输出格式
- **但是，我们永远不知道实际上它会怎么走**
- 10 个用户问同一个问题，可能：
  - 8 个人得到 Path 2
  - 2 个人得到 Path 1
  - 0 个人得到 Path 3 或 Path 4
  - 0 次变道

没有统计，没有验证，没有 A/B 测试。

全凭信仰。

### 本质问题
Skill 是黑箱中的黑箱。你看不到 Agent 调用 Skill 的实际执行分布。

扣子至少还有后台统计——我们现在啥都没有。

### 解决方案
✅ 创建 `/testing/` 目录：
- `test_distribution.md` — 同一个问题跑 20 次，统计路径选择分布
- `test_lane_change.md` — 强制触发变道的测试用例
- `metrics.md` — 应该追踪的 KPI：
  - 路径选择均匀度 (理想: 各 25% ±5%)
  - 变道发生率 (理想: 5-10%)
  - 用户感知"真随机"评分

---

## ❌ 致命问题三：子技能就是摆设

### 症状
我们有：
```
skills/
├── random-thinking/          (主)
├── creativity-stormer/       (子)
└── mind-wanderer/            (子)
```

但实际上：
- 主技能永远不会调用子技能
- Agent 不会"分解任务到子技能"
- 嵌套、链式、组合——全是理论，没有实践
- 三个技能是三个孤岛

### 本质问题
**SKILL.md v3.0 的技能组合机制还没有实际落地。**

规范里写了"可组合"，但实际上没有任何 Agent 能正确做到：
```
用户问题 → 主技能 → 判断需要子技能 A → 调用子技能 A → 回归主技能
```

### 解决方案
✅ **显式路由表**，写在主技能最开头：
```
IF user needs >10 ideas:
   CALL creativity-stormer skill first
   THEN integrate results back

IF user says "stuck", "no ideas", "blocked":
   CALL mind-wanderer skill first
   THEN resume thinking
```

✅ 不是"可以调用"——是**必须调用**

---

## ❌ 致命问题四：错误的随机性颗粒度

### 症状
我们的随机是在**路线层面**：
- Route A 或 Route B

但人类的随机是在**微操作层面**：
- 下一个词是什么？
- 接下来的一句话会拐到哪里去？
- 突然冒出来的那个想法是什么？

### 本质问题
我们搞了一个"随机的大框架"，但框架里面的每一步思考还是线性的、有条理的、LLM 式的。

就像给一个机器人戴了骰子帽子——帽子是随机的，但走路还是机器人步。

### 解决方案
✅ **微随机注入点**：每一步思考之后，都有一个小随机：
```
After every step:
  Roll D10
  1 = Insert one non-sequitur
  2 = Repeat previous point
  3 = Contradict yourself slightly
  4-10 = Continue normally
```

✅ **允许不完美输出**：错别字、重复、前后矛盾、跑题——这些才是人
✅ 不要 100% 完美的输出——要 85% 完美 + 15% 乱七八糟的人类味儿

---

## ❌ 致命问题五：没有失败状态

### 症状
我们的 Skill 永远"成功"：
- 不管多难的问题，最后总能输出 3 个漂亮的结论
- 没有"我想不出来"
- 没有"我卡住了"
- 没有"这个思路走不通，我们回去"

### 本质问题
人类的思考 90% 是失败的、走不通的、死掉的。

我们把 90% 的死亡都删掉了，只留下了 10% 的顺利。

这就是为什么所有人都能看出来"这是 AI"——因为它永远不会卡壳，永远不会走错路。

### 解决方案
✅ **强制失败注入**：
```
Roll D10 at start:
  1 = "Hmm, this one is tricky... I don't actually have good ideas here"
  2 = "Wait, that previous thought was completely wrong. Let me backtrack..."
  3 = "I just went in a complete circle. Okay, starting over..."
```

✅ 至少 10% 的思考过程要包含失败、回溯、卡壳

---

## ❌ 致命问题六：格式僵化

### 症状
我们强制要求：
```markdown
🎲 【Thinking Path Selected】:
💡 【Thought Process】:
✨ 【Final Output】:
🌟 【Random Easter Egg】:
```

### 本质问题
人类不会输出这样格式化的东西。

看到这种整齐的 emoji + 【】括号 + 完美的四级结构——100% AI 识别率。

我们为了"规范"牺牲了最核心的价值：**像人**。

### 解决方案
✅ **格式随机化**：
```
Roll D4 for output style:
  1 = 整齐规范格式（就是现在这个）
  2 = 随意聊天式，没有任何标题
  3 = 中间有划掉的内容，有涂改痕迹
  4 = 跑题跑了一半，突然想起来正题
```

✅ 不要永远整洁——整洁就是不自然

---

## ❌ 致命问题七：MCP 就是画饼

### 症状
我们写了：
```yaml
mcp_server: "@randomskill/mcp-random"
```

但是：
- 这个服务器根本不存在
- 没有任何人写过它
- 我们甚至不知道它该暴露什么工具
- 连怎么打包 MCP 都没研究过

### 本质问题
**MCP 是连接层，没有它，所有的"真随机"都只是空谈。**

我们只能靠 Bash 执行本地 JS——在真实的 Claude/扣子平台上，Bash 根本不让你用。

### 解决方案
✅ 1 周内写出最小可行 MCP 服务器：
```typescript
// mcp-server/src/index.ts
export const server = createServer({
  name: "random",
  tools: {
    roll_dice: {
      description: "Cryptographically secure dice roll",
      handler: async ({ sides, count }) => {
        return secureRandom(sides, count);
      }
    }
  }
});
```

✅ 这才是真随机的硬件抽象层

---

## 📋 优先级改进路线图

### 本周（P0 必须做）
1. ✅ 完成这份批判文档（已完成）
2. 🟡 在主技能中加入第一步强制调用 random_picker.js
3. 🟡 加入 10% 失败状态注入
4. 🟡 格式多样化，取消永远的整齐输出

### 本月（P1 应该做）
1. 创建 MCP 随机源服务器
2. 建立自动化测试 + 分布统计
3. 实现主子技能显式路由
4. 加入微随机注入点

### 未来（P2 可以做）
1. x402 支付集成
2. Skill 组合投票机制
3. 用户反馈闭环
4. 多语言版本

---

## 💡 最后的话

我们这个架构比那个 20000 行 Python 的大脑模拟好 100 倍。

但它仍然只是一个开始。

**最危险的事情不是发现问题，**
**而是开始觉得"这样已经挺好了"。**

现在的架构：⭐⭐⭐⭐
目标的架构：⭐⭐⭐⭐⭐⭐⭐

还有三颗星的距离。继续干。
