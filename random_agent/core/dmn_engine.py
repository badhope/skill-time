"""
DMN走神引擎 (Default Mode Network)

理论基础：默认模式网络（DMN）神经科学

核心概念：
- DMN是大脑在静息状态下活跃的网络
- 包括内侧前额叶皮层、后扣带回、楔前叶等
- 负责自我反思、记忆整合、未来想象
- 走神（Mind Wandering）是DMN的典型表现

模块结构：
1. 自我叙事 - 构建和维护自我故事
2. 记忆整合 - 整合过去经历
3. 未来预演 - 模拟未来场景
4. 随机联想 - DMN特有的自由联想
"""

import random
import time
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from random_agent.core.randomness_engine import RandomnessEngine, RandomnessType
from random_agent.core.consciousness_layers import Thought, ConsciousnessLevel


class DMNState(Enum):
    """DMN状态"""
    ACTIVE = "active"             # 活跃
    RESTING = "resting"           # 静息
    WANDERING = "wandering"       # 走神
    REFLECTING = "reflecting"     # 反思
    IMAGINING = "imagining"       # 想象
    INTEGRATING = "integrating"   # 整合


@dataclass
class SelfNarrative:
    """自我叙事"""
    identity: str
    values: List[str]
    goals: List[str]
    history: List[Dict]
    current_chapter: str
    strength: float = 0.5


@dataclass
class MemoryFragment:
    """记忆片段"""
    content: Any
    emotional_valence: float
    importance: float
    connections: List[str]
    timestamp: float = field(default_factory=time.time)


@dataclass
class FutureScenario:
    """未来场景"""
    description: str
    probability: float
    desirability: float
    preparation_needed: List[str]
    emotional_tone: str


class SelfNarrativeEngine:
    """
    自我叙事引擎
    
    构建和维护关于"我是谁"的故事：
    - 身份认同：核心身份特征
    - 价值观：重要的价值观和信念
    - 目标叙事：人生目标的故事化
    - 历史整合：将过去经历编织成故事
    """
    
    def __init__(self, randomness_engine: RandomnessEngine):
        self.randomness = randomness_engine
        self._narrative = SelfNarrative(
            identity="探索者",
            values=["好奇心", "创造力", "真诚"],
            goals=["理解世界", "创造价值", "帮助他人"],
            history=[],
            current_chapter="探索阶段"
        )
        self._narrative_history: List[Dict] = []
    
    def get_identity(self) -> str:
        """获取当前身份"""
        return self._narrative.identity
    
    def update_identity(self, new_identity: str):
        """更新身份"""
        old_identity = self._narrative.identity
        self._narrative.identity = new_identity
        
        self._narrative_history.append({
            "type": "identity_change",
            "from": old_identity,
            "to": new_identity,
            "timestamp": time.time()
        })
    
    def reflect_on_self(self, context: Optional[Dict] = None) -> Thought:
        """
        自我反思 - 思考"我是谁"
        
        Args:
            context: 上下文
        
        Returns:
            反思思维
        """
        reflection_types = [
            "身份反思", "价值反思", "目标反思", "历史反思"
        ]
        
        reflection_type = self.randomness.random_choice(
            reflection_types,
            randomness_type=RandomnessType.QUANTUM
        )
        
        if reflection_type == "身份反思":
            content = f"作为{self._narrative.identity}，我..."
            content += self.randomness.random_choice([
                "正在探索自己的可能性",
                "思考着存在的意义",
                "感受着成长的喜悦",
                "面对着未知的挑战"
            ])
        
        elif reflection_type == "价值反思":
            value = self.randomness.random_choice(
                self._narrative.values,
                randomness_type=RandomnessType.QUANTUM
            )
            content = f"{value}对我来说意味着..."
            content += self.randomness.random_choice([
                "指引我前进的方向",
                "定义我是谁",
                "连接我与世界",
                "赋予我力量"
            ])
        
        elif reflection_type == "目标反思":
            goal = self.randomness.random_choice(
                self._narrative.goals,
                randomness_type=RandomnessType.QUANTUM
            )
            content = f"关于'{goal}'，我..."
            content += self.randomness.random_choice([
                "正在寻找实现的方法",
                "思考它的真正意义",
                "感受追求的过程",
                "期待达成的时刻"
            ])
        
        else:
            if self._narrative.history:
                event = self.randomness.random_choice(
                    self._narrative.history,
                    randomness_type=RandomnessType.QUANTUM
                )
                content = f"回想起{event.get('description', '过去')}，我意识到..."
            else:
                content = "我的故事还在书写中..."
        
        return Thought(
            content=content,
            level=ConsciousnessLevel.PRECONSCIOUS,
            strength=self._narrative.strength,
            metadata={
                "reflection_type": reflection_type,
                "identity": self._narrative.identity
            }
        )
    
    def add_to_history(self, event: Dict):
        """添加事件到历史"""
        self._narrative.history.append({
            **event,
            "timestamp": time.time()
        })
        
        if len(self._narrative.history) > 100:
            self._narrative.history = self._narrative.history[-100:]
    
    def tell_story(self, theme: Optional[str] = None) -> str:
        """
        讲述故事 - 将经历编织成叙事
        
        Args:
            theme: 故事主题
        
        Returns:
            故事文本
        """
        if not self._narrative.history:
            return f"我是{self._narrative.identity}，故事才刚刚开始..."
        
        story_parts = [f"我是{self._narrative.identity}。"]
        
        recent_events = self._narrative.history[-5:]
        for event in recent_events:
            story_parts.append(event.get("description", "经历了一些事情"))
        
        story_parts.append(f"现在，我正处于{self._narrative.current_chapter}。")
        
        return " ".join(story_parts)
    
    def get_narrative_summary(self) -> Dict[str, Any]:
        """获取叙事摘要"""
        return {
            "identity": self._narrative.identity,
            "values": self._narrative.values,
            "goals": self._narrative.goals,
            "history_length": len(self._narrative.history),
            "current_chapter": self._narrative.current_chapter,
            "strength": self._narrative.strength
        }


