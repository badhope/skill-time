"""
杏仁核情绪系统 - 情绪处理的核心
基于杏仁核的神经科学原理设计
"""

import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import random
import math


@dataclass
class EmotionalState:
    """情绪状态数据结构"""
    valence: float
    arousal: float
    dominance: float
    primary_emotion: str
    secondary_emotions: List[str]
    intensity: float
    timestamp: float = field(default_factory=lambda: datetime.now().timestamp())


@dataclass
class ThreatAssessment:
    """威胁评估数据结构"""
    threat_level: float
    threat_type: str
    confidence: float
    response_urgency: float
    recommended_action: str
    timestamp: float = field(default_factory=lambda: datetime.now().timestamp())


@dataclass
class EmotionalMemory:
    """情绪记忆数据结构"""
    memory_id: str
    stimulus: str
    emotional_response: EmotionalState
    context: Dict[str, Any]
    reinforcement_count: int
    last_activated: float
    created_at: float = field(default_factory=lambda: datetime.now().timestamp())


class ThreatDetector:
    """威胁检测器 - 快速识别潜在威胁
    
    模拟杏仁核的低路（快速通路）威胁检测
    """
    
    def __init__(self, 
                 threat_threshold: float = 0.6,
                 false_positive_rate: float = 0.1):
        self.threat_threshold = threat_threshold
        self.false_positive_rate = false_positive_rate
        self.threat_patterns = {
            'physical': ['危险', '伤害', '攻击', '威胁', '危险', 'harm', 'danger', 'threat'],
            'social': ['拒绝', '批评', '羞辱', '排斥', 'reject', 'criticize', 'shame'],
            'cognitive': ['错误', '失败', '困惑', '混乱', 'error', 'fail', 'confusion'],
            'emotional': ['恐惧', '焦虑', '愤怒', '悲伤', 'fear', 'anxiety', 'anger'],
        }
        self.detection_history = []
        
    def quick_assess(self, stimulus: Any) -> ThreatAssessment:
        """快速威胁评估（低路）
        
        Args:
            stimulus: 刺激
            
        Returns:
            威胁评估结果
        """
        stimulus_str = str(stimulus).lower()
        
        threat_scores = {}
        for threat_type, patterns in self.threat_patterns.items():
            score = self._calculate_threat_score(stimulus_str, patterns)
            threat_scores[threat_type] = score
        
        max_threat_type = max(threat_scores.items(), key=lambda x: x[1])
        threat_level = max_threat_type[1]
        
        if random.random() < self.false_positive_rate:
            threat_level = min(threat_level + 0.2, 1.0)
        
        confidence = self._calculate_confidence(threat_level)
        
        response_urgency = self._calculate_urgency(threat_level)
        
        recommended_action = self._recommend_action(threat_level, max_threat_type[0])
        
        assessment = ThreatAssessment(
            threat_level=threat_level,
            threat_type=max_threat_type[0],
            confidence=confidence,
            response_urgency=response_urgency,
            recommended_action=recommended_action
        )
        
        self._record_detection(stimulus, assessment)
        
        return assessment
    
    def detailed_assess(self, stimulus: Any, context: Optional[Dict[str, Any]] = None) -> ThreatAssessment:
        """详细威胁评估（高路）
        
        Args:
            stimulus: 刺激
            context: 上下文
            
        Returns:
            威胁评估结果
        """
        quick_assessment = self.quick_assess(stimulus)
        
        if context:
            context_modifier = self._evaluate_context(context)
            quick_assessment.threat_level *= context_modifier
            quick_assessment.threat_level = min(quick_assessment.threat_level, 1.0)
        
        return quick_assessment
    
    def _calculate_threat_score(self, stimulus: str, patterns: List[str]) -> float:
        """计算威胁分数"""
        matches = sum(1 for pattern in patterns if pattern in stimulus)
        
        if matches == 0:
            return 0.0
        
        base_score = matches / len(patterns)
        
        intensity = min(matches * 0.3, 1.0)
        
        return base_score * 0.7 + intensity * 0.3
    
    def _calculate_confidence(self, threat_level: float) -> float:
        """计算置信度"""
        if threat_level > 0.8:
            return 0.9
        elif threat_level > 0.6:
            return 0.7
        elif threat_level > 0.4:
            return 0.5
        else:
            return 0.3
    
    def _calculate_urgency(self, threat_level: float) -> float:
        """计算响应紧迫性"""
        if threat_level > self.threat_threshold:
            return threat_level * 1.2
        else:
            return threat_level * 0.8
    
    def _recommend_action(self, threat_level: float, threat_type: str) -> str:
        """推荐行动"""
        if threat_level > 0.8:
            return 'immediate_response'
        elif threat_level > 0.6:
            return 'heightened_vigilance'
        elif threat_level > 0.4:
            return 'monitoring'
        else:
            return 'no_action_needed'
    
    def _evaluate_context(self, context: Dict[str, Any]) -> float:
        """评估上下文影响"""
        modifier = 1.0
        
        if 'safe_environment' in context and context['safe_environment']:
            modifier *= 0.7
        
        if 'previous_threats' in context:
            modifier *= 1.2
        
        return modifier
    
    def _record_detection(self, stimulus: Any, assessment: ThreatAssessment):
        """记录检测事件"""
        self.detection_history.append({
            'stimulus': str(stimulus)[:50],
            'threat_level': assessment.threat_level,
            'threat_type': assessment.threat_type,
            'timestamp': datetime.now().timestamp(),
        })
        
        if len(self.detection_history) > 500:
            self.detection_history = self.detection_history[-250:]
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            'detection_count': len(self.detection_history),
            'avg_threat_level': np.mean([d['threat_level'] for d in self.detection_history]) if self.detection_history else 0.0,
            'threat_types': list(set(d['threat_type'] for d in self.detection_history)),
        }


