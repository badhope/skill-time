"""
阶段3-5完整测试套件
测试感觉皮层、运动皮层、联合皮层、网络级别和系统级别模块
"""

import unittest
import numpy as np
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from random_agent.brain_inspired.sensory_cortex import (
    SensoryCortex, VisualCortex, AuditoryCortex, SomatosensoryCortex,
    PrimaryVisualCortex, SecondaryVisualCortex, VisualAreaV4, InferiorTemporalCortex,
    PrimaryAuditoryCortex, PrimarySomatosensoryCortex, MultisensoryIntegration,
    SensoryModality, VisualFeature, AuditoryFeature, SomatosensoryFeature
)

from random_agent.brain_inspired.motor_cortex import (
    MotorCortex, PrimaryMotorCortex, PremotorCortex, SupplementaryMotorArea,
    Cerebellum, BasalGangliaMotor, MovementType, MotorCommand, MotorPlan
)

from random_agent.brain_inspired.association_cortex import (
    AssociationCortex, DorsolateralPrefrontalCortex, VentromedialPrefrontalCortex,
    PosteriorParietalCortex, TemporalParietalJunction, WorkingMemory,
    ExecutiveControl, PlanningSystem, ValueSystem, Decision
)

from random_agent.brain_inspired.salience_network import (
    SalienceNetwork, AnteriorInsula, DorsalAnteriorCingulateCortex,
    NetworkSwitchController, SalienceType, SalienceSignal
)

from random_agent.brain_inspired.central_executive_network import (
    CentralExecutiveNetwork, DorsolateralPrefrontalNetwork, PosteriorParietalNetwork,
    ExecutiveControlSystem, ControlMode, AttentionFocus, GoalState
)

from random_agent.brain_inspired.consciousness import (
    ConsciousnessEmergence, GlobalWorkspace, ThalamocorticalSystem,
    IntegrationCenter, AttentionSchema, ConsciousnessLevel, ConsciousContent
)

from random_agent.brain_inspired.self_consciousness import (
    SelfConsciousnessSystem, MedialPrefrontalCortex, PosteriorCingulateCortex,
    Precuneus, SelfRepresentation, AutobiographicalMemory, ReflectionEngine,
    SelfAspect, SelfModel, SelfReflection
)

from random_agent.brain_inspired.intelligence_emergence import (
    IntelligenceEmergence, CognitiveFlexibility, ProblemSolvingEngine,
    LearningSystem, CreativityEngine, EmergenceDetector, IntelligenceType,
    CognitiveCapability, EmergentBehavior
)


