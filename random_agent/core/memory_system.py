"""
记忆系统 (Memory System)

理论基础：认知心理学的记忆模型

记忆类型：
1. 工作记忆 (Working Memory) - 短期、有限容量、活跃处理
2. 长期记忆 (Long-term Memory) - 长期存储、大容量
   - 情景记忆 (Episodic) - 个人经历
   - 语义记忆 (Semantic) - 知识事实
3. 程序记忆 (Procedural Memory) - 技能和习惯

神经基础：
- 工作记忆：前额叶皮层
- 长期记忆：海马体（编码）→ 皮层（存储）
- 程序记忆：基底神经节、小脑
"""

import random
import time
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from collections import deque
from random_agent.core.randomness_engine import RandomnessEngine, RandomnessType


class MemoryType(Enum):
    """记忆类型"""
    WORKING = "working"
    EPISODIC = "episodic"
    SEMANTIC = "semantic"
    PROCEDURAL = "procedural"


class MemoryImportance(Enum):
    """记忆重要性"""
    LOW = 0.2
    MEDIUM = 0.5
    HIGH = 0.8
    CRITICAL = 1.0


@dataclass
class MemoryItem:
    """记忆项"""
    content: Any
    memory_type: MemoryType
    importance: float = 0.5
    emotional_valence: float = 0.5
    created_at: float = field(default_factory=time.time)
    last_accessed: float = field(default_factory=time.time)
    access_count: int = 0
    decay_rate: float = 0.1
    associations: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def access(self):
        """访问记忆"""
        self.last_accessed = time.time()
        self.access_count += 1
    
    def get_strength(self) -> float:
        """获取记忆强度"""
        time_elapsed = time.time() - self.last_accessed
        decay = self.decay_rate * time_elapsed / 3600
        strength = self.importance * (1 - decay) + 0.1 * self.access_count
        return max(0.0, min(1.0, strength))


@dataclass
class WorkingMemorySlot:
    """工作记忆槽位"""
    content: Any
    activation: float = 1.0
    position: int = 0
    timestamp: float = field(default_factory=time.time)


class WorkingMemory:
    """
    工作记忆
    
    神经基础：前额叶皮层
    容量：7±2个信息块（米勒定律）
    持续时间：约20秒
    
    功能：
    - 临时存储：短暂保持信息
    - 信息处理：对信息进行操作
    - 注意力网关：过滤进入长期记忆的信息
    - 任务相关：支持当前任务的执行
    """
    
    def __init__(
        self, 
        randomness_engine: RandomnessEngine,
        capacity: int = 7
    ):
        self.randomness = randomness_engine
        self.capacity = capacity
        self._slots: deque = deque(maxlen=capacity)
        self._focus_index: int = 0
        self._processing_buffer: List[Any] = []
    
    def store(self, content: Any) -> bool:
        """
        存储信息到工作记忆
        
        Args:
            content: 要存储的内容
        
        Returns:
            是否成功存储
        """
        slot = WorkingMemorySlot(
            content=content,
            position=len(self._slots)
        )
        
        if len(self._slots) >= self.capacity:
            self._displace_oldest()
        
        self._slots.append(slot)
        return True
    
    def _displace_oldest(self):
        """替换最旧的信息"""
        if self._slots:
            displaced = self._slots[0]
            self._slots.popleft()
            return displaced
        return None
    
    def retrieve(self, index: Optional[int] = None) -> Optional[Any]:
        """
        从工作记忆中检索信息
        
        Args:
            index: 槽位索引，None则检索当前焦点
        
        Returns:
            检索到的内容
        """
        if not self._slots:
            return None
        
        if index is None:
            index = self._focus_index
        
        if 0 <= index < len(self._slots):
            slot = self._slots[index]
            slot.activation = min(1.0, slot.activation + 0.2)
            return slot.content
        
        return None
    
    def focus_on(self, index: int):
        """将注意力聚焦到特定槽位"""
        if 0 <= index < len(self._slots):
            self._focus_index = index
            self._slots[index].activation = 1.0
    
    def get_focus(self) -> Optional[Any]:
        """获取当前焦点内容"""
        return self.retrieve(self._focus_index)
    
    def shift_focus(self, direction: int = 1):
        """移动焦点"""
        new_index = self._focus_index + direction
        new_index = max(0, min(len(self._slots) - 1, new_index))
        self.focus_on(new_index)
    
    def process(self, operation: str) -> Any:
        """
        处理工作记忆中的信息
        
        Args:
            operation: 操作类型
        
        Returns:
            处理结果
        """
        contents = [slot.content for slot in self._slots]
        
        if operation == "summarize":
            return self._summarize(contents)
        elif operation == "compare":
            return self._compare(contents)
        elif operation == "integrate":
            return self._integrate(contents)
        elif operation == "random_select":
            return self.randomness.random_choice(
                contents,
                randomness_type=RandomnessType.QUANTUM
            )
        else:
            return contents
    
    def _summarize(self, contents: List[Any]) -> str:
        """总结内容"""
        return f"工作记忆中有{len(contents)}个项目"
    
    def _compare(self, contents: List[Any]) -> Dict:
        """比较内容"""
        return {
            "count": len(contents),
            "unique": len(set(str(c) for c in contents))
        }
    
    def _integrate(self, contents: List[Any]) -> str:
        """整合内容"""
        return " | ".join(str(c)[:30] for c in contents[:3])
    
    def decay(self):
        """衰减 - 模拟工作记忆的自然衰减"""
        for slot in self._slots:
            slot.activation *= 0.95
        
        self._slots = deque(
            [s for s in self._slots if s.activation > 0.1],
            maxlen=self.capacity
        )
    
    def clear(self):
        """清空工作记忆"""
        self._slots.clear()
        self._focus_index = 0
    
    def get_state(self) -> Dict[str, Any]:
        """获取工作记忆状态"""
        return {
            "capacity": self.capacity,
            "used": len(self._slots),
            "available": self.capacity - len(self._slots),
            "focus_index": self._focus_index,
            "contents": [str(s.content)[:30] for s in self._slots],
            "activations": [s.activation for s in self._slots]
        }