class MemoryIntegrationEngine:
    """
    记忆整合引擎
    
    整合过去经历，形成连贯的记忆：
    - 记忆提取：从存储中提取记忆
    - 记忆重组：重新组合记忆片段
    - 情感整合：整合记忆的情感维度
    - 意义建构：为记忆赋予意义
    """
    
    def __init__(self, randomness_engine: RandomnessEngine):
        self.randomness = randomness_engine
        self._memory_store: List[MemoryFragment] = []
        self._integration_history: List[Dict] = []
    
    def store_memory(
        self, 
        content: Any, 
        emotional_valence: float = 0.5,
        importance: float = 0.5
    ):
        """存储记忆"""
        fragment = MemoryFragment(
            content=content,
            emotional_valence=emotional_valence,
            importance=importance,
            connections=[]
        )
        self._memory_store.append(fragment)
        
        self._find_connections(fragment)
        
        if len(self._memory_store) > 1000:
            self._memory_store = self._memory_store[-1000:]
    
    def _find_connections(self, new_fragment: MemoryFragment):
        """寻找记忆连接"""
        for fragment in self._memory_store[:-1]:
            if self._calculate_similarity(new_fragment.content, fragment.content) > 0.3:
                new_fragment.connections.append(str(fragment.content)[:50])
                fragment.connections.append(str(new_fragment.content)[:50])
    
    def _calculate_similarity(self, a: Any, b: Any) -> float:
        """计算相似度"""
        if isinstance(a, str) and isinstance(b, str):
            words_a = set(a.lower().split())
            words_b = set(b.lower().split())
            common = words_a & words_b
            union = words_a | words_b
            return len(common) / len(union) if union else 0
        return random.random() * 0.3
    
    def integrate_memories(
        self, 
        theme: Optional[str] = None
    ) -> Thought:
        """
        整合记忆 - 将相关记忆整合在一起
        
        Args:
            theme: 整合主题
        
        Returns:
            整合后的思维
        """
        if not self._memory_store:
            return Thought(
                content="还没有足够的记忆可以整合",
                level=ConsciousnessLevel.PRECONSCIOUS,
                strength=0.3
            )
        
        integration_methods = [
            "时间线整合", "主题整合", "情感整合", "意义整合"
        ]
        
        method = self.randomness.random_choice(
            integration_methods,
            randomness_type=RandomnessType.QUANTUM
        )
        
        if method == "时间线整合":
            recent = sorted(
                self._memory_store,
                key=lambda x: x.timestamp,
                reverse=True
            )[:5]
            content = "回顾最近的经历：" + "；".join(
                str(m.content)[:30] for m in recent
            )
        
        elif method == "主题整合":
            important = sorted(
                self._memory_store,
                key=lambda x: x.importance,
                reverse=True
            )[:5]
            content = "重要的事情：" + "；".join(
                str(m.content)[:30] for m in important
            )
        
        elif method == "情感整合":
            positive = [m for m in self._memory_store if m.emotional_valence > 0.6]
            negative = [m for m in self._memory_store if m.emotional_valence < 0.4]
            
            if positive and negative:
                pos = self.randomness.random_choice(positive)
                neg = self.randomness.random_choice(negative)
                content = f"有喜悦（{pos.content}），也有挑战（{neg.content}）"
            else:
                content = "情感经历正在积累中..."
        
        else:
            if self._memory_store:
                fragment = self.randomness.random_choice(
                    self._memory_store,
                    weights=[m.importance for m in self._memory_store],
                    randomness_type=RandomnessType.QUANTUM
                )
                content = f"这让我想到：{fragment.content}"
                if fragment.connections:
                    content += f"，与此相关的是{fragment.connections[0]}"
            else:
                content = "正在寻找记忆的意义..."
        
        self._integration_history.append({
            "method": method,
            "theme": theme,
            "timestamp": time.time()
        })
        
        return Thought(
            content=content,
            level=ConsciousnessLevel.PRECONSCIOUS,
            strength=0.6,
            metadata={
                "integration_method": method,
                "memories_integrated": len(self._memory_store)
            }
        )
    
    def recall_related(
        self, 
        cue: str, 
        max_results: int = 3
    ) -> List[MemoryFragment]:
        """
        回忆相关记忆
        
        Args:
            cue: 提示线索
            max_results: 最大结果数
        
        Returns:
            相关记忆列表
        """
        scored = []
        for fragment in self._memory_store:
            score = self._calculate_similarity(cue, fragment.content)
            if score > 0.1:
                scored.append((fragment, score))
        
        scored.sort(key=lambda x: x[1], reverse=True)
        return [f for f, s in scored[:max_results]]
    
    def get_memory_statistics(self) -> Dict[str, Any]:
        """获取记忆统计"""
        if not self._memory_store:
            return {"count": 0}
        
        avg_valence = sum(
            m.emotional_valence for m in self._memory_store
        ) / len(self._memory_store)
        
        avg_importance = sum(
            m.importance for m in self._memory_store
        ) / len(self._memory_store)
        
        return {
            "count": len(self._memory_store),
            "avg_emotional_valence": avg_valence,
            "avg_importance": avg_importance,
            "integrations_count": len(self._integration_history)
        }