class TestSensoryCortex(unittest.TestCase):
    """测试感觉皮层系统"""
    
    def setUp(self):
        """设置测试环境"""
        self.sensory_cortex = SensoryCortex()
        self.visual_cortex = VisualCortex()
        self.auditory_cortex = AuditoryCortex()
        self.somatosensory_cortex = SomatosensoryCortex()
    
    def test_visual_cortex_initialization(self):
        """测试视觉皮层初始化"""
        self.assertIsNotNone(self.visual_cortex.V1)
        self.assertIsNotNone(self.visual_cortex.V2)
        self.assertIsNotNone(self.visual_cortex.V4)
        self.assertIsNotNone(self.visual_cortex.IT)
    
    def test_visual_processing(self):
        """测试视觉处理"""
        visual_input = np.random.rand(100, 100)
        result = self.visual_cortex.process(visual_input, current_time=0.0)
        
        self.assertIsNotNone(result)
        self.assertEqual(result['modality'], 'visual')
        self.assertIn('v1_features', result)
        self.assertIn('v2_features', result)
        self.assertIn('v4_features', result)
        self.assertIn('objects', result)
    
    def test_auditory_processing(self):
        """测试听觉处理"""
        auditory_input = np.random.rand(1000)
        result = self.auditory_cortex.process(auditory_input, current_time=0.0)
        
        self.assertIsNotNone(result)
        self.assertEqual(result['modality'], 'auditory')
        self.assertIn('a1_features', result)
        self.assertIn('frequencies', result)
    
    def test_somatosensory_processing(self):
        """测试体感处理"""
        somatosensory_input = np.random.rand(100)
        result = self.somatosensory_cortex.process(somatosensory_input, current_time=0.0)
        
        self.assertIsNotNone(result)
        self.assertEqual(result['modality'], 'somatosensory')
        self.assertIn('s1_features', result)
        self.assertIn('touch', result)
    
    def test_multisensory_integration(self):
        """测试多感觉整合"""
        result = self.sensory_cortex.process(
            visual_input=np.random.rand(100, 100),
            auditory_input=np.random.rand(1000),
            somatosensory_input=np.random.rand(100),
            current_time=0.0
        )
        
        self.assertIsNotNone(result)
        self.assertIn('visual', result)
        self.assertIn('auditory', result)
        self.assertIn('somatosensory', result)
        self.assertIn('integrated', result)
    
    def test_v1_edge_detection(self):
        """测试V1边缘检测"""
        v1 = PrimaryVisualCortex()
        visual_input = np.random.rand(50, 50)
        edges = v1.extract_edges(visual_input)
        
        self.assertIsNotNone(edges)
        self.assertEqual(edges.shape, (50, 50))
    
    def test_v1_orientation_detection(self):
        """测试V1方向检测"""
        v1 = PrimaryVisualCortex()
        visual_input = np.random.rand(50, 50)
        orientations = v1.detect_orientation(visual_input)
        
        self.assertIsNotNone(orientations)
        self.assertIn('orientation_0', orientations)
        self.assertIn('orientation_45', orientations)
        self.assertIn('orientation_90', orientations)
        self.assertIn('orientation_135', orientations)


class TestMotorCortex(unittest.TestCase):
    """测试运动皮层系统"""
    
    def setUp(self):
        """设置测试环境"""
        self.motor_cortex = MotorCortex()
        self.primary_motor = PrimaryMotorCortex()
        self.premotor = PremotorCortex()
        self.sma = SupplementaryMotorArea()
        self.cerebellum = Cerebellum()
    
    def test_motor_cortex_initialization(self):
        """测试运动皮层初始化"""
        self.assertIsNotNone(self.motor_cortex.M1)
        self.assertIsNotNone(self.motor_cortex.PM)
        self.assertIsNotNone(self.motor_cortex.SMA)
        self.assertIsNotNone(self.motor_cortex.cerebellum)
        self.assertIsNotNone(self.motor_cortex.basal_ganglia)
    
    def test_motor_command_generation(self):
        """测试运动命令生成"""
        target = np.array([1.0, 0.5, 0.0])
        command = self.primary_motor.generate_motor_command(target, MovementType.REACHING)
        
        self.assertIsNotNone(command)
        self.assertEqual(command.movement_type, MovementType.REACHING)
        self.assertIsNotNone(command.velocity)
        self.assertIsNotNone(command.force)
    
    def test_movement_planning(self):
        """测试运动规划"""
        plan = self.motor_cortex.plan_movement('pick_up', context={})
        
        self.assertIsNotNone(plan)
        self.assertIsInstance(plan, MotorPlan)
        self.assertGreater(len(plan.sequence), 0)
    
    def test_movement_execution(self):
        """测试运动执行"""
        plan = self.motor_cortex.plan_movement('point', context={})
        results = self.motor_cortex.execute_plan(plan, current_time=0.0)
        
        self.assertIsNotNone(results)
        self.assertGreater(len(results), 0)
        for result in results:
            self.assertIn('status', result)
    
    def test_cerebellum_coordination(self):
        """测试小脑协调"""
        command = MotorCommand(
            movement_type=MovementType.REACHING,
            target_position=np.array([1.0, 0.0, 0.0]),
            velocity=np.array([0.5, 0.0, 0.0]),
            force=np.array([0.3, 0.0, 0.0])
        )
        
        coordinated = self.cerebellum.coordinate_movement(command)
        
        self.assertIsNotNone(coordinated)
        self.assertEqual(coordinated.movement_type, MovementType.REACHING)
    
    def test_premotor_sequence_planning(self):
        """测试前运动皮层序列规划"""
        sequence = self.premotor.plan_movement_sequence('pick_up')
        
        self.assertIsNotNone(sequence)
        self.assertGreater(len(sequence), 0)
        for cmd in sequence:
            self.assertIsInstance(cmd, MotorCommand)