class EpisodicMemory:
    """
    情景记忆
    
    神经基础：海马体 → 皮层
    内容：个人经历和事件
    
    功能：
    - 事件存储：存储个人经历
    - 时空标记：记录时间和地点
    - 情感关联：与情感体验关联
    - 事件重构：回忆时重构事件
    """
    
    def __init__(self, randomness_engine: RandomnessEngine):
        self.randomness = randomness_engine
        self._episodes: List[MemoryItem] = []
        self._timeline: Dict[float, List[int]] = {}
        self._max_episodes = 1000
    
    def store(
        self, 
        event: Any, 
        context: Optional[Dict] = None,
        emotional_valence: float = 0.5,
        importance: float = 0.5
    ) -> MemoryItem:
        """
        存储事件
        
        Args:
            event: 事件内容
            context: 上下文
            emotional_valence: 情感效价
            importance: 重要性
        
        Returns:
            存储的记忆项
        """
        episode = MemoryItem(
            content=event,
            memory_type=MemoryType.EPISODIC,
            importance=importance,
            emotional_valence=emotional_valence,
            metadata={"context": context or {}}
        )
        
        self._episodes.append(episode)
        episode_index = len(self._episodes) - 1
        
        time_key = time.time()
        if time_key not in self._timeline:
            self._timeline[time_key] = []
        self._timeline[time_key].append(episode_index)
        
        if len(self._episodes) > self._max_episodes:
            self._consolidate_old_memories()
        
        return episode
    
    def recall(
        self, 
        cue: Optional[str] = None,
        time_range: Optional[Tuple[float, float]] = None,
        emotional_filter: Optional[float] = None
    ) -> List[MemoryItem]:
        """
        回忆事件
        
        Args:
            cue: 回忆线索
            time_range: 时间范围
            emotional_filter: 情感过滤
        
        Returns:
            回忆到的事件列表
        """
        results = []
        
        for episode in self._episodes:
            score = episode.get_strength()
            
            if cue:
                similarity = self._calculate_similarity(cue, episode.content)
                score *= similarity
            
            if time_range:
                if not (time_range[0] <= episode.created_at <= time_range[1]):
                    score *= 0.1
            
            if emotional_filter is not None:
                emotional_diff = abs(episode.emotional_valence - emotional_filter)
                score *= (1 - emotional_diff)
            
            if score > 0.1:
                episode.access()
                results.append((episode, score))
        
        results.sort(key=lambda x: x[1], reverse=True)
        return [r[0] for r in results[:10]]
    
    def _calculate_similarity(self, a: Any, b: Any) -> float:
        """计算相似度"""
        if isinstance(a, str) and isinstance(b, str):
            words_a = set(a.lower().split())
            words_b = set(b.lower().split())
            common = words_a & words_b
            union = words_a | words_b
            return len(common) / len(union) if union else 0
        return random.random() * 0.5
    
    def _consolidate_old_memories(self):
        """整合旧记忆 - 模拟记忆巩固"""
        if len(self._episodes) > self._max_episodes * 0.8:
            self._episodes = sorted(
                self._episodes,
                key=lambda x: x.get_strength(),
                reverse=True
            )[:int(self._max_episodes * 0.8)]
    
    def get_recent(self, count: int = 5) -> List[MemoryItem]:
        """获取最近的事件"""
        return sorted(
            self._episodes,
            key=lambda x: x.created_at,
            reverse=True
        )[:count]
    
    def get_significant(self, count: int = 5) -> List[MemoryItem]:
        """获取重要事件"""
        return sorted(
            self._episodes,
            key=lambda x: x.importance,
            reverse=True
        )[:count]