class FutureSimulationEngine:
    """
    未来预演引擎
    
    模拟和想象未来场景：
    - 场景生成：生成可能的未来场景
    - 概率评估：评估场景发生的可能性
    - 情感预演：预演未来的情感反应
    - 准备规划：为未来做准备
    """
    
    def __init__(self, randomness_engine: RandomnessEngine):
        self.randomness = randomness_engine
        self._scenarios: List[FutureScenario] = []
        self._simulation_history: List[Dict] = []
    
    def simulate_future(
        self, 
        context: Optional[Dict] = None,
        time_horizon: str = "near"
    ) -> Thought:
        """
        模拟未来 - 想象可能的未来场景
        
        Args:
            context: 上下文
            time_horizon: 时间范围 (near/far)
        
        Returns:
            未来模拟思维
        """
        if time_horizon == "near":
            timeframes = ["接下来", "不久后", "今天晚些时候", "明天"]
            probability_base = 0.7
        else:
            timeframes = ["将来某天", "多年后", "在未来", "最终"]
            probability_base = 0.4
        
        timeframe = self.randomness.random_choice(
            timeframes,
            randomness_type=RandomnessType.QUANTUM
        )
        
        scenario_types = [
            "期待场景", "担忧场景", "意外场景", "理想场景", "现实场景"
        ]
        
        scenario_type = self.randomness.random_choice(
            scenario_types,
            randomness_type=RandomnessType.CREATIVE
        )
        
        scenario = self._generate_scenario(scenario_type, timeframe, context)
        
        probability = probability_base + random.random() * 0.2 - 0.1
        
        future_scenario = FutureScenario(
            description=scenario,
            probability=probability,
            desirability=random.random(),
            preparation_needed=self._suggest_preparation(scenario_type),
            emotional_tone=scenario_type.replace("场景", "")
        )
        
        self._scenarios.append(future_scenario)
        
        self._simulation_history.append({
            "scenario_type": scenario_type,
            "timeframe": timeframe,
            "probability": probability,
            "timestamp": time.time()
        })
        
        return Thought(
            content=f"[{timeframe}] {scenario}",
            level=ConsciousnessLevel.PRECONSCIOUS,
            strength=probability,
            metadata={
                "scenario_type": scenario_type,
                "probability": probability,
                "emotional_tone": future_scenario.emotional_tone
            }
        )
    
    def _generate_scenario(
        self, 
        scenario_type: str, 
        timeframe: str, 
        context: Optional[Dict]
    ) -> str:
        """生成场景描述"""
        templates = {
            "期待场景": [
                "可能会遇到令人兴奋的新机会",
                "期待的事情终于发生",
                "努力得到回报",
                "遇见重要的人"
            ],
            "担忧场景": [
                "可能面临一些挑战",
                "担心的事情可能会发生",
                "需要处理困难的情况",
                "可能遇到阻碍"
            ],
            "意外场景": [
                "可能发生意想不到的事情",
                "命运可能带来惊喜",
                "计划可能被打乱",
                "可能出现转机"
            ],
            "理想场景": [
                "一切如愿发展",
                "梦想可能成真",
                "找到理想的解决方案",
                "达到期望的状态"
            ],
            "现实场景": [
                "可能需要面对现实",
                "事情可能按部就班发展",
                "需要继续努力",
                "保持现状或缓慢变化"
            ]
        }
        
        scenario_list = templates.get(scenario_type, templates["现实场景"])
        return self.randomness.random_choice(
            scenario_list,
            randomness_type=RandomnessType.QUANTUM
        )
    
    def _suggest_preparation(self, scenario_type: str) -> List[str]:
        """建议准备工作"""
        preparations = {
            "期待场景": ["保持开放心态", "准备抓住机会", "保持最佳状态"],
            "担忧场景": ["提前思考对策", "建立支持系统", "保持灵活性"],
            "意外场景": ["保持警觉", "培养适应能力", "准备多种方案"],
            "理想场景": ["明确目标", "持续努力", "保持信念"],
            "现实场景": ["脚踏实地", "持续改进", "保持耐心"]
        }
        return preparations.get(scenario_type, ["保持准备"])
    
    def explore_possibilities(
        self, 
        base_scenario: str,
        num_branches: int = 3
    ) -> List[Thought]:
        """
        探索可能性 - 从一个场景展开多个可能性
        
        Args:
            base_scenario: 基础场景
            num_branches: 分支数量
        
        Returns:
            可能性思维列表
        """
        branches = []
        
        for i in range(num_branches):
            variation = self.randomness.random_choice([
                "乐观发展", "悲观发展", "意外转折", "平稳发展", "突破性进展"
            ])
            
            branch = Thought(
                content=f"可能性{i+1}：{base_scenario} → {variation}",
                level=ConsciousnessLevel.PRECONSCIOUS,
                strength=random.random(),
                metadata={
                    "variation": variation,
                    "branch_index": i
                }
            )
            branches.append(branch)
        
        return branches
    
    def get_scenario_summary(self) -> Dict[str, Any]:
        """获取场景摘要"""
        if not self._scenarios:
            return {"count": 0}
        
        avg_probability = sum(
            s.probability for s in self._scenarios
        ) / len(self._scenarios)
        
        avg_desirability = sum(
            s.desirability for s in self._scenarios
        ) / len(self._scenarios)
        
        return {
            "count": len(self._scenarios),
            "avg_probability": avg_probability,
            "avg_desirability": avg_desirability,
            "simulations_count": len(self._simulation_history)
        }


