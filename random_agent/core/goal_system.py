"""
目标系统 (Goal System)

功能：
1. 目标设定 - 设定和追踪目标
2. 目标分解 - 将大目标分解为子目标
3. 收敛判断 - 判断何时收敛到答案
4. 进度追踪 - 追踪目标完成进度

设计理念：
- 目标是意识流的边界
- 随机性在边界内自由发挥
- 收敛是动态平衡的结果
"""

import random
import time
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from random_agent.core.randomness_engine import RandomnessEngine, RandomnessType


class GoalStatus(Enum):
    """目标状态"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ABANDONED = "abandoned"
    PAUSED = "paused"


class GoalPriority(Enum):
    """目标优先级"""
    LOW = 0.2
    MEDIUM = 0.5
    HIGH = 0.8
    CRITICAL = 1.0


@dataclass
class Goal:
    """目标"""
    id: str
    description: str
    status: GoalStatus = GoalStatus.PENDING
    priority: GoalPriority = GoalPriority.MEDIUM
    parent_id: Optional[str] = None
    sub_goals: List[str] = field(default_factory=list)
    created_at: float = field(default_factory=time.time)
    deadline: Optional[float] = None
    progress: float = 0.0
    checkpoints: List[Dict] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def add_checkpoint(self, description: str, completed: bool = False):
        """添加检查点"""
        self.checkpoints.append({
            "description": description,
            "completed": completed,
            "timestamp": time.time()
        })
    
    def update_progress(self, amount: float):
        """更新进度"""
        self.progress = max(0.0, min(1.0, self.progress + amount))
        if self.progress >= 1.0:
            self.status = GoalStatus.COMPLETED


@dataclass
class ConvergenceMetrics:
    """收敛指标"""
    relevance_score: float = 0.0
    coherence_score: float = 0.0
    completeness_score: float = 0.0
    stability_score: float = 0.0
    iteration_count: int = 0
    time_elapsed: float = 0.0


class GoalManager:
    """
    目标管理器
    
    管理目标的设定、追踪和完成
    """
    
    def __init__(self, randomness_engine: RandomnessEngine):
        self.randomness = randomness_engine
        self._goals: Dict[str, Goal] = {}
        self._active_goal_id: Optional[str] = None
        self._goal_history: List[Dict] = []
        self._id_counter: int = 0
    
    def _generate_id(self) -> str:
        """生成目标ID"""
        self._id_counter += 1
        return f"goal_{self._id_counter}"
    
    def set_goal(
        self, 
        description: str, 
        priority: GoalPriority = GoalPriority.MEDIUM,
        parent_id: Optional[str] = None,
        deadline: Optional[float] = None
    ) -> Goal:
        """
        设定目标
        
        Args:
            description: 目标描述
            priority: 优先级
            parent_id: 父目标ID
            deadline: 截止时间
        
        Returns:
            创建的目标
        """
        goal_id = self._generate_id()
        
        goal = Goal(
            id=goal_id,
            description=description,
            priority=priority,
            parent_id=parent_id,
            deadline=deadline
        )
        
        self._goals[goal_id] = goal
        
        if parent_id and parent_id in self._goals:
            self._goals[parent_id].sub_goals.append(goal_id)
        
        self._goal_history.append({
            "action": "created",
            "goal_id": goal_id,
            "description": description,
            "timestamp": time.time()
        })
        
        return goal
    
    def decompose_goal(
        self, 
        goal_id: str, 
        sub_descriptions: List[str]
    ) -> List[Goal]:
        """
        分解目标
        
        Args:
            goal_id: 目标ID
            sub_descriptions: 子目标描述列表
        
        Returns:
            创建的子目标列表
        """
        if goal_id not in self._goals:
            return []
        
        parent = self._goals[goal_id]
        sub_goals = []
        
        for desc in sub_descriptions:
            sub_goal = self.set_goal(
                description=desc,
                priority=parent.priority,
                parent_id=goal_id
            )
            sub_goals.append(sub_goal)
        
        self._goal_history.append({
            "action": "decomposed",
            "goal_id": goal_id,
            "sub_goals_count": len(sub_goals),
            "timestamp": time.time()
        })
        
        return sub_goals
    
    def activate_goal(self, goal_id: str) -> bool:
        """激活目标"""
        if goal_id in self._goals:
            self._active_goal_id = goal_id
            self._goals[goal_id].status = GoalStatus.IN_PROGRESS
            return True
        return False
    
    def get_active_goal(self) -> Optional[Goal]:
        """获取当前活跃目标"""
        if self._active_goal_id:
            return self._goals.get(self._active_goal_id)
        return None
    
    def update_progress(
        self, 
        goal_id: str, 
        progress: float
    ):
        """更新目标进度"""
        if goal_id in self._goals:
            goal = self._goals[goal_id]
            goal.update_progress(progress)
            
            if goal.status == GoalStatus.COMPLETED:
                self._propagate_completion(goal_id)
    
    def _propagate_completion(self, goal_id: str):
        """传播完成状态"""
        goal = self._goals[goal_id]
        
        if goal.parent_id:
            parent = self._goals.get(goal.parent_id)
            if parent:
                completed_subs = sum(
                    1 for sid in parent.sub_goals
                    if self._goals.get(sid, Goal(id="", description="")).status == GoalStatus.COMPLETED
                )
                if parent.sub_goals:
                    parent.progress = completed_subs / len(parent.sub_goals)
                    if parent.progress >= 1.0:
                        parent.status = GoalStatus.COMPLETED
                        self._propagate_completion(parent.id)
    
    def abandon_goal(self, goal_id: str, reason: str = ""):
        """放弃目标"""
        if goal_id in self._goals:
            self._goals[goal_id].status = GoalStatus.ABANDONED
            
            self._goal_history.append({
                "action": "abandoned",
                "goal_id": goal_id,
                "reason": reason,
                "timestamp": time.time()
            })
    
    def get_goal_tree(self, goal_id: Optional[str] = None) -> Dict:
        """获取目标树"""
        if goal_id is None:
            roots = [g for g in self._goals.values() if g.parent_id is None]
            return {
                "roots": [self._build_tree(r.id) for r in roots]
            }
        return self._build_tree(goal_id)
    
    def _build_tree(self, goal_id: str) -> Dict:
        """构建目标树"""
        goal = self._goals.get(goal_id)
        if not goal:
            return {}
        
        return {
            "id": goal.id,
            "description": goal.description,
            "status": goal.status.value,
            "progress": goal.progress,
            "sub_goals": [
                self._build_tree(sid) 
                for sid in goal.sub_goals 
                if sid in self._goals
            ]
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息"""
        status_counts = {}
        for goal in self._goals.values():
            status = goal.status.value
            status_counts[status] = status_counts.get(status, 0) + 1
        
        return {
            "total_goals": len(self._goals),
            "status_distribution": status_counts,
            "active_goal": self._active_goal_id,
            "history_count": len(self._goal_history)
        }


