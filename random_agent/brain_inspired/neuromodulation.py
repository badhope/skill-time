"""
神经调质系统与突触可塑性
实现多巴胺、乙酰胆碱、血清素、去甲肾上腺素的调节机制
"""

import numpy as np
from typing import Dict, List, Any, Optional, Tuple, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import random
from collections import defaultdict


class NeuromodulatorType(Enum):
    """神经调质类型"""
    DOPAMINE = "dopamine"
    ACETYLCHOLINE = "acetylcholine"
    SEROTONIN = "serotonin"
    NOREPINEPHRINE = "norepinephrine"


class ReceptorFamily(Enum):
    """受体家族"""
    D1_LIKE = "d1_like"
    D2_LIKE = "d2_like"
    NICOTINIC = "nicotinic"
    MUSCARINIC = "muscarinic"
    HT1 = "5ht1"
    HT2 = "5ht2"
    ALPHA = "alpha"
    BETA = "beta"


@dataclass
class NeuromodulatorState:
    """神经调质状态"""
    concentration: float
    release_rate: float
    clearance_rate: float
    baseline: float
    target_regions: List[str]


class Neuromodulator:
    """神经调质基类"""
    
    def __init__(self, 
                 modulator_type: NeuromodulatorType,
                 baseline: float = 0.5):
        
        self.modulator_type = modulator_type
        self.baseline = baseline
        
        self.state = NeuromodulatorState(
            concentration=baseline,
            release_rate=0.0,
            clearance_rate=0.1,
            baseline=baseline,
            target_regions=[]
        )
        
        self.receptors = self._define_receptors()
        
        self.release_history = []
        
    def _define_receptors(self) -> Dict[str, Dict[str, Any]]:
        """定义受体"""
        raise NotImplementedError
    
    def release(self, 
               stimulus_value: float,
               prediction_error: float = 0.0,
               context: Optional[Dict[str, Any]] = None):
        """释放神经调质"""
        raise NotImplementedError
    
    def update(self, dt: float):
        """更新浓度"""
        self.state.concentration += self.state.release_rate * dt
        
        decay = self.state.clearance_rate * (self.state.concentration - self.baseline)
        self.state.concentration -= decay * dt
        
        self.state.concentration = np.clip(self.state.concentration, 0.0, 1.0)
        
        self.state.release_rate *= 0.9
    
    def modulate_neuron(self, 
                       neuron,
                       receptor_type: str) -> float:
        """调制神经元"""
        if receptor_type not in self.receptors:
            return 0.0
        
        receptor = self.receptors[receptor_type]
        
        effect = self.state.concentration * receptor['efficacy']
        
        if receptor['effect_type'] == 'excitatory':
            neuron.excitability *= (1 + effect)
        elif receptor['effect_type'] == 'inhibitory':
            neuron.excitability *= (1 - effect)
        elif receptor['effect_type'] == 'plasticity':
            neuron.plasticity_rate *= (1 + effect)
        
        return effect
    
    def get_state(self) -> Dict[str, Any]:
        """获取状态"""
        return {
            'modulator_type': self.modulator_type.value,
            'concentration': self.state.concentration,
            'baseline': self.state.baseline,
            'release_rate': self.state.release_rate,
        }


