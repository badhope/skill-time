"""
RandomAgent - 模拟人类直觉跳跃思维的智能体框架

核心理念：世界的底层是随机的，大脑的底层也是随机的

架构层次（从底到上）：
1. 随机底层引擎 - 量子随机、神经噪声、创造性随机
2. 意识层次系统 - 显意识、前意识、潜意识、无意识
3. 意识流引擎 - 自然漂移、联想跳跃、焦点切换
4. DMN走神引擎 - 自我叙事、记忆整合、未来预演
5. 记忆系统 - 工作记忆、长期记忆、程序记忆
6. 目标系统 - 目标设定、分解、收敛判断
7. 影响因素 - 情绪、认知偏见、心智模型、习惯、性格
8. 动态平衡控制器 - 随机性旋钮、探索/利用平衡
9. 输出系统 - 思考过程展示、答案生成
"""

import time
from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum

from random_agent.core.randomness_engine import (
    RandomnessEngine, 
    RandomnessType,
    NoiseConfig
)
from random_agent.core.consciousness_layers import (
    ConsciousnessLayers,
    ConsciousnessLevel,
    Thought
)
from random_agent.core.consciousness_stream import (
    ConsciousnessStream,
    StreamState
)
from random_agent.core.dmn_engine import DMNEngine
from random_agent.core.memory_system import (
    MemorySystem,
    MemoryType
)
from random_agent.core.goal_system import (
    GoalSystem,
    GoalPriority,
    GoalStatus
)
from random_agent.core.influence_factors import (
    InfluenceFactors,
    CognitiveBiasType,
    PersonalityTrait
)
from random_agent.core.balance_controller import (
    BalanceController,
    ThinkingMode
)
from random_agent.core.output_system import (
    OutputSystem,
    OutputFormat
)


class AgentState(Enum):
    """智能体状态"""
    IDLE = "idle"
    THINKING = "thinking"
    EXPLORING = "exploring"
    CONVERGING = "converging"
    RESTING = "resting"


@dataclass
class AgentConfig:
    """智能体配置"""
    randomness_seed: Optional[int] = None
    working_memory_capacity: int = 7
    initial_randomness_level: float = 0.5
    default_thinking_mode: ThinkingMode = ThinkingMode.BALANCED
    
    personality: Dict[str, float] = field(default_factory=lambda: {
        "openness": 0.6,
        "conscientiousness": 0.5,
        "extraversion": 0.5,
        "agreeableness": 0.5,
        "neuroticism": 0.4
    })
    
    noise_config: Dict[str, float] = field(default_factory=lambda: {
        "base_level": 0.1,
        "signal_to_noise_ratio": 0.8,
        "fluctuation_amplitude": 0.2,
        "spontaneous_rate": 0.05
    })


