"""
RandomAgent 提示词工程框架 - 开发者使用示例

本示例展示如何：
1. 使用提示词模板
2. 集成 AI API
3. 自定义配置
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from random_agent.prompt_templates import (
    create_prompt,
    get_system_prompt_only,
    RandomAgentPromptBuilder,
    PromptConfig,
    ThinkingMode,
)

from random_agent.ai_integration import (
    create_ai_agent,
    AIAgent,
    AIConfig,
    AIProvider,
)


def example_1_basic_prompt():
    """示例1: 基本提示词生成"""
    print("=" * 60)
    print("示例1: 基本提示词生成")
    print("=" * 60)
    
    prompt = create_prompt(
        task="什么是创造力？",
        randomness=0.7,
        mode="creative"
    )
    
    print("\n生成的提示词（前500字符）:")
    print(prompt[:500] + "...\n")
    
    print("提示词总长度:", len(prompt), "字符")


def example_2_system_prompt():
    """示例2: 仅获取系统提示词"""
    print("\n" + "=" * 60)
    print("示例2: 获取系统提示词（用于设置 AI 系统消息）")
    print("=" * 60)
    
    system_prompt = get_system_prompt_only(
        randomness=0.5,
        mode="balanced"
    )
    
    print("\n系统提示词:")
    print(system_prompt[:800] + "...\n")


def example_3_custom_config():
    """示例3: 自定义配置"""
    print("\n" + "=" * 60)
    print("示例3: 自定义配置构建提示词")
    print("=" * 60)
    
    config = PromptConfig(
        randomness_level=0.8,
        thinking_mode=ThinkingMode.CREATIVE,
        enable_consciousness_layers=True,
        enable_dmn=True,
        enable_emotions=True,
        language="zh"
    )
    
    builder = RandomAgentPromptBuilder(config)
    
    task = "如何设计一个创新的用户体验？"
    full_prompt = builder.get_full_prompt(task)
    
    print(f"\n任务: {task}")
    print(f"随机性: {config.randomness_level:.0%}")
    print(f"思维模式: {config.thinking_mode.value}")
    print(f"\n提示词长度: {len(full_prompt)} 字符")


def example_4_compact_prompt():
    """示例4: 精简版提示词（节省 token）"""
    print("\n" + "=" * 60)
    print("示例4: 精简版提示词（适合 token 限制场景）")
    print("=" * 60)
    
    prompt = create_prompt(
        task="解释量子计算",
        randomness=0.5,
        mode="analytical",
        style="concise"
    )
    
    print("\n精简版提示词:")
    print(prompt)
    print(f"\n长度: {len(prompt)} 字符")


def example_5_ai_integration_openai():
    """示例5: 集成 OpenAI API"""
    print("\n" + "=" * 60)
    print("示例5: 集成 OpenAI API")
    print("=" * 60)
    
    print("\n使用方法:")
    print("""
from random_agent import create_ai_agent

# 创建 AI Agent
agent = create_ai_agent(
    provider="openai",
    model="gpt-4",
    api_key="your-openai-api-key",
    randomness=0.7,
    thinking_mode="creative"
)

# 思考问题
result = agent.think("什么是创造力？")
print(result["answer"])

# 多轮对话
response = agent.chat("能详细解释一下吗？")
print(response)
""")
    
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        print("\n检测到 OPENAI_API_KEY，正在调用...")
        try:
            agent = create_ai_agent(
                provider="openai",
                model="gpt-4",
                randomness=0.7,
                thinking_mode="creative"
            )
            result = agent.think("用一句话解释什么是创造力")
            print("\nAI 回答:", result["answer"])
        except Exception as e:
            print(f"\n调用失败: {e}")
    else:
        print("\n未检测到 OPENAI_API_KEY 环境变量")


def example_6_ai_integration_claude():
    """示例6: 集成 Claude API"""
    print("\n" + "=" * 60)
    print("示例6: 集成 Claude API")
    print("=" * 60)
    
    print("\n使用方法:")
    print("""
