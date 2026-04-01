"""
动态平衡控制器 (Dynamic Balance Controller)

核心理念：
- 随机性与确定性之间的动态平衡
- 探索与利用的权衡
- 发散与收敛的切换

调节因素：
1. 随机性旋钮 - 控制整体随机性水平
2. 探索/利用平衡 - 控制探索和利用的比例
3. 发散/收敛模式 - 控制思维模式
4. 能量管理 - 控制系统活跃度
"""

import random
import time
from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
from random_agent.core.randomness_engine import RandomnessEngine, RandomnessType


class ThinkingMode(Enum):
    """思维模式"""
    DIVERGENT = "divergent"     # 发散模式
    CONVERGENT = "convergent"   # 收敛模式
    BALANCED = "balanced"       # 平衡模式
    CREATIVE = "creative"       # 创造模式
    ANALYTICAL = "analytical"   # 分析模式


class RandomnessLevel(Enum):
    """随机性水平"""
    VERY_LOW = 0.1
    LOW = 0.25
    MEDIUM = 0.5
    HIGH = 0.75
    VERY_HIGH = 0.9


@dataclass
class BalanceState:
    """平衡状态"""
    randomness_level: float = 0.5
    exploration_ratio: float = 0.5
    thinking_mode: ThinkingMode = ThinkingMode.BALANCED
    energy_level: float = 1.0
    focus_level: float = 0.5
    creativity_boost: float = 0.0


@dataclass
class AdjustmentFactor:
    """调节因素"""
    name: str
    weight: float
    current_value: float
    target_value: float
    adjustment_rate: float = 0.1


class RandomnessKnob:
    """
    随机性旋钮
    
    控制系统整体的随机性水平
    """
    
    def __init__(self, randomness_engine: RandomnessEngine):
        self.randomness = randomness_engine
        self._level = 0.5
        self._min_level = 0.0
        self._max_level = 1.0
        self._adjustment_history: List[Dict] = []
    
    def set_level(self, level: float):
        """设置随机性水平"""
        self._level = max(self._min_level, min(self._max_level, level))
        
        self._adjustment_history.append({
            "action": "set",
            "level": self._level,
            "timestamp": time.time()
        })
    
    def adjust(self, delta: float):
        """调整随机性水平"""
        self._level = max(
            self._min_level, 
            min(self._max_level, self._level + delta)
        )
        
        self._adjustment_history.append({
            "action": "adjust",
            "delta": delta,
            "new_level": self._level,
            "timestamp": time.time()
        })
    
    def increase(self, amount: float = 0.1):
        """增加随机性"""
        self.adjust(amount)
    
    def decrease(self, amount: float = 0.1):
        """减少随机性"""
        self.adjust(-amount)
    
    def get_level(self) -> float:
        """获取当前水平"""
        return self._level
    
    def should_be_random(self) -> bool:
        """判断是否应该随机"""
        return random.random() < self._level
    
    def get_randomness_factor(self) -> float:
        """获取随机性因子"""
        return self._level + self.randomness.inject_randomness(0.0, 0.1)
    
    def auto_adjust(self, context: Dict):
        """根据上下文自动调整"""
        if context.get("stuck", False):
            self.increase(0.1)
        
        if context.get("close_to_goal", False):
            self.decrease(0.1)
        
        if context.get("need_creativity", False):
            self.increase(0.15)
        
        if context.get("need_precision", False):
            self.decrease(0.15)