class FearConditioning:
    """恐惧条件化 - 学习威胁关联
    
    基于经典条件反射和操作性条件反射
    """
    
    def __init__(self, learning_rate: float = 0.1, extinction_rate: float = 0.05):
        self.learning_rate = learning_rate
        self.extinction_rate = extinction_rate
        self.conditioned_responses: Dict[str, float] = {}
        self.conditioning_history = []
        
    def associate(self, 
                 neutral_stimulus: str,
                 threat_stimulus: str,
                 threat_level: float):
        """建立条件反射
        
        Args:
            neutral_stimulus: 中性刺激
            threat_stimulus: 威胁刺激
            threat_level: 威胁等级
        """
        association_key = f"{neutral_stimulus}_{threat_stimulus}"
        
        if association_key not in self.conditioned_responses:
            self.conditioned_responses[association_key] = 0.0
        
        self.conditioned_responses[association_key] += self.learning_rate * threat_level
        self.conditioned_responses[association_key] = min(
            self.conditioned_responses[association_key], 
            1.0
        )
        
        self._record_conditioning('associate', association_key, threat_level)
    
    def check(self, stimulus: str) -> float:
        """检查条件反射
        
        Args:
            stimulus: 刺激
            
        Returns:
            条件反射强度
        """
        max_response = 0.0
        
        for key, response in self.conditioned_responses.items():
            if stimulus in key:
                max_response = max(max_response, response)
        
        return max_response
    
    def extinguish(self, stimulus: str):
        """消退条件反射
        
        Args:
            stimulus: 刺激
        """
        keys_to_update = [
            key for key in self.conditioned_responses.keys()
            if stimulus in key
        ]
        
        for key in keys_to_update:
            self.conditioned_responses[key] *= (1 - self.extinction_rate)
            
            if self.conditioned_responses[key] < 0.1:
                del self.conditioned_responses[key]
            
            self._record_conditioning('extinguish', key, self.conditioned_responses.get(key, 0.0))
    
    def _record_conditioning(self, action: str, association: str, strength: float):
        """记录条件化事件"""
        self.conditioning_history.append({
            'action': action,
            'association': association,
            'strength': strength,
            'timestamp': datetime.now().timestamp(),
        })
        
        if len(self.conditioning_history) > 500:
            self.conditioning_history = self.conditioning_history[-250:]
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            'conditioned_responses_count': len(self.conditioned_responses),
            'avg_response_strength': np.mean(list(self.conditioned_responses.values())) if self.conditioned_responses else 0.0,
            'conditioning_events': len(self.conditioning_history),
        }


