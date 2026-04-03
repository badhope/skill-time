"""
神经元计算模型 - 基于生物物理的精确仿真
实现从离子通道到完整神经元的层次化建模
"""

import numpy as np
from typing import Dict, List, Any, Optional, Tuple, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import math
import random


class IonChannelType(Enum):
    """离子通道类型"""
    NA_FAST = "na_fast"
    NA_PERSISTENT = "na_persistent"
    K_DR = "k_delayed_rectifier"
    K_A = "k_a_type"
    K_M = "k_m_type"
    K_SK = "k_sk"
    K_BK = "k_bk"
    CA_L = "ca_l_type"
    CA_T = "ca_t_type"
    CA_N = "ca_n_type"
    HCN = "hcn_ih"


class ReceptorType(Enum):
    """受体类型"""
    AMPA = "ampa"
    NMDA = "nmda"
    GABA_A = "gaba_a"
    GABA_B = "gaba_b"
    NICOTINIC = "nicotinic"
    MUSCARINIC = "muscarinic"


@dataclass
class IonChannelKinetics:
    """离子通道动力学参数"""
    g_max: float
    E_rev: float
    m_power: int
    h_power: int
    m_tau_scale: float = 1.0
    h_tau_scale: float = 1.0


class IonChannel:
    """离子通道 - 基于Hodgkin-Huxley模型"""
    
    def __init__(self, 
                 channel_type: IonChannelType,
                 kinetics: IonChannelKinetics):
        self.channel_type = channel_type
        self.kinetics = kinetics
        
        self.m = 0.0
        self.h = 1.0
        
        self.current_history = []
        
    def compute_current(self, V: float, dt: float) -> float:
        """计算离子电流
        
        Args:
            V: 膜电位 (mV)
            dt: 时间步长 (ms)
            
        Returns:
            离子电流 (µA/cm²)
        """
        m_inf, tau_m = self._activation_kinetics(V)
        h_inf, tau_h = self._inactivation_kinetics(V)
        
        tau_m *= self.kinetics.m_tau_scale
        tau_h *= self.kinetics.h_tau_scale
        
        self.m += (m_inf - self.m) * (1 - np.exp(-dt / tau_m))
        self.h += (h_inf - self.h) * (1 - np.exp(-dt / tau_h))
        
        g = self.kinetics.g_max * (self.m ** self.kinetics.m_power) * (self.h ** self.kinetics.h_power)
        
        I = g * (V - self.kinetics.E_rev)
        
        self.current_history.append(I)
        if len(self.current_history) > 1000:
            self.current_history = self.current_history[-500:]
        
        return I
    
    def _activation_kinetics(self, V: float) -> Tuple[float, float]:
        """激活动力学"""
        if self.channel_type == IonChannelType.NA_FAST:
            m_inf = 1.0 / (1 + np.exp(-(V + 40) / 6))
            tau_m = 0.1 + 0.4 / (1 + np.exp((V + 30) / 10))
            return m_inf, tau_m
        
        elif self.channel_type == IonChannelType.K_DR:
            n_inf = 1.0 / (1 + np.exp(-(V + 50) / 5))
            tau_n = 1.0 + 5.0 / (1 + np.exp((V + 40) / 10))
            return n_inf, tau_n
        
        elif self.channel_type == IonChannelType.K_A:
            m_inf = 1.0 / (1 + np.exp(-(V + 45) / 10))
            tau_m = 0.5 + 0.5 / (1 + np.exp((V + 35) / 10))
            return m_inf, tau_m
        
        elif self.channel_type == IonChannelType.CA_L:
            m_inf = 1.0 / (1 + np.exp(-(V + 30) / 7))
            tau_m = 2.0
            return m_inf, tau_m
        
        elif self.channel_type == IonChannelType.CA_T:
            m_inf = 1.0 / (1 + np.exp(-(V + 55) / 8))
            tau_m = 1.0
            return m_inf, tau_m
        
        elif self.channel_type == IonChannelType.HCN:
            m_inf = 1.0 / (1 + np.exp((V + 75) / 10))
            tau_m = 100.0 + 500.0 / (1 + np.exp((V + 70) / 10))
            return m_inf, tau_m
        
        else:
            return 0.5, 10.0
    
    def _inactivation_kinetics(self, V: float) -> Tuple[float, float]:
        """失活动力学"""
        if self.channel_type == IonChannelType.NA_FAST:
            h_inf = 1.0 / (1 + np.exp((V + 50) / 5))
            tau_h = 0.5 + 1.5 / (1 + np.exp((V + 30) / 10))
            return h_inf, tau_h
        
        elif self.channel_type == IonChannelType.K_A:
            h_inf = 1.0 / (1 + np.exp((V + 60) / 8))
            tau_h = 20.0 + 50.0 / (1 + np.exp((V + 40) / 10))
            return h_inf, tau_h
        
        elif self.channel_type == IonChannelType.CA_T:
            h_inf = 1.0 / (1 + np.exp((V + 70) / 5))
            tau_h = 30.0
            return h_inf, tau_h
        
        else:
            return 1.0, 100.0
    
    def reset(self):
        """重置通道状态"""
        self.m = 0.0
        self.h = 1.0
        self.current_history = []


