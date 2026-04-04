"""
自我意识系统 - 自我模型和自我反思
基于2024-2025最新神经科学研究
"""

import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime

from random_agent.brain_inspired.ensemble import NeuralEnsemble
from random_agent.brain_inspired.neuron import Neuron


class SelfAspect(Enum):
    """自我方面"""
    PHYSICAL = "physical"
    PSYCHOLOGICAL = "psychological"
    SOCIAL = "social"
    NARRATIVE = "narrative"
    EXTENDED = "extended"


@dataclass
class SelfModel:
    """自我模型"""
    identity: str
    traits: Dict[str, float]
    values: List[str]
    goals: List[str]
    beliefs: Dict[str, Any]
    autobiographical_memories: List[Any]
    coherence: float


@dataclass
class SelfReflection:
    """自我反思"""
    aspect: SelfAspect
    insight: str
    confidence: float
    emotional_valence: float
    timestamp: float


class MedialPrefrontalCortex:
    """内侧前额叶皮层（mPFC）- 自我参照处理"""
    
    def __init__(self):
        self.self_representation = SelfRepresentation()
        self.self_reference_processor = SelfReferenceProcessor()
        
    def process_self_reference(self, information: Any) -> float:
        """处理自我参照"""
        return self.self_reference_processor.compute_relevance(information)
    
    def update_self_model(self, new_information: Dict[str, Any]):
        """更新自我模型"""
        self.self_representation.update(new_information)
    
    def retrieve_self_knowledge(self, query: str) -> Any:
        """检索自我知识"""
        return self.self_representation.retrieve(query)
    
    def process(self, input_data: Dict[str, Any], current_time: float = 0.0) -> Dict[str, Any]:
        """处理输入"""
        self_relevance = 0.0
        if 'information' in input_data:
            self_relevance = self.process_self_reference(input_data['information'])
        
        if 'self_update' in input_data:
            self.update_self_model(input_data['self_update'])
        
        return {
            'self_relevance': self_relevance,
            'self_model_state': self.self_representation.get_state(),
            'timestamp': current_time
        }


class SelfRepresentation:
    """自我表征"""
    
    def __init__(self):
        self.traits = {
            'openness': 0.5,
            'conscientiousness': 0.5,
            'extraversion': 0.5,
            'agreeableness': 0.5,
            'neuroticism': 0.5
        }
        self.values = ['knowledge', 'growth', 'creativity']
        self.goals = []
        self.beliefs = {}
        
    def update(self, new_information: Dict[str, Any]):
        """更新"""
        if 'traits' in new_information:
            for trait, value in new_information['traits'].items():
                if trait in self.traits:
                    self.traits[trait] = 0.9 * self.traits[trait] + 0.1 * value
        
        if 'values' in new_information:
            self.values.extend(new_information['values'])
            self.values = list(set(self.values))[:10]
        
        if 'goals' in new_information:
            self.goals.extend(new_information['goals'])
            self.goals = self.goals[-10:]
        
        if 'beliefs' in new_information:
            self.beliefs.update(new_information['beliefs'])
    
    def retrieve(self, query: str) -> Any:
        """检索"""
        if query in self.traits:
            return self.traits[query]
        if query in self.beliefs:
            return self.beliefs[query]
        return None
    
    def get_state(self) -> Dict[str, Any]:
        """获取状态"""
        return {
            'traits': self.traits.copy(),
            'n_values': len(self.values),
            'n_goals': len(self.goals),
            'n_beliefs': len(self.beliefs)
        }


class SelfReferenceProcessor:
    """自我参照处理器"""
    
    def __init__(self):
        self.self_keywords = ['我', '我的', '自己', 'self', 'me', 'my']
        
    def compute_relevance(self, information: Any) -> float:
        """计算自我相关性"""
        if isinstance(information, str):
            for keyword in self.self_keywords:
                if keyword in information.lower():
                    return 0.8
            return 0.3
        
        return 0.5


class PosteriorCingulateCortex:
    """后扣带回皮层（PCC）- 自我反思和记忆整合"""
    
    def __init__(self):
        self.autobiographical_memory = AutobiographicalMemory()
        self.reflection_engine = ReflectionEngine()
        
    def retrieve_autobiographical_memory(self, cue: Any) -> List[Any]:
        """检索自传体记忆"""
        return self.autobiographical_memory.retrieve(cue)
    
    def reflect(self, topic: str, current_time: float = 0.0) -> SelfReflection:
        """反思"""
        return self.reflection_engine.reflect(topic, current_time)
    
    def integrate_memory(self, experience: Any, emotional_valence: float):
        """整合记忆"""
        self.autobiographical_memory.store(experience, emotional_valence)
    
    def process(self, input_data: Dict[str, Any], current_time: float = 0.0) -> Dict[str, Any]:
        """处理输入"""
        memories = []
        if 'memory_cue' in input_data:
            memories = self.retrieve_autobiographical_memory(input_data['memory_cue'])
        
        reflection = None
        if 'reflection_topic' in input_data:
            reflection = self.reflect(input_data['reflection_topic'], current_time)
        
        if 'experience' in input_data:
            self.integrate_memory(
                input_data['experience'],
                input_data.get('emotional_valence', 0.5)
            )
        
        return {
            'retrieved_memories': memories,
            'reflection': reflection,
            'memory_state': self.autobiographical_memory.get_state(),
            'timestamp': current_time
        }


