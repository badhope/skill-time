"""
突显网络系统 - 检测显著刺激并切换大脑网络
基于2024-2025最新神经科学研究
"""

import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

from random_agent.brain_inspired.ensemble import CorticalColumn, NeuralEnsemble
from random_agent.brain_inspired.neuron import Neuron


class SalienceType(Enum):
    """显著性类型"""
    INTEROCEPTIVE = "interoceptive"
    COGNITIVE = "cognitive"
    EMOTIONAL = "emotional"
    NOVEL = "novel"
    REWARD = "reward"


@dataclass
class SalienceSignal:
    """显著性信号"""
    salience_type: SalienceType
    intensity: float
    location: Optional[Tuple[float, ...]] = None
    timestamp: float = 0.0
    context: Optional[Dict[str, Any]] = None


class AnteriorInsula:
    """前脑岛（AI）"""
    
    def __init__(self):
        self.interoceptive_columns = self._create_interoceptive_columns()
        self.emotion_integrator = EmotionIntegrator()
        self.salience_detector = InteroceptiveSalienceDetector()
        
    def _create_interoceptive_columns(self) -> List[CorticalColumn]:
        """创建内感受柱"""
        columns = []
        modalities = ['heartbeat', 'respiration', 'hunger', 'thirst', 'pain']
        
        for modality in modalities:
            column = CorticalColumn(column_id=f"AI_{modality}")
            columns.append(column)
        
        return columns
    
    def detect_interoceptive_salience(self, interoceptive_input: Dict[str, float]) -> SalienceSignal:
        """检测内感受显著性"""
        salience_intensity = self.salience_detector.compute(interoceptive_input)
        
        dominant_modality = max(interoceptive_input, key=interoceptive_input.get) if interoceptive_input else 'unknown'
        
        signal = SalienceSignal(
            salience_type=SalienceType.INTEROCEPTIVE,
            intensity=salience_intensity,
            timestamp=0.0,
            context={'dominant_modality': dominant_modality}
        )
        
        return signal
    
    def integrate_emotion(self, emotional_input: Dict[str, float]) -> Dict[str, Any]:
        """整合情绪"""
        return self.emotion_integrator.integrate(emotional_input)
    
    def process(self, input_data: Dict[str, Any], current_time: float = 0.0) -> Dict[str, Any]:
        """处理输入"""
        interoceptive = input_data.get('interoceptive', {})
        salience = self.detect_interoceptive_salience(interoceptive)
        
        emotional = input_data.get('emotional', {})
        emotion_state = self.integrate_emotion(emotional)
        
        return {
            'interoceptive_salience': salience,
            'emotion_state': emotion_state,
            'timestamp': current_time
        }


class InteroceptiveSalienceDetector:
    """内感受显著性检测器"""
    
    def __init__(self):
        self.threshold = 0.5
        self.baseline = {
            'heartbeat': 0.5,
            'respiration': 0.5,
            'hunger': 0.3,
            'thirst': 0.3,
            'pain': 0.1
        }
        
    def compute(self, interoceptive_input: Dict[str, float]) -> float:
        """计算显著性"""
        if not interoceptive_input:
            return 0.0
        
        deviations = []
        for modality, value in interoceptive_input.items():
            baseline = self.baseline.get(modality, 0.5)
            deviation = abs(value - baseline)
            deviations.append(deviation)
        
        salience = np.mean(deviations) if deviations else 0.0
        
        return float(np.clip(salience, 0, 1))


class EmotionIntegrator:
    """情绪整合器"""
    
    def __init__(self):
        self.emotion_weights = {
            'valence': 0.4,
            'arousal': 0.3,
            'dominance': 0.3
        }
        
    def integrate(self, emotional_input: Dict[str, float]) -> Dict[str, Any]:
        """整合情绪"""
        if not emotional_input:
            return {'integrated_emotion': 0.5}
        
        integrated = 0.0
        for emotion, value in emotional_input.items():
            weight = self.emotion_weights.get(emotion, 0.33)
            integrated += value * weight
        
        return {
            'integrated_emotion': integrated,
            'components': emotional_input
        }


