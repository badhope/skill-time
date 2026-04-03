#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RandomAgent AI 接入完整演示

展示 RandomAgent 如何直接接入各种 AI 服务
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def demo_ai_integration_overview():
    """演示 AI 接入概览"""
    print("\n" + "=" * 70)
    print("RandomAgent AI 接入能力概览")
    print("=" * 70)
    
    print("\n【重要发现】RandomAgent 已经内置了完整的 AI 接入功能！\n")
    
    print("已支持的 AI 提供商:")
    print("-" * 60)
    
    providers = [
        ("1. OpenAI", "GPT-4, GPT-3.5-turbo", "pip install openai", "OPENAI_API_KEY"),
        ("2. Anthropic Claude", "Claude 3 Opus/Sonnet/Haiku", "pip install anthropic", "ANTHROPIC_API_KEY"),
        ("3. Ollama 本地模型", "Llama 2, Mistral, CodeLlama", "无需安装", "无需 API Key"),
        ("4. 自定义 API", "任何兼容的 API 接口", "-", "-"),
        ("5. Google Gemini", "Gemini Pro/PaLM", "pip install google-generativeai", "GOOGLE_API_KEY"),
        ("6. Cohere", "Command 系列", "pip install cohere", "COHERE_API_KEY"),
    ]
    
    for name, models, install, key in providers:
        print(f"\n{name}")
        print(f"   模型: {models}")
        print(f"   安装: {install}")
        print(f"   配置: {key}")
    
    print("\n" + "-" * 60)
    print("\n核心类：AIAgent")
    print("- AIAgent 是 RandomAgent 的核心 AI 集成类")
    print("- 自动生成 RandomAgent 系统提示词")
    print("- 调用真实的 AI 模型 API")
    print("- 返回结构化的思考结果")


def show_ai_code_examples():
    """展示 AI 接入代码示例"""
    print("\n" + "=" * 70)
    print("代码示例：如何接入 AI")
    print("=" * 70)
    
    print("\n" + "=" * 60)
    print("示例 1: 使用 OpenAI GPT-4")
    print("=" * 60)
    
    code_example_1 = '''
from random_agent import AIAgent, AIConfig, AIProvider

config = AIConfig(
    provider=AIProvider.OPENAI,
    model="gpt-4",
    randomness_level=0.7,
    thinking_mode="creative"
)

agent = AIAgent(config)

result = agent.think("什么是创造力？")

print(result["answer"])
print(result["thinking"])
'''
    
    print(code_example_1)
    
    print("\n" + "=" * 60)
    print("示例 2: 使用本地 Ollama 模型（免费！无需API Key）")
    print("=" * 60)
    
    code_example_2 = '''
from random_agent import AIAgent, AIConfig, AIProvider

# 前提：已安装并运行 Ollama
# 安装: https://ollama.ai
# 运行: ollama serve
# 下载模型: ollama pull llama2

config = AIConfig(
    provider=AIProvider.OLLAMA,
    model="llama2",
    base_url="http://localhost:11434",
    randomness_level=0.6,
    thinking_mode="balanced"
)

agent = AIAgent(config)

result = agent.think("解释量子计算的基本原理")
print(result["answer"])
'''
    
    print(code_example_2)
    
    print("\n" + "=" * 60)
    print("示例 3: 使用 Anthropic Claude")
    print("=" * 60)
    
    code_example_3 = '''
from random_agent import AIAgent, AIConfig, AIProvider

config = AIConfig(
    provider=AIProvider.ANTHROPIC,
    model="claude-3-opus-20240229",
    randomness_level=0.8,
    thinking_mode="divergent"
)

agent = AIAgent(config)

result = agent.think("设计一个创新的智能家居产品")
print(result["answer"])
'''
    
    print(code_example_3)
    
    print("\n" + "=" * 60)
    print("示例 4: 使用扩展提供商 (Google Gemini)")
    print("=" * 60)
    
    code_example_4 = '''
from random_agent import create_extended_ai_agent

agent = create_extended_ai_agent(
    provider_type="google",
    model="gemini-pro",
    api_key="your-google-api-key",
    randomness_level=0.7
)

result = agent.think("人工智能的未来发展方向")
print(result["answer"])
'''
    
    print(code_example_4)