class AutobiographicalMemory:
    """自传体记忆"""
    
    def __init__(self, capacity: int = 100):
        self.capacity = capacity
        self.memories: List[Tuple[Any, float, float]] = []
        
    def store(self, experience: Any, emotional_valence: float):
        """存储"""
        timestamp = datetime.now().timestamp()
        
        self.memories.append((experience, emotional_valence, timestamp))
        
        if len(self.memories) > self.capacity:
            self.memories.pop(0)
    
    def retrieve(self, cue: Any) -> List[Any]:
        """检索"""
        if not self.memories:
            return []
        
        relevant = []
        for experience, valence, timestamp in self.memories:
            relevance = self._compute_relevance(experience, cue)
            if relevance > 0.3:
                relevant.append({
                    'experience': experience,
                    'emotional_valence': valence,
                    'relevance': relevance
                })
        
        relevant.sort(key=lambda x: x['relevance'], reverse=True)
        
        return relevant[:5]
    
    def _compute_relevance(self, experience: Any, cue: Any) -> float:
        """计算相关性"""
        if experience == cue:
            return 1.0
        
        if isinstance(experience, str) and isinstance(cue, str):
            if cue.lower() in experience.lower():
                return 0.7
        
        return 0.3
    
    def get_state(self) -> Dict[str, Any]:
        """获取状态"""
        return {
            'n_memories': len(self.memories),
            'capacity': self.capacity
        }


class ReflectionEngine:
    """反思引擎"""
    
    def __init__(self):
        self.reflection_patterns = {
            'behavior': ['我为什么这样做？', '这符合我的价值观吗？'],
            'emotion': ['我为什么会有这种感觉？', '这种感觉意味着什么？'],
            'thought': ['这个想法合理吗？', '有没有其他角度？'],
            'goal': ['这个目标重要吗？', '我在朝着正确的方向前进吗？']
        }
        
    def reflect(self, topic: str, current_time: float) -> SelfReflection:
        """反思"""
        aspect = self._determine_aspect(topic)
        
        insights = self._generate_insight(topic, aspect)
        
        reflection = SelfReflection(
            aspect=aspect,
            insight=insights,
            confidence=0.7,
            emotional_valence=0.5,
            timestamp=current_time
        )
        
        return reflection
    
    def _determine_aspect(self, topic: str) -> SelfAspect:
        """确定方面"""
        if any(word in topic.lower() for word in ['身体', 'physical', '健康']):
            return SelfAspect.PHYSICAL
        elif any(word in topic.lower() for word in ['心理', 'psychological', '情绪']):
            return SelfAspect.PSYCHOLOGICAL
        elif any(word in topic.lower() for word in ['社交', 'social', '关系']):
            return SelfAspect.SOCIAL
        elif any(word in topic.lower() for word in ['故事', 'narrative', '经历']):
            return SelfAspect.NARRATIVE
        else:
            return SelfAspect.EXTENDED
    
    def _generate_insight(self, topic: str, aspect: SelfAspect) -> str:
        """生成洞察"""
        pattern_key = 'behavior'
        if aspect == SelfAspect.PSYCHOLOGICAL:
            pattern_key = 'emotion'
        elif aspect == SelfAspect.NARRATIVE:
            pattern_key = 'thought'
        elif aspect == SelfAspect.EXTENDED:
            pattern_key = 'goal'
        
        questions = self.reflection_patterns.get(pattern_key, ['这是一个值得思考的问题'])
        
        return f"关于'{topic}'的反思：{questions[0]}"