class TestAssociationCortex(unittest.TestCase):
    """测试联合皮层系统"""
    
    def setUp(self):
        """设置测试环境"""
        self.association_cortex = AssociationCortex()
        self.dlpfc = DorsolateralPrefrontalCortex()
        self.vmpfc = VentromedialPrefrontalCortex()
        self.ppc = PosteriorParietalCortex()
    
    def test_association_cortex_initialization(self):
        """测试联合皮层初始化"""
        self.assertIsNotNone(self.association_cortex.dlPFC)
        self.assertIsNotNone(self.association_cortex.vmPFC)
        self.assertIsNotNone(self.association_cortex.PPC)
        self.assertIsNotNone(self.association_cortex.TPJ)
    
    def test_working_memory(self):
        """测试工作记忆"""
        wm = WorkingMemory(capacity=5)
        
        wm.store('item1', 0.8, 0.0)
        wm.store('item2', 0.6, 0.0)
        
        state = wm.get_state()
        self.assertEqual(state['n_items'], 2)
        self.assertEqual(state['capacity'], 5)
    
    def test_decision_making(self):
        """测试决策制定"""
        options = ['option1', 'option2', 'option3']
        decision = self.vmpfc.make_value_based_decision(options, context={'reward': 0.8})
        
        self.assertIsNotNone(decision)
        self.assertIn(decision.selected, options)
        self.assertGreater(decision.confidence, 0)
    
    def test_planning(self):
        """测试规划"""
        plan = self.dlpfc.plan('solve_problem', constraints={'time': 10})
        
        self.assertIsNotNone(plan)
        self.assertGreater(len(plan), 0)
    
    def test_spatial_processing(self):
        """测试空间处理"""
        input_data = {
            'spatial_targets': [(0.0, 0.0), (1.0, 1.0)]
        }
        result = self.ppc.process(input_data, current_time=0.0)
        
        self.assertIsNotNone(result)
        self.assertIn('spatial_representation', result)
        self.assertIn('attention_allocation', result)
    
    def test_full_processing(self):
        """测试完整处理流程"""
        input_data = {
            'to_remember': 'important_info',
            'salience': 0.8,
            'options': ['A', 'B', 'C'],
            'goal': 'test_goal'
        }
        
        result = self.association_cortex.process(input_data, current_time=0.0)
        
        self.assertIsNotNone(result)
        self.assertIn('dlPFC', result)
        self.assertIn('PPC', result)
        self.assertIn('TPJ', result)


class TestSalienceNetwork(unittest.TestCase):
    """测试突显网络系统"""
    
    def setUp(self):
        """设置测试环境"""
        self.salience_network = SalienceNetwork()
        self.ai = AnteriorInsula()
        self.dacc = DorsalAnteriorCingulateCortex()
    
    def test_salience_network_initialization(self):
        """测试突显网络初始化"""
        self.assertIsNotNone(self.salience_network.AI)
        self.assertIsNotNone(self.salience_network.dACC)
        self.assertIsNotNone(self.salience_network.switch_controller)
    
    def test_interoceptive_salience(self):
        """测试内感受显著性"""
        interoceptive_input = {
            'heartbeat': 0.7,
            'respiration': 0.5,
            'hunger': 0.3
        }
        
        signal = self.ai.detect_interoceptive_salience(interoceptive_input)
        
        self.assertIsNotNone(signal)
        self.assertEqual(signal.salience_type, SalienceType.INTEROCEPTIVE)
        self.assertGreaterEqual(signal.intensity, 0)
        self.assertLessEqual(signal.intensity, 1)
    
    def test_cognitive_salience(self):
        """测试认知显著性"""
        cognitive_input = {
            'novelty': 0.8,
            'relevance': 0.7,
            'urgency': 0.6
        }
        
        signal = self.dacc.detect_cognitive_salience(cognitive_input)
        
        self.assertIsNotNone(signal)
        self.assertEqual(signal.salience_type, SalienceType.COGNITIVE)
    
    def test_network_switching(self):
        """测试网络切换"""
        input_data = {
            'interoceptive': {'heartbeat': 0.8},
            'cognitive': {'novelty': 0.9}
        }
        
        result = self.salience_network.process(input_data, current_time=0.0)
        
        self.assertIsNotNone(result)
        self.assertIn('total_salience', result)
        self.assertIn('active_network', result)
    
    def test_switch_controller(self):
        """测试切换控制器"""
        controller = NetworkSwitchController()
        
        initial_network = controller.get_current_network()
        self.assertEqual(initial_network, 'DMN')
        
        controller.switch_to_CEN()
        current_network = controller.get_current_network()
        self.assertEqual(current_network, 'CEN')


