# RandomAgent

**模拟人类直觉跳跃思维的智能体框架 - 提示词工程**

核心理念：**世界的底层是随机的，大脑的底层也是随机的**

## 🎯 项目定位

RandomAgent 是一个**提示词工程框架**，提供：

1. **提示词模板** - 生成可直接使用的系统提示词
2. **AI 集成** - 调用真实的 AI 模型（OpenAI/Claude/Ollama）
3. **思维模拟** - 模拟人类意识流和随机思维过程

## 📦 安装

```bash
# 从源码安装
git clone https://github.com/yourusername/random-agent.git
cd random-agent
pip install -e .

# 安装 AI 支持（可选）
pip install -e ".[openai]"      # OpenAI 支持
pip install -e ".[anthropic]"   # Claude 支持
pip install -e ".[all]"         # 所有支持
```

## 🚀 快速开始

### 1. 生成提示词

```python
from random_agent import create_prompt

# 生成完整提示词（可直接复制给 AI 使用）
prompt = create_prompt(
    task="什么是创造力？",
    randomness=0.7,      # 随机性水平 0-1
    mode="creative"      # 思维模式
)

print(prompt)
```

### 2. 获取系统提示词

```python
from random_agent import get_system_prompt_only

# 获取系统提示词（用于设置 AI 的 system message）
system_prompt = get_system_prompt_only(
    randomness=0.5,
    mode="balanced"
)

# 然后在你的 AI 调用中使用
# messages = [
#     {"role": "system", "content": system_prompt},
#     {"role": "user", "content": "你的问题"}
# ]
```

### 3. 集成 AI API

#### OpenAI

```python
from random_agent import create_ai_agent

agent = create_ai_agent(
    provider="openai",
    model="gpt-4",
    api_key="your-openai-api-key",  # 或设置环境变量 OPENAI_API_KEY
    randomness=0.7,
    thinking_mode="creative"
)

result = agent.think("什么是创造力？")
print(result["answer"])
```

#### Claude

```python
from random_agent import create_ai_agent

agent = create_ai_agent(
    provider="anthropic",
    model="claude-3-opus-20240229",
    api_key="your-anthropic-api-key",  # 或设置环境变量 ANTHROPIC_API_KEY
    randomness=0.6
)

result = agent.think("什么是意识？")
print(result["answer"])
```

#### Ollama（本地模型）

```python
from random_agent import create_ai_agent

agent = create_ai_agent(
    provider="ollama",
    model="llama2",
    randomness=0.5
)

result = agent.think("什么是人工智能？")
print(result["answer"])
```

## 🎨 思维模式

| 模式 | 说明 | 适用场景 |
|------|------|----------|
| `divergent` | 发散思维 | 头脑风暴、创意探索 |
| `convergent` | 收敛思维 | 总结归纳、决策分析 |
| `balanced` | 平衡思维 | 一般问题（默认） |
| `creative` | 创造性思维 | 艺术创作、创新设计 |
| `analytical` | 分析性思维 | 逻辑推理、数据分析 |

## 🔧 高级用法

### 自定义配置

```python
from random_agent import RandomAgentPromptBuilder, PromptConfig, ThinkingMode

config = PromptConfig(
    randomness_level=0.8,
    thinking_mode=ThinkingMode.CREATIVE,
    enable_consciousness_layers=True,  # 启用意识层次
    enable_dmn=True,                   # 启用默认模式网络
    enable_emotions=True,              # 启用情绪系统
    language="zh"
)

builder = RandomAgentPromptBuilder(config)
prompt = builder.get_full_prompt("你的问题")
```

### 自定义 AI 提供商

```python
from random_agent import AIAgent, AIConfig, AIProvider

def my_custom_call(system_prompt: str, user_message: str) -> str:
    # 实现你自己的 AI 调用逻辑
    return "你的 AI 回答"

config = AIConfig(provider=AIProvider.CUSTOM)
agent = AIAgent(config)
agent.provider.set_call_function(my_custom_call)

result = agent.think("你好")
```

### 多轮对话

```python
agent = create_ai_agent(provider="openai", api_key="your-key")

# 第一轮
response1 = agent.chat("什么是量子计算？")

# 第二轮（保持上下文）
response2 = agent.chat("能详细解释一下吗？")

# 清除历史
agent.clear_history()
```

## 📚 核心概念

### 有边界的随机

- **边界**：需要完成的目标或回答的问题
- **过程**：达到目标的路径是随机的、跳跃的

就像人类思考一样：
- 会突然想到看似无关的事物
- 会把两个不相关的概念连接起来
- 会在思考过程中"走神"
- 最终会回到目标上来

### 意识层次系统

1. **显意识** - 当前主动思考的内容
2. **前意识** - 稍加注意就能意识到的内容
3. **潜意识** - 自动化的思维模式
4. **无意识** - 深层的驱动力和模式

### 默认模式网络 (DMN)

模拟大脑的"走神"模式：
- 自我叙事
- 记忆整合
- 未来预演
- 随机联想

## 📁 项目结构

```
random_agent/
├── core/                    # 核心模块
│   ├── randomness_engine.py # 随机底层引擎
│   ├── consciousness_layers.py # 意识层次
│   ├── consciousness_stream.py # 意识流
│   ├── dmn_engine.py        # DMN 引擎
│   ├── memory_system.py     # 记忆系统
│   ├── goal_system.py       # 目标系统
│   ├── influence_factors.py # 影响因素
│   ├── balance_controller.py # 平衡控制器
│   └── output_system.py     # 输出系统
├── prompt_templates.py      # 提示词模板
├── ai_integration.py        # AI API 集成
└── agent.py                 # 主 Agent 类

examples/
├── developer_guide.py       # 开发者指南
└── example_usage.py         # 使用示例
```

## 🤝 使用场景

1. **提示词工程师** - 生成创新的系统提示词
2. **AI 应用开发者** - 集成到现有项目中
3. **研究者** - 研究随机性在 AI 思维中的作用
4. **创意工作者** - 获得不同寻常的 AI 回答

## 📄 License

MIT License

## 🙏 致谢

本项目基于以下理论和研究：
- 量子力学的不确定性原理
- 神经科学的神经噪声研究
- 认知心理学的双系统理论
- 意识流理论（William James）
- 默认模式网络研究
