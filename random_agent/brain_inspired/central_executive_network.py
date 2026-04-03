"""
中央执行网络系统 - 认知控制和目标导向行为
基于2024-2025最新神经科学研究
"""

import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

from random_agent.brain_inspired.ensemble import CorticalColumn, NeuralEnsemble
from random_agent.brain_inspired.neuron import Neuron


class ControlMode(Enum):
    """控制模式"""
    SUSTAINED = "sustained"
    SELECTIVE = "selective"
    DIVIDED = "divided"
    EXECUTIVE = "executive"


@dataclass
class AttentionFocus:
    """注意焦点"""
    target: Any
    intensity: float
    duration: float
    mode: ControlMode


@dataclass
class GoalState:
    """目标状态"""
    goal: str
    sub_goals: List[str]
    progress: float
    priority: float
    deadline: Optional[float] = None


class DorsolateralPrefrontalNetwork:
    """背外侧前额叶网络"""
    
    def __init__(self):
        self.working_memory = NetworkedWorkingMemory()
        self.goal_manager = GoalManager()
        self.control_signals = ControlSignalGenerator()
        
    def maintain_goal(self, goal: str, priority: float = 0.5):
        """维持目标"""
        self.goal_manager.set_goal(goal, priority)
    
    def update_working_memory(self, information: Any, salience: float = 0.5):
        """更新工作记忆"""
        self.working_memory.store(information, salience)
    
    def generate_control_signal(self, target: str, strength: float = 0.5) -> Dict[str, Any]:
        """生成控制信号"""
        return self.control_signals.generate(target, strength)
    
    def process(self, input_data: Dict[str, Any], current_time: float = 0.0) -> Dict[str, Any]:
        """处理输入"""
        if 'goal' in input_data:
            self.maintain_goal(input_data['goal'], input_data.get('priority', 0.5))
        
        if 'information' in input_data:
            self.update_working_memory(input_data['information'], input_data.get('salience', 0.5))
        
        control_signal = None
        if 'control_target' in input_data:
            control_signal = self.generate_control_signal(
                input_data['control_target'],
                input_data.get('control_strength', 0.5)
            )
        
        return {
            'goal_state': self.goal_manager.get_state(),
            'working_memory_state': self.working_memory.get_state(),
            'control_signal': control_signal,
            'timestamp': current_time
        }


class NetworkedWorkingMemory:
    """网络化工作记忆"""
    
    def __init__(self, capacity: int = 7):
        self.capacity = capacity
        self.items: List[Tuple[Any, float, float]] = []
        self.decay_rate = 0.05
        
    def store(self, information: Any, salience: float):
        """存储"""
        if len(self.items) >= self.capacity:
            self._evict()
        
        self.items.append((information, salience, 0.0))
    
    def _evict(self):
        """驱逐"""
        if self.items:
            min_idx = min(range(len(self.items)), key=lambda i: self.items[i][1])
            self.items.pop(min_idx)
    
    def retrieve(self, query: Any = None) -> Optional[Any]:
        """检索"""
        if not self.items:
            return None
        
        if query is None:
            return max(self.items, key=lambda x: x[1])[0]
        
        best_match = None
        best_score = 0.0
        
        for item, salience, _ in self.items:
            score = salience
            if score > best_score:
                best_score = score
                best_match = item
        
        return best_match
    
    def update(self, dt: float):
        """更新"""
        new_items = []
        for item, salience, age in self.items:
            new_salience = salience * (1 - self.decay_rate * dt)
            if new_salience > 0.1:
                new_items.append((item, new_salience, age + dt))
        
        self.items = new_items
    
    def get_state(self) -> Dict[str, Any]:
        """获取状态"""
        return {
            'n_items': len(self.items),
            'capacity': self.capacity,
            'total_salience': sum(s for _, s, _ in self.items)
        }


class GoalManager:
    """目标管理器"""
    
    def __init__(self):
        self.current_goal: Optional[GoalState] = None
        self.goal_stack: List[GoalState] = []
        self.max_goals = 5
        
    def set_goal(self, goal: str, priority: float = 0.5):
        """设置目标"""
        goal_state = GoalState(
            goal=goal,
            sub_goals=[],
            progress=0.0,
            priority=priority
        )
        
        if self.current_goal is None:
            self.current_goal = goal_state
        else:
            if priority > self.current_goal.priority:
                self.goal_stack.append(self.current_goal)
                self.current_goal = goal_state
            else:
                self.goal_stack.append(goal_state)
        
        if len(self.goal_stack) > self.max_goals:
            self.goal_stack.pop(0)
    
    def update_progress(self, progress: float):
        """更新进度"""
        if self.current_goal:
            self.current_goal.progress = progress
            
            if progress >= 1.0:
                self._complete_goal()
    
    def _complete_goal(self):
        """完成目标"""
        if self.goal_stack:
            self.current_goal = self.goal_stack.pop()
        else:
            self.current_goal = None
    
    def get_state(self) -> Dict[str, Any]:
        """获取状态"""
        return {
            'current_goal': self.current_goal.goal if self.current_goal else None,
            'current_progress': self.current_goal.progress if self.current_goal else 0.0,
            'n_pending_goals': len(self.goal_stack)
        }


