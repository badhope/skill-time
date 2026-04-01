"""
意识层次系统 (Consciousness Layers)

理论基础：弗洛伊德冰山模型 + 现代神经科学

层次结构（从上到下）：
1. 显意识层 (Conscious) - 有觉察、理性、慢、高能耗
2. 前意识层 (Preconscious) - 可唤起、潜在、中能耗
3. 潜意识层 (Subconscious) - 被压抑、深层驱动、低能耗
4. 无意识层 (Unconscious) - 自动化、本能、极低能耗

神经基础：
- 显意识：前额叶皮层
- 前意识：海马体、皮层存储区
- 潜意识：边缘系统、杏仁核、基底神经节
- 无意识：脑干、脊髓、自主神经系统

信息流动：
- 自下而上：直觉闪现、情绪驱动、记忆涌现
- 自上而下：目标引导、注意力聚焦、习惯抑制
- 随机穿透：任何层都可以随机影响其他层
"""

import random
import time
from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
from random_agent.core.randomness_engine import RandomnessEngine, RandomnessType


class ConsciousnessLevel(Enum):
    """意识层次"""
    CONSCIOUS = "conscious"          # 显意识
    PRECONSCIOUS = "preconscious"    # 前意识
    SUBCONSCIOUS = "subconscious"    # 潜意识
    UNCONSCIOUS = "unconscious"      # 无意识


@dataclass
class Thought:
    """思维单元"""
    content: Any
    level: ConsciousnessLevel
    strength: float = 0.5
    timestamp: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        self.strength = max(0.0, min(1.0, self.strength))


@dataclass
class LayerState:
    """层次状态"""
    level: ConsciousnessLevel
    active_thoughts: List[Thought] = field(default_factory=list)
    activation_level: float = 0.5
    noise_level: float = 0.1
    energy_level: float = 1.0