class DorsalAnteriorCingulateCortex:
    """背侧前扣带回（dACC）"""
    
    def __init__(self):
        self.conflict_detector = ConflictDetector()
        self.cognitive_salience_detector = CognitiveSalienceDetector()
        self.error_monitor = ErrorMonitor()
        
    def detect_cognitive_salience(self, cognitive_input: Dict[str, Any]) -> SalienceSignal:
        """检测认知显著性"""
        salience_intensity = self.cognitive_salience_detector.compute(cognitive_input)
        
        signal = SalienceSignal(
            salience_type=SalienceType.COGNITIVE,
            intensity=salience_intensity,
            timestamp=0.0,
            context=cognitive_input
        )
        
        return signal
    
    def detect_conflict(self, options: List[Any]) -> float:
        """检测冲突"""
        return self.conflict_detector.detect(options)
    
    def monitor_errors(self, expected: Any, actual: Any) -> float:
        """监控错误"""
        return self.error_monitor.compute(expected, actual)
    
    def process(self, input_data: Dict[str, Any], current_time: float = 0.0) -> Dict[str, Any]:
        """处理输入"""
        cognitive = input_data.get('cognitive', {})
        salience = self.detect_cognitive_salience(cognitive)
        
        conflict = 0.0
        if 'options' in input_data:
            conflict = self.detect_conflict(input_data['options'])
        
        error = 0.0
        if 'expected' in input_data and 'actual' in input_data:
            error = self.monitor_errors(input_data['expected'], input_data['actual'])
        
        return {
            'cognitive_salience': salience,
            'conflict_level': conflict,
            'error_signal': error,
            'timestamp': current_time
        }


class ConflictDetector:
    """冲突检测器"""
    
    def __init__(self):
        self.conflict_threshold = 0.5
        
    def detect(self, options: List[Any]) -> float:
        """检测冲突"""
        if len(options) <= 1:
            return 0.0
        
        n_options = len(options)
        conflict = min(1.0, n_options / 5.0)
        
        return conflict


class CognitiveSalienceDetector:
    """认知显著性检测器"""
    
    def __init__(self):
        self.salience_weights = {
            'novelty': 0.3,
            'relevance': 0.4,
            'urgency': 0.3
        }
        
    def compute(self, cognitive_input: Dict[str, Any]) -> float:
        """计算显著性"""
        if not cognitive_input:
            return 0.0
        
        salience = 0.0
        for key, weight in self.salience_weights.items():
            if key in cognitive_input:
                salience += cognitive_input[key] * weight
        
        return float(np.clip(salience, 0, 1))


class ErrorMonitor:
    """错误监控器"""
    
    def __init__(self):
        self.error_history = []
        
    def compute(self, expected: Any, actual: Any) -> float:
        """计算错误"""
        if expected == actual:
            return 0.0
        
        error = 1.0
        self.error_history.append(error)
        
        return error


class NetworkSwitchController:
    """网络切换控制器"""
    
    def __init__(self):
        self.current_network = 'DMN'
        self.switch_threshold = 0.6
        self.switch_history = []
        
    def evaluate_switch(self, total_salience: float) -> bool:
        """评估是否切换"""
        should_switch = total_salience > self.switch_threshold
        return should_switch
    
    def switch_to_CEN(self):
        """切换到中央执行网络"""
        if self.current_network != 'CEN':
            self.switch_history.append(('CEN', 0.0))
            self.current_network = 'CEN'
    
    def switch_to_DMN(self):
        """切换到默认模式网络"""
        if self.current_network != 'DMN':
            self.switch_history.append(('DMN', 0.0))
            self.current_network = 'DMN'
    
    def get_current_network(self) -> str:
        """获取当前网络"""
        return self.current_network


class SalienceNetwork:
    """完整突显网络系统"""
    
    def __init__(self):
        self.AI = AnteriorInsula()
        self.dACC = DorsalAnteriorCingulateCortex()
        self.switch_controller = NetworkSwitchController()
        
        self.salience_history = []
        
    def detect_salience(self, stimulus: Dict[str, Any], current_time: float = 0.0) -> float:
        """检测显著性"""
        ai_result = self.AI.process(stimulus, current_time)
        dacc_result = self.dACC.process(stimulus, current_time)
        
        interoceptive_salience = ai_result['interoceptive_salience'].intensity
        cognitive_salience = dacc_result['cognitive_salience'].intensity
        
        total_salience = 0.5 * interoceptive_salience + 0.5 * cognitive_salience
        
        salience_record = {
            'total': total_salience,
            'interoceptive': interoceptive_salience,
            'cognitive': cognitive_salience,
            'timestamp': current_time
        }
        self.salience_history.append(salience_record)
        
        return total_salience
    
    def switch_network(self, total_salience: float) -> str:
        """切换网络"""
        should_switch = self.switch_controller.evaluate_switch(total_salience)
        
        if should_switch:
            self.switch_controller.switch_to_CEN()
        else:
            self.switch_controller.switch_to_DMN()
        
        return self.switch_controller.get_current_network()
    
    def process(self, input_data: Dict[str, Any], current_time: float = 0.0) -> Dict[str, Any]:
        """完整处理流程"""
        total_salience = self.detect_salience(input_data, current_time)
        active_network = self.switch_network(total_salience)
        
        ai_result = self.AI.process(input_data, current_time)
        dacc_result = self.dACC.process(input_data, current_time)
        
        result = {
            'total_salience': total_salience,
            'active_network': active_network,
            'AI_result': ai_result,
            'dACC_result': dacc_result,
            'switch_occurred': len(self.switch_controller.switch_history) > 0,
            'timestamp': current_time
        }
        
        return result
