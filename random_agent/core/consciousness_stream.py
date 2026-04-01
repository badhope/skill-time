"""
意识流引擎 (Consciousness Stream)

理论基础：威廉·詹姆斯的意识流理论

核心概念：
- 意识不是离散的点，而是连续流动的"河流"
- 思维不断变化，没有固定的形态
- 每个思维都与前后思维相连
- 意识有自己的"流向"和"流速"

模块结构：
1. 自然漂移 - 意识的自然流动
2. 联想跳跃 - 思维的跳跃性连接
3. 焦点边缘切换 - 注意力的转移
4. 流速控制 - 思维速度的调节
"""

import random
import time
from typing import List, Dict, Any, Optional, Callable, Tuple
from dataclasses import dataclass, field
from enum import Enum
from random_agent.core.randomness_engine import RandomnessEngine, RandomnessType
from random_agent.core.consciousness_layers import (
    ConsciousnessLayers,
    ConsciousnessLevel,
    Thought
)


class StreamState(Enum):
    """意识流状态"""
    FLOWING = "flowing"           # 流动中
    PAUSED = "paused"             # 暂停
    RAPID = "rapid"               # 快速流动
    SLOW = "slow"                 # 缓慢流动
    TURBULENT = "turbulent"       # 湍流（混乱）
    FOCUSED = "focused"           # 聚焦


@dataclass
class StreamNode:
    """意识流节点"""
    thought: Thought
    prev_node: Optional['StreamNode'] = None
    next_nodes: List['StreamNode'] = field(default_factory=list)
    branch_probability: float = 0.0
    timestamp: float = field(default_factory=time.time)
    
    def add_branch(self, node: 'StreamNode', probability: float = 0.5):
        """添加分支"""
        node.branch_probability = probability
        self.next_nodes.append(node)
        node.prev_node = self


@dataclass
class FlowMetrics:
    """流动指标"""
    speed: float = 0.5
    coherence: float = 0.5
    turbulence: float = 0.1
    depth: float = 0.5
    width: float = 0.5


class NaturalDrift:
    """
    自然漂移 - 意识的自然流动
    
    模拟意识在没有明确目标时的自然漂移：
    - 随机联想：一个想法自然引发另一个想法
    - 主题漂移：话题逐渐变化
    - 情绪影响：情绪状态影响漂移方向
    - 环境刺激：外部刺激改变漂移路径
    """
    
    def __init__(self, randomness_engine: RandomnessEngine):
        self.randomness = randomness_engine
        self._drift_history: List[Dict] = []
        self._current_theme: Optional[str] = None
        self._theme_duration: float = 0.0
    
    def drift(
        self, 
        current_thought: Thought,
        context: Optional[Dict] = None
    ) -> Thought:
        """
        自然漂移 - 从当前思维漂移到下一个思维
        
        Args:
            current_thought: 当前思维
            context: 上下文
        
        Returns:
            漂移后的思维
        """
        drift_types = [
            "联想漂移", "主题漂移", "情绪漂移", 
            "记忆漂移", "随机漂移", "环境漂移"
        ]
        
        drift_type = self.randomness.random_choice(
            drift_types,
            randomness_type=RandomnessType.QUANTUM
        )
        
        next_content = self._generate_drift_content(
            current_thought, 
            drift_type, 
            context
        )
        
        drift_distance = random.random()
        
        next_thought = Thought(
            content=next_content,
            level=self._determine_next_level(current_thought.level, drift_distance),
            strength=current_thought.strength * (0.8 + random.random() * 0.4),
            metadata={
                "drift_type": drift_type,
                "drift_distance": drift_distance,
                "previous_thought": str(current_thought.content)[:50]
            }
        )
        
        self._record_drift(current_thought, next_thought, drift_type)
        
        return next_thought
    
    def _generate_drift_content(
        self, 
        current: Thought, 
        drift_type: str,
        context: Optional[Dict]
    ) -> str:
        """生成漂移内容"""
        current_str = str(current.content)
        
        if drift_type == "联想漂移":
            associations = [
                f"这让我想到...{self._random_association()}",
                f"与此相关的是...{self._random_association()}",
                f"类似的还有...{self._random_association()}"
            ]
            return self.randomness.random_choice(associations)
        
        elif drift_type == "主题漂移":
            themes = ["时间", "空间", "关系", "变化", "意义", "可能性"]
            new_theme = self.randomness.random_choice(themes)
            return f"话题转向...关于{new_theme}的思考"
        
        elif drift_type == "情绪漂移":
            emotions = ["好奇", "疑惑", "兴奋", "平静", "焦虑", "期待"]
            emotion = self.randomness.random_choice(emotions)
            return f"感到{emotion}，这让我..."
        
        elif drift_type == "记忆漂移":
            return f"这让我回想起...{self._random_memory_fragment()}"
        
        elif drift_type == "随机漂移":
            return self.randomness.creative_layer.get_random_concept()
        
        else:
            if context and "stimulus" in context:
                return f"注意到{context['stimulus']}..."
            return f"突然想到...{self._random_association()}"
    
    def _random_association(self) -> str:
        """生成随机联想"""
        return self.randomness.creative_layer.get_random_concept()
    
    def _random_memory_fragment(self) -> str:
        """生成随机记忆片段"""
        fragments = [
            "过去的某个时刻",
            "似曾相识的感觉",
            "模糊的记忆画面",
            "遥远的往事"
        ]
        return self.randomness.random_choice(fragments)
    
    def _determine_next_level(
        self, 
        current_level: ConsciousnessLevel,
        drift_distance: float
    ) -> ConsciousnessLevel:
        """确定下一个思维的意识层次"""
        if drift_distance > 0.8:
            levels = list(ConsciousnessLevel)
            return self.randomness.random_choice(
                levels,
                randomness_type=RandomnessType.QUANTUM
            )
        
        return current_level
    
    def _record_drift(self, from_thought: Thought, to_thought: Thought, drift_type: str):
        """记录漂移"""
        self._drift_history.append({
            "from": str(from_thought.content)[:50],
            "to": str(to_thought.content)[:50],
            "type": drift_type,
            "timestamp": time.time()
        })
        
        if len(self._drift_history) > 500:
            self._drift_history = self._drift_history[-500:]