class ConvergenceDetector:
    """
    收敛检测器
    
    判断思考过程何时收敛到答案
    """
    
    def __init__(self, randomness_engine: RandomnessEngine):
        self.randomness = randomness_engine
        self._metrics = ConvergenceMetrics()
        self._thought_history: List[Dict] = []
        self._convergence_threshold = 0.7
        self._min_iterations = 3
        self._max_iterations = 20
    
    def add_thought(
        self, 
        thought: Any, 
        relevance: float,
        goal: str
    ):
        """
        添加思考记录
        
        Args:
            thought: 思考内容
            relevance: 与目标的相关性
            goal: 目标描述
        """
        self._thought_history.append({
            "content": str(thought)[:100],
            "relevance": relevance,
            "goal": goal,
            "timestamp": time.time()
        })
        
        self._metrics.iteration_count += 1
        
        self._update_metrics()
    
    def _update_metrics(self):
        """更新收敛指标"""
        if not self._thought_history:
            return
        
        recent = self._thought_history[-5:]
        
        self._metrics.relevance_score = sum(
            t["relevance"] for t in recent
        ) / len(recent)
        
        if len(self._thought_history) > 1:
            prev_relevance = self._thought_history[-2]["relevance"]
            curr_relevance = self._thought_history[-1]["relevance"]
            self._metrics.stability_score = 1.0 - abs(curr_relevance - prev_relevance)
        
        if self._thought_history:
            first_time = self._thought_history[0]["timestamp"]
            self._metrics.time_elapsed = time.time() - first_time
        
        unique_goals = set(t["goal"] for t in self._thought_history)
        self._metrics.coherence_score = (
            1.0 if len(unique_goals) == 1 else 0.5
        )
    
    def check_convergence(self) -> Dict[str, Any]:
        """
        检查是否收敛
        
        Returns:
            收敛判断结果
        """
        should_converge = False
        reason = ""
        
        if self._metrics.iteration_count < self._min_iterations:
            reason = f"迭代次数不足（{self._metrics.iteration_count}/{self._min_iterations}）"
        
        elif self._metrics.iteration_count >= self._max_iterations:
            should_converge = True
            reason = "达到最大迭代次数"
        
        elif self._metrics.relevance_score >= self._convergence_threshold:
            if self._metrics.stability_score >= 0.8:
                should_converge = True
                reason = "达到收敛条件：高相关性和稳定性"
            else:
                reason = "相关性高但稳定性不足"
        
        convergence_score = self._calculate_convergence_score()
        
        return {
            "should_converge": should_converge,
            "reason": reason,
            "convergence_score": convergence_score,
            "metrics": {
                "relevance": self._metrics.relevance_score,
                "stability": self._metrics.stability_score,
                "coherence": self._metrics.coherence_score,
                "iterations": self._metrics.iteration_count,
                "time_elapsed": self._metrics.time_elapsed
            }
        }
    
    def _calculate_convergence_score(self) -> float:
        """计算收敛分数"""
        weights = {
            "relevance": 0.4,
            "stability": 0.3,
            "coherence": 0.2,
            "progress": 0.1
        }
        
        progress_score = min(
            1.0, 
            self._metrics.iteration_count / self._max_iterations
        )
        
        score = (
            weights["relevance"] * self._metrics.relevance_score +
            weights["stability"] * self._metrics.stability_score +
            weights["coherence"] * self._metrics.coherence_score +
            weights["progress"] * progress_score
        )
        
        return score
    
    def reset(self):
        """重置收敛检测器"""
        self._metrics = ConvergenceMetrics()
        self._thought_history.clear()
    
    def set_threshold(self, threshold: float):
        """设置收敛阈值"""
        self._convergence_threshold = max(0.0, min(1.0, threshold))
    
    def get_progress(self) -> float:
        """获取收敛进度"""
        return self._calculate_convergence_score()


