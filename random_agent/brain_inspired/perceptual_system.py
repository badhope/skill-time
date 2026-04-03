"""
感知觉特征处理系统 - 模拟感觉皮层
基于大脑感觉皮层的功能设计
"""

import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import re


@dataclass
class PerceptualFeatures:
    """感知觉特征数据结构"""
    semantic_features: Dict[str, float]
    structural_features: Dict[str, Any]
    emotional_valence: float
    salience: float
    modality: str


class FeatureExtractor:
    """特征提取器 - 从原始输入中提取关键特征"""
    
    def __init__(self):
        self.semantic_patterns = {
            'question': r'[？?]',
            'exclamation': r'[！!]',
            'statement': r'[。.]',
            'number': r'\d+',
            'emotion_words': r'(好|坏|喜欢|讨厌|开心|难过|愤怒|恐惧)',
        }
        
    def extract(self, raw_input: str) -> Dict[str, Any]:
        """从原始输入提取特征"""
        features = {
            'length': len(raw_input),
            'word_count': len(raw_input.split()),
            'has_question': bool(re.search(self.semantic_patterns['question'], raw_input)),
            'has_exclamation': bool(re.search(self.semantic_patterns['exclamation'], raw_input)),
            'has_number': bool(re.search(self.semantic_patterns['number'], raw_input)),
            'emotion_detected': re.findall(self.semantic_patterns['emotion_words'], raw_input),
            'semantic_density': self._calculate_semantic_density(raw_input),
            'complexity': self._calculate_complexity(raw_input),
        }
        
        return features
    
    def _calculate_semantic_density(self, text: str) -> float:
        """计算语义密度"""
        words = text.split()
        if not words:
            return 0.0
        
        unique_words = set(words)
        return len(unique_words) / len(words)
    
    def _calculate_complexity(self, text: str) -> float:
        """计算文本复杂度"""
        sentences = re.split(r'[。！？.!?]', text)
        sentences = [s for s in sentences if s.strip()]
        
        if not sentences:
            return 0.0
        
        avg_sentence_length = np.mean([len(s.split()) for s in sentences])
        return min(avg_sentence_length / 20.0, 1.0)


class PatternRecognizer:
    """模式识别器 - 识别输入中的模式和结构"""
    
    def __init__(self):
        self.patterns = {
            'task_pattern': r'(帮我|请|如何|怎么|为什么|什么)',
            'creative_pattern': r'(创作|写|设计|想象|发明)',
            'analysis_pattern': r'(分析|比较|评估|判断)',
            'learning_pattern': r'(学习|理解|掌握|了解)',
        }
        
    def recognize(self, features: Dict[str, Any], raw_input: str) -> Dict[str, Any]:
        """识别模式"""
        patterns_detected = {}
        
        for pattern_name, pattern_regex in self.patterns.items():
            match = re.search(pattern_regex, raw_input)
            if match:
                patterns_detected[pattern_name] = {
                    'matched': True,
                    'match_text': match.group(),
                    'position': match.span()
                }
            else:
                patterns_detected[pattern_name] = {'matched': False}
        
        patterns_detected['input_type'] = self._classify_input_type(patterns_detected)
        patterns_detected['urgency'] = self._assess_urgency(features)
        
        return patterns_detected
    
    def _classify_input_type(self, patterns: Dict) -> str:
        """分类输入类型"""
        if patterns['task_pattern']['matched']:
            return 'task_oriented'
        elif patterns['creative_pattern']['matched']:
            return 'creative'
        elif patterns['analysis_pattern']['matched']:
            return 'analytical'
        elif patterns['learning_pattern']['matched']:
            return 'learning'
        else:
            return 'general'
    
    def _assess_urgency(self, features: Dict) -> float:
        """评估紧急程度"""
        urgency = 0.0
        
        if features.get('has_exclamation'):
            urgency += 0.3
        if features.get('has_question'):
            urgency += 0.2
        if features.get('emotion_detected'):
            urgency += 0.3
        
        return min(urgency, 1.0)


class AttentionFilter:
    """注意力过滤器 - 过滤无关信息，增强相关信号"""
    
    def __init__(self, attention_capacity: float = 7.0):
        self.attention_capacity = attention_capacity
        self.attention_weights = {}
        
    def filter(self, features: Dict, patterns: Dict) -> Dict[str, Any]:
        """过滤和增强信息"""
        filtered = {
            'attended_features': {},
            'ignored_features': [],
            'attention_priority': 0.0,
        }
        
        all_items = {**features, **patterns}
        
        sorted_items = sorted(
            all_items.items(),
            key=lambda x: self._calculate_importance(x[0], x[1]),
            reverse=True
        )
        
        for i, (key, value) in enumerate(sorted_items):
            if i < self.attention_capacity:
                filtered['attended_features'][key] = value
            else:
                filtered['ignored_features'].append(key)
        
        if filtered['attended_features']:
            priorities = [
                self._calculate_importance(k, v)
                for k, v in filtered['attended_features'].items()
            ]
            filtered['attention_priority'] = np.mean(priorities)
        
        return filtered
    
    def _calculate_importance(self, key: str, value: Any) -> float:
        """计算信息重要性"""
        importance_weights = {
            'input_type': 1.0,
            'urgency': 0.9,
            'has_question': 0.8,
            'emotion_detected': 0.7,
            'complexity': 0.6,
            'semantic_density': 0.5,
        }
        
        base_weight = importance_weights.get(key, 0.3)
        
        if isinstance(value, dict):
            if value.get('matched'):
                return base_weight * 1.5
            return base_weight * 0.5
        elif isinstance(value, bool):
            return base_weight if value else 0.1
        elif isinstance(value, (int, float)):
            return base_weight * min(value, 1.0)
        elif isinstance(value, list):
            return base_weight * min(len(value) / 5.0, 1.0)
        else:
            return base_weight


