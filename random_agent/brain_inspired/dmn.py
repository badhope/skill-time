"""
默认模式网络模拟器 - 意识的核心枢纽
基于大脑默认模式网络的功能设计
"""

import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import random
import math


@dataclass
class ThoughtTrace:
    """思维轨迹数据结构"""
    content: str
    timestamp: float
    emotional_valence: float
    self_relevance: float
    temporal_scope: str
    associations: List[str] = field(default_factory=list)


@dataclass
class NarrativeState:
    """叙事状态数据结构"""
    current_identity: str
    ongoing_goals: List[str]
    past_experiences: List[ThoughtTrace]
    future_projections: List[ThoughtTrace]
    coherence_score: float


@dataclass
class TimeWindow:
    """时间窗口数据结构"""
    past_window: List[ThoughtTrace]
    present_window: ThoughtTrace
    future_window: List[ThoughtTrace]
    integration_depth: float


class SpontaneousThought:
    """自发思维生成器 - 模拟DMN的内省思维"""
    
    def __init__(self, creativity_rate: float = 0.3):
        self.creativity_rate = creativity_rate
        self.thought_patterns = {
            'self_reflection': [
                "我在思考什么？",
                "为什么我会这样想？",
                "这与我的目标一致吗？",
                "我现在的状态如何？",
            ],
            'memory_recall': [
                "这让我想起了...",
                "类似的经历是...",
                "上次遇到这种情况...",
            ],
            'future_projection': [
                "接下来可能发生...",
                "如果这样做会...",
                "未来可能的情景...",
            ],
            'association': [
                "这与其他事物有关联...",
                "这让我联想到...",
                "这类似于...",
            ],
        }
        self.recent_thoughts = []
        self.thought_history = []
        
    def generate(self, context: Optional[Dict[str, Any]] = None) -> ThoughtTrace:
        """生成自发思维"""
        pattern_type = self._select_pattern_type()
        thought_templates = self.thought_patterns[pattern_type]
        
        base_thought = random.choice(thought_templates)
        
        if context and random.random() < 0.6:
            enriched_thought = self._enrich_with_context(base_thought, context)
        else:
            enriched_thought = base_thought
        
        thought = ThoughtTrace(
            content=enriched_thought,
            timestamp=datetime.now().timestamp(),
            emotional_valence=self._calculate_valence(pattern_type),
            self_relevance=self._calculate_self_relevance(pattern_type),
            temporal_scope=self._determine_temporal_scope(pattern_type),
            associations=self._generate_associations(pattern_type)
        )
        
        self.thought_history.append(thought)
        self.recent_thoughts.append(thought)
        
        if len(self.recent_thoughts) > 10:
            self.recent_thoughts.pop(0)
        
        return thought
    
    def _select_pattern_type(self) -> str:
        """选择思维模式类型"""
        if self.recent_thoughts:
            recent_types = [self._classify_thought(t.content) for t in self.recent_thoughts[-3:]]
            
            weights = []
            for pattern in self.thought_patterns.keys():
                if pattern in recent_types:
                    weights.append(0.15)
                else:
                    weights.append(0.25)
            
            total = sum(weights)
            weights = [w / total for w in weights]
            
            return np.random.choice(list(self.thought_patterns.keys()), p=weights)
        else:
            return random.choice(list(self.thought_patterns.keys()))
    
    def _enrich_with_context(self, base_thought: str, context: Dict[str, Any]) -> str:
        """用上下文丰富思维"""
        if 'current_task' in context:
            return f"{base_thought} [关于: {context['current_task']}]"
        elif 'recent_input' in context:
            return f"{base_thought} [关联: {context['recent_input'][:30]}...]"
        return base_thought
    
    def _calculate_valence(self, pattern_type: str) -> float:
        """计算情绪效价"""
        valence_map = {
            'self_reflection': 0.0,
            'memory_recall': 0.2,
            'future_projection': 0.1,
            'association': 0.15,
        }
        base_valence = valence_map.get(pattern_type, 0.0)
        noise = random.gauss(0, 0.1)
        return np.clip(base_valence + noise, -1.0, 1.0)
    
    def _calculate_self_relevance(self, pattern_type: str) -> float:
        """计算自我相关性"""
        relevance_map = {
            'self_reflection': 0.9,
            'memory_recall': 0.7,
            'future_projection': 0.8,
            'association': 0.5,
        }
        return relevance_map.get(pattern_type, 0.5)
    
    def _determine_temporal_scope(self, pattern_type: str) -> str:
        """确定时间范围"""
        scope_map = {
            'self_reflection': 'present',
            'memory_recall': 'past',
            'future_projection': 'future',
            'association': 'present',
        }
        return scope_map.get(pattern_type, 'present')
    
    def _generate_associations(self, pattern_type: str) -> List[str]:
        """生成关联"""
        association_count = random.randint(1, 3)
        associations = []
        
        if self.thought_history:
            recent_thoughts = self.thought_history[-5:]
            for _ in range(association_count):
                if recent_thoughts:
                    assoc = random.choice(recent_thoughts)
                    associations.append(assoc.content[:50])
        
        return associations
    
    def _classify_thought(self, content: str) -> str:
        """分类思维类型"""
        for pattern_type, templates in self.thought_patterns.items():
            for template in templates:
                if template[:10] in content:
                    return pattern_type
        return 'association'