class ConsciousLayer:
    """
    显意识层
    
    神经基础：前额叶皮层
    时间尺度：慢（秒级以上）
    能耗：高
    
    功能：
    - 目标监控：检查当前思考是否偏离目标
    - 逻辑推理：进行有意识的逻辑分析
    - 否决权：可以阻止潜意识产生的冲动
    - 收敛判断：决定何时停止发散，开始收敛
    """
    
    def __init__(self, randomness_engine: RandomnessEngine):
        self.randomness = randomness_engine
        self.state = LayerState(
            level=ConsciousnessLevel.CONSCIOUS,
            activation_level=0.8,
            noise_level=0.05
        )
        self._veto_threshold = 0.7
        self._goal_check_history: List[Dict] = []
    
    def goal_check(
        self, 
        current_thought: Thought, 
        goal: str,
        tolerance: float = 0.3
    ) -> Dict[str, Any]:
        """
        目标监控 - 检查当前思考是否偏离目标
        
        Args:
            current_thought: 当前思维
            goal: 目标
            tolerance: 容忍度
        
        Returns:
            检查结果
        """
        relevance = self._calculate_relevance(current_thought.content, goal)
        
        deviation = 1.0 - relevance
        
        is_deviant = deviation > tolerance
        
        result = {
            "thought": current_thought.content,
            "goal": goal,
            "relevance": relevance,
            "deviation": deviation,
            "is_deviant": is_deviant,
            "should_redirect": is_deviant and random.random() > 0.3
        }
        
        self._goal_check_history.append(result)
        if len(self._goal_check_history) > 100:
            self._goal_check_history = self._goal_check_history[-100:]
        
        return result
    
    def _calculate_relevance(self, thought_content: Any, goal: str) -> float:
        """计算相关性（简化版）"""
        if isinstance(thought_content, str):
            goal_words = set(goal.lower().split())
            thought_words = set(str(thought_content).lower().split())
            common = goal_words & thought_words
            if goal_words:
                return len(common) / len(goal_words)
        return random.random()
    
    def logical_reasoning(
        self, 
        premises: List[Any],
        context: Optional[Dict] = None
    ) -> Thought:
        """
        逻辑推理 - 进行有意识的逻辑分析
        
        Args:
            premises: 前提条件
            context: 上下文
        
        Returns:
            推理结果思维
        """
        reasoning_methods = [
            "演绎推理", "归纳推理", "类比推理", "因果推理",
            "逆向推理", "假设检验", "排除法", "综合分析"
        ]
        
        method = self.randomness.random_choice(
            reasoning_methods,
            randomness_type=RandomnessType.QUANTUM
        )
        
        conclusion = f"通过{method}，基于{len(premises)}个前提得出结论"
        
        return Thought(
            content=conclusion,
            level=ConsciousnessLevel.CONSCIOUS,
            strength=0.8,
            metadata={
                "method": method,
                "premises_count": len(premises),
                "context": context
            }
        )
    
    def veto(self, impulse: Thought) -> Dict[str, Any]:
        """
        否决权 - 可以阻止潜意识产生的冲动
        
        基于里贝特实验：显意识有"自由否决"能力
        
        Args:
            impulse: 冲动思维
        
        Returns:
            否决结果
        """
        veto_decision = False
        veto_reason = None
        
        if impulse.level in [ConsciousnessLevel.SUBCONSCIOUS, ConsciousnessLevel.UNCONSCIOUS]:
            if impulse.strength > self._veto_threshold:
                veto_decision = self.randomness.random_choice(
                    [True, False],
                    weights=[0.3, 0.7],
                    randomness_type=RandomnessType.QUANTUM
                )
                if veto_decision:
                    veto_reason = self.randomness.random_choice([
                        "不符合当前目标",
                        "可能带来负面后果",
                        "需要更多信息",
                        "直觉建议谨慎",
                        "时机不合适"
                    ])
        
        return {
            "impulse": impulse.content,
            "vetoed": veto_decision,
            "reason": veto_reason,
            "impulse_strength": impulse.strength
        }
    
    def convergence_check(
        self, 
        progress: List[Thought],
        goal: str,
        min_progress: int = 5
    ) -> Dict[str, Any]:
        """
        收敛判断 - 决定何时停止发散，开始收敛
        
        Args:
            progress: 进度列表
            goal: 目标
            min_progress: 最小进度数
        
        Returns:
            收敛判断结果
        """
        if len(progress) < min_progress:
            return {
                "should_converge": False,
                "reason": "进度不足",
                "progress_count": len(progress)
            }
        
        recent_relevance = []
        for thought in progress[-5:]:
            result = self.goal_check(thought, goal)
            recent_relevance.append(result["relevance"])
        
        avg_relevance = sum(recent_relevance) / len(recent_relevance) if recent_relevance else 0
        
        convergence_score = avg_relevance * 0.6 + (len(progress) / 20) * 0.4
        
        should_converge = convergence_score > 0.5 or len(progress) > 15
        
        return {
            "should_converge": should_converge,
            "convergence_score": convergence_score,
            "avg_relevance": avg_relevance,
            "progress_count": len(progress),
            "reason": "达到收敛条件" if should_converge else "继续探索"
        }
    
    def add_thought(self, thought: Thought):
        """添加思维到显意识层"""
        if thought.level != ConsciousnessLevel.CONSCIOUS:
            thought = Thought(
                content=thought.content,
                level=ConsciousnessLevel.CONSCIOUS,
                strength=thought.strength * 0.8,
                metadata=thought.metadata
            )
        self.state.active_thoughts.append(thought)
        if len(self.state.active_thoughts) > 10:
            self.state.active_thoughts = self.state.active_thoughts[-10:]