class SynapticReceptor:
    """突触受体"""
    
    def __init__(self, 
                 receptor_type: ReceptorType,
                 reversal_potential: float,
                 tau_rise: float,
                 tau_decay: float):
        self.receptor_type = receptor_type
        self.E_rev = reversal_potential
        self.tau_rise = tau_rise
        self.tau_decay = tau_decay
        
        self.g = 0.0
        self.g_peak = 0.0
        
        self.open_probability = 0.0
        
    def activate(self, weight: float, V_post: float = -70.0) -> float:
        """激活受体
        
        Args:
            weight: 突触权重
            V_post: 突触后膜电位
            
        Returns:
            突触电流
        """
        if self.receptor_type == ReceptorType.NMDA:
            Mg_block = 1.0 / (1 + 0.28 * np.exp(-0.062 * V_post))
            self.g_peak = weight * Mg_block
        else:
            self.g_peak = weight
        
        self.open_probability = 1.0
        
        I = self.g * (V_post - self.E_rev)
        
        return I
    
    def update(self, dt: float, V_post: float = -70.0) -> float:
        """更新受体状态
        
        Args:
            dt: 时间步长
            V_post: 突触后膜电位
            
        Returns:
            突触电流
        """
        dg_rise = -self.g / self.tau_rise + self.open_probability * self.g_peak / self.tau_rise
        dg_decay = -self.g / self.tau_decay
        
        self.g += (dg_rise + dg_decay) * dt
        
        self.open_probability *= np.exp(-dt / self.tau_rise)
        
        if self.receptor_type == ReceptorType.NMDA:
            Mg_block = 1.0 / (1 + 0.28 * np.exp(-0.062 * V_post))
            I = self.g * Mg_block * (V_post - self.E_rev)
        else:
            I = self.g * (V_post - self.E_rev)
        
        return I
    
    def reset(self):
        """重置受体状态"""
        self.g = 0.0
        self.g_peak = 0.0
        self.open_probability = 0.0