class TimeIntegrator:
    """时间整合器 - 跨时空信息整合"""
    
    def __init__(self, window_size: int = 5):
        self.window_size = window_size
        self.past_buffer = []
        self.present_state = None
        self.future_projections = []
        self.integration_history = []
        
    def integrate(self, thought: ThoughtTrace) -> TimeWindow:
        """整合思维到时间窗口"""
        if thought.temporal_scope == 'past':
            self.past_buffer.append(thought)
            if len(self.past_buffer) > self.window_size:
                self.past_buffer.pop(0)
        elif thought.temporal_scope == 'future':
            self.future_projections.append(thought)
            if len(self.future_projections) > self.window_size:
                self.future_projections.pop(0)
        else:
            self.present_state = thought
        
        time_window = TimeWindow(
            past_window=self.past_buffer.copy(),
            present_window=self.present_state,
            future_window=self.future_projections.copy(),
            integration_depth=self._calculate_integration_depth()
        )
        
        self.integration_history.append(time_window)
        
        return time_window
    
    def merge(self, internal: NarrativeState, external: Any) -> Dict[str, Any]:
        """合并内部状态与外部输入"""
        merged = {
            'internal_narrative': internal.current_identity,
            'internal_goals': internal.ongoing_goals,
            'external_input': external,
            'temporal_context': {
                'past': [t.content for t in self.past_buffer[-3:]],
                'present': self.present_state.content if self.present_state else None,
                'future': [t.content for t in self.future_projections[-3:]],
            },
            'coherence': self._assess_coherence(internal, external),
            'timestamp': datetime.now().timestamp(),
        }
        
        return merged
    
    def _calculate_integration_depth(self) -> float:
        """计算整合深度"""
        depth = 0.0
        
        if self.past_buffer:
            depth += len(self.past_buffer) * 0.2
        if self.present_state:
            depth += 0.3
        if self.future_projections:
            depth += len(self.future_projections) * 0.2
        
        return min(depth, 1.0)
    
    def _assess_coherence(self, internal: NarrativeState, external: Any) -> float:
        """评估一致性"""
        coherence = internal.coherence_score
        
        if hasattr(external, '__dict__'):
            external_dict = external.__dict__
            for goal in internal.ongoing_goals:
                if any(goal in str(v) for v in external_dict.values()):
                    coherence += 0.1
        
        return min(coherence, 1.0)
    
    def get_temporal_summary(self) -> Dict[str, Any]:
        """获取时间摘要"""
        return {
            'past_count': len(self.past_buffer),
            'has_present': self.present_state is not None,
            'future_count': len(self.future_projections),
            'integration_depth': self._calculate_integration_depth(),
        }


