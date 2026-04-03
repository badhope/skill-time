"""
脑启发架构集成测试
验证所有模块的功能和集成
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
import time
from datetime import datetime

from random_agent.brain_inspired import (
    PerceptualSystem,
    DefaultModeNetwork,
    HippocampalMemorySystem,
    GlobalWorkspace,
    PrefrontalExecutiveSystem,
    AmygdalaEmotionSystem,
    EventDrivenArchitecture,
    EventType,
    BrainEvent,
    InformationPacket,
)


class TestPerceptualSystem(unittest.TestCase):
    """感知觉系统测试"""
    
    def setUp(self):
        self.perceptual_system = PerceptualSystem()
    
    def test_process_input(self):
        """测试输入处理"""
        raw_input = "这是一个测试输入，包含一些关键信息。"
        result = self.perceptual_system.process(raw_input)
        
        self.assertIsNotNone(result)
        self.assertTrue(hasattr(result, 'semantic_features'))
        self.assertTrue(hasattr(result, 'structural_features'))
        self.assertGreater(result.salience, 0)
    
    def test_feature_extraction(self):
        """测试特征提取"""
        raw_input = "帮我分析这个问题：如何提高效率？"
        result = self.perceptual_system.process(raw_input)
        
        self.assertIn('length', result.semantic_features)
        self.assertIn('word_count', result.semantic_features)
    
    def test_pattern_recognition(self):
        """测试模式识别"""
        raw_input = "帮我完成这个任务"
        result = self.perceptual_system.process(raw_input)
        
        self.assertIsNotNone(result.structural_features)


class TestDefaultModeNetwork(unittest.TestCase):
    """默认模式网络测试"""
    
    def setUp(self):
        self.dmn = DefaultModeNetwork()
    
    def test_idle_mode(self):
        """测试空闲模式"""
        results = self.dmn.run_idle_mode(iterations=3)
        
        self.assertEqual(len(results), 3)
        for result in results:
            self.assertIn('thought', result)
            self.assertIn('narrative_state', result)
    
    def test_external_input_integration(self):
        """测试外部输入整合"""
        external_input = "外部测试输入"
        result = self.dmn.integrate_external_input(external_input)
        
        self.assertIsNotNone(result)
        self.assertIn('merged_state', result)
    
    def test_reflection(self):
        """测试自我反思"""
        self.dmn.run_idle_mode(iterations=2)
        reflection = self.dmn.reflect()
        
        self.assertIsNotNone(reflection)
        self.assertIn('narrative', reflection)
        self.assertIn('metacognition', reflection)


class TestHippocampalMemorySystem(unittest.TestCase):
    """海马体记忆系统测试"""
    
    def setUp(self):
        self.hippocampus = HippocampalMemorySystem()
    
    def test_memory_encoding(self):
        """测试记忆编码"""
        experience = "今天学习了一个新概念"
        trace = self.hippocampus.encode(experience)
        
        self.assertIsNotNone(trace)
        self.assertEqual(trace.content, experience)
        self.assertGreater(trace.importance, 0)
    
    def test_memory_retrieval(self):
        """测试记忆检索"""
        experience = "重要的记忆内容"
        self.hippocampus.encode(experience)
        
        results = self.hippocampus.retrieve("重要")
        
        self.assertGreater(len(results), 0)
        self.assertEqual(results[0][0].content, experience)
    
    def test_memory_consolidation(self):
        """测试记忆巩固"""
        for i in range(5):
            self.hippocampus.encode(f"经验 {i}")
        
        consolidated = self.hippocampus.consolidate_memories(iterations=3)
        
        self.assertGreater(len(consolidated), 0)
    
    def test_memory_stats(self):
        """测试记忆统计"""
        self.hippocampus.encode("测试记忆")
        stats = self.hippocampus.get_memory_stats()
        
        self.assertIn('total_memories', stats)
        self.assertGreater(stats['total_memories'], 0)


class TestGlobalWorkspace(unittest.TestCase):
    """全局工作空间测试"""
    
    def setUp(self):
        self.workspace = GlobalWorkspace()
        
        def mock_callback(content):
            pass
        
        self.workspace.register_module('test_module', mock_callback)
    
    def test_information_submission(self):
        """测试信息提交"""
        packet = InformationPacket(
            source='test',
            content='测试内容',
            salience=0.8,
            modality='test'
        )
        
        self.workspace.submit(packet)
        
        stats = self.workspace.get_workspace_stats()
        self.assertGreater(stats['buffer_stats']['total_packets'], 0)
    
    def test_consciousness_emergence(self):
        """测试意识涌现"""
        for i in range(5):
            packet = InformationPacket(
                source=f'source_{i}',
                content=f'内容_{i}',
                salience=0.5 + i * 0.1,
                modality='test'
            )
            self.workspace.submit(packet)
        
        conscious_content = self.workspace.process()
        
        self.assertIsNotNone(conscious_content)
        self.assertGreater(conscious_content.integration_level, 0)
    
    def test_workspace_state(self):
        """测试工作空间状态"""
        state = self.workspace.get_state()
        
        self.assertIsNotNone(state)
        self.assertIn('attention_focus', state.__dict__)


class TestPrefrontalExecutiveSystem(unittest.TestCase):
    """前额叶执行系统测试"""
    
    def setUp(self):
        self.executive_system = PrefrontalExecutiveSystem()
    
    def test_decision_making(self):
        """测试决策制定"""
        task = "选择最佳方案"
        decision = self.executive_system.control(task, goals=['优化', '效率'])
        
        self.assertIsNotNone(decision)
        self.assertIsNotNone(decision.selected_option)
        self.assertGreater(decision.confidence, 0)
    
    def test_planning(self):
        """测试规划"""
        goal = "完成项目"
        actions = ['分析', '设计', '实现', '测试']
        
        plan = self.executive_system.plan(goal, actions)
        
        self.assertIsNotNone(plan)
        self.assertEqual(plan.goal, goal)
        self.assertGreater(len(plan.steps), 0)
    
    def test_working_memory(self):
        """测试工作记忆"""
        self.executive_system.working_memory.load("项目A", importance=0.9)
        self.executive_system.working_memory.load("项目B", importance=0.7)
        
        stats = self.executive_system.working_memory.get_stats()
        
        self.assertEqual(stats['item_count'], 2)
        self.assertGreater(stats['load'], 0)
    
    def test_cognitive_flexibility(self):
        """测试认知灵活性"""
        cost1 = self.executive_system.switch_task("任务A")
        cost2 = self.executive_system.switch_task("任务B")
        cost3 = self.executive_system.switch_task("任务A")
        
        self.assertGreater(cost1, 0)
        self.assertGreater(cost2, 0)
        self.assertLess(cost3, cost1)


class TestAmygdalaEmotionSystem(unittest.TestCase):
    """杏仁核情绪系统测试"""
    
    def setUp(self):
        self.emotion_system = AmygdalaEmotionSystem()
    
    def test_emotion_processing(self):
        """测试情绪处理"""
        stimulus = "这是一个危险的警告"
        emotional_state = self.emotion_system.process_emotion(stimulus)
        
        self.assertIsNotNone(emotional_state)
        self.assertLess(emotional_state.valence, 0)
        self.assertGreater(emotional_state.arousal, 0)
    
    def test_threat_detection(self):
        """测试威胁检测"""
        threat_stimulus = "紧急危险情况"
        safe_stimulus = "安全的环境"
        
        threat_assessment = self.emotion_system.assess_threat(threat_stimulus)
        safe_assessment = self.emotion_system.assess_threat(safe_stimulus)
        
        self.assertGreater(threat_assessment.threat_level, safe_assessment.threat_level)
    
    def test_emotional_memory(self):
        """测试情绪记忆"""
        stimulus = "重要事件"
        self.emotion_system.process_emotion(stimulus)
        
        memory = self.emotion_system.get_emotional_memory(stimulus)
        
        self.assertIsNotNone(memory)
        self.assertEqual(memory.stimulus, stimulus)
    
    def test_emotion_regulation(self):
        """测试情绪调节"""
        stimulus = "令人焦虑的情况"
        emotional_state = self.emotion_system.process_emotion(stimulus)
        
        regulated_state = self.emotion_system.regulate_emotion(
            emotional_state, 
            prefrontal_input=0.8
        )
        
        self.assertLess(abs(regulated_state.valence), abs(emotional_state.valence))


class TestEventDrivenArchitecture(unittest.TestCase):
    """事件驱动架构测试"""
    
    def setUp(self):
        self.architecture = EventDrivenArchitecture()
        self.received_events = []
        
        def mock_handler(event):
            self.received_events.append(event)
        
        self.mock_handler = mock_handler
    
    def test_module_registration(self):
        """测试模块注册"""
        self.architecture.register_module(
            'test_module',
            None,
            {EventType.PERCEPTION_INPUT: self.mock_handler}
        )
        
        stats = self.architecture.get_architecture_stats()
        self.assertIn('test_module', stats['modules'])
    
    def test_event_publication(self):
        """测试事件发布"""
        self.architecture.register_module(
            'test_module',
            None,
            {EventType.PERCEPTION_INPUT: self.mock_handler}
        )
        
        event = BrainEvent(
            event_type=EventType.PERCEPTION_INPUT,
            source='external',
            target='test_module',
            data={'test': 'data'}
        )
        
        self.architecture.event_bus.publish(event, async_mode=False)
        
        self.assertEqual(len(self.received_events), 1)
    
    def test_module_connection(self):
        """测试模块连接"""
        self.architecture.connect_modules('module_a', 'module_b', strength=0.8)
        
        pathway = self.architecture.connection_manager.get_pathway('module_a', 'module_b')
        
        self.assertIsNotNone(pathway)
        self.assertEqual(pathway.strength, 0.8)


class TestIntegratedBrainSystem(unittest.TestCase):
    """集成脑系统测试"""
    
    def setUp(self):
        self.perceptual = PerceptualSystem()
        self.dmn = DefaultModeNetwork()
        self.hippocampus = HippocampalMemorySystem()
        self.workspace = GlobalWorkspace()
        self.executive = PrefrontalExecutiveSystem()
        self.emotion = AmygdalaEmotionSystem()
        
        self.received_broadcasts = []
        
        def broadcast_receiver(content):
            self.received_broadcasts.append(content)
        
        self.workspace.register_module('test_receiver', broadcast_receiver)
    
    def test_full_processing_pipeline(self):
        """测试完整处理流程"""
        input_text = "帮我分析这个复杂的问题并制定解决方案"
        
        perceptual_result = self.perceptual.process(input_text)
        self.assertIsNotNone(perceptual_result)
        
        packet = InformationPacket(
            source='perceptual',
            content=perceptual_result,
            salience=perceptual_result.salience,
            modality='text'
        )
        self.workspace.submit(packet)
        
        conscious_content = self.workspace.process()
        self.assertIsNotNone(conscious_content)
        
        emotional_state = self.emotion.process_emotion(input_text)
        self.assertIsNotNone(emotional_state)
        
        memory_trace = self.hippocampus.encode(input_text)
        self.assertIsNotNone(memory_trace)
        
        decision = self.executive.control(input_text, goals=['分析', '解决'])
        self.assertIsNotNone(decision)
    
    def test_memory_consolidation_cycle(self):
        """测试记忆巩固周期"""
        experiences = [
            "学习新知识",
            "解决问题",
            "总结经验",
            "反思改进",
        ]
        
        for exp in experiences:
            self.hippocampus.encode(exp)
        
        consolidated = self.hippocampus.consolidate_memories(iterations=2)
        
        self.assertGreater(len(consolidated), 0)
    
    def test_emotion_cognition_interaction(self):
        """测试情绪-认知交互"""
        threat_stimulus = "紧急情况需要立即处理"
        
        emotional_state = self.emotion.process_emotion(threat_stimulus)
        
        decision = self.executive.control(
            threat_stimulus,
            goals=['快速响应', '安全处理']
        )
        
        self.assertIsNotNone(emotional_state)
        self.assertIsNotNone(decision)
        self.assertGreater(emotional_state.arousal, 0.5)
    
    def test_dmn_integration(self):
        """测试DMN整合"""
        self.dmn.run_idle_mode(iterations=2)
        
        external_input = "新的外部信息"
        result = self.dmn.integrate_external_input(external_input)
        
        self.assertIsNotNone(result)
        self.assertIn('merged_state', result)
        
        reflection = self.dmn.reflect()
        self.assertIsNotNone(reflection)


def run_brain_architecture_tests():
    """运行脑启发架构测试"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestPerceptualSystem))
    suite.addTests(loader.loadTestsFromTestCase(TestDefaultModeNetwork))
    suite.addTests(loader.loadTestsFromTestCase(TestHippocampalMemorySystem))
    suite.addTests(loader.loadTestsFromTestCase(TestGlobalWorkspace))
    suite.addTests(loader.loadTestsFromTestCase(TestPrefrontalExecutiveSystem))
    suite.addTests(loader.loadTestsFromTestCase(TestAmygdalaEmotionSystem))
    suite.addTests(loader.loadTestsFromTestCase(TestEventDrivenArchitecture))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegratedBrainSystem))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


if __name__ == '__main__':
    print("=" * 80)
    print("脑启发架构集成测试")
    print("=" * 80)
    print()
    
    result = run_brain_architecture_tests()
    
    print()
    print("=" * 80)
    print("测试结果总结")
    print("=" * 80)
    print(f"运行测试数: {result.testsRun}")
    print(f"成功: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"失败: {len(result.failures)}")
    print(f"错误: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("\n✓ 所有测试通过！脑启发架构功能正常。")
    else:
        print("\n✗ 部分测试失败，请检查错误信息。")
    
    print("=" * 80)
