"""
前额叶执行控制系统 - 高级认知功能的核心
基于前额叶皮层的神经科学原理设计
"""

import numpy as np
from typing import Dict, List, Any, Optional, Tuple, Callable
from dataclasses import dataclass, field
from datetime import datetime
import random
import math


@dataclass
class WorkingMemoryItem:
    """工作记忆项数据结构"""
    content: Any
    importance: float
    activation_level: float
    decay_rate: float
    created_at: float
    last_accessed: float


@dataclass
class Decision:
    """决策数据结构"""
    decision_id: str
    options: List[Any]
    selected_option: Any
    confidence: float
    reasoning: str
    timestamp: float = field(default_factory=lambda: datetime.now().timestamp())


@dataclass
class Plan:
    """规划数据结构"""
    plan_id: str
    goal: str
    steps: List[Dict[str, Any]]
    current_step: int
    estimated_duration: float
    priority: float
    status: str = 'pending'


class WorkingMemory:
    """工作记忆 - 暂存和操作信息
    
    基于前额叶的工作记忆功能
    容量有限，需要持续激活维持
    """
    
    def __init__(self, capacity: int = 7, decay_rate: float = 0.1):
        self.capacity = capacity
        self.decay_rate = decay_rate
        self.items: Dict[str, WorkingMemoryItem] = {}
        self.access_history = []
        
    def load(self, content: Any, importance: float = 0.5) -> bool:
        """加载内容到工作记忆
        
        Args:
            content: 内容
            importance: 重要性
            
        Returns:
            是否成功加载
        """
        if len(self.items) >= self.capacity:
            self._evict_least_important()
        
        item_id = self._generate_item_id(content)
        
        item = WorkingMemoryItem(
            content=content,
            importance=importance,
            activation_level=1.0,
            decay_rate=self.decay_rate,
            created_at=datetime.now().timestamp(),
            last_accessed=datetime.now().timestamp()
        )
        
        self.items[item_id] = item
        
        self._record_access('load', item_id)
        
        return True
    
    def retrieve(self, item_id: str) -> Optional[Any]:
        """检索工作记忆中的内容
        
        Args:
            item_id: 项目ID
            
        Returns:
            内容
        """
        if item_id not in self.items:
            return None
        
        item = self.items[item_id]
        item.activation_level = min(item.activation_level + 0.2, 1.0)
        item.last_accessed = datetime.now().timestamp()
        
        self._record_access('retrieve', item_id)
        
        return item.content
    
    def update(self, item_id: str, new_content: Any) -> bool:
        """更新工作记忆内容
        
        Args:
            item_id: 项目ID
            new_content: 新内容
            
        Returns:
            是否成功更新
        """
        if item_id not in self.items:
            return False
        
        self.items[item_id].content = new_content
        self.items[item_id].last_accessed = datetime.now().timestamp()
        
        self._record_access('update', item_id)
        
        return True
    
    def remove(self, item_id: str) -> bool:
        """从工作记忆中移除
        
        Args:
            item_id: 项目ID
            
        Returns:
            是否成功移除
        """
        if item_id in self.items:
            del self.items[item_id]
            self._record_access('remove', item_id)
            return True
        return False
    
    def decay(self):
        """衰减工作记忆"""
        items_to_remove = []
        
        for item_id, item in self.items.items():
            item.activation_level -= item.decay_rate
            
            if item.activation_level < 0.1:
                items_to_remove.append(item_id)
        
        for item_id in items_to_remove:
            self.remove(item_id)
    
    def refresh(self, item_id: str):
        """刷新工作记忆项"""
        if item_id in self.items:
            self.items[item_id].activation_level = 1.0
            self.items[item_id].last_accessed = datetime.now().timestamp()
    
    def get_contents(self) -> List[Any]:
        """获取所有内容"""
        return [item.content for item in self.items.values()]
    
    def get_load(self) -> float:
        """获取工作记忆负载"""
        return len(self.items) / self.capacity
    
    def _evict_least_important(self):
        """驱逐最不重要的项目"""
        if not self.items:
            return
        
        least_important_id = min(
            self.items.items(),
            key=lambda x: x[1].importance * x[1].activation_level
        )[0]
        
        self.remove(least_important_id)
    
    def _generate_item_id(self, content: Any) -> str:
        """生成项目ID"""
        import hashlib
        content_str = str(content) + str(datetime.now().timestamp())
        return hashlib.md5(content_str.encode()).hexdigest()[:8]
    
    def _record_access(self, action: str, item_id: str):
        """记录访问"""
        self.access_history.append({
            'action': action,
            'item_id': item_id,
            'timestamp': datetime.now().timestamp(),
        })
        
        if len(self.access_history) > 500:
            self.access_history = self.access_history[-250:]
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            'item_count': len(self.items),
            'capacity': self.capacity,
            'load': self.get_load(),
            'avg_activation': np.mean([item.activation_level for item in self.items.values()]) if self.items else 0.0,
            'avg_importance': np.mean([item.importance for item in self.items.values()]) if self.items else 0.0,
        }