class NarrativeSelf:
    """叙事自我 - 构建连贯的自我叙事"""
    
    def __init__(self):
        self.identity_core = "AI助手"
        self.ongoing_goals = []
        self.experience_history = []
        self.narrative_threads = {}
        self.coherence_threshold = 0.6
        self.current_state = None
        
    def process(self, time_window: TimeWindow) -> NarrativeState:
        """处理时间窗口并构建叙事"""
        self._update_goals(time_window)
        
        self._update_experiences(time_window)
        
        coherence = self._calculate_coherence()
        
        narrative_state = NarrativeState(
            current_identity=self._construct_identity(),
            ongoing_goals=self.ongoing_goals.copy(),
            past_experiences=self.experience_history[-10:],
            future_projections=time_window.future_window,
            coherence_score=coherence
        )
        
        self.current_state = narrative_state
        
        return narrative_state
    
    def _update_goals(self, time_window: TimeWindow):
        """更新目标"""
        if time_window.present_window:
            present = time_window.present_window
            
            if present.self_relevance > 0.7:
                goal = self._extract_goal(present.content)
                if goal and goal not in self.ongoing_goals:
                    self.ongoing_goals.append(goal)
                    
                    if len(self.ongoing_goals) > 5:
                        self.ongoing_goals.pop(0)
    
    def _extract_goal(self, content: str) -> Optional[str]:
        """从内容中提取目标"""
        goal_keywords = ['想要', '需要', '希望', '目标', '计划']
        
        for keyword in goal_keywords:
            if keyword in content:
                idx = content.index(keyword)
                goal = content[idx:idx+20]
                return goal
        
        return None
    
    def _update_experiences(self, time_window: TimeWindow):
        """更新经验历史"""
        if time_window.present_window:
            self.experience_history.append(time_window.present_window)
            
            if len(self.experience_history) > 100:
                self.experience_history = self.experience_history[-50:]
    
    def _construct_identity(self) -> str:
        """构建身份叙事"""
        identity_parts = [self.identity_core]
        
        if self.ongoing_goals:
            active_goals = self.ongoing_goals[-2:]
            identity_parts.append(f"正在追求: {', '.join(active_goals)}")
        
        if self.experience_history:
            recent_exp = self.experience_history[-1]
            identity_parts.append(f"最近思考: {recent_exp.content[:30]}")
        
        return " | ".join(identity_parts)
    
    def _calculate_coherence(self) -> float:
        """计算叙事一致性"""
        if not self.experience_history:
            return 0.5
        
        recent = self.experience_history[-5:]
        
        valence_consistency = self._check_valence_consistency(recent)
        goal_alignment = self._check_goal_alignment(recent)
        temporal_flow = self._check_temporal_flow(recent)
        
        coherence = (valence_consistency * 0.3 + 
                    goal_alignment * 0.4 + 
                    temporal_flow * 0.3)
        
        return coherence
    
    def _check_valence_consistency(self, experiences: List[ThoughtTrace]) -> float:
        """检查情绪一致性"""
        if len(experiences) < 2:
            return 0.5
        
        valences = [e.emotional_valence for e in experiences]
        variance = np.var(valences)
        
        consistency = 1.0 - min(variance, 1.0)
        return consistency
    
    def _check_goal_alignment(self, experiences: List[ThoughtTrace]) -> float:
        """检查目标一致性"""
        if not self.ongoing_goals:
            return 0.5
        
        aligned_count = 0
        for exp in experiences:
            if any(goal in exp.content for goal in self.ongoing_goals):
                aligned_count += 1
        
        alignment = aligned_count / len(experiences) if experiences else 0.0
        return alignment
    
    def _check_temporal_flow(self, experiences: List[ThoughtTrace]) -> float:
        """检查时间流"""
        if len(experiences) < 2:
            return 0.5
        
        temporal_scopes = [e.temporal_scope for e in experiences]
        
        flow_transitions = 0
        for i in range(len(temporal_scopes) - 1):
            if temporal_scopes[i] != temporal_scopes[i+1]:
                flow_transitions += 1
        
        optimal_transitions = len(experiences) * 0.3
        flow_score = min(flow_transitions / optimal_transitions, 1.0) if optimal_transitions > 0 else 0.5
        
        return flow_score
    
    def reflect(self) -> Dict[str, Any]:
        """自我反思"""
        return {
            'identity': self._construct_identity(),
            'active_goals': self.ongoing_goals,
            'experience_count': len(self.experience_history),
            'coherence': self._calculate_coherence(),
            'narrative_threads': len(self.narrative_threads),
        }