class PreconsciousLayer:
    """
    前意识层
    
    神经基础：海马体、皮层存储区
    时间尺度：中
    能耗：中
    
    功能：
    - 记忆存储：长期记忆的仓库
    - 知识检索：根据线索调取相关知识
    - 经验匹配：将当前情境与过去经验对比
    - 可调用性：随时可以被意识访问
    """
    
    def __init__(self, randomness_engine: RandomnessEngine):
        self.randomness = randomness_engine
        self.state = LayerState(
            level=ConsciousnessLevel.PRECONSCIOUS,
            activation_level=0.6,
            noise_level=0.1
        )
        self._memory_store: Dict[str, List[Any]] = {}
        self._knowledge_index: Dict[str, List[str]] = {}
    
    def store_memory(self, experience: Any, category: str = "general"):
        """
        存储记忆
        
        Args:
            experience: 经验内容
            category: 类别
        """
        if category not in self._memory_store:
            self._memory_store[category] = []
        
        self._memory_store[category].append({
            "content": experience,
            "timestamp": time.time(),
            "access_count": 0
        })
        
        self._update_index(experience, category)
    
    def _update_index(self, experience: Any, category: str):
        """更新索引"""
        if isinstance(experience, str):
            words = experience.lower().split()
            for word in words:
                if word not in self._knowledge_index:
                    self._knowledge_index[word] = []
                if category not in self._knowledge_index[word]:
                    self._knowledge_index[word].append(category)
    
    def retrieve_knowledge(
        self, 
        cue: str,
        max_results: int = 5
    ) -> List[Thought]:
        """
        知识检索 - 根据线索调取相关知识
        
        Args:
            cue: 检索线索
            max_results: 最大结果数
        
        Returns:
            检索到的知识列表
        """
        results = []
        
        if isinstance(cue, str):
            words = cue.lower().split()
            relevant_categories = set()
            
            for word in words:
                if word in self._knowledge_index:
                    relevant_categories.update(self._knowledge_index[word])
            
            for category in relevant_categories:
                if category in self._memory_store:
                    for memory in self._memory_store[category]:
                        memory["access_count"] += 1
                        results.append(Thought(
                            content=memory["content"],
                            level=ConsciousnessLevel.PRECONSCIOUS,
                            strength=0.6,
                            metadata={
                                "category": category,
                                "access_count": memory["access_count"]
                            }
                        ))
        
        if len(results) > max_results:
            results = self.randomness.random_choice(
                results,
                randomness_type=RandomnessType.NEURAL_NOISE
            )
            if not isinstance(results, list):
                results = [results]
        
        return results[:max_results]
    
    def match_experience(
        self, 
        situation: Any,
        threshold: float = 0.3
    ) -> List[Thought]:
        """
        经验匹配 - 将当前情境与过去经验对比
        
        Args:
            situation: 当前情境
            threshold: 匹配阈值
        
        Returns:
            匹配的经验列表
        """
        matches = []
        
        for category, memories in self._memory_store.items():
            for memory in memories:
                similarity = self._calculate_similarity(situation, memory["content"])
                if similarity > threshold:
                    matches.append(Thought(
                        content=memory["content"],
                        level=ConsciousnessLevel.PRECONSCIOUS,
                        strength=similarity,
                        metadata={
                            "category": category,
                            "similarity": similarity,
                            "original_situation": situation
                        }
                    ))
        
        matches.sort(key=lambda x: x.strength, reverse=True)
        return matches[:5]
    
    def _calculate_similarity(self, a: Any, b: Any) -> float:
        """计算相似度"""
        if isinstance(a, str) and isinstance(b, str):
            words_a = set(a.lower().split())
            words_b = set(b.lower().split())
            common = words_a & words_b
            union = words_a | words_b
            if union:
                return len(common) / len(union)
        return random.random() * 0.5
    
    def random_activation(self) -> Optional[Thought]:
        """
        随机激活 - 随机激活一个记忆
        
        Returns:
            激活的思维，如果没有则返回None
        """
        if random.random() < 0.1:
            all_memories = []
            for memories in self._memory_store.values():
                all_memories.extend(memories)
            
            if all_memories:
                memory = self.randomness.random_choice(
                    all_memories,
                    randomness_type=RandomnessType.QUANTUM
                )
                return Thought(
                    content=memory["content"],
                    level=ConsciousnessLevel.PRECONSCIOUS,
                    strength=0.4,
                    metadata={"activation_type": "random"}
                )
        
        return None


