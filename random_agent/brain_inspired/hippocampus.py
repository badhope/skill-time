"""
海马体记忆系统 - 情景记忆的核心
基于海马体的神经科学原理设计
"""

import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import hashlib
import math


@dataclass
class EpisodicTrace:
    """情景记忆痕迹数据结构"""
    trace_id: str
    content: str
    temporal_context: Dict[str, Any]
    spatial_context: Dict[str, Any]
    emotional_valence: float
    importance: float
    associations: List[str] = field(default_factory=list)
    consolidation_level: float = 0.0
    retrieval_count: int = 0
    created_at: float = field(default_factory=lambda: datetime.now().timestamp())


@dataclass
class SynapticWeight:
    """突触权重数据结构"""
    pre_neuron: str
    post_neuron: str
    weight: float
    last_updated: float
    ltp_count: int = 0
    ltd_count: int = 0


class SynapticPlasticity:
    """突触可塑性机制 - LTP/LTD实现
    
    基于赫布学习规则和STDP机制
    """
    
    def __init__(self, 
                 ltp_threshold: float = 0.7,
                 ltd_threshold: float = 0.3,
                 learning_rate: float = 0.1,
                 decay_rate: float = 0.01):
        self.ltp_threshold = ltp_threshold
        self.ltd_threshold = ltd_threshold
        self.learning_rate = learning_rate
        self.decay_rate = decay_rate
        self.synapses: Dict[str, SynapticWeight] = {}
        self.plasticity_history = []
        
    def strengthen(self, 
                   pre_activation: float, 
                   post_activation: float,
                   connection_id: str) -> float:
        """长时程增强（LTP）
        
        高频刺激导致突触增强
        """
        if pre_activation > self.ltp_threshold and post_activation > self.ltp_threshold:
            if connection_id not in self.synapses:
                self.synapses[connection_id] = SynapticWeight(
                    pre_neuron=connection_id.split('_')[0],
                    post_neuron=connection_id.split('_')[1] if '_' in connection_id else connection_id,
                    weight=0.5,
                    last_updated=datetime.now().timestamp()
                )
            
            synapse = self.synapses[connection_id]
            
            hebbian_product = pre_activation * post_activation
            weight_increase = self.learning_rate * hebbian_product
            
            synapse.weight = min(synapse.weight + weight_increase, 1.0)
            synapse.ltp_count += 1
            synapse.last_updated = datetime.now().timestamp()
            
            self._record_plasticity('LTP', connection_id, weight_increase)
            
            return synapse.weight
        
        return 0.0
    
    def weaken(self,
               pre_activation: float,
               post_activation: float,
               connection_id: str) -> float:
        """长时程抑制（LTD）
        
        低频刺激导致突触减弱
        """
        if pre_activation < self.ltd_threshold or post_activation < self.ltd_threshold:
            if connection_id not in self.synapses:
                return 0.0
            
            synapse = self.synapses[connection_id]
            
            weight_decrease = self.learning_rate * (1 - max(pre_activation, post_activation))
            
            synapse.weight = max(synapse.weight - weight_decrease, 0.01)
            synapse.ltd_count += 1
            synapse.last_updated = datetime.now().timestamp()
            
            self._record_plasticity('LTD', connection_id, -weight_decrease)
            
            return synapse.weight
        
        return 0.0
    
    def apply_stdp(self,
                   pre_spike_time: float,
                   post_spike_time: float,
                   connection_id: str) -> float:
        """尖峰时间依赖可塑性（STDP）
        
        根据前后神经元尖峰时间差调整权重
        """
        time_diff = post_spike_time - pre_spike_time
        
        if connection_id not in self.synapses:
            self.synapses[connection_id] = SynapticWeight(
                pre_neuron=connection_id.split('_')[0],
                post_neuron=connection_id.split('_')[1] if '_' in connection_id else connection_id,
                weight=0.5,
                last_updated=datetime.now().timestamp()
            )
        
        synapse = self.synapses[connection_id]
        
        if time_diff > 0:
            weight_change = self.learning_rate * math.exp(-time_diff / 20.0)
            synapse.weight = min(synapse.weight + weight_change, 1.0)
            synapse.ltp_count += 1
        else:
            weight_change = self.learning_rate * math.exp(time_diff / 20.0)
            synapse.weight = max(synapse.weight - weight_change, 0.01)
            synapse.ltd_count += 1
        
        synapse.last_updated = datetime.now().timestamp()
        
        return synapse.weight
    
    def homeostatic_scaling(self, target_activity: float = 0.5):
        """稳态可塑性 - 维持网络活动稳定"""
        if not self.synapses:
            return
        
        current_avg_weight = np.mean([s.weight for s in self.synapses.values()])
        
        scaling_factor = target_activity / (current_avg_weight + 0.01)
        
        for synapse in self.synapses.values():
            synapse.weight *= scaling_factor
            synapse.weight = np.clip(synapse.weight, 0.01, 1.0)
    
    def decay_weights(self):
        """权重衰减 - 模拟自然遗忘"""
        for synapse in self.synapses.values():
            synapse.weight *= (1 - self.decay_rate)
            synapse.weight = max(synapse.weight, 0.01)
    
    def _record_plasticity(self, 
                          plasticity_type: str,
                          connection_id: str,
                          weight_change: float):
        """记录可塑性变化"""
        self.plasticity_history.append({
            'type': plasticity_type,
            'connection': connection_id,
            'change': weight_change,
            'timestamp': datetime.now().timestamp(),
        })
        
        if len(self.plasticity_history) > 1000:
            self.plasticity_history = self.plasticity_history[-500:]
    
    def get_synapse_stats(self) -> Dict[str, Any]:
        """获取突触统计信息"""
        if not self.synapses:
            return {
                'total_synapses': 0,
                'avg_weight': 0.0,
                'total_ltp': 0,
                'total_ltd': 0,
            }
        
        return {
            'total_synapses': len(self.synapses),
            'avg_weight': np.mean([s.weight for s in self.synapses.values()]),
            'max_weight': max(s.weight for s in self.synapses.values()),
            'min_weight': min(s.weight for s in self.synapses.values()),
            'total_ltp': sum(s.ltp_count for s in self.synapses.values()),
            'total_ltd': sum(s.ltd_count for s in self.synapses.values()),
        }