class AssociativeJump:
    """
    联想跳跃 - 思维的跳跃性连接
    
    模拟人类思维的跳跃性：
    - 远距离联想：连接看似无关的概念
    - 隐喻跳跃：通过隐喻连接不同领域
    - 直觉跳跃：基于直觉的快速跳跃
    - 创造性跳跃：产生新颖的连接
    """
    
    def __init__(self, randomness_engine: RandomnessEngine):
        self.randomness = randomness_engine
        self._jump_history: List[Dict] = []
        self._jump_patterns: Dict[str, List[str]] = {
            "相似性": ["像", "类似", "相同", "相近"],
            "对比性": ["但是", "相反", "不同", "然而"],
            "因果性": ["因为", "所以", "导致", "引起"],
            "时空性": ["之前", "之后", "旁边", "里面"],
            "情感性": ["喜欢", "讨厌", "害怕", "期待"],
            "象征性": ["代表", "象征", "意味着", "暗示"]
        }
    
    def jump(
        self, 
        current_thought: Thought,
        jump_intensity: float = 0.5
    ) -> Thought:
        """
        联想跳跃 - 从当前思维跳跃到另一个思维
        
        Args:
            current_thought: 当前思维
            jump_intensity: 跳跃强度（0-1）
        
        Returns:
            跳跃后的思维
        """
        jump_type = self.randomness.random_choice(
            list(self._jump_patterns.keys()),
            randomness_type=RandomnessType.CREATIVE
        )
        
        target_concept = self.randomness.creative_layer.get_random_concept()
        
        if jump_intensity > 0.7:
            jump_result = self.randomness.creative_layer.conceptual_jump(
                str(current_thought.content)[:20]
            )
            target_concept = jump_result.get("target_concept", target_concept)
        
        connector = self.randomness.random_choice(
            self._jump_patterns[jump_type],
            randomness_type=RandomnessType.QUANTUM
        )
        
        new_content = f"{current_thought.content} {connector} {target_concept}"
        
        jump_thought = Thought(
            content=new_content,
            level=self._determine_jump_level(jump_intensity),
            strength=current_thought.strength * (0.5 + jump_intensity * 0.5),
            metadata={
                "jump_type": jump_type,
                "jump_intensity": jump_intensity,
                "connector": connector,
                "target_concept": target_concept
            }
        )
        
        self._record_jump(current_thought, jump_thought, jump_type, jump_intensity)
        
        return jump_thought
    
    def multi_hop_jump(
        self, 
        start_thought: Thought,
        hops: int = 3
    ) -> List[Thought]:
        """
        多跳联想 - 连续多次跳跃
        
        Args:
            start_thought: 起始思维
            hops: 跳跃次数
        
        Returns:
            跳跃路径上的思维列表
        """
        path = [start_thought]
        current = start_thought
        
        for i in range(hops):
            intensity = 0.3 + (i / hops) * 0.5
            next_thought = self.jump(current, intensity)
            path.append(next_thought)
            current = next_thought
        
        return path
    
    def creative_leap(
        self, 
        concepts: List[str]
    ) -> Thought:
        """
        创造性飞跃 - 产生新颖的连接
        
        Args:
            concepts: 概念列表
        
        Returns:
            创造性思维
        """
        if len(concepts) < 2:
            return Thought(
                content="需要更多概念进行创造性飞跃",
                level=ConsciousnessLevel.CONSCIOUS,
                strength=0.3
            )
        
        combination = self.randomness.creative_layer.combinatorial_innovation(concepts)
        
        return Thought(
            content=f"创造性连接：{combination['description']}",
            level=ConsciousnessLevel.SUBCONSCIOUS,
            strength=combination['innovation_score'],
            metadata={
                "combination_method": combination['combination_method'],
                "elements": combination['elements'],
                "is_creative_leap": True
            }
        )
    
    def _determine_jump_level(self, intensity: float) -> ConsciousnessLevel:
        """根据跳跃强度确定意识层次"""
        if intensity > 0.8:
            return self.randomness.random_choice(
                list(ConsciousnessLevel),
                randomness_type=RandomnessType.QUANTUM
            )
        elif intensity > 0.5:
            return ConsciousnessLevel.PRECONSCIOUS
        else:
            return ConsciousnessLevel.CONSCIOUS
    
    def _record_jump(
        self, 
        from_thought: Thought, 
        to_thought: Thought,
        jump_type: str,
        intensity: float
    ):
        """记录跳跃"""
        self._jump_history.append({
            "from": str(from_thought.content)[:50],
            "to": str(to_thought.content)[:50],
            "type": jump_type,
            "intensity": intensity,
            "timestamp": time.time()
        })
        
        if len(self._jump_history) > 500:
            self._jump_history = self._jump_history[-500:]