class EmotionalMemorySystem:
    """情绪记忆系统 - 增强情绪相关记忆"""
    
    def __init__(self, enhancement_factor: float = 1.5):
        self.enhancement_factor = enhancement_factor
        self.emotional_memories: Dict[str, EmotionalMemory] = {}
        self.memory_history = []
        
    def encode(self, 
              stimulus: str,
              emotional_response: EmotionalState,
              context: Optional[Dict[str, Any]] = None) -> EmotionalMemory:
        """编码情绪记忆
        
        Args:
            stimulus: 刺激
            emotional_response: 情绪反应
            context: 上下文
            
        Returns:
            情绪记忆
        """
        memory_id = self._generate_memory_id(stimulus)
        
        memory = EmotionalMemory(
            memory_id=memory_id,
            stimulus=stimulus,
            emotional_response=emotional_response,
            context=context or {},
            reinforcement_count=1,
            last_activated=datetime.now().timestamp()
        )
        
        self.emotional_memories[memory_id] = memory
        
        self._record_memory('encode', memory)
        
        return memory
    
    def retrieve(self, stimulus: str) -> Optional[EmotionalMemory]:
        """检索情绪记忆
        
        Args:
            stimulus: 刺激
            
        Returns:
            情绪记忆
        """
        for memory_id, memory in self.emotional_memories.items():
            if stimulus in memory.stimulus or memory.stimulus in stimulus:
                memory.last_activated = datetime.now().timestamp()
                memory.reinforcement_count += 1
                
                self._record_memory('retrieve', memory)
                
                return memory
        
        return None
    
    def enhance(self, stimulus: str, emotional_intensity: float):
        """增强情绪记忆
        
        Args:
            stimulus: 刺激
            emotional_intensity: 情绪强度
        """
        memory = self.retrieve(stimulus)
        
        if memory:
            enhancement = emotional_intensity * self.enhancement_factor
            
            memory.emotional_response.intensity = min(
                memory.emotional_response.intensity + enhancement * 0.1,
                1.0
            )
            
            self._record_memory('enhance', memory)
    
    def consolidate(self):
        """巩固情绪记忆"""
        current_time = datetime.now().timestamp()
        
        memories_to_remove = []
        
        for memory_id, memory in self.emotional_memories.items():
            age = current_time - memory.created_at
            
            if memory.reinforcement_count < 2 and age > 3600:
                memories_to_remove.append(memory_id)
        
        for memory_id in memories_to_remove:
            del self.emotional_memories[memory_id]
    
    def _generate_memory_id(self, stimulus: str) -> str:
        """生成记忆ID"""
        import hashlib
        content = stimulus + str(datetime.now().timestamp())
        return hashlib.md5(content.encode()).hexdigest()[:8]
    
    def _record_memory(self, action: str, memory: EmotionalMemory):
        """记录记忆事件"""
        self.memory_history.append({
            'action': action,
            'memory_id': memory.memory_id,
            'stimulus': memory.stimulus[:30],
            'intensity': memory.emotional_response.intensity,
            'timestamp': datetime.now().timestamp(),
        })
        
        if len(self.memory_history) > 500:
            self.memory_history = self.memory_history[-250:]
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            'memory_count': len(self.emotional_memories),
            'avg_intensity': np.mean([m.emotional_response.intensity for m in self.emotional_memories.values()]) if self.emotional_memories else 0.0,
            'total_reinforcements': sum(m.reinforcement_count for m in self.emotional_memories.values()),
        }