class EpisodicEncoder:
    """情景编码器 - 时空信息整合编码"""
    
    def __init__(self, encoding_strength: float = 0.8):
        self.encoding_strength = encoding_strength
        self.encoding_history = []
        
    def encode(self, 
               experience: Any,
               temporal_context: Optional[Dict[str, Any]] = None,
               spatial_context: Optional[Dict[str, Any]] = None,
               emotional_valence: float = 0.0) -> EpisodicTrace:
        """编码新经验
        
        Args:
            experience: 经验内容
            temporal_context: 时间上下文
            spatial_context: 空间上下文
            emotional_valence: 情绪效价
            
        Returns:
            EpisodicTrace: 情景记忆痕迹
        """
        trace_id = self._generate_trace_id(experience)
        
        if temporal_context is None:
            temporal_context = {
                'timestamp': datetime.now().timestamp(),
                'time_of_day': datetime.now().hour,
                'day_of_week': datetime.now().weekday(),
            }
        
        if spatial_context is None:
            spatial_context = {
                'context_type': 'general',
                'related_concepts': [],
            }
        
        importance = self._calculate_importance(experience, emotional_valence)
        
        trace = EpisodicTrace(
            trace_id=trace_id,
            content=str(experience),
            temporal_context=temporal_context,
            spatial_context=spatial_context,
            emotional_valence=emotional_valence,
            importance=importance,
            associations=self._extract_associations(experience),
        )
        
        self.encoding_history.append({
            'trace_id': trace_id,
            'timestamp': datetime.now().timestamp(),
        })
        
        return trace
    
    def _generate_trace_id(self, experience: Any) -> str:
        """生成记忆痕迹ID"""
        content_str = str(experience) + str(datetime.now().timestamp())
        return hashlib.md5(content_str.encode()).hexdigest()[:12]
    
    def _calculate_importance(self, experience: Any, emotional_valence: float) -> float:
        """计算记忆重要性"""
        base_importance = 0.5
        
        content_str = str(experience)
        length_factor = min(len(content_str) / 100.0, 0.2)
        
        emotional_factor = abs(emotional_valence) * 0.3
        
        importance = base_importance + length_factor + emotional_factor
        importance *= self.encoding_strength
        
        return min(importance, 1.0)
    
    def _extract_associations(self, experience: Any) -> List[str]:
        """提取关联概念"""
        content_str = str(experience)
        words = content_str.split()
        
        associations = []
        for word in words:
            if len(word) > 2:
                associations.append(word)
        
        return associations[:10]