class CognitiveFlexibility:
    """认知灵活性 - 任务切换和适应能力"""
    
    def __init__(self, switch_cost: float = 0.3):
        self.switch_cost = switch_cost
        self.current_task: Optional[str] = None
        self.task_history: List[str] = []
        self.switch_count = 0
        self.flexibility_score = 1.0
        
    def switch_task(self, new_task: str) -> float:
        """切换任务
        
        Args:
            new_task: 新任务
            
        Returns:
            切换成本
        """
        if self.current_task == new_task:
            return 0.0
        
        cost = self.switch_cost
        
        if self.task_history and len(self.task_history) > 0:
            recent_tasks = self.task_history[-5:]
            if new_task in recent_tasks:
                cost *= 0.5
        
        self.current_task = new_task
        self.task_history.append(new_task)
        self.switch_count += 1
        
        self._update_flexibility()
        
        return cost
    
    def assess(self) -> float:
        """评估认知灵活性
        
        Returns:
            灵活性分数
        """
        return self.flexibility_score
    
    def _update_flexibility(self):
        """更新灵活性分数"""
        if len(self.task_history) < 2:
            return
        
        recent_tasks = self.task_history[-10:]
        unique_tasks = len(set(recent_tasks))
        
        self.flexibility_score = min(unique_tasks / 5.0, 1.0)
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            'current_task': self.current_task,
            'switch_count': self.switch_count,
            'flexibility_score': self.flexibility_score,
            'task_history_length': len(self.task_history),
        }


class InhibitoryControl:
    """抑制控制 - 抑制不当反应"""
    
    def __init__(self, inhibition_strength: float = 0.7):
        self.inhibition_strength = inhibition_strength
        self.inhibition_history = []
        self.success_rate = 1.0
        
    def inhibit(self, 
               response: Any,
               context: Dict[str, Any]) -> Tuple[bool, float]:
        """抑制反应
        
        Args:
            response: 待抑制的反应
            context: 上下文
            
        Returns:
            (是否成功抑制, 抑制强度)
        """
        should_inhibit = self._should_inhibit(response, context)
        
        if should_inhibit:
            inhibition_success = random.random() < self.inhibition_strength
            
            self._record_inhibition(response, inhibition_success)
            
            return inhibition_success, self.inhibition_strength
        
        return False, 0.0
    
    def regulate(self, responses: List[Any]) -> List[Any]:
        """调节反应列表
        
        Args:
            responses: 反应列表
            
        Returns:
            调节后的反应列表
        """
        regulated = []
        
        for response in responses:
            should_inhibit = self._evaluate_response(response)
            
            if not should_inhibit:
                regulated.append(response)
        
        return regulated
    
    def _should_inhibit(self, response: Any, context: Dict[str, Any]) -> bool:
        """判断是否应该抑制"""
        inhibition_keywords = ['冲动', '不当', '错误', '风险']
        
        response_str = str(response).lower()
        
        for keyword in inhibition_keywords:
            if keyword in response_str:
                return True
        
        if 'goal' in context:
            goal = context['goal']
            if goal and goal not in response_str:
                return random.random() < 0.3
        
        return False
    
    def _evaluate_response(self, response: Any) -> bool:
        """评估反应是否应该抑制"""
        return random.random() < (1 - self.inhibition_strength) * 0.5
    
    def _record_inhibition(self, response: Any, success: bool):
        """记录抑制事件"""
        self.inhibition_history.append({
            'response': str(response)[:50],
            'success': success,
            'timestamp': datetime.now().timestamp(),
        })
        
        if len(self.inhibition_history) > 500:
            self.inhibition_history = self.inhibition_history[-250:]
        
        recent = self.inhibition_history[-20:]
        self.success_rate = sum(1 for h in recent if h['success']) / len(recent)
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            'inhibition_strength': self.inhibition_strength,
            'success_rate': self.success_rate,
            'inhibition_count': len(self.inhibition_history),
        }