class Synapse:
    """突触模型 - 包含短期和长期可塑性"""
    
    def __init__(self,
                 pre_neuron_id: str,
                 post_neuron_id: str,
                 weight: float = 0.5,
                 delay: float = 1.0,
                 synapse_type: str = 'excitatory'):
        
        self.pre_neuron_id = pre_neuron_id
        self.post_neuron_id = post_neuron_id
        self.weight = weight
        self.delay = delay
        self.synapse_type = synapse_type
        
        self.receptors = self._create_receptors()
        
        self.U = 0.5
        self.D = 0.2
        self.F = 0.05
        
        self.utilization = self.U
        self.R = 1.0
        
        self.tau_rec = 800.0
        self.tau_facil = 1000.0
        
        self.last_spike_time = -1000.0
        
        self.spike_history = []
        
    def _create_receptors(self) -> Dict[str, SynapticReceptor]:
        """创建受体"""
        receptors = {}
        
        if self.synapse_type == 'excitatory':
            receptors['AMPA'] = SynapticReceptor(
                receptor_type=ReceptorType.AMPA,
                reversal_potential=0.0,
                tau_rise=0.5,
                tau_decay=2.0
            )
            receptors['NMDA'] = SynapticReceptor(
                receptor_type=ReceptorType.NMDA,
                reversal_potential=0.0,
                tau_rise=2.0,
                tau_decay=100.0
            )
        else:
            receptors['GABA_A'] = SynapticReceptor(
                receptor_type=ReceptorType.GABA_A,
                reversal_potential=-70.0,
                tau_rise=0.5,
                tau_decay=5.0
            )
            receptors['GABA_B'] = SynapticReceptor(
                receptor_type=ReceptorType.GABA_B,
                reversal_potential=-90.0,
                tau_rise=50.0,
                tau_decay=200.0
            )
        
        return receptors
    
    def transmit(self, 
                pre_spike_time: float,
                V_post: float,
                dt: float) -> float:
        """突触传递
        
        Args:
            pre_spike_time: 突触前尖峰时间
            V_post: 突触后膜电位
            dt: 时间步长
            
        Returns:
            突触电流
        """
        if pre_spike_time - self.last_spike_time < 0.1:
            return self._update_receptors(dt, V_post)
        
        self.last_spike_time = pre_spike_time
        
        delta_t = pre_spike_time - self.last_spike_time
        
        self.utilization = self.U + self.utilization * (1 - self.U) * np.exp(-delta_t / self.tau_facil)
        self.R = 1 - (1 - self.R * (1 - self.utilization)) * np.exp(-delta_t / self.tau_rec)
        
        release_prob = self.utilization * self.R
        
        if random.random() < release_prob:
            self.spike_history.append(pre_spike_time)
            
            I_total = 0.0
            for receptor_name, receptor in self.receptors.items():
                I = receptor.activate(self.weight, V_post)
                I_total += I
            
            return I_total
        
        return self._update_receptors(dt, V_post)
    
    def _update_receptors(self, dt: float, V_post: float) -> float:
        """更新受体状态"""
        I_total = 0.0
        for receptor in self.receptors.values():
            I_total += receptor.update(dt, V_post)
        
        return I_total
    
    def update_weight_stdp(self, 
                          pre_spike_time: float,
                          post_spike_time: float,
                          A_plus: float = 0.1,
                          A_minus: float = 0.1,
                          tau_plus: float = 20.0,
                          tau_minus: float = 20.0):
        """STDP权重更新"""
        delta_t = post_spike_time - pre_spike_time
        
        if delta_t > 0:
            delta_w = A_plus * np.exp(-delta_t / tau_plus)
        else:
            delta_w = -A_minus * np.exp(delta_t / tau_minus)
        
        self.weight = np.clip(self.weight + delta_w, 0.01, 2.0)
        
        return delta_w
    
    def reset(self):
        """重置突触状态"""
        self.utilization = self.U
        self.R = 1.0
        self.last_spike_time = -1000.0
        
        for receptor in self.receptors.values():
            receptor.reset()