class PatternSeparator:
    """模式分离器 - 区分相似记忆
    
    基于齿状回的功能，实现模式分离
    防止记忆干扰
    """
    
    def __init__(self, separation_threshold: float = 0.7):
        self.separation_threshold = separation_threshold
        self.separation_history = []
        
    def separate(self, 
                 new_trace: EpisodicTrace,
                 existing_traces: List[EpisodicTrace]) -> Tuple[EpisodicTrace, float]:
        """模式分离
        
        Args:
            new_trace: 新记忆痕迹
            existing_traces: 现有记忆痕迹列表
            
        Returns:
            分离后的记忆痕迹和分离程度
        """
        if not existing_traces:
            return new_trace, 1.0
        
        similarities = []
        for trace in existing_traces:
            similarity = self._calculate_similarity(new_trace, trace)
            similarities.append(similarity)
        
        max_similarity = max(similarities) if similarities else 0.0
        
        if max_similarity > self.separation_threshold:
            separated_trace = self._apply_separation(new_trace, existing_traces)
            separation_degree = 1.0 - max_similarity
        else:
            separated_trace = new_trace
            separation_degree = 1.0
        
        self.separation_history.append({
            'trace_id': new_trace.trace_id,
            'max_similarity': max_similarity,
            'separation_degree': separation_degree,
            'timestamp': datetime.now().timestamp(),
        })
        
        return separated_trace, separation_degree
    
    def _calculate_similarity(self, 
                             trace1: EpisodicTrace, 
                             trace2: EpisodicTrace) -> float:
        """计算两个记忆痕迹的相似度"""
        content_sim = self._jaccard_similarity(
            trace1.content.split(),
            trace2.content.split()
        )
        
        temporal_sim = self._temporal_similarity(
            trace1.temporal_context,
            trace2.temporal_context
        )
        
        association_sim = self._jaccard_similarity(
            trace1.associations,
            trace2.associations
        )
        
        similarity = (content_sim * 0.5 + 
                     temporal_sim * 0.2 + 
                     association_sim * 0.3)
        
        return similarity
    
    def _jaccard_similarity(self, set1: List[str], set2: List[str]) -> float:
        """Jaccard相似度"""
        if not set1 or not set2:
            return 0.0
        
        set1_set = set(set1)
        set2_set = set(set2)
        
        intersection = len(set1_set & set2_set)
        union = len(set1_set | set2_set)
        
        return intersection / union if union > 0 else 0.0
    
    def _temporal_similarity(self,
                            context1: Dict[str, Any],
                            context2: Dict[str, Any]) -> float:
        """时间上下文相似度"""
        if 'timestamp' not in context1 or 'timestamp' not in context2:
            return 0.0
        
        time_diff = abs(context1['timestamp'] - context2['timestamp'])
        
        time_sim = math.exp(-time_diff / 86400.0)
        
        return time_sim
    
    def _apply_separation(self,
                         trace: EpisodicTrace,
                         existing_traces: List[EpisodicTrace]) -> EpisodicTrace:
        """应用模式分离"""
        unique_associations = set(trace.associations)
        
        for existing in existing_traces:
            similarity = self._calculate_similarity(trace, existing)
            if similarity > self.separation_threshold:
                for assoc in existing.associations:
                    unique_associations.discard(assoc)
        
        trace.associations = list(unique_associations)
        
        trace.importance *= (1 + 0.1 * len(unique_associations))
        trace.importance = min(trace.importance, 1.0)
        
        return trace


class PatternCompleter:
    """模式完成器 - 从部分线索恢复完整记忆
    
    基于CA3区的功能，实现模式完成
    """
    
    def __init__(self, completion_threshold: float = 0.3):
        self.completion_threshold = completion_threshold
        self.completion_history = []
        
    def complete(self,
                 cue: Any,
                 memory_store: List[EpisodicTrace],
                 top_k: int = 5) -> List[Tuple[EpisodicTrace, float]]:
        """模式完成
        
        Args:
            cue: 检索线索
            memory_store: 记忆存储
            top_k: 返回前k个结果
            
        Returns:
            记忆痕迹和置信度列表
        """
        if not memory_store:
            return []
        
        cue_features = self._extract_features(cue)
        
        scores = []
        for trace in memory_store:
            score = self._calculate_completion_score(cue_features, trace)
            if score > self.completion_threshold:
                scores.append((trace, score))
        
        scores.sort(key=lambda x: x[1], reverse=True)
        
        results = scores[:top_k]
        
        for trace, score in results:
            trace.retrieval_count += 1
        
        self.completion_history.append({
            'cue': str(cue)[:50],
            'results_count': len(results),
            'top_score': results[0][1] if results else 0.0,
            'timestamp': datetime.now().timestamp(),
        })
        
        return results
    
    def _extract_features(self, cue: Any) -> Dict[str, Any]:
        """提取线索特征"""
        cue_str = str(cue)
        
        return {
            'words': cue_str.split(),
            'length': len(cue_str),
            'keywords': [w for w in cue_str.split() if len(w) > 2],
        }
    
    def _calculate_completion_score(self,
                                   cue_features: Dict[str, Any],
                                   trace: EpisodicTrace) -> float:
        """计算完成分数"""
        word_overlap = len(
            set(cue_features['words']) & set(trace.content.split())
        )
        word_score = word_overlap / max(len(cue_features['words']), 1)
        
        keyword_overlap = len(
            set(cue_features['keywords']) & set(trace.associations)
        )
        keyword_score = keyword_overlap / max(len(cue_features['keywords']), 1)
        
        retrieval_bonus = min(trace.retrieval_count * 0.05, 0.2)
        
        importance_factor = trace.importance * 0.2
        
        score = (word_score * 0.4 + 
                keyword_score * 0.4 + 
                retrieval_bonus + 
                importance_factor)
        
        return min(score, 1.0)


