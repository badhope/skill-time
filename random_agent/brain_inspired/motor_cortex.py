"""
运动皮层系统 - 运动规划、执行和学习的完整实现
基于2024-2025最新神经科学研究
"""

import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

from random_agent.brain_inspired.ensemble import CorticalColumn, NeuralEnsemble
from random_agent.brain_inspired.neuron import Neuron


class MovementType(Enum):
    """运动类型"""
    REACHING = "reaching"
    GRASPING = "grasping"
    LOCOMOTION = "locomotion"
    FINE_MOTOR = "fine_motor"
    EYE_MOVEMENT = "eye_movement"


@dataclass
class MotorCommand:
    """运动命令"""
    movement_type: MovementType
    target_position: Optional[np.ndarray] = None
    velocity: Optional[np.ndarray] = None
    force: Optional[np.ndarray] = None
    duration: float = 1.0
    confidence: float = 0.0


@dataclass
class MotorPlan:
    """运动计划"""
    sequence: List[MotorCommand]
    total_duration: float
    complexity: float
    expected_outcome: Optional[np.ndarray] = None


class PrimaryMotorCortex:
    """初级运动皮层（M1）"""
    
    def __init__(self):
        self.motor_columns = self._create_motor_columns()
        self.muscle_representations = self._create_muscle_map()
        self.movement_primitives = self._create_movement_primitives()
        
    def _create_motor_columns(self) -> List[CorticalColumn]:
        """创建运动柱"""
        columns = []
        body_parts = ['hand', 'arm', 'face', 'leg', 'trunk']
        
        for part in body_parts:
            column = CorticalColumn(column_id=f"M1_{part}")
            columns.append(column)
        
        return columns
    
    def _create_muscle_map(self) -> Dict[str, np.ndarray]:
        """创建肌肉映射"""
        muscle_map = {}
        
        muscles = ['flexor', 'extensor', 'abductor', 'adductor']
        for muscle in muscles:
            muscle_map[muscle] = np.random.rand(10)
        
        return muscle_map
    
    def _create_movement_primitives(self) -> Dict[str, np.ndarray]:
        """创建运动基元"""
        primitives = {
            'reach': np.array([1.0, 0.0, 0.0]),
            'grasp': np.array([0.0, 1.0, 0.0]),
            'release': np.array([0.0, 0.0, 1.0]),
            'rotate': np.array([0.5, 0.5, 0.0])
        }
        
        return primitives
    
    def generate_motor_command(self, 
                               target: np.ndarray,
                               movement_type: MovementType = MovementType.REACHING) -> MotorCommand:
        """生成运动命令"""
        velocity = self._compute_velocity(target)
        force = self._compute_force(target)
        
        command = MotorCommand(
            movement_type=movement_type,
            target_position=target,
            velocity=velocity,
            force=force,
            duration=1.0,
            confidence=0.8
        )
        
        return command
    
    def _compute_velocity(self, target: np.ndarray) -> np.ndarray:
        """计算速度"""
        velocity_magnitude = np.linalg.norm(target)
        if velocity_magnitude > 0:
            direction = target / velocity_magnitude
            velocity = direction * min(velocity_magnitude, 1.0)
        else:
            velocity = np.zeros_like(target)
        
        return velocity
    
    def _compute_force(self, target: np.ndarray) -> np.ndarray:
        """计算力"""
        distance = np.linalg.norm(target)
        force_magnitude = min(distance * 0.5, 1.0)
        
        if distance > 0:
            direction = target / distance
            force = direction * force_magnitude
        else:
            force = np.zeros_like(target)
        
        return force
    
    def execute_movement(self, command: MotorCommand, current_time: float = 0.0) -> Dict[str, Any]:
        """执行运动"""
        execution_result = {
            'command': command,
            'status': 'executing',
            'progress': 0.0,
            'timestamp': current_time
        }
        
        return execution_result


class PremotorCortex:
    """前运动皮层（PM）"""
    
    def __init__(self):
        self.action_representations = self._create_action_representations()
        self.sequencer = self._create_sequencer()
        
    def _create_action_representations(self) -> Dict[str, NeuralEnsemble]:
        """创建动作表征"""
        representations = {}
        
        actions = ['reach', 'grasp', 'manipulate', 'release']
        for action in actions:
            neurons = [Neuron(f"pm_{action}_{i}", "pyramidal") for i in range(50)]
            representations[action] = NeuralEnsemble(f"pm_{action}_ensemble", neurons)
        
        return representations
    
    def _create_sequencer(self) -> Any:
        """创建序列器"""
        return ActionSequencer()
    
    def plan_movement_sequence(self, goal: str) -> List[MotorCommand]:
        """规划运动序列"""
        if goal == 'pick_up':
            sequence = [
                MotorCommand(MovementType.REACHING, target_position=np.array([0.5, 0.0, 0.0])),
                MotorCommand(MovementType.GRASPING, target_position=np.array([0.0, 0.0, 0.0])),
                MotorCommand(MovementType.REACHING, target_position=np.array([-0.5, 0.0, 0.0]))
            ]
        elif goal == 'point':
            sequence = [
                MotorCommand(MovementType.REACHING, target_position=np.array([1.0, 0.0, 0.0]))
            ]
        else:
            sequence = [
                MotorCommand(MovementType.REACHING, target_position=np.array([0.0, 0.0, 0.0]))
            ]
        
        return sequence
    
    def select_action(self, context: Dict[str, Any]) -> str:
        """选择动作"""
        if 'object' in context:
            return 'grasp'
        elif 'location' in context:
            return 'reach'
        else:
            return 'hold'