class TestCentralExecutiveNetwork(unittest.TestCase):
    """测试中央执行网络系统"""
    
    def setUp(self):
        """设置测试环境"""
        self.cen = CentralExecutiveNetwork()
        self.dlpfc_network = DorsolateralPrefrontalNetwork()
        self.pp_network = PosteriorParietalNetwork()
    
    def test_cen_initialization(self):
        """测试中央执行网络初始化"""
        self.assertIsNotNone(self.cen.dlPFC_network)
        self.assertIsNotNone(self.cen.PP_network)
        self.assertIsNotNone(self.cen.executive_control)
    
    def test_attention_control(self):
        """测试注意控制"""
        result = self.cen.control_attention('target1', ControlMode.SELECTIVE, current_time=0.0)
        
        self.assertIsNotNone(result)
        self.assertIn('attention_control', result)
    
    def test_goal_management(self):
        """测试目标管理"""
        self.cen.set_goal('test_goal', priority=0.8, current_time=0.0)
        
        result = self.cen.process({}, current_time=0.0)
        
        self.assertIsNotNone(result)
    
    def test_inhibitory_control(self):
        """测试抑制控制"""
        self.cen.inhibit_distraction('distraction1', strength=0.7, current_time=0.0)
        
        result = self.cen.process({}, current_time=0.0)
        self.assertIsNotNone(result)
    
    def test_task_switching(self):
        """测试任务切换"""
        success = self.cen.switch_task('new_task', current_time=0.0)
        
        self.assertTrue(success)


class TestConsciousnessEmergence(unittest.TestCase):
    """测试意识涌现系统"""
    
    def setUp(self):
        """设置测试环境"""
        self.consciousness = ConsciousnessEmergence()
        self.global_workspace = GlobalWorkspace()
        self.thalamocortical = ThalamocorticalSystem()
    
    def test_consciousness_initialization(self):
        """测试意识系统初始化"""
        self.assertIsNotNone(self.consciousness.global_workspace)
        self.assertIsNotNone(self.consciousness.thalamocortical)
        self.assertIsNotNone(self.consciousness.integration_center)
        self.assertIsNotNone(self.consciousness.attention_schema)
    
    def test_global_workspace_broadcast(self):
        """测试全局工作空间广播"""
        success = self.global_workspace.broadcast('test_content', 0.8, current_time=0.0)
        
        self.assertTrue(success)
    
    def test_global_workspace_access(self):
        """测试全局工作空间访问"""
        self.global_workspace.broadcast('content1', 0.7, current_time=0.0)
        self.global_workspace.broadcast('content2', 0.9, current_time=0.0)
        
        accessed = self.global_workspace.access()
        
        self.assertIsNotNone(accessed)
        self.assertEqual(accessed.content, 'content2')
    
    def test_consciousness_level(self):
        """测试意识水平"""
        level = self.consciousness.get_consciousness_level()
        
        self.assertIn(level, [
            ConsciousnessLevel.UNCONSCIOUS,
            ConsciousnessLevel.PRECONSCIOUS,
            ConsciousnessLevel.CONSCIOUS,
            ConsciousnessLevel.SELF_CONSCIOUS
        ])
    
    def test_consciousness_processing(self):
        """测试意识处理"""
        input_data = {
            'content': 'test_content',
            'salience': 0.8,
            'arousal': 0.7
        }
        
        result = self.consciousness.process(input_data, current_time=0.0)
        
        self.assertIsNotNone(result)
        self.assertIn('consciousness_level', result)
        self.assertIn('workspace_state', result)
        self.assertIn('phi', result)
    
    def test_thalamocortical_gating(self):
        """测试丘脑皮层门控"""
        self.thalamocortical.regulate_arousal(0.8)
        
        gated = self.thalamocortical.gate_information('info', 0.7)
        
        self.assertTrue(gated)


