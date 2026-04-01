"""
RandomAgent 示例代码

展示如何使用RandomAgent框架
"""

from random_agent import Agent
from random_agent.agent import create_agent, AgentConfig
from random_agent.core.randomness_engine import RandomnessType
from random_agent.core.balance_controller import ThinkingMode
from random_agent.core.influence_factors import CognitiveBiasType
from random_agent.core.memory_system import MemoryType


def basic_usage():
    """基本使用示例"""
    print("=" * 60)
    print("基本使用示例")
    print("=" * 60)
    
    agent = create_agent(
        randomness=0.5,
        openness=0.7,
        conscientiousness=0.5
    )
    
    result = agent.think("什么是创造力？")
    
    print("\n【最终答案】")
    print(result["answer"])
    
    print(f"\n【置信度】{result['confidence']:.0%}")
    print(f"【思考步骤】{result['iterations']}步")


def explore_mode():
    """探索模式示例"""
    print("\n" + "=" * 60)
    print("探索模式示例")
    print("=" * 60)
    
    agent = create_agent(randomness=0.7)
    
    results = agent.explore("人工智能的未来", depth=5)
    
    print("\n探索结果：")
    for i, r in enumerate(results):
        print(f"{i+1}. [{r['level']}] {r['content'][:50]}...")


def wander_mode():
    """走神模式示例"""
    print("\n" + "=" * 60)
    print("走神模式示例")
    print("=" * 60)
    
    agent = create_agent(randomness=0.6)
    
    thoughts = agent.wander(duration=5)
    
    print("\n走神产生的思维：")
    for i, t in enumerate(thoughts):
        print(f"{i+1}. {t['content'][:60]}...")


def custom_config():
    """自定义配置示例"""
    print("\n" + "=" * 60)
    print("自定义配置示例")
    print("=" * 60)
    
    config = AgentConfig(
        randomness_seed=42,
        working_memory_capacity=5,
        initial_randomness_level=0.6,
        default_thinking_mode=ThinkingMode.CREATIVE,
        personality={
            "openness": 0.8,
            "conscientiousness": 0.3,
            "extraversion": 0.6,
            "agreeableness": 0.5,
            "neuroticism": 0.3
        },
        noise_config={
            "base_level": 0.15,
            "signal_to_noise_ratio": 0.7,
            "fluctuation_amplitude": 0.25,
            "spontaneous_rate": 0.08
        }
    )
    
    agent = Agent(config)
    
    result = agent.think("如何设计一个创新的解决方案？")
    
    print("\n【最终答案】")
    print(result["answer"])


def cognitive_bias_example():
    """认知偏见示例"""
    print("\n" + "=" * 60)
    print("认知偏见示例")
    print("=" * 60)
    
    agent = create_agent(randomness=0.5)
    
    agent.enable_bias(CognitiveBiasType.CONFIRMATION_BIAS, 0.7)
    agent.enable_bias(CognitiveBiasType.ANCHORING, 0.5)
    
    result = agent.think("这个方案是否可行？")
    print("\n启用确认偏见和锚定效应后：")
    print(result["answer"])
    
    agent.disable_bias(CognitiveBiasType.CONFIRMATION_BIAS)
    agent.disable_bias(CognitiveBiasType.ANCHORING)


def memory_example():
    """记忆系统示例"""
    print("\n" + "=" * 60)
    print("记忆系统示例")
    print("=" * 60)
    
    agent = create_agent(randomness=0.5)
    
    agent.add_memory(
        "RandomAgent是一个模拟人类思维的框架",
        MemoryType.SEMANTIC,
        importance=0.8
    )
    
    agent.add_memory(
        "今天学习了意识流理论",
        MemoryType.EPISODIC,
        importance=0.6
    )
    
    result = agent.think("RandomAgent是什么？")
    print("\n【回答】")
    print(result["answer"])


def thinking_modes():
    """思维模式示例"""
    print("\n" + "=" * 60)
    print("思维模式示例")
    print("=" * 60)
    
    agent = create_agent(randomness=0.5)
    
    modes = [
        ThinkingMode.DIVERGENT,
        ThinkingMode.CONVERGENT,
        ThinkingMode.CREATIVE,
        ThinkingMode.ANALYTICAL
    ]
    
    question = "如何解决复杂问题？"
    
    for mode in modes:
        agent.set_mode(mode)
        result = agent.think(question, max_iterations=5)
        print(f"\n【{mode.value}模式】")
        print(result["answer"][:100] + "...")


def agent_state():
    """智能体状态示例"""
    print("\n" + "=" * 60)
    print("智能体状态示例")
    print("=" * 60)
    
    agent = create_agent(randomness=0.5)
    
    agent.think("测试问题")
    
    state = agent.get_state()
    
    print("\n【智能体状态】")
    print(f"状态: {state['state']}")
    print(f"当前目标: {state['current_goal']}")
    print(f"随机性水平: {state['balance']['randomness_level']:.2f}")
    print(f"思维模式: {state['balance']['thinking_mode'].value}")
    print(f"能量水平: {state['balance']['energy_level']:.2f}")


def full_report():
    """完整报告示例"""
    print("\n" + "=" * 60)
    print("完整报告示例")
    print("=" * 60)
    
    agent = create_agent(randomness=0.5)
    
    agent.think("什么是创新思维？")
    
    report = agent.get_full_report()
    
    print("\n【平衡报告】")
    balance = report["balance_report"]["balance_state"]
    print(f"随机性: {balance['randomness_level']:.2f}")
    print(f"探索比例: {balance['exploration_ratio']:.2f}")
    print(f"专注度: {balance['focus_level']:.2f}")
    print(f"创造力加成: {balance['creativity_boost']:.2f}")
    
    print("\n【建议】")
    for rec in report["balance_report"]["recommendations"]:
        print(f"• {rec}")


def main():
    """运行所有示例"""
    print("\n" + "=" * 60)
    print("RandomAgent 示例演示")
    print("=" * 60)
    
    basic_usage()
    explore_mode()
    wander_mode()
    custom_config()
    cognitive_bias_example()
    memory_example()
    thinking_modes()
    agent_state()
    full_report()
    
    print("\n" + "=" * 60)
    print("示例演示完成")
    print("=" * 60)


if __name__ == "__main__":
    main()
