"""
神经元集群与皮层柱架构
实现从单个神经元到功能性集群的层次化组织
"""

import numpy as np
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import random
from collections import defaultdict

from .neuron import (
    Neuron, 
    Synapse, 
    IonChannelType,
    DendriticCompartment,
)


class NeuronType(Enum):
    """神经元类型"""
    PYRAMIDAL_RS = "pyramidal_regular_spiking"
    PYRAMIDAL_IB = "pyramidal_intrinsically_bursting"
    INTERNEURON_FS = "interneuron_fast_spiking"
    INTERNEURON_LTS = "interneuron_low_threshold_spiking"
    CHANDELIER = "chandelier"
    MARTINOTTI = "martinotti"
    GRANULE = "granule"
    STELLATE = "stellate"


class EnsembleState(Enum):
    """集群状态"""
    INACTIVE = "inactive"
    ACTIVE = "active"
    POTENTIATED = "potentiated"
    DEPRESSED = "depressed"


@dataclass
class EnsembleActivity:
    """集群活动记录"""
    timestamp: float
    activity_level: float
    active_neurons: List[str]
    synchrony_index: float
    mean_firing_rate: float


class NeuralEnsemble:
    """神经元集群 - 协同工作的神经元群体"""
    
    def __init__(self,
                 ensemble_id: str,
                 neurons: List[Neuron],
                 connection_probability: float = 0.1):
        
        self.ensemble_id = ensemble_id
        self.neurons = neurons
        self.neuron_map = {n.neuron_id: n for n in neurons}
        
        self.connection_matrix = self._build_connections(connection_probability)
        
        self.state = EnsembleState.INACTIVE
        self.activation_threshold = 0.3
        
        self.activity_history: List[EnsembleActivity] = []
        
        self.attractors: List[np.ndarray] = []
        self.attractor_labels: List[str] = []
        
        self.preferred_stimulus = None
        self.selectivity_index = 0.0
        
        self.plasticity_rate = 0.01
        
    def _build_connections(self, probability: float) -> np.ndarray:
        """构建集群内连接"""
        n = len(self.neurons)
        matrix = np.zeros((n, n))
        
        for i in range(n):
            for j in range(n):
                if i != j:
                    if self.neurons[i].neuron_type == 'pyramidal' and \
                       self.neurons[j].neuron_type == 'pyramidal':
                        if random.random() < probability * 0.5:
                            matrix[i, j] = random.uniform(0.1, 0.3)
                    
                    elif self.neurons[i].neuron_type == 'pyramidal' and \
                         self.neurons[j].neuron_type == 'interneuron':
                        if random.random() < probability:
                            matrix[i, j] = random.uniform(0.2, 0.5)
                    
                    elif self.neurons[i].neuron_type == 'interneuron' and \
                         self.neurons[j].neuron_type == 'pyramidal':
                        if random.random() < probability:
                            matrix[i, j] = -random.uniform(0.2, 0.5)
        
        return matrix
    
    def activate(self, 
                input_pattern: np.ndarray,
                current_time: float,
                dt: float) -> EnsembleActivity:
        """激活集群
        
        Args:
            input_pattern: 输入模式
            current_time: 当前时间
            dt: 时间步长
            
        Returns:
            集群活动记录
        """
        n = len(self.neurons)
        activities = np.zeros(n)
        spike_counts = np.zeros(n)
        
        for i, neuron in enumerate(self.neurons):
            external_input = input_pattern[i] if i < len(input_pattern) else 0
            
            internal_input = np.sum(self.connection_matrix[:, i] * activities)
            
            total_input = external_input + internal_input
            
            V, has_spiked = neuron.update(total_input, dt, current_time)
            
            activities[i] = neuron.firing_rate / 100.0
            spike_counts[i] = 1 if has_spiked else 0
        
        ensemble_activity = np.mean(activities)
        
        if ensemble_activity > self.activation_threshold:
            self.state = EnsembleState.ACTIVE
        else:
            self.state = EnsembleState.INACTIVE
        
        synchrony_index = self._compute_synchrony(spike_counts)
        
        active_neurons = [
            self.neurons[i].neuron_id 
            for i in range(n) 
            if activities[i] > 0.1
        ]
        
        activity_record = EnsembleActivity(
            timestamp=current_time,
            activity_level=ensemble_activity,
            active_neurons=active_neurons,
            synchrony_index=synchrony_index,
            mean_firing_rate=np.mean([n.firing_rate for n in self.neurons])
        )
        
        self.activity_history.append(activity_record)
        
        return activity_record
    
    def _compute_synchrony(self, spike_counts: np.ndarray) -> float:
        """计算同步指数"""
        if np.sum(spike_counts) == 0:
            return 0.0
        
        mean_rate = np.mean(spike_counts)
        variance = np.var(spike_counts)
        
        if mean_rate == 0:
            return 0.0
        
        synchrony = 1 - variance / (mean_rate * (1 - mean_rate) + 1e-6)
        
        return max(0, synchrony)
    
    def learn_pattern(self, 
                     pattern: np.ndarray,
                     label: str = "",
                     learning_rate: float = 0.01):
        """学习模式（吸引子）"""
        n = len(self.neurons)
        
        for i in range(n):
            for j in range(n):
                if i != j:
                    pre_activity = pattern[i] if i < len(pattern) else 0
                    post_activity = pattern[j] if j < len(pattern) else 0
                    
                    delta_w = learning_rate * pre_activity * post_activity
                    
                    if self.connection_matrix[i, j] > 0:
                        self.connection_matrix[i, j] += delta_w
                    else:
                        self.connection_matrix[i, j] -= delta_w * 0.5
        
        self.attractors.append(pattern.copy())
        self.attractor_labels.append(label)
        
        self._normalize_weights()
    
    def _normalize_weights(self):
        """归一化权重"""
        max_weight = np.max(np.abs(self.connection_matrix))
        if max_weight > 1.0:
            self.connection_matrix /= max_weight
    
    def recall_pattern(self, 
                      partial_pattern: np.ndarray,
                      current_time: float,
                      dt: float,
                      max_iterations: int = 100) -> Tuple[np.ndarray, float, str]:
        """回忆模式（模式完成）
        
        Args:
            partial_pattern: 部分模式
            current_time: 当前时间
            dt: 时间步长
            max_iterations: 最大迭代次数
            
        Returns:
            (完成的模式, 相似度, 标签)
        """
        current_pattern = partial_pattern.copy()
        
        for _ in range(max_iterations):
            activity = self.activate(current_pattern, current_time, dt)
            
            new_pattern = np.array([
                self.neurons[i].firing_rate / 100.0 
                for i in range(len(self.neurons))
            ])
            
            if np.allclose(current_pattern, new_pattern, atol=0.01):
                break
            
            current_pattern = new_pattern
        
        best_similarity = 0.0
        best_label = ""
        
        for attractor, label in zip(self.attractors, self.attractor_labels):
            similarity = np.dot(current_pattern, attractor) / (
                np.linalg.norm(current_pattern) * np.linalg.norm(attractor) + 1e-6
            )
            
            if similarity > best_similarity:
                best_similarity = similarity
                best_label = label
        
        return current_pattern, best_similarity, best_label
    
    def compute_selectivity(self, stimuli: List[np.ndarray]) -> float:
        """计算选择性指数"""
        responses = []
        
        for stimulus in stimuli:
            activity = self.activate(stimulus, 0.0, 1.0)
            responses.append(activity.activity_level)
        
        responses = np.array(responses)
        
        max_response = np.max(responses)
        mean_response = np.mean(responses)
        
        if max_response == 0:
            return 0.0
        
        self.selectivity_index = (max_response - mean_response) / max_response
        
        self.preferred_stimulus = stimuli[np.argmax(responses)]
        
        return self.selectivity_index
    
    def apply_neuromodulation(self, 
                             modulator: str,
                             level: float):
        """应用神经调质"""
        for neuron in self.neurons:
            neuron.neuromodulator_levels[modulator] = level
        
        if modulator == 'dopamine':
            self.plasticity_rate *= (1 + 0.5 * level)
        elif modulator == 'acetylcholine':
            self.activation_threshold *= (1 - 0.2 * level)
    
    def get_state(self) -> Dict[str, Any]:
        """获取集群状态"""
        return {
            'ensemble_id': self.ensemble_id,
            'state': self.state.value,
            'neuron_count': len(self.neurons),
            'active_neuron_count': len([
                n for n in self.neurons 
                if n.firing_rate > 0
            ]),
            'mean_firing_rate': np.mean([n.firing_rate for n in self.neurons]),
            'attractor_count': len(self.attractors),
            'selectivity_index': self.selectivity_index,
        }
    
    def reset(self):
        """重置集群状态"""
        self.state = EnsembleState.INACTIVE
        self.activity_history = []
        
        for neuron in self.neurons:
            neuron.reset()