class DecisionMaker:
    """决策制定器 - 评估选项并做出选择"""
    
    def __init__(self, 
                 decision_threshold: float = 0.6,
                 exploration_rate: float = 0.1):
        self.decision_threshold = decision_threshold
        self.exploration_rate = exploration_rate
        self.decision_history = []
        self.value_estimates: Dict[str, float] = {}
        
    def decide(self, 
              options: List[Any],
              context: Optional[Dict[str, Any]] = None) -> Decision:
        """做出决策
        
        Args:
            options: 选项列表
            context: 上下文
            
        Returns:
            决策结果
        """
        if not options:
            return Decision(
                decision_id='empty',
                options=[],
                selected_option=None,
                confidence=0.0,
                reasoning='No options available'
            )
        
        if len(options) == 1:
            return Decision(
                decision_id=self._generate_decision_id(),
                options=options,
                selected_option=options[0],
                confidence=1.0,
                reasoning='Only one option available'
            )
        
        if random.random() < self.exploration_rate:
            selected = random.choice(options)
            confidence = 0.5
            reasoning = 'Exploratory choice'
        else:
            scores = self._evaluate_options(options, context)
            
            max_score = max(scores.values())
            selected = max(scores.items(), key=lambda x: x[1])[0]
            
            sorted_scores = sorted(scores.values(), reverse=True)
            if len(sorted_scores) > 1:
                confidence = (sorted_scores[0] - sorted_scores[1]) / (sorted_scores[0] + 0.01)
            else:
                confidence = 1.0
            
            reasoning = self._generate_reasoning(selected, scores)
        
        decision = Decision(
            decision_id=self._generate_decision_id(),
            options=options,
            selected_option=selected,
            confidence=confidence,
            reasoning=reasoning
        )
        
        self.decision_history.append(decision)
        
        return decision
    
    def update_value(self, option: str, reward: float):
        """更新选项价值估计
        
        Args:
            option: 选项
            reward: 奖励
        """
        if option not in self.value_estimates:
            self.value_estimates[option] = 0.5
        
        learning_rate = 0.1
        self.value_estimates[option] += learning_rate * (reward - self.value_estimates[option])
    
    def _evaluate_options(self, 
                         options: List[Any],
                         context: Optional[Dict[str, Any]]) -> Dict[Any, float]:
        """评估选项"""
        scores = {}
        
        for option in options:
            base_score = self.value_estimates.get(str(option), 0.5)
            
            context_bonus = 0.0
            if context:
                context_bonus = self._calculate_context_bonus(option, context)
            
            scores[option] = base_score + context_bonus
        
        return scores
    
    def _calculate_context_bonus(self, option: Any, context: Dict[str, Any]) -> float:
        """计算上下文加成"""
        bonus = 0.0
        
        if 'goal' in context:
            goal = context['goal']
            if goal and goal in str(option):
                bonus += 0.2
        
        if 'urgency' in context:
            urgency = context['urgency']
            if urgency > 0.7:
                bonus += 0.1
        
        return bonus
    
    def _generate_reasoning(self, 
                           selected: Any,
                           scores: Dict[Any, float]) -> str:
        """生成推理说明"""
        selected_score = scores[selected]
        
        if selected_score > 0.8:
            return f"High confidence choice with score {selected_score:.2f}"
        elif selected_score > 0.6:
            return f"Moderate confidence choice with score {selected_score:.2f}"
        else:
            return f"Low confidence choice with score {selected_score:.2f}"
    
    def _generate_decision_id(self) -> str:
        """生成决策ID"""
        import hashlib
        content = str(datetime.now().timestamp())
        return hashlib.md5(content.encode()).hexdigest()[:8]
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            'decision_count': len(self.decision_history),
            'exploration_rate': self.exploration_rate,
            'avg_confidence': np.mean([d.confidence for d in self.decision_history]) if self.decision_history else 0.0,
            'value_estimates_count': len(self.value_estimates),
        }