class SubconsciousLayer:
    """
    潜意识层
    
    神经基础：边缘系统、杏仁核、基底神经节
    时间尺度：快（毫秒级）
    能耗：低
    
    功能：
    - 欲望引擎：产生深层动机和欲望
    - 情感驱动：情绪影响思考方向
    - 直觉来源：快速、自动的判断
    - 模式识别：自动识别情境模式
    """
    
    def __init__(self, randomness_engine: RandomnessEngine):
        self.randomness = randomness_engine
        self.state = LayerState(
            level=ConsciousnessLevel.SUBCONSCIOUS,
            activation_level=0.4,
            noise_level=0.2
        )
        self._desires: List[Dict] = []
        self._emotional_state: Dict[str, float] = {
            "joy": 0.5,
            "fear": 0.3,
            "anger": 0.2,
            "sadness": 0.2,
            "surprise": 0.3,
            "curiosity": 0.6
        }
        self._intuition_history: List[Dict] = []
    
    def generate_desire(
        self, 
        context: Optional[Dict] = None
    ) -> Thought:
        """
        欲望引擎 - 产生深层动机和欲望
        
        Args:
            context: 上下文
        
        Returns:
            欲望思维
        """
        desire_types = [
            "探索欲", "求知欲", "创造欲", "成就欲",
            "社交欲", "安全欲", "自由欲", "表达欲"
        ]
        
        desire_type = self.randomness.random_choice(
            desire_types,
            randomness_type=RandomnessType.CREATIVE
        )
        
        intensity = random.random()
        
        desire = {
            "type": desire_type,
            "intensity": intensity,
            "context": context,
            "timestamp": time.time()
        }
        self._desires.append(desire)
        
        return Thought(
            content=f"产生{desire_type}（强度：{intensity:.2f}）",
            level=ConsciousnessLevel.SUBCONSCIOUS,
            strength=intensity,
            metadata={
                "desire_type": desire_type,
                "context": context
            }
        )
    
    def emotional_drive(
        self, 
        emotion: Optional[str] = None
    ) -> Thought:
        """
        情感驱动 - 情绪影响思考方向
        
        Args:
            emotion: 指定情绪，None则使用当前主导情绪
        
        Returns:
            情感驱动的思维
        """
        if emotion is None:
            dominant_emotion = max(
                self._emotional_state.items(),
                key=lambda x: x[1]
            )
            emotion = dominant_emotion[0]
        
        emotion_thoughts = {
            "joy": ["这让我感到愉悦", "也许可以尝试更多", "一切都很顺利"],
            "fear": ["需要谨慎", "可能存在风险", "应该做好准备"],
            "anger": ["这不公平", "需要改变", "应该采取行动"],
            "sadness": ["有些遗憾", "需要时间", "也许需要放手"],
            "surprise": ["没想到会这样", "需要重新评估", "有趣的发展"],
            "curiosity": ["想知道更多", "这是什么原理", "有没有其他可能"]
        }
        
        thoughts = emotion_thoughts.get(emotion, ["有一种感觉..."])
        
        content = self.randomness.random_choice(
            thoughts,
            randomness_type=RandomnessType.QUANTUM
        )
        
        intensity = self._emotional_state.get(emotion, 0.5)
        
        return Thought(
            content=f"[{emotion}] {content}",
            level=ConsciousnessLevel.SUBCONSCIOUS,
            strength=intensity,
            metadata={
                "emotion": emotion,
                "intensity": intensity
            }
        )
    
    def intuition_flash(
        self, 
        situation: Any
    ) -> Thought:
        """
        直觉闪现 - 快速、自动的判断
        
        Args:
            situation: 情境
        
        Returns:
            直觉思维
        """
        intuition_types = [
            "感觉不对劲", "这个方向是对的", "需要小心",
            "可以信任", "有隐藏的东西", "即将有变化",
            "应该这样做", "这个很重要", "可以忽略"
        ]
        
        content = self.randomness.random_choice(
            intuition_types,
            randomness_type=RandomnessType.CREATIVE
        )
        
        confidence = random.random()
        
        self._intuition_history.append({
            "situation": situation,
            "intuition": content,
            "confidence": confidence,
            "timestamp": time.time()
        })
        
        return Thought(
            content=f"直觉：{content}",
            level=ConsciousnessLevel.SUBCONSCIOUS,
            strength=confidence,
            metadata={
                "intuition_type": content,
                "confidence": confidence,
                "situation": str(situation)[:100]
            }
        )
    
    def pattern_recognition(
        self, 
        input_data: Any
    ) -> Optional[Thought]:
        """
        模式识别 - 自动识别情境模式
        
        Args:
            input_data: 输入数据
        
        Returns:
            识别结果思维
        """
        patterns = [
            "重复出现的模式",
            "与过去相似的情况",
            "潜在的趋势",
            "隐藏的关联",
            "异常信号"
        ]
        
        if random.random() < 0.3:
            pattern = self.randomness.random_choice(
                patterns,
                randomness_type=RandomnessType.QUANTUM
            )
            
            return Thought(
                content=f"识别到：{pattern}",
                level=ConsciousnessLevel.SUBCONSCIOUS,
                strength=0.5,
                metadata={
                    "pattern": pattern,
                    "input": str(input_data)[:100]
                }
            )
        
        return None
    
    def update_emotional_state(
        self, 
        emotion: str, 
        delta: float
    ):
        """更新情绪状态"""
        if emotion in self._emotional_state:
            self._emotional_state[emotion] = max(
                0.0,
                min(1.0, self._emotional_state[emotion] + delta)
            )
    
    def get_dominant_emotion(self) -> tuple:
        """获取主导情绪"""
        return max(
            self._emotional_state.items(),
            key=lambda x: x[1]
        )