class CorticalLayer:
    """皮层分层"""
    
    def __init__(self,
                 layer_name: str,
                 neuron_count: int,
                 neuron_types: List[str]):
        
        self.layer_name = layer_name
        self.neuron_count = neuron_count
        self.neuron_types = neuron_types
        
        self.neurons = self._create_neurons()
        
        self.ensembles: List[NeuralEnsemble] = []
        
        self.mean_activity = 0.0
        self.oscillation_phase = 0.0
        self.oscillation_frequency = 40.0
        
    def _create_neurons(self) -> List[Neuron]:
        """创建神经元"""
        neurons = []
        
        for i in range(self.neuron_count):
            neuron_type = random.choice(self.neuron_types)
            
            neuron_id = f"{self.layer_name}_neuron_{i}"
            
            neuron = Neuron(
                neuron_id=neuron_id,
                neuron_type=neuron_type
            )
            
            if neuron_type == 'pyramidal':
                dendrite = DendriticCompartment(
                    length=200.0,
                    diameter=2.0
                )
                neuron.add_dendrite(dendrite)
            
            neurons.append(neuron)
        
        return neurons
    
    def create_ensembles(self, 
                        ensemble_size: int = 10,
                        overlap: float = 0.2):
        """创建集群"""
        n_ensembles = int(self.neuron_count / (ensemble_size * (1 - overlap)))
        
        all_indices = list(range(self.neuron_count))
        random.shuffle(all_indices)
        
        for i in range(n_ensembles):
            start_idx = int(i * ensemble_size * (1 - overlap))
            end_idx = start_idx + ensemble_size
            
            if end_idx > self.neuron_count:
                break
            
            ensemble_neurons = [self.neurons[j] for j in all_indices[start_idx:end_idx]]
            
            ensemble = NeuralEnsemble(
                ensemble_id=f"{self.layer_name}_ensemble_{i}",
                neurons=ensemble_neurons
            )
            
            self.ensembles.append(ensemble)
    
    def activate(self, 
                input_activity: np.ndarray,
                current_time: float,
                dt: float) -> np.ndarray:
        """激活层
        
        Args:
            input_activity: 输入活动
            current_time: 当前时间
            dt: 时间步长
            
        Returns:
            层输出活动
        """
        output_activity = np.zeros(self.neuron_count)
        
        for i, neuron in enumerate(self.neurons):
            input_current = input_activity[i] if i < len(input_activity) else 0
            
            V, has_spiked = neuron.update(input_current, dt, current_time)
            
            output_activity[i] = neuron.firing_rate / 100.0
        
        self.mean_activity = np.mean(output_activity)
        
        self.oscillation_phase += 2 * np.pi * self.oscillation_frequency * dt / 1000.0
        self.oscillation_phase = self.oscillation_phase % (2 * np.pi)
        
        return output_activity
    
    def get_state(self) -> Dict[str, Any]:
        """获取层状态"""
        return {
            'layer_name': self.layer_name,
            'neuron_count': self.neuron_count,
            'ensemble_count': len(self.ensembles),
            'mean_activity': self.mean_activity,
            'oscillation_phase': self.oscillation_phase,
            'oscillation_frequency': self.oscillation_frequency,
        }


