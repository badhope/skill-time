# RandomAgent

**模拟人类直觉跳跃思维的智能体框架 - 提示词工程**

核心理念：**世界的底层是随机的，大脑的底层也是随机的**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-0.3.0-green.svg)](https://github.com/yourusername/random-agent)

## ✨ v0.3.0 新特性

- 🎉 **CLI 命令行工具** - 无需编程，一行命令即可使用
- 📋 **16 个预设模板** - 覆盖内容创作、问题解决、学习研究等场景
- 🚀 **一键启动脚本** - 双击即用，自动配置
- 🤖 **智能推荐** - 根据任务自动匹配最佳模板
- 🌍 **全中文界面** - 友好的用户体验

## 🎯 项目定位

RandomAgent 是一个**提示词工程框架**，提供：

1. **提示词模板** - 生成可直接使用的系统提示词
2. **AI 集成** - 调用真实的 AI 模型（OpenAI/Claude/Ollama）
3. **思维模拟** - 模拟人类意识流和随机思维过程
4. **CLI 工具** - 命令行界面，无需编程即可使用
5. **预设模板** - 开箱即用的场景配置

## 📦 安装

### 方式一：一键启动（推荐新手）

**Windows 用户：**
```bash
# 双击 start.bat 即可启动
# 或在命令行运行：
start.bat
```

**Linux/Mac 用户：**
```bash
chmod +x start.sh
./start.sh
```

### 方式二：命令行安装

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

### 方式三：直接使用 CLI（安装后）

```bash
# 查看帮助
random-agent --help

# 首次使用：配置向导
random-agent setup

# 效果演示
random-agent demo
```

## 🚀 快速开始

### 方式一：CLI 命令行（推荐，无需编程）

```bash
# 1. 生成提示词（使用预设模板）
random-agent generate "写一首关于春天的诗" --template creative_writing

# 2. 头脑风暴
random-agent generate "如何提高团队效率？" --template brainstorming

# 3. 与 AI 对话（需要 Ollama 或 API Key）
random-agent chat --provider ollama --model llama2

# 4. 交互式模式（推荐新手）
random-agent interactive

# 5. 查看所有可用模板
random-agent templates
```

### 方式二：Python 编程调用

#### 1. 生成提示词

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

## 📋 预设模板（v0.3.0 新增）

RandomAgent 提供 **16 个开箱即用** 的预设模板，覆盖 5 大类别：

### 📝 内容创作（4个）

| 模板名称 | 说明 | 示例命令 |
|----------|------|----------|
| `creative_writing` | 创意写作（小说、诗歌） | `random-agent generate "写一首诗" --template creative_writing` |
| `copywriting` | 营销文案（广告、推广） | `random-agent generate "产品描述" --template copywriting` |
| `blog_post` | 博客文章（技术、个人） | `random-agent generate "AI教程" --template blog_post` |
| `social_media` | 社交媒体（微博、小红书） | `random-agent generate "推文" --template social_media` |

### 💡 问题解决（3个）

| 模板名称 | 说明 | 适用场景 |
|----------|------|----------|
| `brainstorming` | 头脑风暴 | 创意生成、方案探索 |
| `problem_solving` | 问题分析 | 系统性分析复杂问题 |
| `decision_making` | 决策辅助 | 权衡利弊、做出选择 |

### 📚 学习研究（3个）

| 模板名称 | 说明 | 适用场景 |
|----------|------|----------|
| `learning_explanation` | 概念解释 | 教学式说明复杂概念 |
| `research_assistant` | 研究助手 | 学术研究、文献综述 |
| `idea_development` | 想法深化 | 完善初步想法为完整方案 |

### 🌟 日常生活（3个）

| 模板名称 | 说明 | 适用场景 |
|----------|------|----------|
| `daily_chat` | 日常聊天 | 有趣的对话交流 |
| `life_advice` | 生活建议 | 人生指导和建议 |
| `creative_inspiration` | 创意灵感 | 灵感激发和联想 |

### 💼 专业领域（3个）

| 模板名称 | 说明 | 适用场景 |
|----------|------|----------|
| `business_strategy` | 商业策略 | 战略规划和市场分析 |
| `code_review` | 代码审查 | 编程辅助和代码优化 |
| `interview_prep` | 面试准备 | 求职面试准备 |

**查看所有模板：**
```bash
random-agent templates
```

**智能推荐（自动匹配最佳模板）：**
```python
from random_agent import get_template_for_task

# 根据任务描述自动推荐
recommended = get_template_for_task("帮我写一首关于春天的诗")
# 返回: creative_writing 模板
```

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
├── templates.py             # 预设场景模板 (v0.3.0)
├── cli.py                   # 命令行工具 (v0.3.0)
├── ai_integration.py        # AI API 集成
├── config.py                # 配置管理
├── logger.py                # 日志系统
├── exceptions.py            # 异常处理
├── monitoring.py            # 性能监控
├── async_support.py         # 异步支持
├── extended_providers.py    # 扩展 AI 提供商
└── agent.py                 # 主 Agent 类

# 启动脚本
start.bat                    # Windows 一键启动
start.sh                     # Linux/Mac 一键启动

examples/
├── developer_guide.py       # 开发者指南
├── example_usage.py         # 使用示例
├── ai_integration_demo.py   # AI 集成演示
└── core_principle_demo.py   # 核心原理演示

tests/
└── test_*.py               # 测试文件
```

## 🤝 使用场景

### 适合谁用？

| 用户类型 | 使用方式 | 推荐功能 |
|----------|----------|----------|
| 👩‍💻 **内容创作者** | 写文案、创作内容 | `--template copywriting` / `creative_writing` |
| 🎓 **学生** | 学习概念、写论文 | `--template learning_explanation` |
| 💼 **职场人士** | 头脑风暴、做决策 | `--template brainstorming` / `decision_making` |
| 🔧 **开发者** | 代码审查、技术方案 | `--template code_review` / Python API |
| 👨‍🏫 **教师** | 教学备课、解释概念 | `--template learning_explanation` |
| 📱 **社交媒体运营** | 写推文、发小红书 | `--template social_media` |

### 典型应用

1. **提示词工程师** - 生成创新的系统提示词
2. **AI 应用开发者** - 集成到现有项目中
3. **研究者** - 研究随机性在 AI 思维中的作用
4. **创意工作者** - 获得不同寻常的 AI 回答
5. **普通用户** - 通过 CLI 快速获得 AI 帮助（v0.3.0 新增）

## 📊 版本历史

### v0.3.0 (2026-04-03) - 用户体验全面优化
- ✅ 新增 CLI 命令行工具
- ✅ 新增 16 个预设场景模板
- ✅ 新增一键启动脚本 (start.bat / start.sh)
- ✅ 新增智能模板推荐系统
- ✅ 全中文界面和错误提示

### v0.2.0 - 功能扩展
- ✅ 异步支持系统
- ✅ 性能监控模块
- ✅ 扩展 AI 提供商（Google、Cohere、Azure 等）
- ✅ CI/CD 流水线配置

### v0.1.1 - 基础版本
- ✅ 核心随机引擎
- ✅ 意识层次系统
- ✅ DMN 引擎
- ✅ OpenAI/Claude/Ollama 集成

## ✅ 测试验证 (v0.3.0)

RandomAgent v0.3.0 已通过 **33 项全面测试**，通过率 **100%**：

### 测试覆盖范围

| 测试类别 | 测试项数 | 状态 |
|----------|----------|------|
| 核心模块导入 | 11 项 | ✅ 全部通过 |
| 提示词生成功能 | 5 项 | ✅ 全部通过 |
| 预设模板系统 | 5 项 | ✅ 全部通过 |
| CLI 工具测试 | 2 项 | ✅ 全部通过 |
| 配置和安装测试 | 3 项 | ✅ 全部通过 |
| 边界情况处理 | 5 项 | ✅ 全部通过 |
| 集成测试 | 2 项 | ✅ 全部通过 |

### 关键测试项目

- ✅ 16 个预设模板全部可正常访问和使用
- ✅ 5 种思维模式（divergent/convergent/balanced/creative/analytical）
- ✅ 智能推荐系统准确匹配任务到模板
- ✅ 特殊字符、超长任务等边界情况处理正确
- ✅ CLI 参数解析完整，6 个命令全部可用
- ✅ Python 3.8-3.12 兼容性确认

运行测试：
```bash
python full_test.py
```

## 📄 License

MIT License

## 🙏 致谢

本项目基于以下理论和研究：
- 量子力学的不确定性原理
- 神经科学的神经噪声研究
- 认知心理学的双系统理论
- 意识流理论（William James）
- 默认模式网络研究
