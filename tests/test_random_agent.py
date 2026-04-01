"""
RandomAgent 单元测试
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from random_agent.prompt_templates import (
    create_prompt,
    get_system_prompt_only,
    RandomAgentPromptBuilder,
    PromptConfig,
    ThinkingMode,
    PromptStyle,
)
from random_agent.ai_integration import (
    AIConfig,
    AIProvider,
    AIAgent,
    create_ai_agent,
)
from random_agent.core.randomness_engine import RandomnessEngine, RandomnessType


class TestPromptTemplates(unittest.TestCase):
    """测试提示词模板"""
    
    def test_create_prompt_basic(self):
        """测试基本提示词生成"""
        prompt = create_prompt(
            task="测试问题",
            randomness=0.5,
            mode="balanced"
        )
        
        self.assertIsInstance(prompt, str)
        self.assertIn("测试问题", prompt)
        self.assertIn("RandomAgent", prompt)
    
    def test_create_prompt_with_different_modes(self):
        """测试不同模式的提示词"""
        modes = ["divergent", "convergent", "balanced", "creative", "analytical"]
        
        for mode in modes:
            prompt = create_prompt(
                task="测试",
                randomness=0.5,
                mode=mode
            )
            self.assertIsInstance(prompt, str)
            self.assertIn(mode, prompt.lower())
    
    def test_get_system_prompt_only(self):
        """测试仅获取系统提示词"""
        system_prompt = get_system_prompt_only(
            randomness=0.7,
            mode="creative"
        )
        
        self.assertIsInstance(system_prompt, str)
        self.assertIn("核心理念", system_prompt)
        self.assertIn("RandomAgent", system_prompt)
    
    def test_prompt_config(self):
        """测试提示词配置"""
        config = PromptConfig(
            randomness_level=0.8,
            thinking_mode=ThinkingMode.CREATIVE,
            enable_consciousness_layers=True,
            enable_dmn=True,
            enable_emotions=True
        )
        
        self.assertEqual(config.randomness_level, 0.8)
        self.assertEqual(config.thinking_mode, ThinkingMode.CREATIVE)
        self.assertTrue(config.enable_consciousness_layers)
    
    def test_prompt_builder(self):
        """测试提示词构建器"""
        config = PromptConfig(
            randomness_level=0.6,
            thinking_mode=ThinkingMode.ANALYTICAL
        )
        
        builder = RandomAgentPromptBuilder(config)
        
        system_prompt = builder.build_system_prompt()
        self.assertIsInstance(system_prompt, str)
        
        task_prompt = builder.build_task_prompt("测试任务")
        self.assertIn("测试任务", task_prompt)
        
        full_prompt = builder.get_full_prompt("完整测试")
        self.assertIn("完整测试", full_prompt)
    
    def test_compact_prompt(self):
        """测试精简版提示词"""
        prompt = create_prompt(
            task="测试",
            randomness=0.5,
            mode="balanced",
            style="concise"
        )
        
        self.assertIsInstance(prompt, str)
        self.assertLess(len(prompt), 1000)


class TestAIIntegration(unittest.TestCase):
    """测试 AI 集成"""
    
    def test_ai_config(self):
        """测试 AI 配置"""
        config = AIConfig(
            provider=AIProvider.OPENAI,
            model="gpt-4",
            randomness_level=0.7,
            thinking_mode="creative"
        )
        
        self.assertEqual(config.provider, AIProvider.OPENAI)
        self.assertEqual(config.model, "gpt-4")
        self.assertEqual(config.randomness_level, 0.7)
    
    def test_create_ai_agent(self):
        """测试创建 AI Agent"""
        agent = create_ai_agent(
            provider="openai",
            model="gpt-4",
            randomness=0.5
        )
        
        self.assertIsInstance(agent, AIAgent)
        self.assertEqual(agent.config.provider, AIProvider.OPENAI)
    
    def test_ai_agent_get_prompt(self):
        """测试 AI Agent 获取提示词"""
        agent = create_ai_agent(
            provider="openai",
            randomness=0.5
        )
        
        prompt = agent.get_prompt_only("测试问题")
        self.assertIn("测试问题", prompt)
        
        system_prompt = agent.get_system_prompt()
        self.assertIn("RandomAgent", system_prompt)
    
    def test_ai_agent_set_parameters(self):
        """测试设置参数"""
        agent = create_ai_agent(randomness=0.5)
        
        agent.set_randomness(0.8)
        self.assertEqual(agent.config.randomness_level, 0.8)
        
        agent.set_thinking_mode("creative")
        self.assertEqual(agent.config.thinking_mode, "creative")


class TestRandomnessEngine(unittest.TestCase):
    """测试随机引擎"""
    
    def test_random_choice(self):
        """测试随机选择"""
        engine = RandomnessEngine(seed=42)
        
        options = ["A", "B", "C"]
        result = engine.random_choice(options)
        
        self.assertIn(result, options)
    
    def test_random_choice_with_weights(self):
        """测试带权重的随机选择"""
        engine = RandomnessEngine(seed=42)
        
        options = ["A", "B", "C"]
        weights = [0.1, 0.8, 0.1]
        
        results = [engine.random_choice(options, weights) for _ in range(100)]
        
        count_b = results.count("B")
        self.assertGreater(count_b, 50)
    
    def test_create_superposition(self):
        """测试创建叠加态"""
        engine = RandomnessEngine()
        
        possibilities = ["A", "B", "C"]
        weights = [0.3, 0.4, 0.3]
        
        superposition = engine.create_superposition(possibilities, weights)
        
        self.assertEqual(superposition.possibilities, possibilities)
        self.assertEqual(len(superposition.weights), len(weights))
    
    def test_collapse_superposition(self):
        """测试坍塌叠加态"""
        engine = RandomnessEngine(seed=42)
        
        possibilities = ["A", "B", "C"]
        superposition = engine.create_superposition(possibilities)
        
        result = engine.collapse_superposition(superposition)
        
        self.assertIn(result, possibilities)
    
    def test_inject_randomness(self):
        """测试注入随机性"""
        engine = RandomnessEngine()
        
        value = 100
        noisy_value = engine.inject_randomness(value, probability=1.0)
        
        self.assertIsInstance(noisy_value, float)


class TestCoreModules(unittest.TestCase):
    """测试核心模块"""
    
    def test_consciousness_layers_import(self):
        """测试意识层次模块导入"""
        from random_agent.core.consciousness_layers import ConsciousnessLayers, ConsciousnessLevel
        
        self.assertIsNotNone(ConsciousnessLayers)
        self.assertIsNotNone(ConsciousnessLevel)
    
    def test_consciousness_stream_import(self):
        """测试意识流模块导入"""
        from random_agent.core.consciousness_stream import ConsciousnessStream
        
        self.assertIsNotNone(ConsciousnessStream)
    
    def test_dmn_engine_import(self):
        """测试 DMN 引擎模块导入"""
        from random_agent.core.dmn_engine import DMNEngine
        
        self.assertIsNotNone(DMNEngine)
    
    def test_memory_system_import(self):
        """测试记忆系统模块导入"""
        from random_agent.core.memory_system import MemorySystem, MemoryType
        
        self.assertIsNotNone(MemorySystem)
        self.assertIsNotNone(MemoryType)
    
    def test_goal_system_import(self):
        """测试目标系统模块导入"""
        from random_agent.core.goal_system import GoalSystem
        
        self.assertIsNotNone(GoalSystem)
    
    def test_influence_factors_import(self):
        """测试影响因素模块导入"""
        from random_agent.core.influence_factors import InfluenceFactors, CognitiveBiasType
        
        self.assertIsNotNone(InfluenceFactors)
        self.assertIsNotNone(CognitiveBiasType)
    
    def test_balance_controller_import(self):
        """测试平衡控制器模块导入"""
        from random_agent.core.balance_controller import BalanceController, ThinkingMode
        
        self.assertIsNotNone(BalanceController)
        self.assertIsNotNone(ThinkingMode)
    
    def test_output_system_import(self):
        """测试输出系统模块导入"""
        from random_agent.core.output_system import OutputSystem
        
        self.assertIsNotNone(OutputSystem)


def run_tests():
    """运行所有测试"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestPromptTemplates))
    suite.addTests(loader.loadTestsFromTestCase(TestAIIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestRandomnessEngine))
    suite.addTests(loader.loadTestsFromTestCase(TestCoreModules))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