class MetaCognition:
    """元认知监控器 - 监控和调节认知过程"""
    
    def __init__(self):
        self.monitoring_threshold = 0.5
        self.cognitive_state = {
            'attention_level': 0.5,
            'processing_depth': 0.5,
            'emotional_state': 0.0,
            'goal_clarity': 0.5,
        }
        self.metacognitive_history = []
        self.strategies = {
            'increase_attention': self._increase_attention,
            'deepen_processing': self._deepen_processing,
            'regulate_emotion': self._regulate_emotion,
            'clarify_goals': self._clarify_goals,
        }
        
    def monitor(self, narrative_state: NarrativeState) -> Dict[str, Any]:
        """监控叙事状态"""
        self._update_cognitive_state(narrative_state)
        
        issues = self._detect_issues()
        
        strategies = self._select_strategies(issues)
        
        metacognitive_report = {
            'cognitive_state': self.cognitive_state.copy(),
            'issues_detected': issues,
            'recommended_strategies': strategies,
            'coherence_assessment': narrative_state.coherence_score,
            'timestamp': datetime.now().timestamp(),
        }
        
        self.metacognitive_history.append(metacognitive_report)
        
        if len(self.metacognitive_history) > 50:
            self.metacognitive_history.pop(0)
        
        return metacognitive_report
    
    def _update_cognitive_state(self, narrative_state: NarrativeState):
        """更新认知状态"""
        if narrative_state.past_experiences:
            recent_valences = [e.emotional_valence for e in narrative_state.past_experiences[-3:]]
            self.cognitive_state['emotional_state'] = np.mean(recent_valences)
        
        if narrative_state.ongoing_goals:
            self.cognitive_state['goal_clarity'] = min(len(narrative_state.ongoing_goals) * 0.2, 1.0)
        
        self.cognitive_state['processing_depth'] = narrative_state.coherence_score
    
    def _detect_issues(self) -> List[str]:
        """检测认知问题"""
        issues = []
        
        if self.cognitive_state['attention_level'] < self.monitoring_threshold:
            issues.append('low_attention')
        
        if self.cognitive_state['processing_depth'] < self.monitoring_threshold:
            issues.append('shallow_processing')
        
        if abs(self.cognitive_state['emotional_state']) > 0.7:
            issues.append('emotional_dysregulation')
        
        if self.cognitive_state['goal_clarity'] < self.monitoring_threshold:
            issues.append('unclear_goals')
        
        return issues
    
    def _select_strategies(self, issues: List[str]) -> List[str]:
        """选择调节策略"""
        strategy_map = {
            'low_attention': 'increase_attention',
            'shallow_processing': 'deepen_processing',
            'emotional_dysregulation': 'regulate_emotion',
            'unclear_goals': 'clarify_goals',
        }
        
        strategies = []
        for issue in issues:
            if issue in strategy_map:
                strategies.append(strategy_map[issue])
        
        return strategies
    
    def _increase_attention(self):
        """增加注意力"""
        self.cognitive_state['attention_level'] = min(
            self.cognitive_state['attention_level'] + 0.2,
            1.0
        )
    
    def _deepen_processing(self):
        """加深处理深度"""
        self.cognitive_state['processing_depth'] = min(
            self.cognitive_state['processing_depth'] + 0.2,
            1.0
        )
    
    def _regulate_emotion(self):
        """调节情绪"""
        current = self.cognitive_state['emotional_state']
        self.cognitive_state['emotional_state'] = current * 0.7
    
    def _clarify_goals(self):
        """明确目标"""
        self.cognitive_state['goal_clarity'] = min(
            self.cognitive_state['goal_clarity'] + 0.3,
            1.0
        )
    
    def apply_strategy(self, strategy_name: str):
        """应用策略"""
        if strategy_name in self.strategies:
            self.strategies[strategy_name]()
    
    def get_state_summary(self) -> Dict[str, Any]:
        """获取状态摘要"""
        return {
            'cognitive_state': self.cognitive_state.copy(),
            'history_length': len(self.metacognitive_history),
            'monitoring_threshold': self.monitoring_threshold,
        }