class TestSelfConsciousness(unittest.TestCase):
    """测试自我意识系统"""
    
    def setUp(self):
        """设置测试环境"""
        self.self_consciousness = SelfConsciousnessSystem()
        self.mpfc = MedialPrefrontalCortex()
        self.pcc = PosteriorCingulateCortex()
        self.precuneus = Precuneus()
    
    def test_self_consciousness_initialization(self):
        """测试自我意识系统初始化"""
        self.assertIsNotNone(self.self_consciousness.mPFC)
        self.assertIsNotNone(self.self_consciousness.PCC)
        self.assertIsNotNone(self.self_consciousness.precuneus)
    
    def test_self_reference_processing(self):
        """测试自我参照处理"""
        result = self.mpfc.process({'information': '这是关于我的信息'}, current_time=0.0)
        
        self.assertIsNotNone(result)
        self.assertIn('self_relevance', result)
    
    def test_autobiographical_memory(self):
        """测试自传体记忆"""
        memory = AutobiographicalMemory()
        
        memory.store('experience1', 0.7)
        memory.store('experience2', 0.8)
        
        retrieved = memory.retrieve('experience')
        
        self.assertIsNotNone(retrieved)
        self.assertGreater(len(retrieved), 0)
    
    def test_self_reflection(self):
        """测试自我反思"""
        reflection = self.pcc.reflect('我的行为', current_time=0.0)
        
        self.assertIsNotNone(reflection)
        self.assertIsInstance(reflection, SelfReflection)
        self.assertIn(reflection.aspect, [
            SelfAspect.PHYSICAL,
            SelfAspect.PSYCHOLOGICAL,
            SelfAspect.SOCIAL,
            SelfAspect.NARRATIVE,
            SelfAspect.EXTENDED
        ])
    
    def test_mental_simulation(self):
        """测试心理模拟"""
        simulation = self.precuneus.simulate_scenario('未来情境')
        
        self.assertIsNotNone(simulation)
        self.assertIn('outcomes', simulation)
    
    def test_perspective_taking(self):
        """测试视角采取"""
        perspective = self.precuneus.take_perspective('situation', 'other')
        
        self.assertIsNotNone(perspective)
        self.assertEqual(perspective['perspective'], 'other')