class SemanticMemory:
    """
    语义记忆
    
    神经基础：颞叶皮层
    内容：知识和事实
    
    功能：
    - 知识存储：存储事实性知识
    - 概念网络：概念之间的关联
    - 分类体系：知识的分类组织
    - 快速检索：高效的知识检索
    """
    
    def __init__(self, randomness_engine: RandomnessEngine):
        self.randomness = randomness_engine
        self._knowledge: Dict[str, MemoryItem] = {}
        self._categories: Dict[str, List[str]] = {}
        self._associations: Dict[str, List[str]] = {}
    
    def store(
        self, 
        concept: str, 
        definition: Any,
        category: Optional[str] = None,
        related_concepts: Optional[List[str]] = None
    ) -> MemoryItem:
        """
        存储知识
        
        Args:
            concept: 概念名称
            definition: 定义/解释
            category: 类别
            related_concepts: 相关概念
        
        Returns:
            存储的记忆项
        """
        item = MemoryItem(
            content=definition,
            memory_type=MemoryType.SEMANTIC,
            metadata={
                "concept": concept,
                "category": category
            }
        )
        
        self._knowledge[concept] = item
        
        if category:
            if category not in self._categories:
                self._categories[category] = []
            if concept not in self._categories[category]:
                self._categories[category].append(concept)
        
        if related_concepts:
            if concept not in self._associations:
                self._associations[concept] = []
            for related in related_concepts:
                if related not in self._associations[concept]:
                    self._associations[concept].append(related)
        
        return item
    
    def retrieve(self, concept: str) -> Optional[MemoryItem]:
        """
        检索知识
        
        Args:
            concept: 概念名称
        
        Returns:
            知识项
        """
        if concept in self._knowledge:
            item = self._knowledge[concept]
            item.access()
            return item
        return None
    
    def search(
        self, 
        query: str, 
        category: Optional[str] = None
    ) -> List[MemoryItem]:
        """
        搜索知识
        
        Args:
            query: 搜索查询
            category: 类别限制
        
        Returns:
            搜索结果
        """
        results = []
        
        search_space = (
            self._categories.get(category, []) 
            if category else 
            list(self._knowledge.keys())
        )
        
        for concept in search_space:
            if query.lower() in concept.lower():
                results.append(self._knowledge[concept])
            elif concept in self._knowledge:
                item = self._knowledge[concept]
                if self._calculate_similarity(query, item.content) > 0.3:
                    results.append(item)
        
        return results[:10]
    
    def get_related(self, concept: str) -> List[str]:
        """获取相关概念"""
        return self._associations.get(concept, [])
    
    def get_category(self, category: str) -> List[str]:
        """获取类别中的概念"""
        return self._categories.get(category, [])
    
    def _calculate_similarity(self, a: Any, b: Any) -> float:
        """计算相似度"""
        if isinstance(a, str) and isinstance(b, str):
            words_a = set(a.lower().split())
            words_b = set(b.lower().split())
            common = words_a & words_b
            union = words_a | words_b
            return len(common) / len(union) if union else 0
        return 0.0
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            "total_concepts": len(self._knowledge),
            "categories": len(self._categories),
            "associations": len(self._associations)
        }