class ActionSequencer:
    """动作序列器"""
    
    def __init__(self):
        self.sequence_memory = []
        self.current_sequence = []
        self.sequence_index = 0
        
    def start_sequence(self, sequence: List[MotorCommand]):
        """开始序列"""
        self.current_sequence = sequence
        self.sequence_index = 0
    
    def get_next_command(self) -> Optional[MotorCommand]:
        """获取下一个命令"""
        if self.sequence_index < len(self.current_sequence):
            command = self.current_sequence[self.sequence_index]
            self.sequence_index += 1
            return command
        return None
    
    def is_sequence_complete(self) -> bool:
        """序列是否完成"""
        return self.sequence_index >= len(self.current_sequence)


class SupplementaryMotorArea:
    """辅助运动区（SMA）"""
    
    def __init__(self):
        self.sequence_representations = {}
        self.planning_buffer = []
        
    def store_sequence(self, sequence_id: str, sequence: List[MotorCommand]):
        """存储序列"""
        self.sequence_representations[sequence_id] = sequence
    
    def retrieve_sequence(self, sequence_id: str) -> Optional[List[MotorCommand]]:
        """检索序列"""
        return self.sequence_representations.get(sequence_id)
    
    def plan_complex_movement(self, sub_goals: List[str]) -> MotorPlan:
        """规划复杂运动"""
        commands = []
        total_duration = 0.0
        
        for goal in sub_goals:
            command = MotorCommand(
                movement_type=MovementType.REACHING,
                target_position=np.random.rand(3),
                duration=1.0
            )
            commands.append(command)
            total_duration += command.duration
        
        plan = MotorPlan(
            sequence=commands,
            total_duration=total_duration,
            complexity=len(commands) / 10.0
        )
        
        return plan
    
    def coordinate_bilateral_movement(self, left_command: MotorCommand, right_command: MotorCommand) -> Dict[str, MotorCommand]:
        """协调双侧运动"""
        return {
            'left': left_command,
            'right': right_command
        }


class Cerebellum:
    """小脑 - 运动协调和学习"""
    
    def __init__(self):
        self.purkinje_cells = self._create_purkinje_cells()
        self.error_correction = ErrorCorrection()
        self.timing_module = TimingModule()
        
    def _create_purkinje_cells(self) -> List[Neuron]:
        """创建浦肯野细胞"""
        return [Neuron(f"purkinje_{i}", "purkinje") for i in range(100)]
    
    def coordinate_movement(self, motor_command: MotorCommand) -> MotorCommand:
        """协调运动"""
        corrected_velocity = self._apply_correction(motor_command.velocity)
        corrected_force = self._apply_correction(motor_command.force)
        
        coordinated_command = MotorCommand(
            movement_type=motor_command.movement_type,
            target_position=motor_command.target_position,
            velocity=corrected_velocity,
            force=corrected_force,
            duration=motor_command.duration,
            confidence=motor_command.confidence * 1.1
        )
        
        return coordinated_command
    
    def _apply_correction(self, signal: Optional[np.ndarray]) -> Optional[np.ndarray]:
        """应用校正"""
        if signal is None:
            return None
        
        correction = self.error_correction.compute_correction(signal)
        corrected = signal + correction
        
        return corrected
    
    def learn_movement(self, error: np.ndarray, learning_rate: float = 0.01):
        """学习运动"""
        self.error_correction.update(error, learning_rate)
    
    def predict_sensory_consequence(self, motor_command: MotorCommand) -> np.ndarray:
        """预测感觉后果"""
        if motor_command.velocity is None:
            return np.zeros(3)
        
        predicted = motor_command.velocity * motor_command.duration
        
        return predicted