class FocusEdgeSwitch:
    """
    焦点边缘切换 - 注意力的转移
    
    模拟注意力的焦点和边缘切换：
    - 焦点思维：当前主要关注的思维
    - 边缘思维：在意识边缘的思维
    - 切换机制：焦点和边缘之间的转换
    - 注意力分配：如何在多个思维间分配注意力
    """
    
    def __init__(self, randomness_engine: RandomnessEngine):
        self.randomness = randomness_engine
        self._focus_stack: List[Thought] = []
        self._edge_thoughts: List[Thought] = []
        self._switch_history: List[Dict] = []
        self._max_focus_size = 3
        self._max_edge_size = 7
    
    def set_focus(self, thought: Thought):
        """设置焦点思维"""
        self._focus_stack.append(thought)
        
        if len(self._focus_stack) > self._max_focus_size:
            overflow = self._focus_stack.pop(0)
            self._add_to_edge(overflow)
    
    def _add_to_edge(self, thought: Thought):
        """添加到边缘"""
        self._edge_thoughts.append(thought)
        
        if len(self._edge_thoughts) > self._max_edge_size:
            self._edge_thoughts.pop(0)
    
    def switch_to_edge(self) -> Optional[Thought]:
        """
        切换到边缘 - 将边缘思维移到焦点
        
        Returns:
            切换后的焦点思维
        """
        if not self._edge_thoughts:
            return None
        
        weights = [t.strength for t in self._edge_thoughts]
        selected = self.randomness.random_choice(
            self._edge_thoughts,
            weights=weights,
            randomness_type=RandomnessType.QUANTUM
        )
        
        self._edge_thoughts.remove(selected)
        
        if self._focus_stack:
            old_focus = self._focus_stack[-1]
            self._add_to_edge(old_focus)
        
        self.set_focus(selected)
        
        self._record_switch("to_edge", selected)
        
        return selected
    
    def switch_to_focus(self) -> Optional[Thought]:
        """
        切换到焦点 - 返回焦点思维
        
        Returns:
            当前焦点思维
        """
        if not self._focus_stack:
            return None
        
        if len(self._focus_stack) > 1:
            current = self._focus_stack.pop()
            self._add_to_edge(current)
        
        focus = self._focus_stack[-1] if self._focus_stack else None
        
        if focus:
            self._record_switch("to_focus", focus)
        
        return focus
    
    def random_switch(self) -> Optional[Thought]:
        """
        随机切换 - 随机决定切换方向
        
        Returns:
            切换后的思维
        """
        if random.random() < 0.5:
            return self.switch_to_edge()
        else:
            return self.switch_to_focus()
    
    def get_attention_distribution(self) -> Dict[str, Any]:
        """获取注意力分布"""
        return {
            "focus_count": len(self._focus_stack),
            "edge_count": len(self._edge_thoughts),
            "focus_thoughts": [str(t.content)[:30] for t in self._focus_stack],
            "edge_thoughts": [str(t.content)[:30] for t in self._edge_thoughts],
            "focus_total_strength": sum(t.strength for t in self._focus_stack),
            "edge_total_strength": sum(t.strength for t in self._edge_thoughts)
        }
    
    def _record_switch(self, direction: str, thought: Thought):
        """记录切换"""
        self._switch_history.append({
            "direction": direction,
            "thought": str(thought.content)[:50],
            "timestamp": time.time()
        })
        
        if len(self._switch_history) > 200:
            self._switch_history = self._switch_history[-200:]