class Dopamine(Neuromodulator):
    """多巴胺系统"""
    
    def __init__(self, baseline: float = 0.3):
        super().__init__(NeuromodulatorType.DOPAMINE, baseline)
        
        self.reward_prediction = 0.0
        self.reward_history = []
        
        self.td_error = 0.0
        
    def _define_receptors(self) -> Dict[str, Dict[str, Any]]:
        """定义多巴胺受体"""
        return {
            'D1': {
                'family': ReceptorFamily.D1_LIKE,
                'effect_type': 'excitatory',
                'efficacy': 0.3,
                'target': 'PFC',
                'coupling': 'Gs',
            },
            'D2': {
                'family': ReceptorFamily.D2_LIKE,
                'effect_type': 'inhibitory',
                'efficacy': 0.25,
                'target': 'striatum',
                'coupling': 'Gi',
            },
            'D3': {
                'family': ReceptorFamily.D2_LIKE,
                'effect_type': 'inhibitory',
                'efficacy': 0.2,
                'target': 'nucleus_accumbens',
                'coupling': 'Gi',
            },
            'D4': {
                'family': ReceptorFamily.D2_LIKE,
                'effect_type': 'inhibitory',
                'efficacy': 0.15,
                'target': 'PFC',
                'coupling': 'Gi',
            },
            'D5': {
                'family': ReceptorFamily.D1_LIKE,
                'effect_type': 'excitatory',
                'efficacy': 0.2,
                'target': 'hippocampus',
                'coupling': 'Gs',
            },
        }
    
    def release(self, 
               reward: float,
               prediction_error: Optional[float] = None,
               context: Optional[Dict[str, Any]] = None):
        """释放多巴胺（基于奖励预测误差）"""
        
        if prediction_error is None:
            self.td_error = reward - self.reward_prediction
        else:
            self.td_error = prediction_error
        
        if self.td_error > 0:
            release_amount = 0.5 + 0.5 * self.td_error
        elif self.td_error < 0:
            release_amount = 0.1 * (1 + self.td_error)
        else:
            release_amount = self.baseline
        
        self.state.release_rate = release_amount
        
        self.reward_prediction = 0.3 * reward + 0.7 * self.reward_prediction
        
        self.reward_history.append({
            'reward': reward,
            'prediction': self.reward_prediction,
            'td_error': self.td_error,
            'release': release_amount,
        })
        
        self.release_history.append({
            'timestamp': datetime.now().isoformat(),
            'concentration': self.state.concentration,
            'td_error': self.td_error,
        })
    
    def compute_motivation(self, reward_value: float, effort_cost: float) -> float:
        """计算动机水平"""
        net_value = reward_value - effort_cost
        
        motivation = self.state.concentration * net_value
        
        return max(0, motivation)
    
    def modulate_plasticity(self, 
                           pre_activity: float,
                           post_activity: float,
                           current_weight: float) -> float:
        """调制突触可塑性"""
        eligibility_trace = pre_activity * post_activity
        
        dopamine_modulation = self.state.concentration
        
        if self.td_error > 0:
            weight_change = eligibility_trace * dopamine_modulation * 0.1
        else:
            weight_change = -eligibility_trace * abs(dopamine_modulation) * 0.05
        
        new_weight = current_weight + weight_change
        
        return np.clip(new_weight, 0.01, 2.0)


class Acetylcholine(Neuromodulator):
    """乙酰胆碱系统"""
    
    def __init__(self, baseline: float = 0.4):
        super().__init__(NeuromodulatorType.ACETYLCHOLINE, baseline)
        
        self.attention_level = 0.5
        self.arousal_level = 0.5
        
    def _define_receptors(self) -> Dict[str, Dict[str, Any]]:
        """定义乙酰胆碱受体"""
        return {
            'nAChR_alpha4beta2': {
                'family': ReceptorFamily.NICOTINIC,
                'effect_type': 'excitatory',
                'efficacy': 0.4,
                'target': 'global',
                'kinetics': 'fast',
            },
            'nAChR_alpha7': {
                'family': ReceptorFamily.NICOTINIC,
                'effect_type': 'excitatory',
                'efficacy': 0.3,
                'target': 'hippocampus',
                'kinetics': 'fast',
            },
            'M1': {
                'family': ReceptorFamily.MUSCARINIC,
                'effect_type': 'excitatory',
                'efficacy': 0.35,
                'target': 'cortex',
                'kinetics': 'slow',
            },
            'M2': {
                'family': ReceptorFamily.MUSCARINIC,
                'effect_type': 'inhibitory',
                'efficacy': 0.25,
                'target': 'brainstem',
                'kinetics': 'slow',
            },
        }
    
    def release(self, 
               attention_demand: float,
               arousal: Optional[float] = None,
               context: Optional[Dict[str, Any]] = None):
        """释放乙酰胆碱（基于注意和唤醒）"""
        
        self.attention_level = attention_demand
        
        if arousal is not None:
            self.arousal_level = arousal
        
        release_amount = 0.3 * self.attention_level + 0.3 * self.arousal_level + 0.4 * self.baseline
        
        self.state.release_rate = release_amount
        
        self.release_history.append({
            'timestamp': datetime.now().isoformat(),
            'attention': self.attention_level,
            'arousal': self.arousal_level,
            'release': release_amount,
        })
    
    def modulate_attention(self, 
                          signal_strength: float,
                          noise_level: float) -> Tuple[float, float]:
        """调制注意力（信号增强、噪声抑制）"""
        
        signal_enhancement = 1 + 0.5 * self.state.concentration
        enhanced_signal = signal_strength * signal_enhancement
        
        noise_suppression = 1 - 0.3 * self.state.concentration
        suppressed_noise = noise_level * max(0.1, noise_suppression)
        
        snr = enhanced_signal / (suppressed_noise + 1e-6)
        
        return enhanced_signal, suppressed_noise
    
    def enhance_plasticity(self, 
                          baseline_plasticity: float) -> float:
        """增强突触可塑性"""
        enhancement_factor = 1 + 0.8 * self.state.concentration
        
        return baseline_plasticity * enhancement_factor


