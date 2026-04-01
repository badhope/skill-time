"""
直接测试RandomAgent系统
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from random_agent.agent import RandomAgent, create_agent, AgentConfig

print("=" * 60)
print("RandomAgent 直接测试")
print("=" * 60)

print("\n1. 创建智能体...")
agent = create_agent(randomness=0.5, openness=0.7)
print("✅ 智能体创建成功")

print("\n2. 思考问题...")
result = agent.think("什么是创造力？", max_iterations=5)
print("\n【最终答案】")
print(result["answer"])

print(f"\n【置信度】{result['confidence']:.0%}")
print(f"【思考步骤】{result['iterations']}步")

print("\n3. 探索模式...")
explore_results = agent.explore("人工智能的未来", depth=3)
print(f"\n探索到 {len(explore_results)} 个想法")

print("\n4. 获取状态...")
state = agent.get_state()
print(f"\n状态: {state['state']}")
print(f"随机性: {state['balance']['randomness_level']:.2f}")
print(f"思维模式: {state['balance']['thinking_mode'].value}")

print("\n" + "=" * 60)
print("测试完成！")
print("=" * 60)