class FlowSpeedController:
    """
    流速控制 - 思维速度的调节
    
    控制意识流的流动速度：
    - 快速流动：快速切换思维
    - 缓慢流动：深入思考某个思维
    - 暂停：停止流动
    - 湍流：混乱的快速流动
    """
    
    def __init__(self, randomness_engine: RandomnessEngine):
        self.randomness = randomness_engine
        self._current_speed = 0.5
        self._target_speed = 0.5
        self._speed_history: List[float] = []
        self._acceleration = 0.0
    
    def set_speed(self, speed: float):
        """设置目标速度"""
        self._target_speed = max(0.0, min(1.0, speed))
    
    def accelerate(self, amount: float = 0.1):
        """加速"""
        self._target_speed = min(1.0, self._target_speed + amount)
    
    def decelerate(self, amount: float = 0.1):
        """减速"""
        self._target_speed = max(0.0, self._target_speed - amount)
    
    def update(self) -> float:
        """
        更新速度 - 平滑过渡到目标速度
        
        Returns:
            当前速度
        """
        diff = self._target_speed - self._current_speed
        self._acceleration = diff * 0.1
        
        noise = self.randomness.inject_randomness(0.0, 0.05)
        
        self._current_speed += self._acceleration + noise
        self._current_speed = max(0.0, min(1.0, self._current_speed))
        
        self._speed_history.append(self._current_speed)
        if len(self._speed_history) > 100:
            self._speed_history = self._speed_history[-100:]
        
        return self._current_speed
    
    def get_state(self) -> StreamState:
        """获取当前状态"""
        if self._current_speed < 0.1:
            return StreamState.PAUSED
        elif self._current_speed < 0.3:
            return StreamState.SLOW
        elif self._current_speed < 0.7:
            return StreamState.FLOWING
        elif self._current_speed < 0.9:
            return StreamState.RAPID
        else:
            return StreamState.TURBULENT
    
    def get_metrics(self) -> FlowMetrics:
        """获取流动指标"""
        state = self.get_state()
        
        coherence = 1.0 - abs(self._current_speed - 0.5) * 1.5
        coherence = max(0.0, min(1.0, coherence))
        
        turbulence = 0.0
        if state == StreamState.TURBULENT:
            turbulence = 0.8
        elif state == StreamState.RAPID:
            turbulence = 0.4
        
        return FlowMetrics(
            speed=self._current_speed,
            coherence=coherence,
            turbulence=turbulence,
            depth=1.0 - self._current_speed,
            width=self._current_speed
        )