class Planner:
    """规划器 - 制定和执行多步骤计划"""
    
    def __init__(self, max_plan_steps: int = 10):
        self.max_plan_steps = max_plan_steps
        self.active_plans: Dict[str, Plan] = {}
        self.plan_history = []
        
    def create_plan(self, 
                   goal: str,
                   available_actions: List[str],
                   priority: float = 0.5) -> Plan:
        """创建计划
        
        Args:
            goal: 目标
            available_actions: 可用动作
            priority: 优先级
            
        Returns:
            创建的计划
        """
        steps = self._generate_steps(goal, available_actions)
        
        plan = Plan(
            plan_id=self._generate_plan_id(),
            goal=goal,
            steps=steps,
            current_step=0,
            estimated_duration=len(steps) * 1.0,
            priority=priority
        )
        
        self.active_plans[plan.plan_id] = plan
        
        return plan
    
    def execute_step(self, plan_id: str) -> Optional[Dict[str, Any]]:
        """执行计划的下一步
        
        Args:
            plan_id: 计划ID
            
        Returns:
            当前步骤信息
        """
        if plan_id not in self.active_plans:
            return None
        
        plan = self.active_plans[plan_id]
        
        if plan.current_step >= len(plan.steps):
            plan.status = 'completed'
            self._archive_plan(plan)
            return None
        
        current_step = plan.steps[plan.current_step]
        plan.current_step += 1
        
        if plan.current_step >= len(plan.steps):
            plan.status = 'completed'
            self._archive_plan(plan)
        
        return current_step
    
    def get_next_action(self, plan_id: str) -> Optional[str]:
        """获取下一个动作
        
        Args:
            plan_id: 计划ID
            
        Returns:
            下一个动作
        """
        step = self.execute_step(plan_id)
        
        if step and 'action' in step:
            return step['action']
        
        return None
    
    def _generate_steps(self, 
                       goal: str,
                       available_actions: List[str]) -> List[Dict[str, Any]]:
        """生成计划步骤"""
        steps = []
        
        step_count = min(random.randint(3, 7), self.max_plan_steps)
        
        for i in range(step_count):
            if available_actions:
                action = random.choice(available_actions)
            else:
                action = f"step_{i+1}"
            
            steps.append({
                'step_number': i + 1,
                'action': action,
                'description': f"Execute {action} for goal: {goal}",
                'estimated_time': 1.0,
            })
        
        return steps
    
    def _archive_plan(self, plan: Plan):
        """归档计划"""
        self.plan_history.append({
            'plan_id': plan.plan_id,
            'goal': plan.goal,
            'status': plan.status,
            'steps_completed': plan.current_step,
            'total_steps': len(plan.steps),
            'timestamp': datetime.now().timestamp(),
        })
        
        if plan.plan_id in self.active_plans:
            del self.active_plans[plan.plan_id]
        
        if len(self.plan_history) > 500:
            self.plan_history = self.plan_history[-250:]
    
    def _generate_plan_id(self) -> str:
        """生成计划ID"""
        import hashlib
        content = str(datetime.now().timestamp())
        return hashlib.md5(content.encode()).hexdigest()[:8]
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            'active_plans': len(self.active_plans),
            'completed_plans': len([h for h in self.plan_history if h['status'] == 'completed']),
            'total_plans': len(self.plan_history),
        }