class EmotionRegulator:
    """情绪调节器 - 与前额叶协同调节情绪"""
    
    def __init__(self, regulation_capacity: float = 0.7):
        self.regulation_capacity = regulation_capacity
        self.regulation_strategies = {
            'reappraisal': self._reappraisal,
            'suppression': self._suppression,
            'distraction': self._distraction,
            'acceptance': self._acceptance,
        }
        self.regulation_history = []
        self.current_regulation_level = 0.5
        
    def regulate(self,
                emotional_state: EmotionalState,
                prefrontal_input: Optional[float] = None) -> EmotionalState:
        """调节情绪
        
        Args:
            emotional_state: 情绪状态
            prefrontal_input: 前额叶输入
            
        Returns:
            调节后的情绪状态
        """
        if abs(emotional_state.valence) < 0.3 and emotional_state.arousal < 0.5:
            return emotional_state
        
        regulation_strength = self.regulation_capacity
        
        if prefrontal_input is not None:
            regulation_strength *= (1 + prefrontal_input * 0.3)
        
        strategy = self._select_strategy(emotional_state)
        
        regulated_state = self.regulation_strategies[strategy](
            emotional_state,
            regulation_strength
        )
        
        self._record_regulation(strategy, emotional_state, regulated_state)
        
        return regulated_state
    
    def _select_strategy(self, emotional_state: EmotionalState) -> str:
        """选择调节策略"""
        if emotional_state.arousal > 0.8:
            return 'suppression'
        elif emotional_state.valence < -0.5:
            return 'reappraisal'
        elif emotional_state.arousal > 0.6:
            return 'distraction'
        else:
            return 'acceptance'
    
    def _reappraisal(self, 
                    state: EmotionalState,
                    strength: float) -> EmotionalState:
        """认知重评"""
        new_valence = state.valence * (1 - strength * 0.4)
        new_arousal = state.arousal * (1 - strength * 0.2)
        
        return EmotionalState(
            valence=new_valence,
            arousal=new_arousal,
            dominance=state.dominance + strength * 0.2,
            primary_emotion=state.primary_emotion,
            secondary_emotions=state.secondary_emotions,
            intensity=state.intensity * (1 - strength * 0.3)
        )
    
    def _suppression(self,
                    state: EmotionalState,
                    strength: float) -> EmotionalState:
        """表达抑制"""
        return EmotionalState(
            valence=state.valence,
            arousal=state.arousal * (1 - strength * 0.5),
            dominance=state.dominance,
            primary_emotion=state.primary_emotion,
            secondary_emotions=state.secondary_emotions,
            intensity=state.intensity * (1 - strength * 0.4)
        )
    
    def _distraction(self,
                    state: EmotionalState,
                    strength: float) -> EmotionalState:
        """注意力转移"""
        return EmotionalState(
            valence=state.valence * 0.5,
            arousal=state.arousal * (1 - strength * 0.3),
            dominance=state.dominance + strength * 0.1,
            primary_emotion='neutral',
            secondary_emotions=[],
            intensity=state.intensity * (1 - strength * 0.5)
        )
    
    def _acceptance(self,
                   state: EmotionalState,
                   strength: float) -> EmotionalState:
        """接受"""
        return EmotionalState(
            valence=state.valence * 0.8,
            arousal=state.arousal * 0.9,
            dominance=state.dominance + strength * 0.3,
            primary_emotion=state.primary_emotion,
            secondary_emotions=state.secondary_emotions,
            intensity=state.intensity * 0.85
        )
    
    def _record_regulation(self,
                          strategy: str,
                          before: EmotionalState,
                          after: EmotionalState):
        """记录调节事件"""
        self.regulation_history.append({
            'strategy': strategy,
            'before_valence': before.valence,
            'after_valence': after.valence,
            'before_arousal': before.arousal,
            'after_arousal': after.arousal,
            'timestamp': datetime.now().timestamp(),
        })
        
        if len(self.regulation_history) > 500:
            self.regulation_history = self.regulation_history[-250:]
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            'regulation_capacity': self.regulation_capacity,
            'regulation_events': len(self.regulation_history),
            'strategy_usage': {
                strategy: sum(1 for h in self.regulation_history if h['strategy'] == strategy)
                for strategy in self.regulation_strategies.keys()
            },
        }