class DendriticCompartment:
    """树突隔室 - 被动电缆模型"""
    
    def __init__(self,
                 length: float = 100.0,
                 diameter: float = 1.0,
                 R_m: float = 20000.0,
                 C_m: float = 1.0,
                 R_a: float = 150.0,
                 E_rest: float = -70.0):
        
        self.length = length
        self.diameter = diameter
        self.R_m = R_m
        self.C_m = C_m
        self.R_a = R_a
        self.E_rest = E_rest
        
        self.area = np.pi * diameter * length
        self.tau = R_m * C_m
        
        self.lambda_cable = np.sqrt((diameter * R_m) / (4 * R_a))
        
        self.V = E_rest
        
        self.synapses: List[Synapse] = []
        
        self.ion_channels: Dict[IonChannelType, IonChannel] = {}
        
        self.children: List['DendriticCompartment'] = []
        self.parent: Optional['DendriticCompartment'] = None
        
    def add_synapse(self, synapse: Synapse):
        """添加突触"""
        self.synapses.append(synapse)
    
    def add_ion_channel(self, ion_channel: IonChannel):
        """添加离子通道"""
        self.ion_channels[ion_channel.channel_type] = ion_channel
    
    def compute_synaptic_current(self, current_time: float, dt: float) -> float:
        """计算突触电流"""
        I_syn = 0.0
        
        for synapse in self.synapses:
            I_syn += synapse.transmit(current_time, self.V, dt)
        
        return I_syn
    
    def compute_channel_current(self, dt: float) -> float:
        """计算离子通道电流"""
        I_channel = 0.0
        
        for channel in self.ion_channels.values():
            I_channel += channel.compute_current(self.V, dt)
        
        return I_channel
    
    def compute_axial_current(self, parent_V: Optional[float] = None) -> float:
        """计算轴向电流"""
        if parent_V is None:
            return 0.0
        
        R_axial = (4 * self.R_a * self.length) / (np.pi * self.diameter ** 2)
        
        I_axial = (parent_V - self.V) / R_axial
        
        return I_axial
    
    def update(self, 
              dt: float,
              parent_V: Optional[float] = None,
              current_time: float = 0.0) -> float:
        """更新树突隔室
        
        Args:
            dt: 时间步长
            parent_V: 父隔室电压
            current_time: 当前时间
            
        Returns:
            更新后的膜电位
        """
        I_syn = self.compute_synaptic_current(current_time, dt)
        
        I_channel = self.compute_channel_current(dt)
        
        I_axial = self.compute_axial_current(parent_V)
        
        I_leak = (self.V - self.E_rest) / self.R_m
        
        dV = (-(I_leak + I_syn + I_channel - I_axial)) * dt / (self.R_m * self.C_m)
        
        self.V += dV
        
        return self.V
    
    def reset(self):
        """重置隔室状态"""
        self.V = self.E_rest
        
        for synapse in self.synapses:
            synapse.reset()
        
        for channel in self.ion_channels.values():
            channel.reset()


class Soma:
    """胞体 - 包含完整的离子通道系统"""
    
    def __init__(self,
                 C_m: float = 1.0,
                 E_rest: float = -70.0,
                 E_Na: float = 50.0,
                 E_K: float = -90.0,
                 E_Ca: float = 140.0):
        
        self.C_m = C_m
        self.E_rest = E_rest
        self.E_Na = E_Na
        self.E_K = E_K
        self.E_Ca = E_Ca
        
        self.V = E_rest
        
        self.ion_channels = self._create_channels()
        
        self.spike_threshold = -55.0
        self.refractory_period = 2.0
        self.last_spike_time = -1000.0
        
        self.spike_history = []
        
        self.adaptation_current = 0.0
        self.g_AHP = 0.0
        self.tau_AHP = 100.0
        
    def _create_channels(self) -> Dict[IonChannelType, IonChannel]:
        """创建离子通道"""
        channels = {}
        
        channels[IonChannelType.NA_FAST] = IonChannel(
            channel_type=IonChannelType.NA_FAST,
            kinetics=IonChannelKinetics(
                g_max=120.0,
                E_rev=self.E_Na,
                m_power=3,
                h_power=1
            )
        )
        
        channels[IonChannelType.K_DR] = IonChannel(
            channel_type=IonChannelType.K_DR,
            kinetics=IonChannelKinetics(
                g_max=36.0,
                E_rev=self.E_K,
                m_power=4,
                h_power=0
            )
        )
        
        channels[IonChannelType.K_A] = IonChannel(
            channel_type=IonChannelType.K_A,
            kinetics=IonChannelKinetics(
                g_max=10.0,
                E_rev=self.E_K,
                m_power=1,
                h_power=1
            )
        )
        
        channels[IonChannelType.CA_L] = IonChannel(
            channel_type=IonChannelType.CA_L,
            kinetics=IonChannelKinetics(
                g_max=2.0,
                E_rev=self.E_Ca,
                m_power=1,
                h_power=0
            )
        )
        
        return channels
    
    def compute_currents(self, dt: float) -> float:
        """计算所有电流"""
        I_total = 0.0
        
        for channel in self.ion_channels.values():
            I_total += channel.compute_current(self.V, dt)
        
        I_total += self.adaptation_current
        
        return I_total
    
    def check_spike(self, current_time: float) -> bool:
        """检查是否产生动作电位"""
        if current_time - self.last_spike_time < self.refractory_period:
            return False
        
        if self.V >= self.spike_threshold:
            self.last_spike_time = current_time
            self.spike_history.append(current_time)
            
            self.g_AHP += 0.1
            
            return True
        
        return False
    
    def update_adaptation(self, dt: float):
        """更新自适应电流"""
        self.g_AHP *= np.exp(-dt / self.tau_AHP)
        
        self.adaptation_current = self.g_AHP * (self.V - self.E_K)
    
    def update(self, 
              I_inject: float,
              dt: float,
              current_time: float) -> Tuple[float, bool]:
        """更新胞体状态
        
        Args:
            I_inject: 注入电流
            dt: 时间步长
            current_time: 当前时间
            
        Returns:
            (膜电位, 是否产生动作电位)
        """
        I_channel = self.compute_currents(dt)
        
        self.update_adaptation(dt)
        
        I_leak = (self.V - self.E_rest) * 0.3
        
        dV = (-(I_leak + I_channel) + I_inject) * dt / self.C_m
        
        self.V += dV
        
        has_spiked = self.check_spike(current_time)
        
        if has_spiked:
            self.V = 30.0
        
        return self.V, has_spiked
    
    def reset(self):
        """重置胞体状态"""
        self.V = self.E_rest
        self.last_spike_time = -1000.0
        self.spike_history = []
        self.adaptation_current = 0.0
        self.g_AHP = 0.0
        
        for channel in self.ion_channels.values():
            channel.reset()