class ProceduralMemory:
    """
    程序记忆
    
    神经基础：基底神经节、小脑
    内容：技能和习惯
    
    功能：
    - 技能存储：存储动作技能
    - 习惯形成：形成自动化行为
    - 程序执行：执行已习得的程序
    - 技能迁移：技能的泛化应用
    """
    
    def __init__(self, randomness_engine: RandomnessEngine):
        self.randomness = randomness_engine
        self._procedures: Dict[str, MemoryItem] = {}
        self._habits: Dict[str, Dict] = {}
        self._execution_history: List[Dict] = []
    
    def store_procedure(
        self, 
        name: str, 
        steps: List[Any],
        conditions: Optional[Dict] = None
    ) -> MemoryItem:
        """
        存储程序
        
        Args:
            name: 程序名称
            steps: 执行步骤
            conditions: 执行条件
        
        Returns:
            存储的记忆项
        """
        item = MemoryItem(
            content=steps,
            memory_type=MemoryType.PROCEDURAL,
            metadata={
                "name": name,
                "conditions": conditions or {},
                "step_count": len(steps)
            }
        )
        
        self._procedures[name] = item
        return item
    
    def execute(
        self, 
        name: str, 
        context: Optional[Dict] = None
    ) -> Any:
        """
        执行程序
        
        Args:
            name: 程序名称
            context: 执行上下文
        
        Returns:
            执行结果
        """
        if name not in self._procedures:
            return None
        
        procedure = self._procedures[name]
        procedure.access()
        
        steps = procedure.content
        results = []
        
        for i, step in enumerate(steps):
            if random.random() < 0.05:
                step = self.randomness.inject_randomness(step, 0.1)
            
            results.append(step)
        
        self._execution_history.append({
            "procedure": name,
            "steps_executed": len(results),
            "timestamp": time.time()
        })
        
        if len(self._execution_history) > 500:
            self._execution_history = self._execution_history[-500:]
        
        return results
    
    def form_habit(
        self, 
        name: str, 
        trigger: Dict, 
        action: str,
        strength: float = 0.5
    ):
        """
        形成习惯
        
        Args:
            name: 习惯名称
            trigger: 触发条件
            action: 行为
            strength: 初始强度
        """
        self._habits[name] = {
            "trigger": trigger,
            "action": action,
            "strength": strength,
            "execution_count": 0,
            "created_at": time.time()
        }
    
    def check_habits(
        self, 
        context: Dict
    ) -> List[Dict]:
        """
        检查习惯触发
        
        Args:
            context: 当前上下文
        
        Returns:
            触发的习惯列表
        """
        triggered = []
        
        for name, habit in self._habits.items():
            if self._match_trigger(context, habit["trigger"]):
                if random.random() < habit["strength"]:
                    triggered.append({
                        "name": name,
                        "action": habit["action"],
                        "strength": habit["strength"]
                    })
                    habit["execution_count"] += 1
                    habit["strength"] = min(1.0, habit["strength"] + 0.01)
        
        return triggered
    
    def _match_trigger(self, context: Dict, trigger: Dict) -> bool:
        """匹配触发条件"""
        for key, value in trigger.items():
            if key not in context or context[key] != value:
                return False
        return True
    
    def get_procedure(self, name: str) -> Optional[MemoryItem]:
        """获取程序"""
        return self._procedures.get(name)
    
    def get_habit(self, name: str) -> Optional[Dict]:
        """获取习惯"""
        return self._habits.get(name)
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            "procedures": len(self._procedures),
            "habits": len(self._habits),
            "total_executions": len(self._execution_history)
        }