class CorticalColumn:
    """皮层柱 - 皮层的基本功能单元"""
    
    def __init__(self, column_id: str):
        self.column_id = column_id
        
        self.layers = self._create_layers()
        
        self.interlaminar_connections = self._build_interlaminar_connections()
        
        self.column_activity = 0.0
        self.preferred_stimulus = None
        self.orientation_tuning = None
        
        self.processing_history = []
        
    def _create_layers(self) -> Dict[str, CorticalLayer]:
        """创建皮层分层"""
        layers = {}
        
        layers['I'] = CorticalLayer(
            layer_name='I',
            neuron_count=500,
            neuron_types=['horizontal']
        )
        
        layers['II'] = CorticalLayer(
            layer_name='II',
            neuron_count=2000,
            neuron_types=['pyramidal_small', 'granule']
        )
        
        layers['III'] = CorticalLayer(
            layer_name='III',
            neuron_count=3000,
            neuron_types=['pyramidal_medium', 'interneuron']
        )
        
        layers['IV'] = CorticalLayer(
            layer_name='IV',
            neuron_count=2500,
            neuron_types=['stellate', 'pyramidal_small']
        )
        
        layers['V'] = CorticalLayer(
            layer_name='V',
            neuron_count=1500,
            neuron_types=['pyramidal_large', 'interneuron']
        )
        
        layers['VI'] = CorticalLayer(
            layer_name='VI',
            neuron_count=1000,
            neuron_types=['fusiform', 'pyramidal']
        )
        
        for layer in layers.values():
            layer.create_ensembles(ensemble_size=20, overlap=0.3)
        
        return layers
    
    def _build_interlaminar_connections(self) -> Dict[Tuple[str, str], str]:
        """构建层间连接"""
        connections = {
            ('IV', 'III'): 'feedforward',
            ('III', 'II'): 'feedback',
            ('III', 'V'): 'feedforward',
            ('V', 'VI'): 'feedforward',
            ('VI', 'IV'): 'feedback',
            ('I', 'II'): 'horizontal',
            ('II', 'III'): 'lateral',
            ('V', 'III'): 'feedback',
        }
        
        return connections
    
    def process(self, 
               thalamic_input: np.ndarray,
               current_time: float,
               dt: float) -> Dict[str, Any]:
        """处理输入
        
        Args:
            thalamic_input: 丘脑输入
            current_time: 当前时间
            dt: 时间步长
            
        Returns:
            处理结果
        """
        layer4_activity = self.layers['IV'].activate(thalamic_input, current_time, dt)
        
        layer3_input = np.zeros(self.layers['III'].neuron_count)
        layer3_input[:len(layer4_activity)] = layer4_activity[:len(layer3_input)]
        layer3_activity = self.layers['III'].activate(layer3_input, current_time, dt)
        
        layer2_input = np.zeros(self.layers['II'].neuron_count)
        layer2_input[:len(layer3_activity)] = layer3_activity[:len(layer2_input)]
        layer2_activity = self.layers['II'].activate(layer2_input, current_time, dt)
        
        layer5_input = np.zeros(self.layers['V'].neuron_count)
        layer5_input[:len(layer3_activity)] = layer3_activity[:len(layer5_input)]
        layer5_activity = self.layers['V'].activate(layer5_input, current_time, dt)
        
        layer6_input = np.zeros(self.layers['VI'].neuron_count)
        layer6_input[:len(layer5_activity)] = layer5_activity[:len(layer6_input)]
        layer6_activity = self.layers['VI'].activate(layer6_input, current_time, dt)
        
        feedback_to_layer4 = np.zeros(len(thalamic_input))
        feedback_to_layer4[:len(layer6_activity)] = layer6_activity[:len(feedback_to_layer4)] * 0.3
        
        layer4_activity_updated = self.layers['IV'].activate(
            thalamic_input + feedback_to_layer4,
            current_time,
            dt
        )
        
        output = layer5_activity
        
        self.column_activity = np.mean([
            self.layers['IV'].mean_activity,
            self.layers['III'].mean_activity,
            self.layers['V'].mean_activity,
        ])
        
        result = {
            'column_id': self.column_id,
            'timestamp': current_time,
            'column_activity': self.column_activity,
            'layer_activities': {
                'II': np.mean(layer2_activity),
                'III': np.mean(layer3_activity),
                'IV': np.mean(layer4_activity),
                'V': np.mean(layer5_activity),
                'VI': np.mean(layer6_activity),
            },
            'output': output,
        }
        
        self.processing_history.append(result)
        
        return result
    
    def compute_orientation_tuning(self, 
                                  orientations: List[float],
                                  stimuli: List[np.ndarray]) -> Dict[str, Any]:
        """计算方向调谐"""
        responses = []
        
        for stimulus in stimuli:
            result = self.process(stimulus, 0.0, 1.0)
            responses.append(result['column_activity'])
        
        responses = np.array(responses)
        
        preferred_idx = np.argmax(responses)
        self.preferred_stimulus = orientations[preferred_idx]
        
        max_response = np.max(responses)
        half_max = max_response / 2
        
        tuning_width = 0.0
        for i, (ori, resp) in enumerate(zip(orientations, responses)):
            if resp >= half_max:
                tuning_width += abs(orientations[(i + 1) % len(orientations)] - ori)
        
        self.orientation_tuning = {
            'preferred_orientation': self.preferred_stimulus,
            'tuning_width': tuning_width,
            'max_response': max_response,
            'selectivity': (max_response - np.mean(responses)) / max_response,
        }
        
        return self.orientation_tuning
    
    def apply_neuromodulation(self, 
                             modulator: str,
                             level: float):
        """应用神经调质"""
        for layer in self.layers.values():
            for neuron in layer.neurons:
                neuron.neuromodulator_levels[modulator] = level
            
            for ensemble in layer.ensembles:
                ensemble.apply_neuromodulation(modulator, level)
    
    def get_state(self) -> Dict[str, Any]:
        """获取皮层柱状态"""
        layer_states = {
            name: layer.get_state() 
            for name, layer in self.layers.items()
        }
        
        return {
            'column_id': self.column_id,
            'column_activity': self.column_activity,
            'preferred_stimulus': self.preferred_stimulus,
            'orientation_tuning': self.orientation_tuning,
            'layers': layer_states,
            'total_neurons': sum(
                layer.neuron_count for layer in self.layers.values()
            ),
        }
    
    def reset(self):
        """重置皮层柱状态"""
        self.column_activity = 0.0
        
        for layer in self.layers.values():
            layer.reset()


