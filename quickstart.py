#!/usr/bin/env python3
"""
RandomAgent 快速开始脚本

运行此脚本快速了解如何使用 RandomAgent 框架
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from random_agent import create_prompt, get_system_prompt_only, create_ai_agent


def print_header(title):
    """打印标题"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def print_section(title):
    """打印小节"""
    print(f"\n### {title}")
    print("-" * 60)


def main():
    print_header("RandomAgent 快速开始")
    
    print("""
RandomAgent 是一个提示词工程框架，帮助你：
1. 生成创新的系统提示词
2. 集成 AI API（OpenAI/Claude/Ollama）
3. 模拟人类随机跳跃思维
""")
    
    print_section("示例 1: 生成提示词")
    
    prompt = create_prompt(
        task="什么是真正的创新？",
        randomness=0.7,
        mode="creative"
    )
    
    print("\n生成的提示词（精简版）：")
    print(prompt[:500] + "...")
    
    print_section("示例 2: 获取系统提示词")
    
    system_prompt = get_system_prompt_only(
        randomness=0.5,
        mode="balanced"
    )
    
    print("\n系统提示词（用于设置 AI 的 system message）：")
    print(system_prompt[:400] + "...")
    
    print_section("示例 3: 不同思维模式")
    
    modes = [
        ("divergent", "发散思维 - 广泛探索"),
        ("convergent", "收敛思维 - 聚焦整合"),
        ("creative", "创造性思维 - 最大化随机"),
        ("analytical", "分析性思维 - 逻辑推理"),
    ]
    
    for mode, desc in modes:
        prompt = create_prompt(
            task="如何解决问题？",
            randomness=0.5,
            mode=mode,
            style="concise"
        )
        print(f"\n【{desc}】")
        print(f"模式: {mode}")
        print(f"提示词长度: {len(prompt)} 字符")
    
    print_section("示例 4: CLI 命令行使用")
    
    print("""
命令行工具使用方法：

# 生成提示词
python -m random_agent "你的问题"

# 指定随机性和模式
python -m random_agent "问题" --randomness 0.8 --mode creative

# 仅获取系统提示词
python -m random_agent --system-prompt --mode balanced

# 调用 AI（需要设置 API Key）
python -m random_agent "问题" --call-ai --provider openai
""")
    
    print_section("示例 5: Python API 使用")
    
    print("""
# 生成提示词
from random_agent import create_prompt
prompt = create_prompt("问题", randomness=0.7, mode="creative")

# 调用 AI
from random_agent import create_ai_agent
agent = create_ai_agent(
    provider="openai",
    api_key="your-key",
    randomness=0.7
)
result = agent.think("你的问题")
print(result["answer"])
""")
    
    print_section("示例 6: 随机性水平对比")
    
    levels = [
        (0.2, "低随机性 - 逻辑为主"),
        (0.5, "中等随机性 - 平衡"),
        (0.8, "高随机性 - 跳跃为主"),
    ]
    
    for level, desc in levels:
        prompt = create_prompt(
            task="思考一下",
            randomness=level,
            mode="balanced",
            style="concise"
        )
        print(f"\n【{desc}】")
        print(f"随机性: {level:.0%}")
        print(f"提示词长度: {len(prompt)} 字符")
    
    print_header("下一步")
    
    print("""
1. 📖 阅读完整文档：README.md
2. 📝 查看示例代码：examples/developer_guide.py
3. 🧪 运行测试：python tests/test_random_agent.py
4. 🚀 开始使用：
   - 生成提示词：python -m random_agent "你的问题"
   - 集成到项目：from random_agent import create_prompt
   - 调用 AI：from random_agent import create_ai_agent

提示词工程的核心：
- 随机性水平：控制思维的跳跃程度
- 思维模式：选择适合的思考方式
- 有边界的随机：目标是确定的，路径是随机的
""")
    
    print_header("完成！")
    print("\n✅ 你已经了解了 RandomAgent 的基本用法！\n")


if __name__ == "__main__":
    main()
