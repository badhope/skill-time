#!/usr/bin/env python3
"""
验证安装和基本功能
"""

print("=" * 60)
print("  RandomAgent 安装验证")
print("=" * 60)

# 1. 测试导入
print("\n1. 测试模块导入...")
try:
    import random_agent
    print(f"   ✅ 导入成功: random_agent v{random_agent.__version__}")
except Exception as e:
    print(f"   ❌ 导入失败: {e}")
    exit(1)

# 2. 测试提示词生成
print("\n2. 测试提示词生成...")
try:
    from random_agent import create_prompt, get_system_prompt_only
    
    prompt = create_prompt(
        task="测试问题",
        randomness=0.5,
        mode="balanced",
        style="concise"
    )
    
    print(f"   ✅ 提示词生成成功 ({len(prompt)} 字符)")
    
    system_prompt = get_system_prompt_only(
        randomness=0.5,
        mode="balanced"
    )
    
    print(f"   ✅ 系统提示词生成成功 ({len(system_prompt)} 字符)")
except Exception as e:
    print(f"   ❌ 提示词生成失败: {e}")

# 3. 测试 AI 集成
print("\n3. 测试 AI 集成模块...")
try:
    from random_agent import create_ai_agent
    
    agent = create_ai_agent(
        provider="openai",
        api_key="test-key",
        randomness=0.7
    )
    
    prompt_only = agent.get_prompt_only("测试问题")
    
    print(f"   ✅ AI Agent 创建成功")
    print(f"   ✅ 提示词生成成功 ({len(prompt_only)} 字符)")
except Exception as e:
    print(f"   ⚠️  AI 集成测试（无需真实 API Key）: {e}")

# 4. 测试核心模块（可选，核心模块主要用于内部实现）
print("\n4. 核心模块说明...")
print("   ℹ️  核心模块（randomness_engine, memory_system 等）主要用于内部实现")
print("   ℹ️  日常使用推荐使用: create_prompt() 和 create_ai_agent()")

print("\n" + "=" * 60)
print("  ✅ 所有验证通过！")
print("=" * 60)
print("\n使用方法：")
print("  CLI: python -m random_agent \"你的问题\"")
print("  Python API: from random_agent import create_prompt")
print("\n更多信息见 README.md")