class ControlSignalGenerator:
    """控制信号生成器"""
    
    def __init__(self):
        self.signal_strength = 0.5
        self.signal_duration = 1.0
        
    def generate(self, target: str, strength: float = 0.5) -> Dict[str, Any]:
        """生成"""
        return {
            'target': target,
            'strength': strength,
            'duration': self.signal_duration,
            'type': 'top_down_control'
        }


class PosteriorParietalNetwork:
    """后顶叶网络"""
    
    def __init__(self):
        self.attention_allocator = AttentionAllocator()
        self.spatial_controller = SpatialController()
        self.sensorimotor_coordinator = SensorimotorCoordinator()
        
    def allocate_attention(self, targets: List[Any], priorities: List[float]) -> AttentionFocus:
        """分配注意"""
        return self.attention_allocator.allocate(targets, priorities)
    
    def control_spatial_attention(self, location: Tuple[float, ...], spread: float = 1.0):
        """控制空间注意"""
        self.spatial_controller.focus(location, spread)
    
    def coordinate_sensorimotor(self, sensory: Dict[str, Any], motor: Dict[str, Any]) -> Dict[str, Any]:
        """协调感觉运动"""
        return self.sensorimotor_coordinator.coordinate(sensory, motor)
    
    def process(self, input_data: Dict[str, Any], current_time: float = 0.0) -> Dict[str, Any]:
        """处理输入"""
        attention_focus = None
        if 'attention_targets' in input_data:
            targets = input_data['attention_targets']
            priorities = input_data.get('attention_priorities', [0.5] * len(targets))
            attention_focus = self.allocate_attention(targets, priorities)
        
        spatial_state = None
        if 'spatial_location' in input_data:
            self.control_spatial_attention(
                input_data['spatial_location'],
                input_data.get('spatial_spread', 1.0)
            )
            spatial_state = self.spatial_controller.get_state()
        
        coordination = None
        if 'sensory' in input_data and 'motor' in input_data:
            coordination = self.coordinate_sensorimotor(input_data['sensory'], input_data['motor'])
        
        return {
            'attention_focus': attention_focus,
            'spatial_state': spatial_state,
            'sensorimotor_coordination': coordination,
            'timestamp': current_time
        }


class AttentionAllocator:
    """注意分配器"""
    
    def __init__(self):
        self.max_targets = 4
        self.allocation_strategy = 'priority'
        
    def allocate(self, targets: List[Any], priorities: List[float]) -> AttentionFocus:
        """分配"""
        if not targets:
            return AttentionFocus(
                target=None,
                intensity=0.0,
                duration=0.0,
                mode=ControlMode.SELECTIVE
            )
        
        max_priority_idx = int(np.argmax(priorities))
        selected_target = targets[max_priority_idx]
        intensity = priorities[max_priority_idx]
        
        mode = ControlMode.SELECTIVE
        if len(targets) > 1:
            mode = ControlMode.DIVIDED
        
        return AttentionFocus(
            target=selected_target,
            intensity=intensity,
            duration=1.0,
            mode=mode
        )


class SpatialController:
    """空间控制器"""
    
    def __init__(self):
        self.focus_location = (0.0, 0.0, 0.0)
        self.spread = 1.0
        
    def focus(self, location: Tuple[float, ...], spread: float = 1.0):
        """聚焦"""
        self.focus_location = location
        self.spread = spread
    
    def get_state(self) -> Dict[str, Any]:
        """获取状态"""
        return {
            'focus_location': self.focus_location,
            'spread': self.spread
        }


class SensorimotorCoordinator:
    """感觉运动协调器"""
    
    def __init__(self):
        self.calibration = np.eye(3)
        
    def coordinate(self, sensory: Dict[str, Any], motor: Dict[str, Any]) -> Dict[str, Any]:
        """协调"""
        return {
            'sensory': sensory,
            'motor': motor,
            'coordinated': True
        }