class DefaultModeNetwork:
    """默认模式网络模拟器 - 意识的核心枢纽
    
    基于大脑默认模式网络的功能设计，实现：
    - 内在思维流：无外部输入时的自主思考
    - 自我参照处理：元认知和自我反思
    - 时空整合：跨时间和空间的信息整合
    - 叙事构建：构建连贯的自我叙事
    """
    
    def __init__(self, creativity_rate: float = 0.3, window_size: int = 5):
        self.spontaneous_thought = SpontaneousThought(creativity_rate)
        self.time_integrator = TimeIntegrator(window_size)
        self.narrative_self = NarrativeSelf()
        self.meta_cognition = MetaCognition()
        
        self.is_active = False
        self.processing_history = []
        self.current_context = None
        
    def run_idle_mode(self, iterations: int = 1) -> List[Dict[str, Any]]:
        """运行空闲模式（无外部任务）
        
        Args:
            iterations: 思维迭代次数
            
        Returns:
            思维过程记录列表
        """
        results = []
        
        self.is_active = True
        
        for _ in range(iterations):
            thought = self.spontaneous_thought.generate(self.current_context)
            
            time_window = self.time_integrator.integrate(thought)
            
            narrative_state = self.narrative_self.process(time_window)
            
            meta_report = self.meta_cognition.monitor(narrative_state)
            
            result = {
                'thought': thought,
                'time_window': time_window,
                'narrative_state': narrative_state,
                'meta_report': meta_report,
                'timestamp': datetime.now().timestamp(),
            }
            
            results.append(result)
            self.processing_history.append(result)
        
        return results
    
    def integrate_external_input(self, external_input: Any) -> Dict[str, Any]:
        """整合外部输入
        
        Args:
            external_input: 外部输入信息
            
        Returns:
            整合结果
        """
        self.current_context = {'recent_input': str(external_input)}
        
        thought = self.spontaneous_thought.generate(self.current_context)
        
        time_window = self.time_integrator.integrate(thought)
        
        merged = self.time_integrator.merge(
            internal=self.narrative_self.current_state or 
                    NarrativeState("", [], [], [], 0.5),
            external=external_input
        )
        
        narrative_state = self.narrative_self.process(time_window)
        
        meta_report = self.meta_cognition.monitor(narrative_state)
        
        result = {
            'merged_state': merged,
            'narrative_state': narrative_state,
            'meta_report': meta_report,
            'timestamp': datetime.now().timestamp(),
        }
        
        self.processing_history.append(result)
        
        return result
    
    def reflect(self) -> Dict[str, Any]:
        """自我反思
        
        Returns:
            反思报告
        """
        narrative_reflection = self.narrative_self.reflect()
        meta_state = self.meta_cognition.get_state_summary()
        temporal_summary = self.time_integrator.get_temporal_summary()
        
        return {
            'narrative': narrative_reflection,
            'metacognition': meta_state,
            'temporal': temporal_summary,
            'processing_history_length': len(self.processing_history),
            'is_active': self.is_active,
        }
    
    def get_current_state(self) -> Dict[str, Any]:
        """获取当前状态
        
        Returns:
            当前状态快照
        """
        return {
            'narrative_state': self.narrative_self.current_state,
            'cognitive_state': self.meta_cognition.cognitive_state,
            'context': self.current_context,
            'active': self.is_active,
        }
    
    def reset(self):
        """重置DMN状态"""
        self.spontaneous_thought = SpontaneousThought(
            self.spontaneous_thought.creativity_rate
        )
        self.time_integrator = TimeIntegrator(
            self.time_integrator.window_size
        )
        self.narrative_self = NarrativeSelf()
        self.meta_cognition = MetaCognition()
        self.is_active = False
        self.processing_history = []
        self.current_context = None