class SensoryIntegrator:
    """感觉整合器 - 整合多模态信息"""
    
    def __init__(self):
        self.integration_history = []
        
    def integrate(self, filtered_info: Dict, raw_input: str) -> PerceptualFeatures:
        """整合感知信息"""
        semantic_features = self._extract_semantic_features(filtered_info, raw_input)
        
        structural_features = self._extract_structural_features(filtered_info)
        
        emotional_valence = self._calculate_emotional_valence(filtered_info)
        
        salience = self._calculate_salience(filtered_info)
        
        modality = self._determine_modality(raw_input)
        
        perceptual_features = PerceptualFeatures(
            semantic_features=semantic_features,
            structural_features=structural_features,
            emotional_valence=emotional_valence,
            salience=salience,
            modality=modality
        )
        
        self.integration_history.append({
            'features': perceptual_features,
            'timestamp': len(self.integration_history)
        })
        
        return perceptual_features
    
    def _extract_semantic_features(self, filtered_info: Dict, raw_input: str) -> Dict[str, float]:
        """提取语义特征"""
        attended = filtered_info.get('attended_features', {})
        
        semantic = {
            'complexity': attended.get('complexity', 0.5),
            'semantic_density': attended.get('semantic_density', 0.5),
            'is_question': float(attended.get('has_question', False)),
            'is_creative': float(attended.get('creative_pattern', {}).get('matched', False)),
            'is_analytical': float(attended.get('analysis_pattern', {}).get('matched', False)),
        }
        
        return semantic
    
    def _extract_structural_features(self, filtered_info: Dict) -> Dict[str, Any]:
        """提取结构特征"""
        attended = filtered_info.get('attended_features', {})
        
        structural = {
            'length_category': self._categorize_length(attended.get('length', 0)),
            'word_count_category': self._categorize_word_count(attended.get('word_count', 0)),
            'input_type': attended.get('input_type', 'general'),
            'urgency_level': attended.get('urgency', 0.0),
        }
        
        return structural
    
    def _categorize_length(self, length: int) -> str:
        """分类长度"""
        if length < 20:
            return 'short'
        elif length < 100:
            return 'medium'
        else:
            return 'long'
    
    def _categorize_word_count(self, count: int) -> str:
        """分类词数"""
        if count < 5:
            return 'few'
        elif count < 20:
            return 'moderate'
        else:
            return 'many'
    
    def _calculate_emotional_valence(self, filtered_info: Dict) -> float:
        """计算情感效价"""
        attended = filtered_info.get('attended_features', {})
        emotions = attended.get('emotion_detected', [])
        
        positive_emotions = {'好', '喜欢', '开心'}
        negative_emotions = {'坏', '讨厌', '难过', '愤怒', '恐惧'}
        
        valence = 0.5
        
        for emotion in emotions:
            if emotion in positive_emotions:
                valence += 0.1
            elif emotion in negative_emotions:
                valence -= 0.1
        
        return max(0.0, min(1.0, valence))
    
    def _calculate_salience(self, filtered_info: Dict) -> float:
        """计算显著性"""
        return filtered_info.get('attention_priority', 0.5)
    
    def _determine_modality(self, raw_input: str) -> str:
        """确定模态"""
        return 'text'


class PerceptualSystem:
    """感知觉特征处理系统 - 模拟感觉皮层
    
    基于大脑感觉皮层的功能设计，实现：
    - 特征提取：从原始输入中提取关键特征
    - 模式识别：识别输入中的模式和结构
    - 感觉整合：整合多模态信息
    - 注意力过滤：过滤无关信息，增强相关信号
    """
    
    def __init__(self, attention_capacity: float = 7.0):
        self.feature_extractor = FeatureExtractor()
        self.pattern_recognizer = PatternRecognizer()
        self.attention_filter = AttentionFilter(attention_capacity)
        self.sensory_integrator = SensoryIntegrator()
        
        self.processing_history = []
        
    def process(self, raw_input: str) -> PerceptualFeatures:
        """处理原始输入
        
        Args:
            raw_input: 原始输入文本
            
        Returns:
            PerceptualFeatures: 感知觉特征对象
        """
        features = self.feature_extractor.extract(raw_input)
        
        patterns = self.pattern_recognizer.recognize(features, raw_input)
        
        filtered = self.attention_filter.filter(features, patterns)
        
        integrated = self.sensory_integrator.integrate(filtered, raw_input)
        
        self.processing_history.append({
            'input': raw_input,
            'features': features,
            'patterns': patterns,
            'filtered': filtered,
            'integrated': integrated,
            'timestamp': len(self.processing_history)
        })
        
        return integrated
    
    def get_processing_stats(self) -> Dict[str, Any]:
        """获取处理统计信息"""
        if not self.processing_history:
            return {}
        
        recent = self.processing_history[-10:]
        
        stats = {
            'total_processed': len(self.processing_history),
            'avg_salience': np.mean([
                h['integrated'].salience for h in recent
            ]),
            'avg_emotional_valence': np.mean([
                h['integrated'].emotional_valence for h in recent
            ]),
            'input_type_distribution': {},
        }
        
        for h in recent:
            input_type = h['integrated'].structural_features.get('input_type', 'general')
            stats['input_type_distribution'][input_type] = \
                stats['input_type_distribution'].get(input_type, 0) + 1
        
        return stats
    
    def reset(self):
        """重置系统状态"""
        self.processing_history = []
        self.sensory_integrator.integration_history = []