class Serotonin(Neuromodulator):
    """血清素系统"""
    
    def __init__(self, baseline: float = 0.5):
        super().__init__(NeuromodulatorType.SEROTONIN, baseline)
        
        self.mood_state = 0.5
        self.impulsivity = 0.5
        
    def _define_receptors(self) -> Dict[str, Dict[str, Any]]:
        """定义血清素受体"""
        return {
            '5-HT1A': {
                'family': ReceptorFamily.HT1,
                'effect_type': 'inhibitory',
                'efficacy': 0.3,
                'target': 'raphe',
                'function': 'mood_regulation',
            },
            '5-HT2A': {
                'family': ReceptorFamily.HT2,
                'effect_type': 'excitatory',
                'efficacy': 0.35,
                'target': 'cortex',
                'function': 'cognition',
            },
            '5-HT2C': {
                'family': ReceptorFamily.HT2,
                'effect_type': 'inhibitory',
                'efficacy': 0.25,
                'target': 'hypothalamus',
                'function': 'appetite',
            },
        }
    
    def release(self, 
               stress_level: float,
               reward_omission: bool = False,
               context: Optional[Dict[str, Any]] = None):
        """释放血清素"""
        
        if reward_omission:
            release_amount = 0.7
        else:
            release_amount = self.baseline + 0.3 * stress_level
        
        self.state.release_rate = release_amount
        
        self.mood_state = 0.7 * self.mood_state + 0.3 * (1 - stress_level)
        
        self.impulsivity = 1 - self.state.concentration
        
        self.release_history.append({
            'timestamp': datetime.now().isoformat(),
            'stress': stress_level,
            'mood': self.mood_state,
            'impulsivity': self.impulsivity,
        })
    
    def regulate_mood(self, 
                     negative_input: float) -> float:
        """调节情绪"""
        mood_regulation = self.state.concentration * 0.5
        
        adjusted_mood = self.mood_state - negative_input + mood_regulation
        
        return np.clip(adjusted_mood, 0, 1)
    
    def control_impulsivity(self, 
                           impulse_strength: float) -> float:
        """控制冲动"""
        inhibition = self.state.concentration * 0.6
        
        controlled_impulse = impulse_strength * (1 - inhibition)
        
        return max(0, controlled_impulse)