class ExecutiveControlSystem:
    """执行控制系统"""
    
    def __init__(self):
        self.inhibitor = InhibitoryControl()
        self.task_switcher = TaskSwitcher()
        self.conflict_resolver = ConflictResolver()
        
    def inhibit_distraction(self, distraction: Any, strength: float = 0.5):
        """抑制干扰"""
        self.inhibitor.inhibit(distraction, strength)
    
    def switch_task(self, new_task: str) -> bool:
        """切换任务"""
        return self.task_switcher.switch(new_task)
    
    def resolve_conflict(self, conflicts: List[Any]) -> Any:
        """解决冲突"""
        return self.conflict_resolver.resolve(conflicts)
    
    def process(self, input_data: Dict[str, Any], current_time: float = 0.0) -> Dict[str, Any]:
        """处理输入"""
        inhibition_result = None
        if 'distraction' in input_data:
            self.inhibit_distraction(
                input_data['distraction'],
                input_data.get('inhibition_strength', 0.5)
            )
            inhibition_result = self.inhibitor.get_state()
        
        switch_result = None
        if 'new_task' in input_data:
            switch_result = self.switch_task(input_data['new_task'])
        
        resolution = None
        if 'conflicts' in input_data:
            resolution = self.resolve_conflict(input_data['conflicts'])
        
        return {
            'inhibition': inhibition_result,
            'task_switch': switch_result,
            'conflict_resolution': resolution,
            'timestamp': current_time
        }


class InhibitoryControl:
    """抑制控制"""
    
    def __init__(self):
        self.inhibition_strength = 0.5
        self.inhibited_items = []
        
    def inhibit(self, item: Any, strength: float = 0.5):
        """抑制"""
        self.inhibited_items.append((item, strength))
        
        if len(self.inhibited_items) > 10:
            self.inhibited_items.pop(0)
    
    def get_state(self) -> Dict[str, Any]:
        """获取状态"""
        return {
            'n_inhibited': len(self.inhibited_items),
            'avg_strength': np.mean([s for _, s in self.inhibited_items]) if self.inhibited_items else 0.0
        }


class TaskSwitcher:
    """任务切换器"""
    
    def __init__(self):
        self.current_task = None
        self.task_stack = []
        self.switch_cost = 0.2
        
    def switch(self, new_task: str) -> bool:
        """切换"""
        if self.current_task:
            self.task_stack.append(self.current_task)
        
        self.current_task = new_task
        return True
    
    def get_switch_cost(self) -> float:
        """获取切换成本"""
        return self.switch_cost


class ConflictResolver:
    """冲突解决器"""
    
    def __init__(self):
        self.resolution_strategy = 'priority'
        
    def resolve(self, conflicts: List[Any]) -> Any:
        """解决"""
        if not conflicts:
            return None
        
        return conflicts[0]


class CentralExecutiveNetwork:
    """完整中央执行网络系统"""
    
    def __init__(self):
        self.dlPFC_network = DorsolateralPrefrontalNetwork()
        self.PP_network = PosteriorParietalNetwork()
        self.executive_control = ExecutiveControlSystem()
        
        self.network_activity = []
        
    def control_attention(self, target: Any, mode: ControlMode = ControlMode.SELECTIVE, current_time: float = 0.0) -> Dict[str, Any]:
        """控制注意"""
        dlPFC_result = self.dlPFC_network.process(
            {'control_target': str(target), 'control_strength': 0.7},
            current_time
        )
        
        PP_result = self.PP_network.process(
            {'attention_targets': [target], 'attention_priorities': [0.8]},
            current_time
        )
        
        result = {
            'attention_control': {
                'target': target,
                'mode': mode,
                'dlPFC': dlPFC_result,
                'PP': PP_result
            },
            'timestamp': current_time
        }
        
        self.network_activity.append(result)
        
        return result
    
    def maintain_information(self, information: Any, salience: float = 0.5, current_time: float = 0.0):
        """维持信息"""
        self.dlPFC_network.process(
            {'information': information, 'salience': salience},
            current_time
        )
    
    def set_goal(self, goal: str, priority: float = 0.5, current_time: float = 0.0):
        """设置目标"""
        self.dlPFC_network.process(
            {'goal': goal, 'priority': priority},
            current_time
        )
    
    def inhibit_distraction(self, distraction: Any, strength: float = 0.5, current_time: float = 0.0):
        """抑制干扰"""
        self.executive_control.process(
            {'distraction': distraction, 'inhibition_strength': strength},
            current_time
        )
    
    def switch_task(self, new_task: str, current_time: float = 0.0) -> bool:
        """切换任务"""
        result = self.executive_control.process(
            {'new_task': new_task},
            current_time
        )
        
        return result['task_switch']
    
    def process(self, input_data: Dict[str, Any], current_time: float = 0.0) -> Dict[str, Any]:
        """完整处理流程"""
        dlPFC_result = self.dlPFC_network.process(input_data, current_time)
        PP_result = self.PP_network.process(input_data, current_time)
        executive_result = self.executive_control.process(input_data, current_time)
        
        result = {
            'dlPFC': dlPFC_result,
            'PP': PP_result,
            'executive': executive_result,
            'network_state': 'active',
            'timestamp': current_time
        }
        
        self.network_activity.append(result)
        
        return result