class PrefrontalExecutiveSystem:
    """前额叶执行控制系统
    
    基于前额叶皮层的神经科学原理，实现：
    - 工作记忆：信息暂存和操作
    - 认知灵活性：任务切换和适应
    - 抑制控制：抑制不当反应
    - 决策制定：评估和选择
    - 规划能力：制定和执行多步骤计划
    """
    
    def __init__(self,
                 working_memory_capacity: int = 7,
                 inhibition_strength: float = 0.7,
                 decision_threshold: float = 0.6):
        
        self.working_memory = WorkingMemory(capacity=working_memory_capacity)
        self.cognitive_flexibility = CognitiveFlexibility()
        self.inhibitory_control = InhibitoryControl(inhibition_strength=inhibition_strength)
        self.decision_maker = DecisionMaker(decision_threshold=decision_threshold)
        self.planner = Planner()
        
        self.current_goals: List[str] = []
        self.execution_history = []
        
    def control(self, 
               task: Any,
               goals: Optional[List[str]] = None) -> Decision:
        """执行控制
        
        Args:
            task: 任务
            goals: 目标列表
            
        Returns:
            决策结果
        """
        if goals:
            self.current_goals = goals
        
        self.working_memory.load(task, importance=0.8)
        
        options = self._generate_options(task)
        
        regulated_options = self.inhibitory_control.regulate(options)
        
        context = {
            'task': task,
            'goals': self.current_goals,
            'working_memory_load': self.working_memory.get_load(),
        }
        
        decision = self.decision_maker.decide(regulated_options, context)
        
        self._record_execution(task, decision)
        
        return decision
    
    def plan(self, goal: str, available_actions: List[str]) -> Plan:
        """制定计划
        
        Args:
            goal: 目标
            available_actions: 可用动作
            
        Returns:
            计划
        """
        self.current_goals.append(goal)
        
        plan = self.planner.create_plan(goal, available_actions)
        
        self.working_memory.load(plan, importance=0.9)
        
        return plan
    
    def execute_plan(self, plan_id: str) -> Optional[str]:
        """执行计划
        
        Args:
            plan_id: 计划ID
            
        Returns:
            下一个动作
        """
        action = self.planner.get_next_action(plan_id)
        
        if action:
            self.working_memory.load(action, importance=0.7)
        
        return action
    
    def switch_task(self, new_task: str) -> float:
        """切换任务
        
        Args:
            new_task: 新任务
            
        Returns:
            切换成本
        """
        return self.cognitive_flexibility.switch_task(new_task)
    
    def inhibit_response(self, response: Any) -> bool:
        """抑制反应
        
        Args:
            response: 待抑制的反应
            
        Returns:
            是否成功抑制
        """
        context = {'goals': self.current_goals}
        success, _ = self.inhibitory_control.inhibit(response, context)
        return success
    
    def update_decision_value(self, option: str, reward: float):
        """更新决策价值
        
        Args:
            option: 选项
            reward: 奖励
        """
        self.decision_maker.update_value(option, reward)
    
    def _generate_options(self, task: Any) -> List[str]:
        """生成选项"""
        base_options = [
            'analyze',
            'execute',
            'plan',
            'defer',
            'delegate',
        ]
        
        task_str = str(task).lower()
        
        if '紧急' in task_str or 'urgent' in task_str:
            base_options.insert(0, 'immediate_action')
        
        if '复杂' in task_str or 'complex' in task_str:
            base_options.insert(0, 'break_down')
        
        return base_options
    
    def _record_execution(self, task: Any, decision: Decision):
        """记录执行"""
        self.execution_history.append({
            'task': str(task)[:50],
            'decision': decision.selected_option,
            'confidence': decision.confidence,
            'timestamp': datetime.now().timestamp(),
        })
        
        if len(self.execution_history) > 500:
            self.execution_history = self.execution_history[-250:]
    
    def get_system_stats(self) -> Dict[str, Any]:
        """获取系统统计"""
        return {
            'working_memory': self.working_memory.get_stats(),
            'cognitive_flexibility': self.cognitive_flexibility.get_stats(),
            'inhibitory_control': self.inhibitory_control.get_stats(),
            'decision_maker': self.decision_maker.get_stats(),
            'planner': self.planner.get_stats(),
            'current_goals': self.current_goals,
            'execution_count': len(self.execution_history),
        }
    
    def reset(self):
        """重置系统"""
        self.working_memory = WorkingMemory(capacity=self.working_memory.capacity)
        self.cognitive_flexibility = CognitiveFlexibility()
        self.inhibitory_control = InhibitoryControl(
            inhibition_strength=self.inhibitory_control.inhibition_strength
        )
        self.decision_maker = DecisionMaker(
            decision_threshold=self.decision_maker.decision_threshold
        )
        self.planner = Planner()
        self.current_goals = []
        self.execution_history = []
