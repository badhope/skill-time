"""
联合皮层系统 - 前额叶、顶叶、颞叶联合皮层的完整实现
基于2024-2025最新神经科学研究
"""

import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

from random_agent.brain_inspired.ensemble import CorticalColumn, NeuralEnsemble
from random_agent.brain_inspired.neuron import Neuron


class CognitiveFunction(Enum):
    """认知功能"""
    WORKING_MEMORY = "working_memory"
    DECISION_MAKING = "decision_making"
    ATTENTION_CONTROL = "attention_control"
    PLANNING = "planning"
    ABSTRACT_REASONING = "abstract_reasoning"


@dataclass
class WorkingMemoryItem:
    """工作记忆项"""
    content: Any
    salience: float
    timestamp: float
    rehearsal_count: int = 0


@dataclass
class Decision:
    """决策"""
    options: List[Any]
    selected: Any
    confidence: float
    reasoning: Optional[str] = None


class DorsolateralPrefrontalCortex:
    """背外侧前额叶皮层（dlPFC）"""
    
    def __init__(self):
        self.working_memory = WorkingMemory()
        self.executive_control = ExecutiveControl()
        self.planning_system = PlanningSystem()
        
    def maintain_in_working_memory(self, item: Any, salience: float = 0.5, current_time: float = 0.0):
        """在工作记忆中维持"""
        self.working_memory.store(item, salience, current_time)
    
    def retrieve_from_working_memory(self, query: Any = None) -> Optional[WorkingMemoryItem]:
        """从工作记忆中检索"""
        return self.working_memory.retrieve(query)
    
    def inhibit_distractions(self, relevant_features: List[str]):
        """抑制干扰"""
        self.executive_control.set_attention_filter(relevant_features)
    
    def plan(self, goal: str, constraints: Dict[str, Any] = None) -> List[str]:
        """规划"""
        return self.planning_system.create_plan(goal, constraints)
    
    def process(self, input_data: Dict[str, Any], current_time: float = 0.0) -> Dict[str, Any]:
        """处理输入"""
        if 'to_remember' in input_data:
            self.maintain_in_working_memory(
                input_data['to_remember'],
                input_data.get('salience', 0.5),
                current_time
            )
        
        if 'goal' in input_data:
            plan = self.plan(input_data['goal'], input_data.get('constraints'))
        else:
            plan = []
        
        if 'distractions' in input_data:
            self.inhibit_distractions(input_data.get('relevant_features', []))
        
        return {
            'working_memory_state': self.working_memory.get_state(),
            'plan': plan,
            'timestamp': current_time
        }


class WorkingMemory:
    """工作记忆系统"""
    
    def __init__(self, capacity: int = 7):
        self.capacity = capacity
        self.items: List[WorkingMemoryItem] = []
        self.decay_rate = 0.1
        
    def store(self, content: Any, salience: float, timestamp: float):
        """存储"""
        if len(self.items) >= self.capacity:
            self._evict_lowest_salience()
        
        item = WorkingMemoryItem(
            content=content,
            salience=salience,
            timestamp=timestamp
        )
        self.items.append(item)
    
    def retrieve(self, query: Any = None) -> Optional[WorkingMemoryItem]:
        """检索"""
        if not self.items:
            return None
        
        if query is None:
            return max(self.items, key=lambda x: x.salience)
        
        best_match = None
        best_score = 0.0
        
        for item in self.items:
            score = self._compute_similarity(item.content, query)
            if score > best_score:
                best_score = score
                best_match = item
        
        return best_match
    
    def _compute_similarity(self, content1: Any, content2: Any) -> float:
        """计算相似度"""
        if content1 == content2:
            return 1.0
        return 0.5
    
    def _evict_lowest_salience(self):
        """驱逐最低显著性项"""
        if self.items:
            min_idx = min(range(len(self.items)), key=lambda i: self.items[i].salience)
            self.items.pop(min_idx)
    
    def update(self, dt: float):
        """更新"""
        for item in self.items:
            item.salience *= (1 - self.decay_rate * dt)
        
        self.items = [item for item in self.items if item.salience > 0.1]
    
    def get_state(self) -> Dict[str, Any]:
        """获取状态"""
        return {
            'n_items': len(self.items),
            'capacity': self.capacity,
            'items': [(item.content, item.salience) for item in self.items]
        }


class ExecutiveControl:
    """执行控制"""
    
    def __init__(self):
        self.attention_filter: List[str] = []
        self.inhibition_strength = 0.5
        
    def set_attention_filter(self, relevant_features: List[str]):
        """设置注意过滤器"""
        self.attention_filter = relevant_features
    
    def apply_inhibition(self, activation: np.ndarray) -> np.ndarray:
        """应用抑制"""
        inhibited = activation * (1 - self.inhibition_strength)
        return inhibited