def demo_quick_start():
    """快速开始指南"""
    print("\n" + "=" * 70)
    print("快速开始：3 步接入 AI")
    print("=" * 70)
    
    print("\n步骤 1: 安装依赖")
    print("-" * 50)
    print("# 基础安装")
    print("pip install -e .")
    print("")
    print("# 可选：安装特定 AI 提供商支持")
    print("pip install openai          # OpenAI 支持")
    print("pip install anthropic       # Claude 支持")
    print("# Ollama 无需安装 Python 包")
    
    print("\n步骤 2: 配置 API Key（可选）")
    print("-" * 50)
    print("方式 A: 环境变量（推荐）")
    print('export OPENAI_API_KEY="sk-..."')
    print('')
    print("方式 B: .env 文件")
    print("创建 .env 文件并写入:")
    print("OPENAI_API_KEY=sk-...")
    print("")
    print("注意：使用 Ollama 本地模型不需要 API Key！")
    
    print("\n步骤 3: 开始使用")
    print("-" * 50)
    print("最简单的例子（使用 Ollama 本地模型）:\n")

    simple_code = '''from random_agent import AIAgent, AIConfig, AIProvider

agent = AIAgent(AIConfig(
    provider=AIProvider.OLLAMA,
    model="llama2"
))

result = agent.think("你好，请自我介绍")
print(result["answer"])

# 就这么简单！
'''
    
    print(simple_code)


def demo_advanced_features():
    """高级功能演示"""
    print("\n" + "=" * 70)
    print("高级功能：AIAgent 完整能力")
    print("=" * 70)
    
    features = [
        ("对话历史管理", """
agent = AIAgent(config)
result1 = agent.think("什么是机器学习？")
result2 = agent.think("那深度学习呢？")  # 会记住上下文
agent.clear_history()  # 清空历史
"""),
        
        ("批量处理", """
questions = ["什么是创造力？", "如何提高创新能力？"]
for q in questions:
    result = agent.think(q)
    print(f"Q: {q}")
    print(f"A: {result['answer'][:100]}...")
"""),
        
        ("自定义系统提示词", """
from random_agent.prompt_templates import PromptConfig, ThinkingMode

prompt_config = PromptConfig(
    randomness_level=0.9,
    thinking_mode=ThinkingMode.CREATIVE
)
agent = AIAgent(config, prompt_config=prompt_config)
"""),
        
        ("错误处理和重试", """
try:
    result = agent.think("问题")
except Exception as e:
    print(f"错误: {e}")
"""),
    ]
    
    for title, code in features:
        print(f"\n{title}")
        print("-" * 40)
        print(code)


def demo_architecture():
    """架构说明"""
    print("\n" + "=" * 70)
    print("RandomAgent 架构说明")
    print("=" * 70)
    
    print("""
架构图:

                    用户 (You)
                        |
                        v
                AIAgent (统一接口)
               - think(question) -> 调用 AI
               - manage history -> 对话历史
               - generate prompt -> 自动生成系统提示词
                        |
            +-----------+-----------+
            |           |           |
        OpenAI      Claude      Ollama
        Provider    Provider    Provider
            |           |           |
            +-----------+-----------+
                        |
              RandomAgent 提示词引擎
             - 核心理念 (随机性、创造力)
             - 思维框架 (发散/收敛/平衡)
             - 意识层次 (表层/深层/潜意识)
             - DMN 模拟 (默认模式网络)
             - 情绪系统 (积极/中性/消极)

工作流程:
1. 用户调用 agent.think("问题")
2. AIAgent 根据 config 生成 RandomAgent 系统提示词
3. 将系统提示词 + 用户问题发送给 AI 提供商
4. AI 提供商返回结果
5. AIAgent 格式化返回结果 (answer, thinking, metadata)

关键点:
✅ 用户不需要手动复制粘贴提示词
✅ 一行代码即可完成 AI 调用
✅ 自动应用 RandomAgent 的思维框架
✅ 支持多种 AI 后端切换
✅ 统一的接口和错误处理
""")


def main():
    """主函数"""
    demo_ai_integration_overview()
    
    input("\n按 Enter 键继续查看代码示例...")
    show_ai_code_examples()
    
    input("\n按 Enter 键继续查看快速开始指南...")
    demo_quick_start()
    
    input("\n按 Enter 键继续查看高级功能...")
    demo_advanced_features()
    
    input("\n按 Enter 键继续查看架构说明...")
    demo_architecture()
    
    print("\n" + "=" * 70)
    print("总结")
    print("=" * 70)
    
    print("""
你的问题完全正确！

RandomAgent 确实需要能够接入 AI，而且已经实现了这个功能！

核心组件:
✅ AIAgent 类 - 统一的 AI 接口
✅ 多种提供商支持 - OpenAI/Claude/Ollama/自定义
✅ 自动提示词生成 - 无需手动操作
✅ 扩展提供商 - Google/Cohere/Azure 等

推荐的使用方式:

对于大多数用户:
1. 本地开发/测试: 使用 Ollama（免费、无需 API Key）
2. 生产环境: 使用 OpenAI 或 Claude（质量更高）
3. 特殊需求: 使用扩展提供商或自定义 API

下一步行动:

1. 尝试运行本演示中的代码示例
2. 查看 ai_integration.py 了解详细实现
3. 阅读 README.md 获取更多文档
4. 根据需求选择合适的 AI 提供商

现在你已经了解了 RandomAgent 的完整 AI 接入能力！
可以直接开始使用了！
""")
    print("=" * 70)


if __name__ == "__main__":
    main()