class Minicolumn:
    """微柱 - 皮层柱的子单元"""
    
    def __init__(self, 
                 minicolumn_id: str,
                 parent_column: CorticalColumn,
                 neuron_count: int = 100):
        
        self.minicolumn_id = minicolumn_id
        self.parent_column = parent_column
        self.neuron_count = neuron_count
        
        self.neurons = self._create_neurons()
        
        self.activity = 0.0
        self.winner = False
        
    def _create_neurons(self) -> List[Neuron]:
        """创建神经元"""
        neurons = []
        
        for i in range(self.neuron_count):
            neuron = Neuron(
                neuron_id=f"{self.minicolumn_id}_neuron_{i}",
                neuron_type='pyramidal' if random.random() > 0.2 else 'interneuron'
            )
            neurons.append(neuron)
        
        return neurons
    
    def activate(self, 
                input_pattern: np.ndarray,
                current_time: float,
                dt: float) -> float:
        """激活微柱"""
        activities = []
        
        for i, neuron in enumerate(self.neurons):
            input_current = input_pattern[i] if i < len(input_pattern) else 0
            
            V, has_spiked = neuron.update(input_current, dt, current_time)
            activities.append(neuron.firing_rate / 100.0)
        
        self.activity = np.mean(activities)
        
        return self.activity
    
    def compete(self, other_minicolumns: List['Minicolumn']) -> bool:
        """竞争（胜者全得）"""
        max_activity = max(mc.activity for mc in other_minicolumns)
        
        self.winner = (self.activity >= max_activity)
        
        return self.winner
    
    def reset(self):
        """重置微柱状态"""
        self.activity = 0.0
        self.winner = False
        
        for neuron in self.neurons:
            neuron.reset()