class Precuneus:
    """楔前叶 - 自我意识和心理模拟"""
    
    def __init__(self):
        self.mental_simulator = MentalSimulator()
        self.perspective_taker = PerspectiveTaker()
        
    def simulate_scenario(self, scenario: str) -> Dict[str, Any]:
        """模拟场景"""
        return self.mental_simulator.simulate(scenario)
    
    def take_perspective(self, situation: Any, perspective: str = 'self') -> Dict[str, Any]:
        """采取视角"""
        return self.perspective_taker.take(situation, perspective)
    
    def process(self, input_data: Dict[str, Any], current_time: float = 0.0) -> Dict[str, Any]:
        """处理输入"""
        simulation = None
        if 'scenario' in input_data:
            simulation = self.simulate_scenario(input_data['scenario'])
        
        perspective = None
        if 'situation' in input_data:
            perspective = self.take_perspective(
                input_data['situation'],
                input_data.get('perspective', 'self')
            )
        
        return {
            'simulation': simulation,
            'perspective': perspective,
            'timestamp': current_time
        }


class MentalSimulator:
    """心理模拟器"""
    
    def __init__(self):
        self.simulation_depth = 3
        
    def simulate(self, scenario: str) -> Dict[str, Any]:
        """模拟"""
        outcomes = []
        
        for i in range(3):
            outcome = {
                'description': f"可能结果{i+1}: {scenario}的发展",
                'probability': 0.33,
                'emotional_impact': np.random.rand()
            }
            outcomes.append(outcome)
        
        return {
            'scenario': scenario,
            'outcomes': outcomes,
            'best_outcome': max(outcomes, key=lambda x: x['probability'])
        }


class PerspectiveTaker:
    """视角采取器"""
    
    def __init__(self):
        self.perspectives = ['self', 'other', 'observer']
        
    def take(self, situation: Any, perspective: str) -> Dict[str, Any]:
        """采取视角"""
        if perspective == 'self':
            interpretation = f"从自我视角看：{situation}"
        elif perspective == 'other':
            interpretation = f"从他人视角看：{situation}"
        else:
            interpretation = f"从观察者视角看：{situation}"
        
        return {
            'perspective': perspective,
            'interpretation': interpretation,
            'empathy_level': 0.7 if perspective == 'other' else 0.5
        }


class SelfConsciousnessSystem:
    """完整自我意识系统"""
    
    def __init__(self):
        self.mPFC = MedialPrefrontalCortex()
        self.PCC = PosteriorCingulateCortex()
        self.precuneus = Precuneus()
        
        self.self_model = SelfModel(
            identity="AI Agent",
            traits={},
            values=[],
            goals=[],
            beliefs={},
            autobiographical_memories=[],
            coherence=0.5
        )
        
        self.consciousness_history = []
        
    def process(self, input_data: Dict[str, Any], current_time: float = 0.0) -> Dict[str, Any]:
        """完整处理流程"""
        mpfc_result = self.mPFC.process(input_data, current_time)
        pcc_result = self.PCC.process(input_data, current_time)
        precuneus_result = self.precuneus.process(input_data, current_time)
        
        self._update_self_model(mpfc_result, pcc_result)
        
        coherence = self._compute_coherence()
        self.self_model.coherence = coherence
        
        result = {
            'mPFC': mpfc_result,
            'PCC': pcc_result,
            'precuneus': precuneus_result,
            'self_model': {
                'identity': self.self_model.identity,
                'coherence': coherence,
                'n_goals': len(self.self_model.goals),
                'n_memories': len(self.self_model.autobiographical_memories)
            },
            'self_awareness_level': self._compute_self_awareness(mpfc_result),
            'timestamp': current_time
        }
        
        self.consciousness_history.append(result)
        
        return result
    
    def _update_self_model(self, mpfc_result: Dict[str, Any], pcc_result: Dict[str, Any]):
        """更新自我模型"""
        if 'self_model_state' in mpfc_result:
            state = mpfc_result['self_model_state']
            self.self_model.traits.update(state.get('traits', {}))
        
        if 'memory_state' in pcc_result:
            memory_state = pcc_result['memory_state']
            if isinstance(memory_state, dict):
                if 'autobiographical' in memory_state:
                    self.self_model.autobiographical_memories.extend(
                        memory_state['autobiographical']
                    )
    
    def _compute_coherence(self) -> float:
        """计算一致性"""
        return 0.7
    
    def _compute_self_awareness(self, mpfc_result: Dict[str, Any]) -> float:
        """计算自我意识水平"""
        self_relevance = mpfc_result.get('self_relevance', 0.0)
        
        awareness = self_relevance * self.self_model.coherence
        
        return float(np.clip(awareness, 0, 1))
    
    def reflect_on_self(self, topic: str, current_time: float = 0.0) -> SelfReflection:
        """自我反思"""
        return self.PCC.reflect(topic, current_time)
    
    def simulate_future_self(self, scenario: str) -> Dict[str, Any]:
        """模拟未来自我"""
        return self.precuneus.simulate_scenario(scenario)
    
    def get_self_model(self) -> SelfModel:
        """获取自我模型"""
        return self.self_model