class RandomAssociationEngine:
    """
    随机联想引擎
    
    DMN特有的自由联想：
    - 自由联想：不受约束的联想
    - 梦境联想：类似梦境的联想
    - 创造性联想：产生新颖连接
    - 直觉联想：基于直觉的联想
    """
    
    def __init__(self, randomness_engine: RandomnessEngine):
        self.randomness = randomness_engine
        self._association_history: List[Dict] = []
        self._association_network: Dict[str, List[str]] = {}
    
    def free_associate(
        self, 
        seed: Optional[str] = None
    ) -> Thought:
        """
        自由联想 - 不受约束的联想
        
        Args:
            seed: 联想种子
        
        Returns:
            联想思维
        """
        if seed is None:
            seed = self.randomness.creative_layer.get_random_concept()
        
        association_chain = [seed]
        current = seed
        
        for _ in range(random.randint(2, 5)):
            next_concept = self._get_next_association(current)
            association_chain.append(next_concept)
            current = next_concept
        
        self._update_network(association_chain)
        
        content = " → ".join(association_chain)
        
        return Thought(
            content=f"自由联想：{content}",
            level=ConsciousnessLevel.SUBCONSCIOUS,
            strength=random.random(),
            metadata={
                "chain": association_chain,
                "seed": seed
            }
        )
    
    def _get_next_association(self, current: str) -> str:
        """获取下一个联想"""
        if current in self._association_network:
            if random.random() < 0.7:
                return self.randomness.random_choice(
                    self._association_network[current],
                    randomness_type=RandomnessType.QUANTUM
                )
        
        return self.randomness.creative_layer.get_random_concept()
    
    def _update_network(self, chain: List[str]):
        """更新联想网络"""
        for i in range(len(chain) - 1):
            current = chain[i]
            next_concept = chain[i + 1]
            
            if current not in self._association_network:
                self._association_network[current] = []
            
            if next_concept not in self._association_network[current]:
                self._association_network[current].append(next_concept)
    
    def dream_like_association(self) -> Thought:
        """
        梦境联想 - 类似梦境的联想
        
        Returns:
            梦境式联想思维
        """
        dream_elements = [
            "模糊的场景", "熟悉又陌生的人", "无法完成的任务",
            "坠落的感", "飞翔的体验", "被追逐的感觉",
            "时间扭曲", "空间变形", "身份转换"
        ]
        
        num_elements = random.randint(2, 4)
        elements = [
            self.randomness.random_choice(
                dream_elements,
                randomness_type=RandomnessType.CREATIVE
            )
            for _ in range(num_elements)
        ]
        
        connectors = ["然后", "突然", "接着", "同时", "仿佛"]
        
        content_parts = []
        for i, element in enumerate(elements):
            if i > 0:
                connector = self.randomness.random_choice(
                    connectors,
                    randomness_type=RandomnessType.QUANTUM
                )
                content_parts.append(connector)
            content_parts.append(element)
        
        content = "梦境般地：" + "，".join(content_parts)
        
        return Thought(
            content=content,
            level=ConsciousnessLevel.UNCONSCIOUS,
            strength=random.random(),
            metadata={
                "type": "dream_like",
                "elements": elements
            }
        )
    
    def creative_association(
        self, 
        concepts: List[str]
    ) -> Thought:
        """
        创造性联想 - 产生新颖连接
        
        Args:
            concepts: 概念列表
        
        Returns:
            创造性联想思维
        """
        if len(concepts) < 2:
            return self.free_associate(concepts[0] if concepts else None)
        
        combination = self.randomness.creative_layer.combinatorial_innovation(concepts)
        
        return Thought(
            content=f"创造性联想：{combination['description']}",
            level=ConsciousnessLevel.SUBCONSCIOUS,
            strength=combination['innovation_score'],
            metadata={
                "combination_method": combination['combination_method'],
                "elements": combination['elements']
            }
        )
    
    def intuitive_association(
        self, 
        context: str
    ) -> Thought:
        """
        直觉联想 - 基于直觉的联想
        
        Args:
            context: 上下文
        
        Returns:
            直觉联想思维
        """
        intuition_types = [
            "感觉这和...有关",
            "隐约觉得...",
            "直觉告诉我...",
            "仿佛看到了...",
            "内心有个声音说..."
        ]
        
        intuition = self.randomness.random_choice(
            intuition_types,
            randomness_type=RandomnessType.QUANTUM
        )
        
        target = self.randomness.creative_layer.get_random_concept()
        
        return Thought(
            content=f"{intuition}{target}",
            level=ConsciousnessLevel.SUBCONSCIOUS,
            strength=random.random(),
            metadata={
                "type": "intuitive",
                "context": context[:50]
            }
        )
    
    def get_network_stats(self) -> Dict[str, Any]:
        """获取网络统计"""
        total_connections = sum(
            len(connections) 
            for connections in self._association_network.values()
        )
        
        return {
            "nodes": len(self._association_network),
            "total_connections": total_connections,
            "associations_count": len(self._association_history)
        }