class MemoryConsolidation:
    """记忆巩固 - 短期记忆向长期记忆转化
    
    基于睡眠和重复激活的巩固机制
    """
    
    def __init__(self, 
                 consolidation_threshold: float = 0.6,
                 replay_rate: float = 0.1):
        self.consolidation_threshold = consolidation_threshold
        self.replay_rate = replay_rate
        self.consolidation_queue = []
        self.consolidated_memories = []
        self.consolidation_history = []
        
    def initiate(self, trace: EpisodicTrace):
        """启动巩固过程"""
        self.consolidation_queue.append({
            'trace': trace,
            'replay_count': 0,
            'consolidation_progress': 0.0,
            'added_at': datetime.now().timestamp(),
        })
    
    def consolidate(self, 
                   memory_store: List[EpisodicTrace],
                   iterations: int = 1) -> List[EpisodicTrace]:
        """执行巩固
        
        Args:
            memory_store: 记忆存储
            iterations: 巩固迭代次数
            
        Returns:
            已巩固的记忆列表
        """
        consolidated = []
        
        for _ in range(iterations):
            if not self.consolidation_queue:
                break
            
            for item in self.consolidation_queue:
                item['replay_count'] += 1
                
                item['consolidation_progress'] += self.replay_rate
                
                item['trace'].consolidation_level = item['consolidation_progress']
                
                if item['consolidation_progress'] >= self.consolidation_threshold:
                    consolidated.append(item['trace'])
                    self.consolidated_memories.append(item['trace'])
                    
                    self._record_consolidation(item['trace'], item['replay_count'])
        
        self.consolidation_queue = [
            item for item in self.consolidation_queue
            if item['consolidation_progress'] < self.consolidation_threshold
        ]
        
        return consolidated
    
    def replay(self, memory_store: List[EpisodicTrace]) -> List[EpisodicTrace]:
        """记忆重放 - 模拟睡眠时的记忆重放"""
        if not memory_store:
            return []
        
        replayed = []
        
        for trace in memory_store:
            if trace.importance > 0.5 and random.random() < self.replay_rate:
                trace.consolidation_level = min(
                    trace.consolidation_level + 0.1,
                    1.0
                )
                replayed.append(trace)
        
        return replayed
    
    def _record_consolidation(self, trace: EpisodicTrace, replay_count: int):
        """记录巩固事件"""
        self.consolidation_history.append({
            'trace_id': trace.trace_id,
            'replay_count': replay_count,
            'consolidation_level': trace.consolidation_level,
            'timestamp': datetime.now().timestamp(),
        })
    
    def get_consolidation_stats(self) -> Dict[str, Any]:
        """获取巩固统计信息"""
        return {
            'queue_length': len(self.consolidation_queue),
            'consolidated_count': len(self.consolidated_memories),
            'history_length': len(self.consolidation_history),
            'avg_replay_count': np.mean([
                item['replay_count'] for item in self.consolidation_queue
            ]) if self.consolidation_queue else 0.0,
        }


