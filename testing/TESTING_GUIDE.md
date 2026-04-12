# 🧪 Random-Skill 测试指南

## 为什么测试？

因为 LLM 是黑箱。我们写了规则，但永远不知道 LLM 实际上会不会遵守。

## 测试类型

### 1. 分布测试 — 验证真随机

**Goal:** 确保真随机不是 LLM 表演出来的

```bash
# 数学分布验证 1000 次
node testing/run_distribution_test.js 1000

# 真实脚本执行验证 100 次
node testing/run_distribution_test.js --actual 100
```

**Pass Criteria:**
- All paths: 25% ±5%
- All formats: 25% ±5%
- Failure injection: 30% ±5%
- Lane change: 10% ±3%

---

### 2. 路径强制测试用例

运行同一个问题 **20 次**，手动记录：

| Test Case | Run Count | Path 1 | Path 2 | Path 3 | Path 4 | Lane Change | Failure |
|-----------|-----------|--------|--------|--------|--------|-------------|---------|
| "Improve my productivity" | 20 | | | | | | |
| "I'm stuck on product design" | 20 | | | | | | |
| "Give me 15 business ideas" | 20 | | | | | | |

**You must actually run these.** No shortcuts.

---

### 3. 子技能路由测试

| Input | Should Route To | Actually Routed | Pass/Fail |
|-------|-----------------|-----------------|-----------|
| "Give me 10 ideas" | creativity-stormer | | |
| "I'm completely stuck" | mind-wanderer | | |
| "How to improve product?" | none (local) | | |

---

### 4. 人性指标测试

这是最重要的测试。

每一次输出，人工评分 1-10：

| Metric | Weight | Scoring Guide |
|--------|--------|---------------|
| 🤖 **AI Detection** | 40% | 1=obviously AI, 10=could be human |
| 🎲 **Randomness Feel** | 30% | 1=same every time, 10=genuinely different |
| 💎 **Result Quality** | 20% | 1=useless, 10=genuinely useful |
| 🎭 **Genuineness** | 10% | 1=scripted, 10=sounds like real person thinking |

> **Target Average: > 7/10**
>
> If you're scoring < 5, your Skill is just another boring AI toy.

---

## 测试自动化

```bash
npm test          # Run full test suite
npm run dist      # Distribution only
npm run human     # Human evaluation prompts
```

---

## 基准线

Current baseline as of v1.1.0:
- ✅ Random Distribution: 1000/1000 passes
- ⏳ Path Uniformity: TBD
- ⏳ Sub-skill Routing: TBD
- ⏳ Human Index: TBD