class Norepinephrine(Neuromodulator):
    """去甲肾上腺素系统"""
    
    def __init__(self, baseline: float = 0.4):
        super().__init__(NeuromodulatorType.NOREPINEPHRINE, baseline)
        
        self.arousal_level = 0.5
        self.vigilance = 0.5
        
        self.phasic_mode = False
        
    def _define_receptors(self) -> Dict[str, Dict[str, Any]]:
        """定义去甲肾上腺素受体"""
        return {
            'α1': {
                'family': ReceptorFamily.ALPHA,
                'effect_type': 'excitatory',
                'efficacy': 0.35,
                'target': 'cortex',
                'function': 'arousal',
            },
            'α2': {
                'family': ReceptorFamily.ALPHA,
                'effect_type': 'inhibitory',
                'efficacy': 0.3,
                'target': 'LC',
                'function': 'autoinhibition',
            },
            'β1': {
                'family': ReceptorFamily.BETA,
                'effect_type': 'excitatory',
                'efficacy': 0.3,
                'target': 'heart',
                'function': 'cardiovascular',
            },
            'β2': {
                'family': ReceptorFamily.BETA,
                'effect_type': 'excitatory',
                'efficacy': 0.25,
                'target': 'lungs',
                'function': 'respiratory',
            },
        }
    
    def release(self, 
               novelty: float,
               salience: float,
               arousal: Optional[float] = None,
               context: Optional[Dict[str, Any]] = None):
        """释放去甲肾上腺素"""
        
        if arousal is not None:
            self.arousal_level = arousal
        
        if novelty > 0.7 or salience > 0.7:
            self.phasic_mode = True
            release_amount = 0.8
        else:
            self.phasic_mode = False
            release_amount = self.baseline + 0.2 * (novelty + salience) / 2
        
        self.state.release_rate = release_amount
        
        self.vigilance = 0.5 + 0.5 * self.state.concentration
        
        self.release_history.append({
            'timestamp': datetime.now().isoformat(),
            'novelty': novelty,
            'salience': salience,
            'phasic': self.phasic_mode,
            'vigilance': self.vigilance,
        })
    
    def optimize_performance(self, 
                            task_difficulty: float) -> Tuple[float, str]:
        """优化任务表现（Yerkes-Dodson定律）"""
        
        optimal_arousal = 0.5 + 0.3 * task_difficulty
        
        arousal_deviation = abs(self.arousal_level - optimal_arousal)
        
        performance = 1 - arousal_deviation
        
        if self.arousal_level < optimal_arousal - 0.2:
            mode = "under_aroused"
        elif self.arousal_level > optimal_arousal + 0.2:
            mode = "over_aroused"
        else:
            mode = "optimal"
        
        return performance, mode
    
    def enhance_signal_detection(self, 
                                signal: float,
                                noise: float) -> Tuple[float, float]:
        """增强信号检测"""
        gain = 1 + 0.4 * self.state.concentration
        
        enhanced_signal = signal * gain
        
        threshold_adjustment = 0.2 * (1 - self.vigilance)
        adjusted_threshold = 0.5 - threshold_adjustment
        
        return enhanced_signal, adjusted_threshold


class NeuromodulatorySystem:
    """完整的神经调质系统"""
    
    def __init__(self):
        
        self.dopamine = Dopamine()
        self.acetylcholine = Acetylcholine()
        self.serotonin = Serotonin()
        self.norepinephrine = Norepinephrine()
        
        self.systems = {
            NeuromodulatorType.DOPAMINE: self.dopamine,
            NeuromodulatorType.ACETYLCHOLINE: self.acetylcholine,
            NeuromodulatorType.SEROTONIN: self.serotonin,
            NeuromodulatorType.NOREPINEPHRINE: self.norepinephrine,
        }
        
        self.interactions = self._define_interactions()
        
    def _define_interactions(self) -> Dict[Tuple[str, str], float]:
        """定义系统间相互作用"""
        return {
            ('dopamine', 'acetylcholine'): 0.3,
            ('dopamine', 'serotonin'): -0.2,
            ('dopamine', 'norepinephrine'): 0.4,
            ('acetylcholine', 'norepinephrine'): 0.5,
            ('serotonin', 'norepinephrine'): 0.2,
        }
    
    def update(self, dt: float):
        """更新所有系统"""
        for system in self.systems.values():
            system.update(dt)
        
        self._apply_interactions()
    
    def _apply_interactions(self):
        """应用系统间相互作用"""
        for (source, target), strength in self.interactions.items():
            source_system = self.systems[NeuromodulatorType(source)]
            target_system = self.systems[NeuromodulatorType(target)]
            
            interaction_effect = source_system.state.concentration * strength * 0.1
            
            target_system.state.concentration += interaction_effect
            target_system.state.concentration = np.clip(
                target_system.state.concentration, 0, 1
            )
    
    def process_event(self, 
                     event_type: str,
                     event_params: Dict[str, Any]):
        """处理事件"""
        
        if event_type == 'reward':
            self.dopamine.release(
                reward=event_params.get('reward', 0),
                prediction_error=event_params.get('prediction_error')
            )
        
        elif event_type == 'attention':
            self.acetylcholine.release(
                attention_demand=event_params.get('attention', 0.5),
                arousal=event_params.get('arousal')
            )
        
        elif event_type == 'stress':
            self.serotonin.release(
                stress_level=event_params.get('stress', 0),
                reward_omission=event_params.get('reward_omission', False)
            )
        
        elif event_type == 'novelty':
            self.norepinephrine.release(
                novelty=event_params.get('novelty', 0),
                salience=event_params.get('salience', 0),
                arousal=event_params.get('arousal')
            )
    
    def get_global_state(self) -> Dict[str, Any]:
        """获取全局状态"""
        return {
            'dopamine': self.dopamine.get_state(),
            'acetylcholine': self.acetylcholine.get_state(),
            'serotonin': self.serotonin.get_state(),
            'norepinephrine': self.norepinephrine.get_state(),
            'summary': {
                'motivation': self.dopamine.compute_motivation(1.0, 0.3),
                'attention': self.acetylcholine.attention_level,
                'mood': self.serotonin.mood_state,
                'arousal': self.norepinephrine.arousal_level,
                'vigilance': self.norepinephrine.vigilance,
            }
        }