class HippocampalMemorySystem:
    """海马体记忆系统
    
    基于海马体的神经科学原理，实现：
    - 情景记忆编码：时空信息整合
    - 模式分离：区分相似记忆
    - 模式完成：从部分线索恢复记忆
    - 记忆巩固：短期到长期记忆转化
    - 突触可塑性：LTP/LTD机制
    """
    
    def __init__(self,
                 ltp_threshold: float = 0.7,
                 separation_threshold: float = 0.7,
                 completion_threshold: float = 0.3,
                 consolidation_threshold: float = 0.6):
        
        self.synaptic_plasticity = SynapticPlasticity(ltp_threshold=ltp_threshold)
        self.episodic_encoder = EpisodicEncoder()
        self.pattern_separator = PatternSeparator(separation_threshold=separation_threshold)
        self.pattern_completer = PatternCompleter(completion_threshold=completion_threshold)
        self.consolidation = MemoryConsolidation(consolidation_threshold=consolidation_threshold)
        
        self.memory_store: List[EpisodicTrace] = []
        self.encoding_history = []
        
    def encode(self, 
               experience: Any,
               temporal_context: Optional[Dict[str, Any]] = None,
               spatial_context: Optional[Dict[str, Any]] = None,
               emotional_valence: float = 0.0) -> EpisodicTrace:
        """编码新经验
        
        Args:
            experience: 经验内容
            temporal_context: 时间上下文
            spatial_context: 空间上下文
            emotional_valence: 情绪效价
            
        Returns:
            编码后的记忆痕迹
        """
        trace = self.episodic_encoder.encode(
            experience=experience,
            temporal_context=temporal_context,
            spatial_context=spatial_context,
            emotional_valence=emotional_valence
        )
        
        separated_trace, separation_degree = self.pattern_separator.separate(
            new_trace=trace,
            existing_traces=self.memory_store
        )
        
        self._apply_ltp(separated_trace)
        
        self.memory_store.append(separated_trace)
        
        self.consolidation.initiate(separated_trace)
        
        self.encoding_history.append({
            'trace_id': separated_trace.trace_id,
            'separation_degree': separation_degree,
            'timestamp': datetime.now().timestamp(),
        })
        
        return separated_trace
    
    def retrieve(self, 
                 cue: Any,
                 top_k: int = 5) -> List[Tuple[EpisodicTrace, float]]:
        """检索记忆
        
        Args:
            cue: 检索线索
            top_k: 返回前k个结果
            
        Returns:
            记忆痕迹和置信度列表
        """
        results = self.pattern_completer.complete(
            cue=cue,
            memory_store=self.memory_store,
            top_k=top_k
        )
        
        for trace, confidence in results:
            self._strengthen_retrieved_memory(trace, confidence)
        
        return results
    
    def consolidate_memories(self, iterations: int = 1) -> List[EpisodicTrace]:
        """巩固记忆
        
        Args:
            iterations: 巩固迭代次数
            
        Returns:
            已巩固的记忆列表
        """
        consolidated = self.consolidation.consolidate(
            memory_store=self.memory_store,
            iterations=iterations
        )
        
        return consolidated
    
    def replay_memories(self) -> List[EpisodicTrace]:
        """重放记忆（模拟睡眠巩固）"""
        return self.consolidation.replay(self.memory_store)
    
    def forget_weak_memories(self, threshold: float = 0.1):
        """遗忘弱记忆
        
        Args:
            threshold: 遗忘阈值
        """
        initial_count = len(self.memory_store)
        
        self.memory_store = [
            trace for trace in self.memory_store
            if trace.importance > threshold or 
               trace.consolidation_level > 0.5 or
               trace.retrieval_count > 2
        ]
        
        forgotten_count = initial_count - len(self.memory_store)
        
        return forgotten_count
    
    def _apply_ltp(self, trace: EpisodicTrace):
        """应用LTP增强记忆"""
        for association in trace.associations:
            connection_id = f"{trace.trace_id}_{association}"
            
            self.synaptic_plasticity.strengthen(
                pre_activation=trace.importance,
                post_activation=0.8,
                connection_id=connection_id
            )
    
    def _strengthen_retrieved_memory(self, trace: EpisodicTrace, confidence: float):
        """增强被检索的记忆"""
        trace.importance = min(trace.importance + 0.05 * confidence, 1.0)
        
        for association in trace.associations:
            connection_id = f"{trace.trace_id}_{association}"
            
            self.synaptic_plasticity.strengthen(
                pre_activation=confidence,
                post_activation=trace.importance,
                connection_id=connection_id
            )
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """获取记忆系统统计信息"""
        return {
            'total_memories': len(self.memory_store),
            'consolidated_memories': sum(
                1 for t in self.memory_store if t.consolidation_level > 0.6
            ),
            'avg_importance': np.mean([t.importance for t in self.memory_store]) 
                             if self.memory_store else 0.0,
            'avg_consolidation': np.mean([t.consolidation_level for t in self.memory_store])
                                if self.memory_store else 0.0,
            'synaptic_stats': self.synaptic_plasticity.get_synapse_stats(),
            'consolidation_stats': self.consolidation.get_consolidation_stats(),
        }
    
    def clear_memory_store(self):
        """清空记忆存储"""
        self.memory_store = []
        self.encoding_history = []
        self.consolidation = MemoryConsolidation(
            consolidation_threshold=self.consolidation.consolidation_threshold
        )