class RandomAgent:
    """
    RandomAgent - 模拟人类直觉跳跃思维的智能体
    
    核心特点：
    1. 以随机性为底层驱动
    2. 模拟人类意识的多层次结构
    3. 实现有边界的随机思维
    4. 动态平衡探索与收敛
    """
    
    def __init__(self, config: Optional[AgentConfig] = None):
        self.config = config or AgentConfig()
        
        self._init_components()
        
        self._state = AgentState.IDLE
        self._current_goal: Optional[str] = None
        self._thinking_history: List[Dict] = []
        self._session_start: float = time.time()
    
    def _init_components(self):
        """初始化所有组件"""
        noise_config = NoiseConfig(**self.config.noise_config)
        
        self.randomness = RandomnessEngine(
            seed=self.config.randomness_seed,
            noise_config=noise_config
        )
        
        self.consciousness = ConsciousnessLayers(self.randomness)
        
        self.stream = ConsciousnessStream(
            self.randomness,
            self.consciousness
        )
        
        self.dmn = DMNEngine(self.randomness)
        
        self.memory = MemorySystem(
            self.randomness,
            self.config.working_memory_capacity
        )
        
        self.goal = GoalSystem(self.randomness)
        
        self.influence = InfluenceFactors(self.randomness)
        self._setup_personality()
        
        self.balance = BalanceController(self.randomness)
        self.balance.set_randomness(self.config.initial_randomness_level)
        self.balance.set_mode(self.config.default_thinking_mode)
        
        self.output = OutputSystem(self.randomness)
    
    def _setup_personality(self):
        """设置性格"""
        p = self.config.personality
        self.influence.set_personality(
            openness=p.get("openness", 0.5),
            conscientiousness=p.get("conscientiousness", 0.5),
            extraversion=p.get("extraversion", 0.5),
            agreeableness=p.get("agreeableness", 0.5),
            neuroticism=p.get("neuroticism", 0.5)
        )
    
    def think(
        self, 
        question: str, 
        max_iterations: int = 10,
        show_process: bool = True
    ) -> Dict[str, Any]:
        """
        思考问题
        
        Args:
            question: 问题
            max_iterations: 最大迭代次数
            show_process: 是否显示思考过程
        
        Returns:
            思考结果
        """
        self._state = AgentState.THINKING
        self._current_goal = question
        
        self.goal.set_main_goal(question, GoalPriority.HIGH)
        
        self.output.clear()
        
        initial_thought = Thought(
            content=f"开始思考：{question}",
            level=ConsciousnessLevel.CONSCIOUS,
            strength=0.9
        )
        self.output.record_thought(initial_thought, is_key_decision=True)
        
        thoughts = self._run_thinking_loop(max_iterations)
        
        result = self.output.generate_output(question, confidence=0.7)
        
        self._state = AgentState.IDLE
        
        return {
            "answer": result.final_answer,
            "thinking_process": [
                {"content": s.content, "level": s.level}
                for s in result.thinking_process
            ],
            "confidence": result.confidence,
            "iterations": len(thoughts)
        }
    
    def _run_thinking_loop(self, max_iterations: int) -> List[Thought]:
        """运行思考循环"""
        thoughts = []
        
        for iteration in range(max_iterations):
            self.balance.update({
                "convergence_score": self.goal.detector.get_progress(),
                "creativity_need": 0.5,
                "analysis_need": 0.3
            })
            
            thought = self._generate_next_thought(iteration, max_iterations)
            
            if thought:
                thoughts.append(thought)
                
                relevance = self._calculate_relevance(thought)
                self.goal.record_progress(thought, relevance)
                
                is_key = self._is_key_decision(thought)
                self.output.record_thought(thought, is_key)
                
                self._store_thought_in_memory(thought)
                
                status = self.goal.check_status()
                if status["convergence"]["should_converge"]:
                    break
            
            self.influence.decay_emotions()
        
        return thoughts
    
    def _generate_next_thought(
        self, 
        iteration: int, 
        max_iterations: int
    ) -> Optional[Thought]:
        """生成下一个思维"""
        thought_sources = []
        
        if self.balance.should_be_random():
            spontaneous = self.consciousness.process(goal=self._current_goal)
            thought_sources.append(("spontaneous", spontaneous, 0.3))
        
        if self.balance.should_explore():
            dmn_thought = self.dmn.spontaneous_thought()
            if dmn_thought:
                thought_sources.append(("dmn", dmn_thought, 0.25))
        
        stream_thoughts = self.stream.flow(steps=1, goal=self._current_goal)
        if stream_thoughts:
            thought_sources.append(("stream", stream_thoughts[0], 0.3))
        
        memory_thought = self.memory.random_recall()
        if memory_thought:
            thought_sources.append(("memory", Thought(
                content=memory_thought.content,
                level=ConsciousnessLevel.PRECONSCIOUS,
                strength=memory_thought.get_strength()
            ), 0.15))
        
        if not thought_sources:
            return None
        
        source_name, thought, weight = self.randomness.random_choice(
            thought_sources,
            weights=[w for _, _, w in thought_sources],
            randomness_type=RandomnessType.QUANTUM
        )
        
        thought = self._apply_influences(thought)
        
        self.balance.record_exploration() if source_name in ["spontaneous", "dmn"] else \
            self.balance.record_exploitation()
        
        return thought
    
    def _apply_influences(self, thought: Thought) -> Thought:
        """应用影响因素"""
        content = self.influence.process(
            thought.content,
            {"generate_emotion": True}
        )
        
        return Thought(
            content=content,
            level=thought.level,
            strength=thought.strength,
            metadata=thought.metadata
        )
    
    def _calculate_relevance(self, thought: Thought) -> float:
        """计算相关性"""
        if not self._current_goal:
            return 0.5
        
        goal_words = set(self._current_goal.lower().split())
        thought_words = set(str(thought.content).lower().split())
        
        common = goal_words & thought_words
        
        base_relevance = len(common) / len(goal_words) if goal_words else 0
        
        noise = self.randomness.inject_randomness(0.0, 0.1)
        
        return max(0.0, min(1.0, base_relevance + noise))
    
    def _is_key_decision(self, thought: Thought) -> bool:
        """判断是否是关键决策"""
        key_indicators = [
            "结论", "因此", "所以", "答案",
            "决定", "选择", "发现", "关键"
        ]
        
        content = str(thought.content)
        
        if any(indicator in content for indicator in key_indicators):
            return True
        
        if thought.level == ConsciousnessLevel.CONSCIOUS and thought.strength > 0.7:
            return True
        
        return False
    
    def _store_thought_in_memory(self, thought: Thought):
        """存储思维到记忆"""
        self.memory.encode(
            content=thought.content,
            memory_type=MemoryType.EPISODIC,
            importance=thought.strength
        )
    
    def explore(
        self, 
        topic: str, 
        depth: int = 5
    ) -> List[Dict[str, Any]]:
        """
        探索主题
        
        Args:
            topic: 主题
            depth: 探索深度
        
        Returns:
            探索结果列表
        """
        self._state = AgentState.EXPLORING
        
        self.balance.set_mode(ThinkingMode.DIVERGENT)
        self.balance.set_randomness(0.7)
        
        results = []
        
        for _ in range(depth):
            thoughts = self.stream.flow(steps=3)
            
            for thought in thoughts:
                influenced = self._apply_influences(thought)
                results.append({
                    "content": influenced.content,
                    "level": influenced.level.value,
                    "strength": influenced.strength
                })
        
        self.balance.set_mode(ThinkingMode.BALANCED)
        self._state = AgentState.IDLE
        
        return results
    
    def wander(self, duration: int = 5) -> List[Dict[str, Any]]:
        """
        走神模式
        
        Args:
            duration: 持续时间
        
        Returns:
            走神产生的思维列表
        """
        self._state = AgentState.RESTING
        
        self.dmn.activate()
        
        thoughts = self.dmn.mind_wander(duration)
        
        results = [
            {
                "content": t.content,
                "level": t.level.value,
                "strength": t.strength
            }
            for t in thoughts
        ]
        
        self.dmn.deactivate()
        self._state = AgentState.IDLE
        
        return results
    
    def set_randomness(self, level: float):
        """设置随机性水平"""
        self.balance.set_randomness(level)
    
    def set_mode(self, mode: ThinkingMode):
        """设置思维模式"""
        self.balance.set_mode(mode)
    
    def enable_bias(self, bias_type: CognitiveBiasType, strength: float = 0.5):
        """启用认知偏见"""
        self.influence.enable_bias(bias_type, strength)
    
    def disable_bias(self, bias_type: CognitiveBiasType):
        """禁用认知偏见"""
        self.influence.disable_bias(bias_type)
    
    def add_memory(
        self, 
        content: Any, 
        memory_type: MemoryType = MemoryType.EPISODIC,
        importance: float = 0.5
    ):
        """添加记忆"""
        self.memory.encode(
            content=content,
            memory_type=memory_type,
            importance=importance
        )
    
    def get_state(self) -> Dict[str, Any]:
        """获取智能体状态"""
        return {
            "state": self._state.value,
            "current_goal": self._current_goal,
            "balance": self.balance.get_state().__dict__,
            "consciousness": self.consciousness.get_state_summary(),
            "dmn": self.dmn.get_state_summary(),
            "memory": self.memory.get_memory_state(),
            "influence": self.influence.get_state(),
            "session_duration": time.time() - self._session_start
        }
    
    def get_full_report(self) -> Dict[str, Any]:
        """获取完整报告"""
        return {
            "agent_state": self.get_state(),
            "balance_report": self.balance.get_full_report(),
            "output_stats": self.output.get_statistics(),
            "goal_stats": self.goal.manager.get_statistics()
        }
    
    def reset(self):
        """重置智能体"""
        self._state = AgentState.IDLE
        self._current_goal = None
        self._thinking_history.clear()
        self._session_start = time.time()
        
        self.output.clear()
        self.goal.manager._goals.clear()
        self.goal.detector.reset()
        
        self.balance.set_randomness(self.config.initial_randomness_level)
        self.balance.set_mode(self.config.default_thinking_mode)
    
    def configure(self, **kwargs):
        """配置智能体"""
        if "randomness" in kwargs:
            self.set_randomness(kwargs["randomness"])
        
        if "mode" in kwargs:
            self.set_mode(kwargs["mode"])
        
        if "personality" in kwargs:
            p = kwargs["personality"]
            self.influence.set_personality(**p)
        
        if "working_memory_capacity" in kwargs:
            self.memory.working.capacity = kwargs["working_memory_capacity"]


def create_agent(
    randomness: float = 0.5,
    openness: float = 0.6,
    conscientiousness: float = 0.5,
    **kwargs
) -> RandomAgent:
    """
    创建智能体的便捷函数
    
    Args:
        randomness: 初始随机性水平
        openness: 开放性
        conscientiousness: 尽责性
        **kwargs: 其他配置
    
    Returns:
        RandomAgent实例
    """
    config = AgentConfig(
        initial_randomness_level=randomness,
        personality={
            "openness": openness,
            "conscientiousness": conscientiousness,
            **kwargs.get("personality", {})
        }
    )
    
    return RandomAgent(config)