class GoalSystem:
    """
    目标系统 - 整合目标管理和收敛检测
    """
    
    def __init__(
        self, 
        randomness_engine: Optional[RandomnessEngine] = None
    ):
        self.randomness = randomness_engine or RandomnessEngine()
        
        self.manager = GoalManager(self.randomness)
        self.detector = ConvergenceDetector(self.randomness)
        
        self._current_trajectory: List[Dict] = []
        self._exploration_mode = False
    
    def set_main_goal(
        self, 
        description: str, 
        priority: GoalPriority = GoalPriority.HIGH
    ) -> Goal:
        """
        设定主目标
        
        Args:
            description: 目标描述
            priority: 优先级
        
        Returns:
            创建的目标
        """
        goal = self.manager.set_goal(description, priority)
        self.manager.activate_goal(goal.id)
        
        self.detector.reset()
        self._current_trajectory.clear()
        
        return goal
    
    def decompose(
        self, 
        sub_descriptions: List[str]
    ) -> List[Goal]:
        """
        分解当前目标
        
        Args:
            sub_descriptions: 子目标描述
        
        Returns:
            子目标列表
        """
        active = self.manager.get_active_goal()
        if active:
            return self.manager.decompose_goal(active.id, sub_descriptions)
        return []
    
    def record_progress(
        self, 
        thought: Any, 
        relevance: float
    ):
        """
        记录思考进度
        
        Args:
            thought: 思考内容
            relevance: 与目标的相关性
        """
        active = self.manager.get_active_goal()
        goal_desc = active.description if active else "未知目标"
        
        self.detector.add_thought(thought, relevance, goal_desc)
        
        self._current_trajectory.append({
            "thought": str(thought)[:100],
            "relevance": relevance,
            "timestamp": time.time()
        })
    
    def check_status(self) -> Dict[str, Any]:
        """
        检查目标状态
        
        Returns:
            状态信息
        """
        active = self.manager.get_active_goal()
        convergence = self.detector.check_convergence()
        
        return {
            "active_goal": {
                "id": active.id if active else None,
                "description": active.description if active else None,
                "progress": active.progress if active else 0.0,
                "status": active.status.value if active else None
            },
            "convergence": convergence,
            "trajectory_length": len(self._current_trajectory),
            "exploration_mode": self._exploration_mode
        }
    
    def should_explore(self) -> bool:
        """
        判断是否应该继续探索
        
        Returns:
            是否继续探索
        """
        convergence = self.detector.check_convergence()
        
        if convergence["should_converge"]:
            return False
        
        if convergence["convergence_score"] < 0.3:
            return True
        
        return self.randomness.random_choice(
            [True, False],
            weights=[0.3, 0.7],
            randomness_type=RandomnessType.QUANTUM
        )
    
    def set_exploration_mode(self, enabled: bool):
        """设置探索模式"""
        self._exploration_mode = enabled
    
    def get_next_sub_goal(self) -> Optional[Goal]:
        """
        获取下一个待完成的子目标
        
        Returns:
            子目标
        """
        active = self.manager.get_active_goal()
        if not active:
            return None
        
        for sub_id in active.sub_goals:
            sub = self.manager._goals.get(sub_id)
            if sub and sub.status == GoalStatus.PENDING:
                return sub
        
        return None
    
    def complete_current_sub_goal(self):
        """完成当前子目标"""
        active = self.manager.get_active_goal()
        if active:
            for sub_id in active.sub_goals:
                sub = self.manager._goals.get(sub_id)
                if sub and sub.status == GoalStatus.IN_PROGRESS:
                    sub.status = GoalStatus.COMPLETED
                    sub.progress = 1.0
                    self.manager._propagate_completion(sub_id)
                    break
    
    def get_trajectory(self) -> List[Dict]:
        """获取思考轨迹"""
        return self._current_trajectory.copy()
    
    def adjust_convergence_threshold(self, threshold: float):
        """调整收敛阈值"""
        self.detector.set_threshold(threshold)
    
    def get_goal_tree(self) -> Dict:
        """获取目标树"""
        return self.manager.get_goal_tree()
    
    def abandon_current_goal(self, reason: str = ""):
        """放弃当前目标"""
        active = self.manager.get_active_goal()
        if active:
            self.manager.abandon_goal(active.id, reason)
            self._current_trajectory.clear()
            self.detector.reset()