class UnconsciousLayer:
    """
    无意识层
    
    神经基础：脑干、脊髓、自主神经系统
    时间尺度：极快（<12毫秒）
    能耗：极低
    
    功能：
    - 本能反应：生存相关的自动反应
    - 习惯执行：自动化行为模式
    - 快速响应：无需思考的即时反应
    - 生理调节：维持基本生命功能
    """
    
    def __init__(self, randomness_engine: RandomnessEngine):
        self.randomness = randomness_engine
        self.state = LayerState(
            level=ConsciousnessLevel.UNCONSCIOUS,
            activation_level=0.3,
            noise_level=0.3
        )
        self._instincts: Dict[str, float] = {
            "survival": 0.9,
            "safety": 0.8,
            "reproduction": 0.7,
            "social": 0.6,
            "exploration": 0.5
        }
        self._habits: List[Dict] = []
        self._response_history: List[Dict] = []
    
    def instinct_reaction(
        self, 
        stimulus: Any,
        threshold: float = 0.5
    ) -> Optional[Thought]:
        """
        本能反应 - 生存相关的自动反应
        
        Args:
            stimulus: 刺激
            threshold: 反应阈值
        
        Returns:
            反应思维
        """
        instinct_responses = {
            "survival": ["立即行动", "寻找安全", "保护自己"],
            "safety": ["检查环境", "保持警惕", "准备应对"],
            "reproduction": ["吸引注意", "展示价值", "建立联系"],
            "social": ["寻求群体", "建立连接", "获得认可"],
            "exploration": ["探索未知", "尝试新事物", "扩展边界"]
        }
        
        for instinct, base_strength in self._instincts.items():
            if random.random() < base_strength * 0.1:
                responses = instinct_responses.get(instinct, ["本能反应"])
                content = self.randomness.random_choice(
                    responses,
                    randomness_type=RandomnessType.QUANTUM
                )
                
                return Thought(
                    content=f"[本能-{instinct}] {content}",
                    level=ConsciousnessLevel.UNCONSCIOUS,
                    strength=base_strength,
                    metadata={
                        "instinct": instinct,
                        "stimulus": str(stimulus)[:50]
                    }
                )
        
        return None
    
    def execute_habit(
        self, 
        context: Dict
    ) -> Optional[Thought]:
        """
        习惯执行 - 自动化行为模式
        
        Args:
            context: 上下文
        
        Returns:
            习惯思维
        """
        for habit in self._habits:
            if self._match_context(context, habit.get("trigger", {})):
                if random.random() < habit.get("strength", 0.5):
                    return Thought(
                        content=f"习惯性：{habit['action']}",
                        level=ConsciousnessLevel.UNCONSCIOUS,
                        strength=habit.get("strength", 0.5),
                        metadata={
                            "habit_id": habit.get("id"),
                            "habit_name": habit.get("name")
                        }
                    )
        
        return None
    
    def _match_context(self, context: Dict, trigger: Dict) -> bool:
        """匹配上下文"""
        if not trigger:
            return False
        
        matches = 0
        for key, value in trigger.items():
            if key in context and context[key] == value:
                matches += 1
        
        return matches > 0
    
    def quick_response(
        self, 
        threat_level: float = 0.5
    ) -> Thought:
        """
        快速响应 - 无需思考的即时反应
        
        模拟杏仁核的快速通路（12毫秒）
        
        Args:
            threat_level: 威胁等级
        
        Returns:
            快速响应思维
        """
        responses = [
            "立即反应", "快速评估", "准备行动",
            "保持警觉", "寻找掩护", "评估风险"
        ]
        
        content = self.randomness.random_choice(
            responses,
            randomness_type=RandomnessType.QUANTUM
        )
        
        response_time = random.uniform(0.01, 0.05)
        
        self._response_history.append({
            "response": content,
            "threat_level": threat_level,
            "response_time": response_time,
            "timestamp": time.time()
        })
        
        return Thought(
            content=f"[快速响应] {content}",
            level=ConsciousnessLevel.UNCONSCIOUS,
            strength=threat_level,
            metadata={
                "response_time": response_time,
                "threat_level": threat_level
            }
        )
    
    def add_habit(
        self, 
        name: str, 
        action: str, 
        trigger: Dict, 
        strength: float = 0.5
    ):
        """添加习惯"""
        self._habits.append({
            "id": len(self._habits),
            "name": name,
            "action": action,
            "trigger": trigger,
            "strength": strength,
            "created_at": time.time()
        })
    
    def neural_noise_base(self) -> float:
        """
        基础神经噪声 - 底层随机性来源
        
        Returns:
            噪声值
        """
        return self.randomness.inject_randomness(0.0, 0.3)