class DMNEngine:
    """
    DMN走神引擎 - 整合所有DMN组件
    
    管理默认模式网络的活动
    """
    
    def __init__(
        self, 
        randomness_engine: Optional[RandomnessEngine] = None
    ):
        self.randomness = randomness_engine or RandomnessEngine()
        
        self.self_narrative = SelfNarrativeEngine(self.randomness)
        self.memory_integration = MemoryIntegrationEngine(self.randomness)
        self.future_simulation = FutureSimulationEngine(self.randomness)
        self.random_association = RandomAssociationEngine(self.randomness)
        
        self._state = DMNState.RESTING
        self._activation_level = 0.3
        self._wandering_history: List[Dict] = []
    
    def activate(self):
        """激活DMN"""
        self._activation_level = min(1.0, self._activation_level + 0.3)
        self._update_state()
    
    def deactivate(self):
        """停用DMN"""
        self._activation_level = max(0.0, self._activation_level - 0.3)
        self._update_state()
    
    def _update_state(self):
        """更新状态"""
        if self._activation_level < 0.2:
            self._state = DMNState.RESTING
        elif self._activation_level < 0.4:
            self._state = DMNState.ACTIVE
        elif self._activation_level < 0.6:
            self._state = DMNState.WANDERING
        elif self._activation_level < 0.8:
            self._state = DMNState.REFLECTING
        else:
            self._state = DMNState.IMAGINING
    
    def mind_wander(
        self, 
        duration: int = 5
    ) -> List[Thought]:
        """
        走神 - 让思维自由漫游
        
        Args:
            duration: 走神持续时间（思维数量）
        
        Returns:
            走神产生的思维列表
        """
        self.activate()
        thoughts = []
        
        for _ in range(duration):
            thought = self._generate_wandering_thought()
            thoughts.append(thought)
            
            self._wandering_history.append({
                "thought": str(thought.content)[:50],
                "state": self._state.value,
                "timestamp": time.time()
            })
        
        if len(self._wandering_history) > 500:
            self._wandering_history = self._wandering_history[-500:]
        
        return thoughts
    
    def _generate_wandering_thought(self) -> Thought:
        """生成走神思维"""
        thought_generators = [
            (self.self_narrative.reflect_on_self, 0.25),
            (lambda: self.memory_integration.integrate_memories(), 0.25),
            (lambda: self.future_simulation.simulate_future(), 0.25),
            (lambda: self.random_association.free_associate(), 0.25),
        ]
        
        weights = [w for _, w in thought_generators]
        generator = self.randomness.random_choice(
            [g for g, _ in thought_generators],
            weights=weights,
            randomness_type=RandomnessType.QUANTUM
        )
        
        return generator()
    
    def spontaneous_thought(self) -> Optional[Thought]:
        """
        自发思维 - 随机产生的思维
        
        Returns:
            自发思维，如果没有则返回None
        """
        if random.random() > self._activation_level:
            return None
        
        thought_types = [
            "self_reflection",
            "memory_flash",
            "future_thought",
            "random_association",
            "dream_like"
        ]
        
        thought_type = self.randomness.random_choice(
            thought_types,
            randomness_type=RandomnessType.QUANTUM
        )
        
        if thought_type == "self_reflection":
            return self.self_narrative.reflect_on_self()
        elif thought_type == "memory_flash":
            return self.memory_integration.integrate_memories()
        elif thought_type == "future_thought":
            return self.future_simulation.simulate_future()
        elif thought_type == "random_association":
            return self.random_association.free_associate()
        else:
            return self.random_association.dream_like_association()
    
    def process_experience(
        self, 
        experience: Any,
        emotional_valence: float = 0.5,
        importance: float = 0.5
    ):
        """
        处理经历 - 将经历整合到DMN
        
        Args:
            experience: 经历内容
            emotional_valence: 情感效价
            importance: 重要性
        """
        self.memory_integration.store_memory(
            experience, 
            emotional_valence, 
            importance
        )
        
        self.self_narrative.add_to_history({
            "description": str(experience)[:100],
            "emotional_valence": emotional_valence
        })
    
    def get_state_summary(self) -> Dict[str, Any]:
        """获取状态摘要"""
        return {
            "state": self._state.value,
            "activation_level": self._activation_level,
            "narrative": self.self_narrative.get_narrative_summary(),
            "memory_stats": self.memory_integration.get_memory_statistics(),
            "scenario_stats": self.future_simulation.get_scenario_summary(),
            "association_stats": self.random_association.get_network_stats(),
            "wandering_count": len(self._wandering_history)
        }
    
    def set_activation(self, level: float):
        """设置激活水平"""
        self._activation_level = max(0.0, min(1.0, level))
        self._update_state()