class Axon:
    """轴突 - 动作电位传导"""
    
    def __init__(self,
                 length: float = 1000.0,
                 diameter: float = 1.0,
                 myelinated: bool = False,
                 internode_length: float = 100.0):
        
        self.length = length
        self.diameter = diameter
        self.myelinated = myelinated
        self.internode_length = internode_length
        
        if myelinated:
            self.conduction_velocity = 6.0 * np.sqrt(diameter)
            self.nodes_of_ranvier = int(length / internode_length)
        else:
            self.conduction_velocity = 0.5 * np.sqrt(diameter)
            self.nodes_of_ranvier = 0
        
        self.delay = length / (self.conduction_velocity * 1000.0)
        
        self.spike_queue = []
        
    def propagate(self, spike_time: float) -> float:
        """传导动作电位
        
        Args:
            spike_time: 尖峰时间
            
        Returns:
            到达时间
        """
        arrival_time = spike_time + self.delay
        
        self.spike_queue.append(arrival_time)
        
        return arrival_time
    
    def get_arriving_spikes(self, current_time: float) -> int:
        """获取到达的尖峰"""
        arriving = sum(1 for t in self.spike_queue if t <= current_time)
        
        self.spike_queue = [t for t in self.spike_queue if t > current_time]
        
        return arriving
    
    def reset(self):
        """重置轴突状态"""
        self.spike_queue = []