class SynapticPlasticityRule:
    """突触可塑性规则"""
    
    def __init__(self, rule_type: str = 'stdp'):
        self.rule_type = rule_type
        
        self.A_plus = 0.1
        self.A_minus = 0.1
        self.tau_plus = 20.0
        self.tau_minus = 20.0
        
        self.learning_rate = 0.01
        
    def compute_weight_change(self,
                             pre_spike_time: float,
                             post_spike_time: float,
                             current_weight: float,
                             neuromodulator_level: float = 0.5) -> float:
        """计算权重变化"""
        
        if self.rule_type == 'stdp':
            return self._stdp(pre_spike_time, post_spike_time, neuromodulator_level)
        
        elif self.rule_type == 'hebbian':
            return self._hebbian(pre_spike_time, post_spike_time)
        
        elif self.rule_type == 'anti_hebbian':
            return self._anti_hebbian(pre_spike_time, post_spike_time)
        
        return 0.0
    
    def _stdp(self, 
             pre_time: float,
             post_time: float,
             neuromodulator: float) -> float:
        """STDP规则"""
        delta_t = post_time - pre_time
        
        if delta_t > 0:
            delta_w = self.A_plus * np.exp(-delta_t / self.tau_plus)
        else:
            delta_w = -self.A_minus * np.exp(delta_t / self.tau_minus)
        
        delta_w *= (0.5 + neuromodulator)
        
        return delta_w * self.learning_rate
    
    def _hebbian(self, pre_time: float, post_time: float) -> float:
        """Hebbian规则"""
        time_window = 50.0
        
        if abs(pre_time - post_time) < time_window:
            return self.learning_rate
        return 0.0
    
    def _anti_hebbian(self, pre_time: float, post_time: float) -> float:
        """反Hebbian规则"""
        time_window = 50.0
        
        if abs(pre_time - post_time) < time_window:
            return -self.learning_rate
        return 0.0


class PlasticityManager:
    """可塑性管理器"""
    
    def __init__(self):
        self.rules: Dict[str, SynapticPlasticityRule] = {}
        
        self.consolidation_threshold = 0.7
        self.degradation_threshold = 0.1
        
        self.weight_history = defaultdict(list)
        
    def add_rule(self, 
                rule_name: str,
                rule: SynapticPlasticityRule):
        """添加可塑性规则"""
        self.rules[rule_name] = rule
    
    def apply_plasticity(self,
                        synapse,
                        pre_spike_time: float,
                        post_spike_time: float,
                        neuromodulator_levels: Dict[str, float]) -> float:
        """应用可塑性"""
        
        rule = self.rules.get('stdp', SynapticPlasticityRule('stdp'))
        
        neuromodulator = neuromodulator_levels.get('dopamine', 0.5)
        
        delta_w = rule.compute_weight_change(
            pre_spike_time,
            post_spike_time,
            synapse.weight,
            neuromodulator
        )
        
        new_weight = synapse.weight + delta_w
        
        new_weight = np.clip(new_weight, 0.01, 2.0)
        
        synapse.weight = new_weight
        
        self.weight_history[synapse.pre_neuron_id + '_' + synapse.post_neuron_id].append({
            'weight': new_weight,
            'delta': delta_w,
            'timestamp': datetime.now().isoformat(),
        })
        
        return new_weight
    
    def consolidate(self, synapse):
        """巩固突触"""
        history = self.weight_history.get(
            synapse.pre_neuron_id + '_' + synapse.post_neuron_id, []
        )
        
        if len(history) < 10:
            return
        
        recent_weights = [h['weight'] for h in history[-10:]]
        mean_weight = np.mean(recent_weights)
        weight_stability = 1 - np.std(recent_weights) / (mean_weight + 1e-6)
        
        if weight_stability > self.consolidation_threshold:
            synapse.weight = mean_weight
            synapse.consolidated = True
        
        elif mean_weight < self.degradation_threshold:
            synapse.weight = 0.01