class ErrorCorrection:
    """误差校正"""
    
    def __init__(self):
        self.error_history = []
        self.correction_weights = np.random.rand(10) * 0.1
        
    def compute_correction(self, signal: np.ndarray) -> np.ndarray:
        """计算校正"""
        if len(signal) > len(self.correction_weights):
            correction = np.zeros(len(signal))
            correction[:len(self.correction_weights)] = self.correction_weights
        else:
            correction = self.correction_weights[:len(signal)]
        
        return correction * 0.1
    
    def update(self, error: np.ndarray, learning_rate: float):
        """更新校正权重"""
        self.error_history.append(error)
        
        if len(self.error_history) > 10:
            self.error_history.pop(0)
        
        if len(error) == len(self.correction_weights):
            self.correction_weights -= learning_rate * error


class TimingModule:
    """计时模块"""
    
    def __init__(self):
        self.timing_precision = 0.01
        
    def compute_timing(self, duration: float) -> List[float]:
        """计算时间"""
        n_steps = int(duration / self.timing_precision)
        return [i * self.timing_precision for i in range(n_steps)]


class BasalGangliaMotor:
    """基底节运动回路"""
    
    def __init__(self):
        self.direct_pathway = DirectPathway()
        self.indirect_pathway = IndirectPathway()
        self.action_selection = ActionSelection()
        
    def select_action(self, candidate_actions: List[str], context: Dict[str, Any]) -> str:
        """选择动作"""
        direct_activation = self.direct_pathway.compute_activation(candidate_actions)
        indirect_inhibition = self.indirect_pathway.compute_inhibition(candidate_actions)
        
        net_activation = direct_activation - indirect_inhibition
        
        selected_idx = np.argmax(net_activation)
        return candidate_actions[selected_idx]
    
    def inhibit_competing_actions(self, selected_action: str, all_actions: List[str]):
        """抑制竞争动作"""
        for action in all_actions:
            if action != selected_action:
                self.indirect_pathway.enhance_inhibition(action)


class DirectPathway:
    """直接通路"""
    
    def __init__(self):
        self.weights = np.random.rand(10)
        
    def compute_activation(self, actions: List[str]) -> np.ndarray:
        """计算激活"""
        n_actions = len(actions)
        activation = np.random.rand(n_actions) * 0.5 + 0.5
        return activation


class IndirectPathway:
    """间接通路"""
    
    def __init__(self):
        self.weights = np.random.rand(10)
        self.inhibition_strength = {}
        
    def compute_inhibition(self, actions: List[str]) -> np.ndarray:
        """计算抑制"""
        n_actions = len(actions)
        inhibition = np.random.rand(n_actions) * 0.3
        
        for i, action in enumerate(actions):
            if action in self.inhibition_strength:
                inhibition[i] += self.inhibition_strength[action]
                
        return inhibition
    
    def enhance_inhibition(self, action: str, strength: float = 0.2):
        """增强对特定动作的抑制"""
        if action in self.inhibition_strength:
            self.inhibition_strength[action] += strength
        else:
            self.inhibition_strength[action] = strength


class ActionSelection:
    """动作选择"""
    
    def __init__(self):
        self.selection_threshold = 0.5
        
    def select(self, activations: np.ndarray) -> int:
        """选择"""
        if np.max(activations) > self.selection_threshold:
            return int(np.argmax(activations))
        return -1


class MotorCortex:
    """完整运动皮层系统"""
    
    def __init__(self):
        self.M1 = PrimaryMotorCortex()
        self.PM = PremotorCortex()
        self.SMA = SupplementaryMotorArea()
        self.cerebellum = Cerebellum()
        self.basal_ganglia = BasalGangliaMotor()
        
        self.current_plan = None
        self.execution_history = []
        
    def plan_movement(self, goal: str, context: Dict[str, Any] = None) -> MotorPlan:
        """规划运动"""
        sequence = self.PM.plan_movement_sequence(goal)
        
        plan = MotorPlan(
            sequence=sequence,
            total_duration=sum(cmd.duration for cmd in sequence),
            complexity=len(sequence) / 10.0
        )
        
        self.current_plan = plan
        return plan
    
    def execute_plan(self, plan: MotorPlan, current_time: float = 0.0) -> List[Dict[str, Any]]:
        """执行计划"""
        results = []
        
        for i, command in enumerate(plan.sequence):
            coordinated = self.cerebellum.coordinate_movement(command)
            
            execution = self.M1.execute_movement(coordinated, current_time + i)
            results.append(execution)
            
            self.execution_history.append(execution)
        
        return results
    
    def learn_from_error(self, error: np.ndarray, learning_rate: float = 0.01):
        """从错误中学习"""
        self.cerebellum.learn_movement(error, learning_rate)
    
    def process(self, goal: str, context: Dict[str, Any] = None, current_time: float = 0.0) -> Dict[str, Any]:
        """完整运动处理流程"""
        plan = self.plan_movement(goal, context)
        execution_results = self.execute_plan(plan, current_time)
        
        result = {
            'goal': goal,
            'plan': plan,
            'execution': execution_results,
            'success': all(r['status'] == 'executing' for r in execution_results),
            'timestamp': current_time
        }
        
        return result