class ConsciousnessStream:
    """
    意识流引擎 - 整合所有意识流组件
    
    管理意识的连续流动
    """
    
    def __init__(
        self, 
        randomness_engine: Optional[RandomnessEngine] = None,
        consciousness_layers: Optional[ConsciousnessLayers] = None
    ):
        self.randomness = randomness_engine or RandomnessEngine()
        self.layers = consciousness_layers or ConsciousnessLayers(self.randomness)
        
        self.drift = NaturalDrift(self.randomness)
        self.associative_jump = AssociativeJump(self.randomness)
        self.focus_switch = FocusEdgeSwitch(self.randomness)
        self.speed_controller = FlowSpeedController(self.randomness)
        
        self._stream_nodes: List[StreamNode] = []
        self._current_node: Optional[StreamNode] = None
        self._stream_history: List[Dict] = []
    
    def flow(
        self, 
        initial_thought: Optional[Thought] = None,
        steps: int = 5,
        goal: Optional[str] = None
    ) -> List[Thought]:
        """
        意识流动 - 让意识流自然流动
        
        Args:
            initial_thought: 初始思维
            steps: 流动步数
            goal: 目标（可选）
        
        Returns:
            思维流
        """
        stream = []
        
        if initial_thought:
            current = initial_thought
        else:
            current = self.layers.process(goal=goal)
        
        self._add_to_stream(current)
        stream.append(current)
        
        for _ in range(steps):
            speed = self.speed_controller.update()
            state = self.speed_controller.get_state()
            
            next_thought = self._generate_next_thought(
                current, 
                state, 
                speed, 
                goal
            )
            
            self._add_to_stream(next_thought)
            stream.append(next_thought)
            current = next_thought
        
        return stream
    
    def _generate_next_thought(
        self, 
        current: Thought, 
        state: StreamState,
        speed: float,
        goal: Optional[str]
    ) -> Thought:
        """生成下一个思维"""
        if state == StreamState.PAUSED:
            return current
        
        if state == StreamState.FOCUSED and goal:
            return self.layers.process(current, goal)
        
        if state == StreamState.TURBULENT:
            if random.random() < 0.5:
                return self.associative_jump.jump(current, 0.9)
            else:
                return self.drift.drift(current)
        
        if random.random() < 0.3:
            switch_result = self.focus_switch.random_switch()
            if switch_result:
                return switch_result
        
        if random.random() < speed:
            return self.associative_jump.jump(current, speed)
        else:
            return self.drift.drift(current)
    
    def _add_to_stream(self, thought: Thought):
        """添加思维到流"""
        node = StreamNode(thought=thought)
        
        if self._current_node:
            self._current_node.add_branch(node, 1.0)
        
        self._stream_nodes.append(node)
        self._current_node = node
        
        self.focus_switch.set_focus(thought)
        
        self._stream_history.append({
            "content": str(thought.content)[:100],
            "level": thought.level.value,
            "strength": thought.strength,
            "timestamp": time.time()
        })
        
        if len(self._stream_history) > 1000:
            self._stream_history = self._stream_history[-1000:]
    
    def branch(
        self, 
        branch_probability: float = 0.3
    ) -> List[Thought]:
        """
        分支 - 创建思维分支
        
        Args:
            branch_probability: 分支概率
        
        Returns:
            分支思维列表
        """
        if not self._current_node:
            return []
        
        branches = []
        
        if random.random() < branch_probability:
            num_branches = random.randint(1, 3)
            
            for _ in range(num_branches):
                branch_thought = self.associative_jump.jump(
                    self._current_node.thought,
                    random.random()
                )
                
                branch_node = StreamNode(thought=branch_thought)
                self._current_node.add_branch(
                    branch_node, 
                    1.0 / num_branches
                )
                
                branches.append(branch_thought)
        
        return branches
    
    def merge_branches(self) -> Optional[Thought]:
        """
        合并分支 - 将多个分支合并为一个思维
        
        Returns:
            合并后的思维
        """
        if not self._current_node or not self._current_node.next_nodes:
            return None
        
        branches = self._current_node.next_nodes
        contents = [n.thought.content for n in branches]
        
        combined = self.associative_jump.creative_leap(
            [str(c) for c in contents]
        )
        
        return combined
    
    def set_flow_speed(self, speed: float):
        """设置流动速度"""
        self.speed_controller.set_speed(speed)
    
    def accelerate(self):
        """加速流动"""
        self.speed_controller.accelerate()
    
    def decelerate(self):
        """减速流动"""
        self.speed_controller.decelerate()
    
    def get_stream_state(self) -> Dict[str, Any]:
        """获取意识流状态"""
        return {
            "current_speed": self.speed_controller._current_speed,
            "flow_state": self.speed_controller.get_state().value,
            "metrics": self.speed_controller.get_metrics().__dict__,
            "attention": self.focus_switch.get_attention_distribution(),
            "stream_length": len(self._stream_nodes),
            "branches_count": sum(
                len(n.next_nodes) for n in self._stream_nodes
            )
        }
    
    def get_stream_path(self, max_length: int = 20) -> List[str]:
        """获取意识流路径"""
        path = []
        node = self._current_node
        
        while node and len(path) < max_length:
            path.append(str(node.thought.content)[:50])
            node = node.prev_node
        
        return list(reversed(path))
    
    def inject_randomness(self, intensity: float = 0.5):
        """注入随机性到意识流"""
        if random.random() < intensity:
            penetration = self.layers.random_penetration()
            if penetration:
                self._add_to_stream(penetration)
        
        if random.random() < intensity * 0.5:
            self.speed_controller.set_speed(random.random())
        
        if random.random() < intensity * 0.3:
            self.focus_switch.random_switch()