class Neuron:
    """完整神经元模型"""
    
    def __init__(self,
                 neuron_id: str,
                 neuron_type: str = 'pyramidal',
                 C_m: float = 1.0,
                 E_rest: float = -70.0):
        
        self.neuron_id = neuron_id
        self.neuron_type = neuron_type
        self.C_m = C_m
        self.E_rest = E_rest
        
        self.soma = Soma(C_m=C_m, E_rest=E_rest)
        
        self.dendrites: List[DendriticCompartment] = []
        
        self.axon = Axon()
        
        self.input_synapses: List[Synapse] = []
        self.output_synapses: List[Synapse] = []
        
        self.V = E_rest
        
        self.spike_history = []
        self.firing_rate = 0.0
        
        self.metabolism = NeuronMetabolism()
        
        self.neuromodulator_levels = {
            'dopamine': 0.5,
            'acetylcholine': 0.5,
            'serotonin': 0.5,
            'norepinephrine': 0.5,
        }
        
    def add_dendrite(self, dendrite: DendriticCompartment):
        """添加树突"""
        self.dendrites.append(dendrite)
    
    def add_input_synapse(self, synapse: Synapse):
        """添加输入突触"""
        self.input_synapses.append(synapse)
    
    def add_output_synapse(self, synapse: Synapse):
        """添加输出突触"""
        self.output_synapses.append(synapse)
    
    def compute_dendritic_input(self, current_time: float, dt: float) -> float:
        """计算树突输入"""
        I_dendritic = 0.0
        
        for dendrite in self.dendrites:
            parent_V = self.soma.V if dendrite.parent is None else dendrite.parent.V
            dendrite.update(dt, parent_V, current_time)
            I_dendritic += dendrite.compute_axial_current(self.soma.V)
        
        return I_dendritic
    
    def apply_neuromodulation(self):
        """应用神经调质"""
        dopamine = self.neuromodulator_levels['dopamine']
        acetylcholine = self.neuromodulator_levels['acetylcholine']
        
        self.soma.spike_threshold = -55.0 - 5.0 * dopamine
        
        for channel in self.soma.ion_channels.values():
            channel.kinetics.g_max *= (1 + 0.2 * acetylcholine)
    
    def update(self, 
              I_inject: float,
              dt: float,
              current_time: float) -> Tuple[float, bool]:
        """更新神经元状态
        
        Args:
            I_inject: 注入电流
            dt: 时间步长
            current_time: 当前时间
            
        Returns:
            (膜电位, 是否产生动作电位)
        """
        self.apply_neuromodulation()
        
        I_dendritic = self.compute_dendritic_input(current_time, dt)
        
        total_input = I_inject + I_dendritic
        
        fatigue_factor = self.metabolism.get_fatigue_factor()
        total_input *= fatigue_factor
        
        V, has_spiked = self.soma.update(total_input, dt, current_time)
        
        self.V = V
        
        if has_spiked:
            self.spike_history.append(current_time)
            
            spike_count = self.metabolism.update(1, dt)
            
            for synapse in self.output_synapses:
                arrival_time = self.axon.propagate(current_time)
                synapse.transmit(arrival_time, V, dt)
        
        if len(self.spike_history) > 0:
            recent_spikes = [t for t in self.spike_history if current_time - t < 1000.0]
            self.firing_rate = len(recent_spikes)
        
        return V, has_spiked
    
    def get_state(self) -> Dict[str, Any]:
        """获取神经元状态"""
        return {
            'neuron_id': self.neuron_id,
            'V': self.V,
            'firing_rate': self.firing_rate,
            'spike_count': len(self.spike_history),
            'ATP_level': self.metabolism.ATP_level,
            'neuromodulators': self.neuromodulator_levels.copy(),
        }
    
    def reset(self):
        """重置神经元状态"""
        self.V = self.E_rest
        self.spike_history = []
        self.firing_rate = 0.0
        
        self.soma.reset()
        self.axon.reset()
        
        for dendrite in self.dendrites:
            dendrite.reset()
        
        for synapse in self.input_synapses:
            synapse.reset()


class NeuronMetabolism:
    """神经元代谢模型"""
    
    def __init__(self):
        self.ATP_level = 100.0
        self.glucose_level = 100.0
        self.oxygen_level = 100.0
        
        self.ATP_per_spike = 2.4e9
        self.ATP_production_rate = 1.0
        
    def update(self, spike_count: int, dt: float) -> float:
        """更新能量状态"""
        ATP_consumed = spike_count * self.ATP_per_spike * 1e-9
        self.ATP_level -= ATP_consumed
        
        ATP_produced = min(
            self.glucose_level,
            self.oxygen_level,
            self.ATP_production_rate * dt
        )
        self.ATP_level += ATP_produced
        
        self.glucose_level -= ATP_produced * 0.5
        self.oxygen_level -= ATP_produced * 0.5
        
        self.ATP_level = np.clip(self.ATP_level, 0, 100)
        
        return self.ATP_level
    
    def get_fatigue_factor(self) -> float:
        """获取疲劳因子"""
        if self.ATP_level < 20:
            return 0.5
        elif self.ATP_level < 50:
            return 0.8
        else:
            return 1.0
    
    def reset(self):
        """重置代谢状态"""
        self.ATP_level = 100.0
        self.glucose_level = 100.0
        self.oxygen_level = 100.0