class MemorySystem:
    """
    记忆系统 - 整合所有记忆类型
    
    管理工作记忆、情景记忆、语义记忆和程序记忆
    """
    
    def __init__(
        self, 
        randomness_engine: Optional[RandomnessEngine] = None,
        working_memory_capacity: int = 7
    ):
        self.randomness = randomness_engine or RandomnessEngine()
        
        self.working = WorkingMemory(
            self.randomness, 
            working_memory_capacity
        )
        self.episodic = EpisodicMemory(self.randomness)
        self.semantic = SemanticMemory(self.randomness)
        self.procedural = ProceduralMemory(self.randomness)
        
        self._consolidation_queue: List[MemoryItem] = []
        self._retrieval_history: List[Dict] = []
    
    def encode(
        self, 
        content: Any, 
        memory_type: MemoryType = MemoryType.WORKING,
        **kwargs
    ) -> MemoryItem:
        """
        编码记忆
        
        Args:
            content: 内容
            memory_type: 记忆类型
            **kwargs: 其他参数
        
        Returns:
            编码的记忆项
        """
        if memory_type == MemoryType.WORKING:
            self.working.store(content)
            return MemoryItem(
                content=content,
                memory_type=memory_type
            )
        
        elif memory_type == MemoryType.EPISODIC:
            return self.episodic.store(content, **kwargs)
        
        elif memory_type == MemoryType.SEMANTIC:
            concept = kwargs.get("concept", str(content)[:20])
            return self.semantic.store(concept, content, **kwargs)
        
        elif memory_type == MemoryType.PROCEDURAL:
            name = kwargs.get("name", "unnamed_procedure")
            steps = kwargs.get("steps", [content])
            return self.procedural.store_procedure(name, steps, **kwargs)
        
        return MemoryItem(content=content, memory_type=memory_type)
    
    def retrieve(
        self, 
        query: Any, 
        memory_types: Optional[List[MemoryType]] = None
    ) -> List[MemoryItem]:
        """
        检索记忆
        
        Args:
            query: 查询
            memory_types: 要检索的记忆类型
        
        Returns:
            检索结果
        """
        if memory_types is None:
            memory_types = list(MemoryType)
        
        results = []
        
        if MemoryType.WORKING in memory_types:
            working_content = self.working.retrieve()
            if working_content:
                results.append(MemoryItem(
                    content=working_content,
                    memory_type=MemoryType.WORKING
                ))
        
        if MemoryType.EPISODIC in memory_types:
            if isinstance(query, str):
                episodic_results = self.episodic.recall(cue=query)
                results.extend(episodic_results)
        
        if MemoryType.SEMANTIC in memory_types:
            if isinstance(query, str):
                semantic_results = self.semantic.search(query)
                results.extend(semantic_results)
        
        self._retrieval_history.append({
            "query": str(query)[:50],
            "results_count": len(results),
            "timestamp": time.time()
        })
        
        if len(self._retrieval_history) > 200:
            self._retrieval_history = self._retrieval_history[-200:]
        
        return results
    
    def consolidate(self):
        """
        记忆巩固 - 将工作记忆转移到长期记忆
        
        模拟睡眠时的记忆巩固过程
        """
        for slot in self.working._slots:
            if slot.activation > 0.5:
                self._consolidation_queue.append(MemoryItem(
                    content=slot.content,
                    memory_type=MemoryType.EPISODIC,
                    importance=slot.activation
                ))
        
        for item in self._consolidation_queue:
            self.episodic.store(
                item.content,
                importance=item.importance
            )
        
        self._consolidation_queue.clear()
    
    def forget(self, strategy: str = "decay"):
        """
        遗忘机制
        
        Args:
            strategy: 遗忘策略
        """
        if strategy == "decay":
            self.working.decay()
        
        elif strategy == "interference":
            self.working.clear()
        
        elif strategy == "random":
            if self.working._slots:
                forget_index = random.randint(0, len(self.working._slots) - 1)
                del self.working._slots[forget_index]
    
    def transfer_to_long_term(
        self, 
        content: Any, 
        importance: float = 0.5
    ):
        """
        转移到长期记忆
        
        Args:
            content: 内容
            importance: 重要性
        """
        self.episodic.store(content, importance=importance)
    
    def get_memory_state(self) -> Dict[str, Any]:
        """获取记忆系统状态"""
        return {
            "working_memory": self.working.get_state(),
            "episodic_count": len(self.episodic._episodes),
            "semantic_stats": self.semantic.get_statistics(),
            "procedural_stats": self.procedural.get_statistics(),
            "consolidation_queue": len(self._consolidation_queue),
            "retrieval_count": len(self._retrieval_history)
        }
    
    def random_recall(self) -> Optional[MemoryItem]:
        """
        随机回忆 - 随机检索一个记忆
        
        Returns:
            随机回忆的记忆
        """
        memory_sources = []
        
        if self.episodic._episodes:
            memory_sources.append(("episodic", self.episodic._episodes))
        
        if self.semantic._knowledge:
            memory_sources.append(("semantic", list(self.semantic._knowledge.values())))
        
        if not memory_sources:
            return None
        
        source_name, memories = self.randomness.random_choice(
            memory_sources,
            randomness_type=RandomnessType.QUANTUM
        )
        
        memory = self.randomness.random_choice(
            memories,
            randomness_type=RandomnessType.QUANTUM
        )
        
        if isinstance(memory, MemoryItem):
            memory.access()
        
        return memory