class ExplorationExploitationBalancer:
    """
    探索/利用平衡器
    
    控制探索新可能性和利用已知信息之间的平衡
    """
    
    def __init__(self, randomness_engine: RandomnessEngine):
        self.randomness = randomness_engine
        self._exploration_ratio = 0.5
        self._exploration_count = 0
        self._exploitation_count = 0
        self._epsilon = 0.1
    
    def set_ratio(self, ratio: float):
        """设置探索比例"""
        self._exploration_ratio = max(0.0, min(1.0, ratio))
    
    def should_explore(self) -> bool:
        """判断是否应该探索"""
        if random.random() < self._epsilon:
            return True
        return random.random() < self._exploration_ratio
    
    def record_exploration(self):
        """记录探索"""
        self._exploration_count += 1
        self._auto_adjust()
    
    def record_exploitation(self):
        """记录利用"""
        self._exploitation_count += 1
        self._auto_adjust()
    
    def _auto_adjust(self):
        """自动调整比例"""
        total = self._exploration_count + self._exploitation_count
        if total > 10:
            actual_ratio = self._exploration_count / total
            
            if actual_ratio > self._exploration_ratio + 0.1:
                self._exploration_ratio = min(0.9, self._exploration_ratio + 0.05)
            elif actual_ratio < self._exploration_ratio - 0.1:
                self._exploration_ratio = max(0.1, self._exploration_ratio - 0.05)
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息"""
        total = self._exploration_count + self._exploitation_count
        return {
            "exploration_ratio": self._exploration_ratio,
            "exploration_count": self._exploration_count,
            "exploitation_count": self._exploitation_count,
            "actual_ratio": self._exploration_count / total if total > 0 else 0
        }


class ThinkingModeController:
    """
    思维模式控制器
    
    控制发散/收敛等思维模式的切换
    """
    
    def __init__(self, randomness_engine: RandomnessEngine):
        self.randomness = randomness_engine
        self._current_mode = ThinkingMode.BALANCED
        self._mode_history: List[Dict] = []
        self._mode_durations: Dict[ThinkingMode, float] = {
            mode: 0.0 for mode in ThinkingMode
        }
        self._last_mode_change = time.time()
    
    def set_mode(self, mode: ThinkingMode, reason: str = ""):
        """设置思维模式"""
        self._record_mode_duration()
        
        old_mode = self._current_mode
        self._current_mode = mode
        self._last_mode_change = time.time()
        
        self._mode_history.append({
            "from": old_mode.value,
            "to": mode.value,
            "reason": reason,
            "timestamp": time.time()
        })
        
        if len(self._mode_history) > 100:
            self._mode_history = self._mode_history[-100:]
    
    def _record_mode_duration(self):
        """记录模式持续时间"""
        duration = time.time() - self._last_mode_change
        self._mode_durations[self._current_mode] += duration
    
    def get_mode(self) -> ThinkingMode:
        """获取当前模式"""
        return self._current_mode
    
    def suggest_mode(self, context: Dict) -> ThinkingMode:
        """
        根据上下文建议思维模式
        
        Args:
            context: 上下文
        
        Returns:
            建议的模式
        """
        convergence_score = context.get("convergence_score", 0.5)
        creativity_need = context.get("creativity_need", 0.5)
        analysis_need = context.get("analysis_need", 0.5)
        
        if convergence_score > 0.7:
            return ThinkingMode.CONVERGENT
        
        if creativity_need > 0.7:
            return ThinkingMode.CREATIVE
        
        if analysis_need > 0.7:
            return ThinkingMode.ANALYTICAL
        
        if convergence_score < 0.3:
            return ThinkingMode.DIVERGENT
        
        return ThinkingMode.BALANCED
    
    def auto_switch(self, context: Dict):
        """自动切换模式"""
        suggested = self.suggest_mode(context)
        
        if suggested != self._current_mode:
            if random.random() < 0.3:
                self.set_mode(suggested, "auto_switch")
    
    def get_mode_characteristics(self) -> Dict[str, float]:
        """获取当前模式的特征"""
        characteristics = {
            ThinkingMode.DIVERGENT: {
                "randomness": 0.8,
                "exploration": 0.8,
                "creativity": 0.7,
                "focus": 0.3
            },
            ThinkingMode.CONVERGENT: {
                "randomness": 0.2,
                "exploration": 0.2,
                "creativity": 0.3,
                "focus": 0.9
            },
            ThinkingMode.BALANCED: {
                "randomness": 0.5,
                "exploration": 0.5,
                "creativity": 0.5,
                "focus": 0.5
            },
            ThinkingMode.CREATIVE: {
                "randomness": 0.7,
                "exploration": 0.7,
                "creativity": 0.9,
                "focus": 0.4
            },
            ThinkingMode.ANALYTICAL: {
                "randomness": 0.2,
                "exploration": 0.3,
                "creativity": 0.3,
                "focus": 0.8
            }
        }
        
        return characteristics.get(self._current_mode, characteristics[ThinkingMode.BALANCED])
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            "current_mode": self._current_mode.value,
            "mode_durations": {
                mode.value: duration 
                for mode, duration in self._mode_durations.items()
            },
            "switch_count": len(self._mode_history)
        }


class EnergyManager:
    """
    能量管理器
    
    管理系统的能量/活跃度
    """
    
    def __init__(self, randomness_engine: RandomnessEngine):
        self.randomness = randomness_engine
        self._energy = 1.0
        self._max_energy = 1.0
        self._min_energy = 0.1
        self._recovery_rate = 0.05
        self._consumption_rate = 0.02
        self._energy_history: List[float] = []
    
    def consume(self, amount: float = 0.02):
        """消耗能量"""
        self._energy = max(
            self._min_energy,
            self._energy - amount
        )
        self._record_energy()
    
    def recover(self, amount: float = 0.05):
        """恢复能量"""
        self._energy = min(
            self._max_energy,
            self._energy + amount
        )
        self._record_energy()
    
    def get_energy(self) -> float:
        """获取当前能量"""
        return self._energy
    
    def is_low_energy(self) -> bool:
        """判断是否低能量"""
        return self._energy < 0.3
    
    def _record_energy(self):
        """记录能量"""
        self._energy_history.append(self._energy)
        if len(self._energy_history) > 100:
            self._energy_history = self._energy_history[-100:]
    
    def auto_recover(self):
        """自动恢复"""
        self.recover(self._recovery_rate)
    
    def get_state(self) -> Dict[str, Any]:
        """获取状态"""
        return {
            "current_energy": self._energy,
            "is_low": self.is_low_energy(),
            "avg_energy": sum(self._energy_history) / len(self._energy_history) 
                         if self._energy_history else self._energy
        }


class BalanceController:
    """
    动态平衡控制器 - 整合所有平衡组件
    """
    
    def __init__(
        self, 
        randomness_engine: Optional[RandomnessEngine] = None
    ):
        self.randomness = randomness_engine or RandomnessEngine()
        
        self.randomness_knob = RandomnessKnob(self.randomness)
        self.exploration_balancer = ExplorationExploitationBalancer(self.randomness)
        self.mode_controller = ThinkingModeController(self.randomness)
        self.energy_manager = EnergyManager(self.randomness)
        
        self._state = BalanceState()
        self._adjustment_factors: Dict[str, AdjustmentFactor] = {}
        self._balance_history: List[Dict] = []
    
    def update(self, context: Optional[Dict] = None):
        """
        更新平衡状态
        
        Args:
            context: 上下文
        """
        context = context or {}
        
        self.randomness_knob.auto_adjust(context)
        
        self.mode_controller.auto_switch(context)
        
        if self.energy_manager.is_low_energy():
            self.energy_manager.auto_recover()
        else:
            self.energy_manager.consume()
        
        self._state = BalanceState(
            randomness_level=self.randomness_knob.get_level(),
            exploration_ratio=self.exploration_balancer._exploration_ratio,
            thinking_mode=self.mode_controller.get_mode(),
            energy_level=self.energy_manager.get_energy(),
            focus_level=self._calculate_focus_level(),
            creativity_boost=self._calculate_creativity_boost()
        )
        
        self._record_balance()
    
    def _calculate_focus_level(self) -> float:
        """计算专注水平"""
        mode_chars = self.mode_controller.get_mode_characteristics()
        energy = self.energy_manager.get_energy()
        
        focus = mode_chars["focus"] * 0.7 + energy * 0.3
        return focus
    
    def _calculate_creativity_boost(self) -> float:
        """计算创造力加成"""
        mode_chars = self.mode_controller.get_mode_characteristics()
        randomness = self.randomness_knob.get_level()
        
        boost = mode_chars["creativity"] * 0.6 + randomness * 0.4
        return boost
    
    def _record_balance(self):
        """记录平衡状态"""
        self._balance_history.append({
            "state": {
                "randomness": self._state.randomness_level,
                "exploration": self._state.exploration_ratio,
                "mode": self._state.thinking_mode.value,
                "energy": self._state.energy_level,
                "focus": self._state.focus_level,
                "creativity": self._state.creativity_boost
            },
            "timestamp": time.time()
        })
        
        if len(self._balance_history) > 200:
            self._balance_history = self._balance_history[-200:]
    
    def get_state(self) -> BalanceState:
        """获取当前状态"""
        return self._state
    
    def set_randomness(self, level: float):
        """设置随机性水平"""
        self.randomness_knob.set_level(level)
    
    def set_mode(self, mode: ThinkingMode):
        """设置思维模式"""
        self.mode_controller.set_mode(mode)
    
    def set_exploration_ratio(self, ratio: float):
        """设置探索比例"""
        self.exploration_balancer.set_ratio(ratio)
    
    def should_explore(self) -> bool:
        """判断是否应该探索"""
        return self.exploration_balancer.should_explore()
    
    def should_be_random(self) -> bool:
        """判断是否应该随机"""
        return self.randomness_knob.should_be_random()
    
    def record_exploration(self):
        """记录探索行为"""
        self.exploration_balancer.record_exploration()
    
    def record_exploitation(self):
        """记录利用行为"""
        self.exploration_balancer.record_exploitation()
    
    def get_adjustment_recommendations(self) -> List[str]:
        """获取调整建议"""
        recommendations = []
        
        if self._state.energy_level < 0.3:
            recommendations.append("能量较低，建议休息或简化任务")
        
        if self._state.randomness_level > 0.8:
            recommendations.append("随机性较高，可能需要更多聚焦")
        
        if self._state.randomness_level < 0.2:
            recommendations.append("随机性较低，可能需要更多探索")
        
        mode_stats = self.mode_controller.get_statistics()
        if mode_stats["switch_count"] > 10:
            recommendations.append("模式切换频繁，建议稳定当前模式")
        
        return recommendations
    
    def get_full_report(self) -> Dict[str, Any]:
        """获取完整报告"""
        return {
            "balance_state": {
                "randomness_level": self._state.randomness_level,
                "exploration_ratio": self._state.exploration_ratio,
                "thinking_mode": self._state.thinking_mode.value,
                "energy_level": self._state.energy_level,
                "focus_level": self._state.focus_level,
                "creativity_boost": self._state.creativity_boost
            },
            "randomness_knob": {
                "level": self.randomness_knob.get_level()
            },
            "exploration_balancer": self.exploration_balancer.get_statistics(),
            "mode_controller": self.mode_controller.get_statistics(),
            "energy_manager": self.energy_manager.get_state(),
            "recommendations": self.get_adjustment_recommendations()
        }
    
    def add_adjustment_factor(
        self, 
        name: str, 
        weight: float, 
        target_value: float,
        adjustment_rate: float = 0.1
    ):
        """添加调节因素"""
        self._adjustment_factors[name] = AdjustmentFactor(
            name=name,
            weight=weight,
            current_value=0.5,
            target_value=target_value,
            adjustment_rate=adjustment_rate
        )
    
    def apply_adjustment_factors(self):
        """应用调节因素"""
        for factor in self._adjustment_factors.values():
            diff = factor.target_value - factor.current_value
            factor.current_value += diff * factor.adjustment_rate
            
            if factor.name == "randomness":
                self.randomness_knob.set_level(
                    self.randomness_knob.get_level() + 
                    diff * factor.weight
                )
            elif factor.name == "exploration":
                self.exploration_balancer.set_ratio(
                    self.exploration_balancer._exploration_ratio + 
                    diff * factor.weight
                )