from random_agent import create_ai_agent

agent = create_ai_agent(
    provider="anthropic",
    model="claude-3-opus-20240229",
    api_key="your-anthropic-api-key",
    randomness=0.6
)

result = agent.think("什么是意识？")
print(result["answer"])
""")


def example_7_ai_integration_ollama():
    """示例7: 集成 Ollama 本地模型"""
    print("\n" + "=" * 60)
    print("示例7: 集成 Ollama 本地模型")
    print("=" * 60)
    
    print("\n使用方法:")
    print("""
from random_agent import create_ai_agent

# 使用本地 Ollama
agent = create_ai_agent(
    provider="ollama",
    model="llama2",
    randomness=0.5
)

result = agent.think("什么是人工智能？")
print(result["answer"])
""")


def example_8_custom_provider():
    """示例8: 自定义 AI 提供商"""
    print("\n" + "=" * 60)
    print("示例8: 自定义 AI 提供商")
    print("=" * 60)
    
    print("\n使用方法:")
    print("""
from random_agent import AIAgent, AIConfig, AIProvider

def my_custom_call(system_prompt: str, user_message: str) -> str:
    # 这里实现你自己的 AI 调用逻辑
    # 可以是任何 API 或本地模型
    return "你的 AI 回答"

config = AIConfig(
    provider=AIProvider.CUSTOM,
    randomness_level=0.5
)

agent = AIAgent(config)
# 设置自定义调用函数
agent.provider.set_call_function(my_custom_call)

result = agent.think("你好")
""")


def example_9_prompt_for_different_modes():
    """示例9: 不同思维模式的提示词"""
    print("\n" + "=" * 60)
    print("示例9: 不同思维模式的提示词对比")
    print("=" * 60)
    
    task = "如何解决交通拥堵问题？"
    modes = ["divergent", "convergent", "creative", "analytical"]
    
    for mode in modes:
        prompt = create_prompt(
            task=task,
            randomness=0.5,
            mode=mode,
            style="concise"
        )
        print(f"\n【{mode} 模式】")
        print(prompt[:300] + "...")


def example_10_get_prompt_only():
    """示例10: 仅获取提示词（不调用 AI）"""
    print("\n" + "=" * 60)
    print("示例10: 仅获取提示词（复制粘贴给其他 AI 使用）")
    print("=" * 60)
    
    agent = create_ai_agent(
        provider="openai",
        model="gpt-4",
        randomness=0.7,
        thinking_mode="creative"
    )
    
    question = "什么是真正的创新？"
    prompt = agent.get_prompt_only(question)
    
    print(f"\n问题: {question}")
    print("\n完整提示词（可直接复制给 ChatGPT/Claude 使用）:")
    print("-" * 40)
    print(prompt)
    print("-" * 40)
    
    print("\n系统提示词（可设置为 AI 的 system message）:")
    print("-" * 40)
    print(agent.get_system_prompt()[:500] + "...")
    print("-" * 40)


def main():
    """运行所有示例"""
    print("\n" + "=" * 60)
    print("RandomAgent 提示词工程框架 - 开发者示例")
    print("=" * 60)
    
    example_1_basic_prompt()
    example_2_system_prompt()
    example_3_custom_config()
    example_4_compact_prompt()
    example_5_ai_integration_openai()
    example_6_ai_integration_claude()
    example_7_ai_integration_ollama()
    example_8_custom_provider()
    example_9_prompt_for_different_modes()
    example_10_get_prompt_only()
    
    print("\n" + "=" * 60)
    print("示例演示完成！")
    print("=" * 60)
    
    print("\n📚 快速开始:")
    print("""
# 1. 生成提示词
from random_agent import create_prompt
prompt = create_prompt("你的问题", randomness=0.7, mode="creative")

# 2. 调用 AI
from random_agent import create_ai_agent
agent = create_ai_agent(provider="openai", api_key="your-key")
result = agent.think("你的问题")
""")


if __name__ == "__main__":
    main()