class ConsciousnessLayers:
    """
    意识层次系统 - 整合所有意识层
    
    管理四个意识层次的交互和信息流动
    """
    
    def __init__(self, randomness_engine: Optional[RandomnessEngine] = None):
        self.randomness = randomness_engine or RandomnessEngine()
        
        self.conscious = ConsciousLayer(self.randomness)
        self.preconscious = PreconsciousLayer(self.randomness)
        self.subconscious = SubconsciousLayer(self.randomness)
        self.unconscious = UnconsciousLayer(self.randomness)
        
        self._layer_interactions: List[Dict] = []
    
    def process(
        self, 
        input_thought: Optional[Thought] = None,
        goal: Optional[str] = None
    ) -> Thought:
        """
        处理思维 - 通过所有层次处理
        
        Args:
            input_thought: 输入思维
            goal: 当前目标
        
        Returns:
            处理后的思维
        """
        thoughts_queue = []
        
        if input_thought:
            thoughts_queue.append(input_thought)
        
        unconscious_thought = self.unconscious.instinct_reaction("processing")
        if unconscious_thought:
            thoughts_queue.append(unconscious_thought)
        
        spontaneous = self.unconscious.neural_noise_base()
        if abs(spontaneous) > 0.1:
            thoughts_queue.append(Thought(
                content=f"自发活动（强度：{abs(spontaneous):.2f}）",
                level=ConsciousnessLevel.UNCONSCIOUS,
                strength=abs(spontaneous)
            ))
        
        if random.random() < 0.2:
            intuition = self.subconscious.intuition_flash("current_context")
            thoughts_queue.append(intuition)
        
        if random.random() < 0.15:
            emotion_thought = self.subconscious.emotional_drive()
            thoughts_queue.append(emotion_thought)
        
        if random.random() < 0.1:
            random_memory = self.preconscious.random_activation()
            if random_memory:
                thoughts_queue.append(random_memory)
        
        if thoughts_queue:
            selected = self.randomness.random_choice(
                thoughts_queue,
                weights=[t.strength for t in thoughts_queue],
                randomness_type=RandomnessType.QUANTUM
            )
            
            if selected.level != ConsciousnessLevel.CONSCIOUS:
                veto_result = self.conscious.veto(selected)
                if veto_result["vetoed"]:
                    return Thought(
                        content=f"[已否决] {selected.content} - 原因：{veto_result['reason']}",
                        level=ConsciousnessLevel.CONSCIOUS,
                        strength=0.3,
                        metadata={"vetoed": True, "original_level": selected.level.value}
                    )
            
            if goal:
                check_result = self.conscious.goal_check(selected, goal)
                if check_result["should_redirect"]:
                    return Thought(
                        content=f"[目标引导] 回到目标：{goal}",
                        level=ConsciousnessLevel.CONSCIOUS,
                        strength=0.7,
                        metadata={"redirected": True, "original_thought": selected.content}
                    )
            
            return selected
        
        return Thought(
            content="等待输入...",
            level=ConsciousnessLevel.CONSCIOUS,
            strength=0.1
        )
    
    def bottom_up_flow(self) -> List[Thought]:
        """
        自下而上的信息流
        
        无意识 → 潜意识 → 前意识 → 显意识
        
        Returns:
            涌现的思维列表
        """
        emerging_thoughts = []
        
        instinct = self.unconscious.instinct_reaction("spontaneous")
        if instinct:
            emerging_thoughts.append(instinct)
        
        intuition = self.subconscious.intuition_flash("emerging")
        if intuition:
            emerging_thoughts.append(intuition)
        
        memory = self.preconscious.random_activation()
        if memory:
            emerging_thoughts.append(memory)
        
        self._record_interaction("bottom_up", len(emerging_thoughts))
        
        return emerging_thoughts
    
    def top_down_flow(
        self, 
        goal: str,
        focus_area: Optional[str] = None
    ) -> List[Thought]:
        """
        自上而下的信息流
        
        显意识 → 前意识 → 潜意识 → 无意识
        
        Args:
            goal: 目标
            focus_area: 聚焦区域
        
        Returns:
            引导的思维列表
        """
        guided_thoughts = []
        
        goal_thought = Thought(
            content=f"聚焦目标：{goal}",
            level=ConsciousnessLevel.CONSCIOUS,
            strength=0.9
        )
        guided_thoughts.append(goal_thought)
        
        relevant_knowledge = self.preconscious.retrieve_knowledge(goal)
        guided_thoughts.extend(relevant_knowledge[:2])
        
        self.subconscious.update_emotional_state("curiosity", 0.1)
        
        self._record_interaction("top_down", len(guided_thoughts))
        
        return guided_thoughts
    
    def random_penetration(self) -> Optional[Thought]:
        """
        随机穿透 - 任何层都可以随机影响其他层
        
        Returns:
            随机穿透的思维
        """
        layers = [
            (self.conscious, ConsciousnessLevel.CONSCIOUS),
            (self.preconscious, ConsciousnessLevel.PRECONSCIOUS),
            (self.subconscious, ConsciousnessLevel.SUBCONSCIOUS),
            (self.unconscious, ConsciousnessLevel.UNCONSCIOUS),
        ]
        
        source_layer, source_level = self.randomness.random_choice(
            layers,
            randomness_type=RandomnessType.CREATIVE
        )
        
        target_layer, target_level = self.randomness.random_choice(
            layers,
            randomness_type=RandomnessType.CREATIVE
        )
        
        if source_level == target_level:
            return None
        
        penetration_types = [
            "灵感闪现", "梦境影响", "直觉突破",
            "习惯打破", "情绪渗透", "记忆涌现"
        ]
        
        penetration_type = self.randomness.random_choice(
            penetration_types,
            randomness_type=RandomnessType.QUANTUM
        )
        
        self._record_interaction(
            "penetration",
            {
                "from": source_level.value,
                "to": target_level.value,
                "type": penetration_type
            }
        )
        
        return Thought(
            content=f"[{penetration_type}] {source_level.value} → {target_level.value}",
            level=target_level,
            strength=random.random(),
            metadata={
                "penetration_type": penetration_type,
                "source_level": source_level.value,
                "target_level": target_level.value
            }
        )
    
    def _record_interaction(self, flow_type: str, data: Any):
        """记录层次交互"""
        self._layer_interactions.append({
            "type": flow_type,
            "data": data,
            "timestamp": time.time()
        })
        
        if len(self._layer_interactions) > 1000:
            self._layer_interactions = self._layer_interactions[-1000:]
    
    def get_state_summary(self) -> Dict[str, Any]:
        """获取状态摘要"""
        return {
            "conscious": {
                "activation": self.conscious.state.activation_level,
                "active_thoughts": len(self.conscious.state.active_thoughts)
            },
            "preconscious": {
                "activation": self.preconscious.state.activation_level,
                "memory_categories": len(self.preconscious._memory_store)
            },
            "subconscious": {
                "activation": self.subconscious.state.activation_level,
                "dominant_emotion": self.subconscious.get_dominant_emotion()
            },
            "unconscious": {
                "activation": self.unconscious.state.activation_level,
                "habits_count": len(self.unconscious._habits)
            },
            "interactions_count": len(self._layer_interactions)
        }
    
    def store_experience(self, experience: Any, category: str = "general"):
        """存储经验到前意识"""
        self.preconscious.store_memory(experience, category)
    
    def add_habit(
        self, 
        name: str, 
        action: str, 
        trigger: Dict, 
        strength: float = 0.5
    ):
        """添加习惯到无意识"""
        self.unconscious.add_habit(name, action, trigger, strength)