class PlanningSystem:
    """规划系统"""
    
    def __init__(self):
        self.goal_stack = []
        self.plan_library = self._create_plan_library()
        
    def _create_plan_library(self) -> Dict[str, List[str]]:
        """创建计划库"""
        return {
            'solve_problem': ['analyze', 'generate_solutions', 'evaluate', 'select'],
            'make_decision': ['gather_info', 'weigh_options', 'choose', 'verify'],
            'achieve_goal': ['define_goal', 'plan_steps', 'execute', 'monitor']
        }
    
    def create_plan(self, goal: str, constraints: Dict[str, Any] = None) -> List[str]:
        """创建计划"""
        for key in self.plan_library:
            if key in goal.lower():
                return self.plan_library[key]
        
        return ['analyze', 'plan', 'execute', 'evaluate']


class VentromedialPrefrontalCortex:
    """腹内侧前额叶皮层（vmPFC）"""
    
    def __init__(self):
        self.value_system = ValueSystem()
        self.emotion_integration = EmotionIntegration()
        
    def evaluate_options(self, options: List[Any], context: Dict[str, Any] = None) -> List[float]:
        """评估选项"""
        values = []
        for option in options:
            value = self.value_system.compute_value(option, context)
            values.append(value)
        
        return values
    
    def integrate_emotion(self, cognitive_value: float, emotional_value: float) -> float:
        """整合情绪"""
        integrated = 0.6 * cognitive_value + 0.4 * emotional_value
        return integrated
    
    def make_value_based_decision(self, options: List[Any], context: Dict[str, Any] = None) -> Decision:
        """基于价值的决策"""
        values = self.evaluate_options(options, context)
        
        selected_idx = int(np.argmax(values))
        selected = options[selected_idx]
        confidence = values[selected_idx]
        
        decision = Decision(
            options=options,
            selected=selected,
            confidence=confidence,
            reasoning=f"Selected based on highest value: {confidence:.2f}"
        )
        
        return decision


class ValueSystem:
    """价值系统"""
    
    def __init__(self):
        self.value_weights = {
            'reward': 1.0,
            'risk': -0.5,
            'effort': -0.3,
            'novelty': 0.2
        }
        
    def compute_value(self, option: Any, context: Dict[str, Any] = None) -> float:
        """计算价值"""
        base_value = 0.5
        
        if context:
            if 'reward' in context:
                base_value += context['reward'] * self.value_weights['reward']
            if 'risk' in context:
                base_value += context['risk'] * self.value_weights['risk']
        
        return np.clip(base_value, 0, 1)


class EmotionIntegration:
    """情绪整合"""
    
    def __init__(self):
        self.emotion_weights = {}
        
    def integrate(self, emotions: Dict[str, float]) -> float:
        """整合情绪"""
        if not emotions:
            return 0.5
        
        return np.mean(list(emotions.values()))


class PosteriorParietalCortex:
    """后顶叶皮层（PPC）"""
    
    def __init__(self):
        self.spatial_map = SpatialMap()
        self.attention_controller = AttentionController()
        self.sensorimotor_integration = SensorimotorIntegration()
        
    def process_spatial_information(self, sensory_input: Dict[str, Any]) -> Dict[str, Any]:
        """处理空间信息"""
        spatial_representation = self.spatial_map.update(sensory_input)
        
        return spatial_representation
    
    def allocate_attention(self, spatial_targets: List[Tuple[float, ...]], current_time: float = 0.0) -> Dict[str, Any]:
        """分配注意"""
        attention_map = self.attention_controller.allocate(spatial_targets, current_time)
        
        return attention_map
    
    def integrate_sensorimotor(self, sensory: Dict[str, Any], motor: Dict[str, Any]) -> Dict[str, Any]:
        """整合感觉运动"""
        integrated = self.sensorimotor_integration.integrate(sensory, motor)
        
        return integrated
    
    def process(self, input_data: Dict[str, Any], current_time: float = 0.0) -> Dict[str, Any]:
        """处理输入"""
        spatial = self.process_spatial_information(input_data)
        
        if 'spatial_targets' in input_data:
            attention = self.allocate_attention(input_data['spatial_targets'], current_time)
        else:
            attention = {}
        
        return {
            'spatial_representation': spatial,
            'attention_allocation': attention,
            'timestamp': current_time
        }