class Hypercolumn:
    """超柱 - 多个皮层柱的集合"""
    
    def __init__(self, 
                 hypercolumn_id: str,
                 column_count: int = 10):
        
        self.hypercolumn_id = hypercolumn_id
        self.column_count = column_count
        
        self.columns = self._create_columns()
        
        self.minicolumns = self._create_minicolumns()
        
        self.winning_column = None
        self.hypercolumn_activity = 0.0
        
    def _create_columns(self) -> List[CorticalColumn]:
        """创建皮层柱"""
        columns = []
        
        for i in range(self.column_count):
            column = CorticalColumn(
                column_id=f"{self.hypercolumn_id}_column_{i}"
            )
            columns.append(column)
        
        return columns
    
    def _create_minicolumns(self) -> List[List[Minicolumn]]:
        """创建微柱"""
        minicolumns = []
        
        for column in self.columns:
            column_minicolumns = []
            
            for i in range(10):
                minicolumn = Minicolumn(
                    minicolumn_id=f"{column.column_id}_mini_{i}",
                    parent_column=column,
                    neuron_count=100
                )
                column_minicolumns.append(minicolumn)
            
            minicolumns.append(column_minicolumns)
        
        return minicolumns
    
    def process(self, 
               input_pattern: np.ndarray,
               current_time: float,
               dt: float) -> Dict[str, Any]:
        """处理输入（竞争）"""
        column_activities = []
        
        for i, column in enumerate(self.columns):
            result = column.process(input_pattern, current_time, dt)
            column_activities.append(result['column_activity'])
        
        winning_idx = np.argmax(column_activities)
        self.winning_column = self.columns[winning_idx]
        
        self.hypercolumn_activity = np.mean(column_activities)
        
        return {
            'hypercolumn_id': self.hypercolumn_id,
            'winning_column_id': self.winning_column.column_id,
            'column_activities': column_activities,
            'hypercolumn_activity': self.hypercolumn_activity,
        }
    
    def get_state(self) -> Dict[str, Any]:
        """获取超柱状态"""
        return {
            'hypercolumn_id': self.hypercolumn_id,
            'column_count': self.column_count,
            'winning_column': self.winning_column.column_id if self.winning_column else None,
            'hypercolumn_activity': self.hypercolumn_activity,
            'columns': [col.get_state() for col in self.columns],
        }
    
    def reset(self):
        """重置超柱状态"""
        self.winning_column = None
        self.hypercolumn_activity = 0.0
        
        for column in self.columns:
            column.reset()