class AmygdalaEmotionSystem:
    """杏仁核情绪系统
    
    基于杏仁核的神经科学原理，实现：
    - 威胁检测：快速识别潜在威胁
    - 恐惧条件化：学习威胁关联
    - 情绪记忆：增强情绪相关记忆
    - 情绪调节：与前额叶协同调节情绪
    - 价值评估：评估刺激的情绪价值
    """
    
    def __init__(self,
                 threat_threshold: float = 0.6,
                 regulation_capacity: float = 0.7):
        
        self.threat_detector = ThreatDetector(threat_threshold=threat_threshold)
        self.fear_conditioning = FearConditioning()
        self.emotional_memory = EmotionalMemorySystem()
        self.emotion_regulator = EmotionRegulator(regulation_capacity=regulation_capacity)
        
        self.current_emotional_state: Optional[EmotionalState] = None
        self.processing_history = []
        
    def process_emotion(self, 
                       stimulus: Any,
                       context: Optional[Dict[str, Any]] = None) -> EmotionalState:
        """处理情绪刺激
        
        Args:
            stimulus: 刺激
            context: 上下文
            
        Returns:
            情绪状态
        """
        threat_assessment = self.threat_detector.quick_assess(stimulus)
        
        if threat_assessment.threat_level > 0.5:
            self.fear_conditioning.associate(
                neutral_stimulus=str(stimulus),
                threat_stimulus='threat',
                threat_level=threat_assessment.threat_level
            )
        
        emotional_state = self._generate_emotional_state(stimulus, threat_assessment)
        
        memory = self.emotional_memory.retrieve(str(stimulus))
        if memory:
            emotional_state.intensity = min(
                emotional_state.intensity + memory.emotional_response.intensity * 0.3,
                1.0
            )
        else:
            self.emotional_memory.encode(
                stimulus=str(stimulus),
                emotional_response=emotional_state,
                context=context
            )
        
        regulated_state = self.emotion_regulator.regulate(emotional_state)
        
        self.current_emotional_state = regulated_state
        
        self._record_processing(stimulus, threat_assessment, regulated_state)
        
        return regulated_state
    
    def assess_threat(self, stimulus: Any) -> ThreatAssessment:
        """评估威胁
        
        Args:
            stimulus: 刺激
            
        Returns:
            威胁评估
        """
        return self.threat_detector.quick_assess(stimulus)
    
    def evaluate_valence(self, stimulus: Any) -> float:
        """评估刺激的情绪效价
        
        Args:
            stimulus: 刺激
            
        Returns:
            效价值（-1到1）
        """
        emotional_state = self.process_emotion(stimulus)
        return emotional_state.valence
    
    def get_emotional_memory(self, stimulus: str) -> Optional[EmotionalMemory]:
        """获取情绪记忆
        
        Args:
            stimulus: 刺激
            
        Returns:
            情绪记忆
        """
        return self.emotional_memory.retrieve(stimulus)
    
    def regulate_emotion(self, 
                        emotional_state: Optional[EmotionalState] = None,
                        prefrontal_input: Optional[float] = None) -> EmotionalState:
        """调节情绪
        
        Args:
            emotional_state: 情绪状态（None则使用当前状态）
            prefrontal_input: 前额叶输入
            
        Returns:
            调节后的情绪状态
        """
        state = emotional_state or self.current_emotional_state
        
        if state is None:
            return EmotionalState(
                valence=0.0,
                arousal=0.0,
                dominance=0.5,
                primary_emotion='neutral',
                secondary_emotions=[],
                intensity=0.0
            )
        
        return self.emotion_regulator.regulate(state, prefrontal_input)
    
    def _generate_emotional_state(self,
                                  stimulus: Any,
                                  threat_assessment: ThreatAssessment) -> EmotionalState:
        """生成情绪状态"""
        valence = -threat_assessment.threat_level
        
        arousal = threat_assessment.response_urgency
        
        dominance = 1.0 - threat_assessment.threat_level
        
        primary_emotion = self._determine_primary_emotion(threat_assessment)
        
        secondary_emotions = self._determine_secondary_emotions(threat_assessment)
        
        intensity = threat_assessment.threat_level
        
        return EmotionalState(
            valence=valence,
            arousal=arousal,
            dominance=dominance,
            primary_emotion=primary_emotion,
            secondary_emotions=secondary_emotions,
            intensity=intensity
        )
    
    def _determine_primary_emotion(self, assessment: ThreatAssessment) -> str:
        """确定主要情绪"""
        if assessment.threat_level > 0.8:
            return 'fear'
        elif assessment.threat_level > 0.6:
            return 'anxiety'
        elif assessment.threat_level > 0.4:
            return 'concern'
        elif assessment.threat_level > 0.2:
            return 'alertness'
        else:
            return 'neutral'
    
    def _determine_secondary_emotions(self, assessment: ThreatAssessment) -> List[str]:
        """确定次要情绪"""
        emotions = []
        
        if assessment.threat_type == 'social':
            emotions.append('embarrassment')
        
        if assessment.threat_type == 'cognitive':
            emotions.append('confusion')
        
        if assessment.confidence < 0.5:
            emotions.append('uncertainty')
        
        return emotions
    
    def _record_processing(self,
                          stimulus: Any,
                          threat_assessment: ThreatAssessment,
                          emotional_state: EmotionalState):
        """记录处理事件"""
        self.processing_history.append({
            'stimulus': str(stimulus)[:50],
            'threat_level': threat_assessment.threat_level,
            'emotional_valence': emotional_state.valence,
            'emotional_arousal': emotional_state.arousal,
            'primary_emotion': emotional_state.primary_emotion,
            'timestamp': datetime.now().timestamp(),
        })
        
        if len(self.processing_history) > 500:
            self.processing_history = self.processing_history[-250:]
    
    def get_system_stats(self) -> Dict[str, Any]:
        """获取系统统计"""
        return {
            'threat_detector': self.threat_detector.get_stats(),
            'fear_conditioning': self.fear_conditioning.get_stats(),
            'emotional_memory': self.emotional_memory.get_stats(),
            'emotion_regulator': self.emotion_regulator.get_stats(),
            'processing_count': len(self.processing_history),
            'current_emotion': self.current_emotional_state.primary_emotion if self.current_emotional_state else None,
        }
    
    def reset(self):
        """重置系统"""
        self.threat_detector = ThreatDetector(
            threat_threshold=self.threat_detector.threat_threshold
        )
        self.fear_conditioning = FearConditioning()
        self.emotional_memory = EmotionalMemorySystem()
        self.emotion_regulator = EmotionRegulator(
            regulation_capacity=self.emotion_regulator.regulation_capacity
        )
        self.current_emotional_state = None
        self.processing_history = []