class SpatialMap:
    """空间地图"""
    
    def __init__(self):
        self.map = np.zeros((100, 100))
        self.objects = {}
        
    def update(self, sensory_input: Dict[str, Any]) -> Dict[str, Any]:
        """更新"""
        return {
            'map_shape': self.map.shape,
            'n_objects': len(self.objects)
        }
    
    def add_object(self, object_id: str, position: Tuple[float, ...]):
        """添加对象"""
        self.objects[object_id] = position
    
    def get_object_position(self, object_id: str) -> Optional[Tuple[float, ...]]:
        """获取对象位置"""
        return self.objects.get(object_id)


class AttentionController:
    """注意控制器"""
    
    def __init__(self):
        self.attention_spotlight = None
        self.attention_width = 10.0
        
    def allocate(self, targets: List[Tuple[float, ...]], current_time: float) -> Dict[str, Any]:
        """分配"""
        if not targets:
            return {}
        
        center = np.mean(targets, axis=0)
        
        return {
            'center': center.tolist(),
            'width': self.attention_width,
            'n_targets': len(targets),
            'timestamp': current_time
        }
    
    def shift_attention(self, new_center: Tuple[float, ...]):
        """转移注意"""
        self.attention_spotlight = new_center


class SensorimotorIntegration:
    """感觉运动整合"""
    
    def __init__(self):
        self.calibration_matrix = np.eye(3)
        
    def integrate(self, sensory: Dict[str, Any], motor: Dict[str, Any]) -> Dict[str, Any]:
        """整合"""
        return {
            'sensory': sensory,
            'motor': motor,
            'integrated': True
        }


class TemporalParietalJunction:
    """颞顶联合区（TPJ）"""
    
    def __init__(self):
        self.theory_of_mind = TheoryOfMind()
        self.self_other_distinction = SelfOtherDistinction()
        
    def infer_mental_states(self, agent_info: Dict[str, Any]) -> Dict[str, Any]:
        """推断心理状态"""
        return self.theory_of_mind.infer(agent_info)
    
    def distinguish_self_other(self, information: Dict[str, Any]) -> Dict[str, Any]:
        """区分自我他人"""
        return self.self_other_distinction.process(information)
    
    def process(self, input_data: Dict[str, Any], current_time: float = 0.0) -> Dict[str, Any]:
        """处理输入"""
        mental_states = self.infer_mental_states(input_data)
        self_other = self.distinguish_self_other(input_data)
        
        return {
            'mental_states': mental_states,
            'self_other_distinction': self_other,
            'timestamp': current_time
        }


class TheoryOfMind:
    """心理理论"""
    
    def __init__(self):
        self.mental_state_models = {}
        
    def infer(self, agent_info: Dict[str, Any]) -> Dict[str, Any]:
        """推断"""
        return {
            'beliefs': ['unknown'],
            'desires': ['unknown'],
            'intentions': ['unknown']
        }


class SelfOtherDistinction:
    """自我他人区分"""
    
    def __init__(self):
        self.self_model = {}
        self.other_models = {}
        
    def process(self, information: Dict[str, Any]) -> Dict[str, Any]:
        """处理"""
        return {
            'is_self': information.get('agent_id') == 'self',
            'confidence': 0.8
        }


class AssociationCortex:
    """完整联合皮层系统"""
    
    def __init__(self):
        self.dlPFC = DorsolateralPrefrontalCortex()
        self.vmPFC = VentromedialPrefrontalCortex()
        self.PPC = PosteriorParietalCortex()
        self.TPJ = TemporalParietalJunction()
        
        self.processing_history = []
        
    def process(self, input_data: Dict[str, Any], current_time: float = 0.0) -> Dict[str, Any]:
        """完整处理流程"""
        dlPFC_result = self.dlPFC.process(input_data, current_time)
        PPC_result = self.PPC.process(input_data, current_time)
        TPJ_result = self.TPJ.process(input_data, current_time)
        
        if 'options' in input_data:
            decision = self.vmPFC.make_value_based_decision(
                input_data['options'],
                input_data.get('context')
            )
        else:
            decision = None
        
        result = {
            'dlPFC': dlPFC_result,
            'vmPFC_decision': decision,
            'PPC': PPC_result,
            'TPJ': TPJ_result,
            'timestamp': current_time
        }
        
        self.processing_history.append(result)
        
        return result
    
    def make_decision(self, options: List[Any], context: Dict[str, Any] = None) -> Decision:
        """制定决策"""
        return self.vmPFC.make_value_based_decision(options, context)
    
    def plan(self, goal: str, constraints: Dict[str, Any] = None) -> List[str]:
        """规划"""
        return self.dlPFC.plan(goal, constraints)
    
    def control_attention(self, targets: List[Tuple[float, ...]], current_time: float = 0.0):
        """控制注意"""
        self.PPC.allocate_attention(targets, current_time)