class TestIntelligenceEmergence(unittest.TestCase):
    """测试智能涌现系统"""
    
    def setUp(self):
        """设置测试环境"""
        self.intelligence = IntelligenceEmergence()
        self.cognitive_flexibility = CognitiveFlexibility()
        self.problem_solving = ProblemSolvingEngine()
        self.learning_system = LearningSystem()
        self.creativity_engine = CreativityEngine()
    
    def test_intelligence_initialization(self):
        """测试智能系统初始化"""
        self.assertIsNotNone(self.intelligence.cognitive_flexibility)
        self.assertIsNotNone(self.intelligence.problem_solving)
        self.assertIsNotNone(self.intelligence.learning_system)
        self.assertIsNotNone(self.intelligence.creativity_engine)
        self.assertIsNotNone(self.intelligence.emergence_detector)
    
    def test_problem_solving(self):
        """测试问题解决"""
        problem = {
            'type': 'analytical',
            'complexity': 0.6
        }
        
        result = self.problem_solving.solve(problem, current_time=0.0)
        
        self.assertIsNotNone(result)
        self.assertIn('strategy', result)
        self.assertIn('success', result)
    
    def test_learning(self):
        """测试学习"""
        experience = {
            'success': True,
            'strategy': 'trial_and_error',
            'skill_type': 'problem_solving'
        }
        
        result = self.learning_system.learn(experience, current_time=0.0)
        
        self.assertIsNotNone(result)
        self.assertIn('insight', result)
        self.assertIn('experience_count', result)
    
    def test_creativity(self):
        """测试创造力"""
        problem = {'type': 'creative', 'description': '设计新方案'}
        
        result = self.creativity_engine.creative_problem_solving(problem)
        
        self.assertIsNotNone(result)
        self.assertIn('ideas', result)
        self.assertIn('creativity_score', result)
    
    def test_cognitive_flexibility(self):
        """测试认知灵活性"""
        context = {'problem_type': 'analytical'}
        
        strategy = self.cognitive_flexibility.adapt_to_context(context)
        
        self.assertIsNotNone(strategy)
    
    def test_emergence_detection(self):
        """测试涌现检测"""
        system_state = {
            'n_components': 5,
            'n_interactions': 10,
            'adaptiveness': 0.8,
            'novelty': 0.7
        }
        
        behavior = self.intelligence.emergence_detector.detect(system_state)
        
        self.assertIsNotNone(behavior)
        self.assertIsInstance(behavior, EmergentBehavior)
    
    def test_full_intelligence_processing(self):
        """测试完整智能处理"""
        input_data = {
            'problem': {'type': 'analytical', 'complexity': 0.7},
            'experience': {'success': True, 'strategy': 'test'},
            'creative_task': {'type': 'creative'}
        }
        
        result = self.intelligence.process(input_data, current_time=0.0)
        
        self.assertIsNotNone(result)
        self.assertIn('problem_solving', result)
        self.assertIn('learning', result)
        self.assertIn('creativity', result)
        self.assertIn('intelligence_level', result)


class TestIntegration(unittest.TestCase):
    """测试系统集成"""
    
    def test_full_system_integration(self):
        """测试完整系统集成"""
        sensory = SensoryCortex()
        motor = MotorCortex()
        association = AssociationCortex()
        salience = SalienceNetwork()
        cen = CentralExecutiveNetwork()
        consciousness = ConsciousnessEmergence()
        self_consciousness = SelfConsciousnessSystem()
        intelligence = IntelligenceEmergence()
        
        visual_input = np.random.rand(50, 50)
        sensory_result = sensory.process(visual_input=visual_input, current_time=0.0)
        
        salience_input = {
            'interoceptive': {'heartbeat': 0.6},
            'cognitive': {'novelty': 0.7}
        }
        salience_result = salience.process(salience_input, current_time=0.0)
        
        consciousness_input = {
            'content': sensory_result,
            'salience': salience_result['total_salience']
        }
        consciousness_result = consciousness.process(consciousness_input, current_time=0.0)
        
        association_input = {
            'to_remember': sensory_result,
            'goal': 'process_sensory'
        }
        association_result = association.process(association_input, current_time=0.0)
        
        motor_result = motor.process('reach', context={'target': sensory_result}, current_time=0.0)
        
        self_consciousness_result = self_consciousness.process(
            {'information': 'processing sensory input'},
            current_time=0.0
        )
        
        intelligence_result = intelligence.process(
            {
                'problem': {'type': 'sensory_processing'},
                'experience': {'success': True}
            },
            current_time=0.0
        )
        
        self.assertIsNotNone(sensory_result)
        self.assertIsNotNone(salience_result)
        self.assertIsNotNone(consciousness_result)
        self.assertIsNotNone(association_result)
        self.assertIsNotNone(motor_result)
        self.assertIsNotNone(self_consciousness_result)
        self.assertIsNotNone(intelligence_result)


if __name__ == '__main__':
    unittest.main(verbosity=2)
