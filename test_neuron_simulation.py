"""
神经元级别仿真完整测试
测试从离子通道到神经元集群的层次化架构
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List, Any
import time

from random_agent.brain_inspired.neuron import (
    Neuron,
    IonChannel,
    IonChannelType,
    IonChannelKinetics,
    Synapse,
    SynapticReceptor,
    ReceptorType,
    DendriticCompartment,
    Soma,
    Axon,
    NeuronMetabolism,
)

from random_agent.brain_inspired.ensemble import (
    NeuralEnsemble,
    CorticalLayer,
    CorticalColumn,
    Minicolumn,
    Hypercolumn,
    NeuronType as EnsembleNeuronType,
)

from random_agent.brain_inspired.neuromodulation import (
    Dopamine,
    Acetylcholine,
    Serotonin,
    Norepinephrine,
    NeuromodulatorySystem,
    SynapticPlasticityRule,
    PlasticityManager,
)


def test_ion_channel():
    """测试离子通道"""
    print("\n" + "="*60)
    print("测试1: 离子通道动力学")
    print("="*60)
    
    na_channel = IonChannel(
        channel_type=IonChannelType.NA_FAST,
        kinetics=IonChannelKinetics(
            g_max=120.0,
            E_rev=50.0,
            m_power=3,
            h_power=1
        )
    )
    
    k_channel = IonChannel(
        channel_type=IonChannelType.K_DR,
        kinetics=IonChannelKinetics(
            g_max=36.0,
            E_rev=-90.0,
            m_power=4,
            h_power=0
        )
    )
    
    voltages = np.linspace(-80, 50, 100)
    na_currents = []
    k_currents = []
    
    dt = 0.01
    
    for V in voltages:
        I_na = na_channel.compute_current(V, dt)
        I_k = k_channel.compute_current(V, dt)
        
        na_currents.append(I_na)
        k_currents.append(I_k)
    
    print(f"✓ Na+通道电流范围: [{min(na_currents):.2f}, {max(na_currents):.2f}] µA/cm²")
    print(f"✓ K+通道电流范围: [{min(k_currents):.2f}, {max(k_currents):.2f}] µA/cm²")
    print(f"✓ Na+通道激活变量 m: {na_channel.m:.3f}")
    print(f"✓ Na+通道失活变量 h: {na_channel.h:.3f}")
    
    return True


def test_synapse():
    """测试突触传递"""
    print("\n" + "="*60)
    print("测试2: 突触传递与可塑性")
    print("="*60)
    
    synapse = Synapse(
        pre_neuron_id="neuron_1",
        post_neuron_id="neuron_2",
        weight=0.5,
        delay=1.0,
        synapse_type='excitatory'
    )
    
    print(f"✓ 初始突触权重: {synapse.weight:.3f}")
    print(f"✓ 突触类型: {synapse.synapse_type}")
    print(f"✓ 受体类型: {list(synapse.receptors.keys())}")
    
    V_post = -70.0
    dt = 0.1
    
    currents = []
    for t in range(10):
        I = synapse.transmit(t * dt, V_post, dt)
        currents.append(I)
    
    print(f"✓ 突触电流序列: {[f'{I:.3f}' for I in currents[:5]]}")
    
    delta_w = synapse.update_weight_stdp(
        pre_spike_time=10.0,
        post_spike_time=10.5
    )
    print(f"✓ STDP权重变化: {delta_w:.4f}")
    print(f"✓ 更新后权重: {synapse.weight:.3f}")
    
    return True


def test_neuron():
    """测试完整神经元"""
    print("\n" + "="*60)
    print("测试3: 完整神经元模型")
    print("="*60)
    
    neuron = Neuron(
        neuron_id="test_neuron",
        neuron_type="pyramidal"
    )
    
    print(f"✓ 神经元ID: {neuron.neuron_id}")
    print(f"✓ 神经元类型: {neuron.neuron_type}")
    print(f"✓ 静息电位: {neuron.E_rest:.1f} mV")
    print(f"✓ 离子通道数量: {len(neuron.soma.ion_channels)}")
    
    dt = 0.01
    current_time = 0.0
    
    membrane_potentials = []
    spike_times = []
    
    for i in range(1000):
        if 200 <= i <= 400:
            I_inject = 10.0
        else:
            I_inject = 0.0
        
        V, has_spiked = neuron.update(I_inject, dt, current_time)
        
        membrane_potentials.append(V)
        if has_spiked:
            spike_times.append(current_time)
        
        current_time += dt
    
    print(f"✓ 产生动作电位数量: {len(spike_times)}")
    print(f"✓ 发放率: {neuron.firing_rate:.1f} Hz")
    print(f"✓ ATP水平: {neuron.metabolism.ATP_level:.1f}%")
    
    state = neuron.get_state()
    print(f"✓ 神经元状态: V={state['V']:.1f}mV, FR={state['firing_rate']:.1f}Hz")
    
    return True


def test_neural_ensemble():
    """测试神经元集群"""
    print("\n" + "="*60)
    print("测试4: 神经元集群")
    print("="*60)
    
    neurons = [
        Neuron(neuron_id=f"ensemble_neuron_{i}", neuron_type="pyramidal")
        for i in range(20)
    ]
    
    ensemble = NeuralEnsemble(
        ensemble_id="test_ensemble",
        neurons=neurons,
        connection_probability=0.15
    )
    
    print(f"✓ 集群ID: {ensemble.ensemble_id}")
    print(f"✓ 神经元数量: {len(ensemble.neurons)}")
    print(f"✓ 连接矩阵形状: {ensemble.connection_matrix.shape}")
    print(f"✓ 连接密度: {np.sum(ensemble.connection_matrix != 0) / (20*20):.2%}")
    
    input_pattern = np.random.rand(20) * 0.5
    
    activity = ensemble.activate(input_pattern, 0.0, 1.0)
    
    print(f"✓ 集群活动水平: {activity.activity_level:.3f}")
    print(f"✓ 激活神经元数量: {len(activity.active_neurons)}")
    print(f"✓ 同步指数: {activity.synchrony_index:.3f}")
    print(f"✓ 平均发放率: {activity.mean_firing_rate:.1f} Hz")
    
    pattern = np.random.rand(20)
    ensemble.learn_pattern(pattern, label="test_pattern", learning_rate=0.01)
    
    print(f"✓ 学习的模式数量: {len(ensemble.attractors)}")
    
    partial_pattern = pattern.copy()
    partial_pattern[5:10] = 0
    
    recalled, similarity, label = ensemble.recall_pattern(
        partial_pattern, 0.0, 1.0, max_iterations=10
    )
    
    print(f"✓ 模式完成相似度: {similarity:.3f}")
    print(f"✓ 回忆标签: {label}")
    
    return True


def test_cortical_column():
    """测试皮层柱"""
    print("\n" + "="*60)
    print("测试5: 皮层柱架构")
    print("="*60)
    
    column = CorticalColumn(column_id="test_column")
    
    print(f"✓ 皮层柱ID: {column.column_id}")
    print(f"✓ 分层数量: {len(column.layers)}")
    print(f"✓ 层名称: {list(column.layers.keys())}")
    
    total_neurons = sum(layer.neuron_count for layer in column.layers.values())
    print(f"✓ 总神经元数量: {total_neurons}")
    
    thalamic_input = np.random.rand(2500) * 0.3
    
    result = column.process(thalamic_input, 0.0, 1.0)
    
    print(f"✓ 皮层柱活动: {result['column_activity']:.3f}")
    print(f"✓ 各层活动:")
    for layer_name, activity in result['layer_activities'].items():
        print(f"  - {layer_name}层: {activity:.3f}")
    
    state = column.get_state()
    print(f"✓ 皮层柱状态: {state['column_activity']:.3f}")
    
    return True


def test_neuromodulation():
    """测试神经调质系统"""
    print("\n" + "="*60)
    print("测试6: 神经调质系统")
    print("="*60)
    
    dopamine = Dopamine(baseline=0.3)
    acetylcholine = Acetylcholine(baseline=0.4)
    serotonin = Serotonin(baseline=0.5)
    norepinephrine = Norepinephrine(baseline=0.4)
    
    print("\n多巴胺系统:")
    dopamine.release(reward=1.0, prediction_error=0.5)
    print(f"✓ 奖励后浓度: {dopamine.state.concentration:.3f}")
    print(f"✓ TD误差: {dopamine.td_error:.3f}")
    print(f"✓ 受体类型: {list(dopamine.receptors.keys())}")
    
    print("\n乙酰胆碱系统:")
    acetylcholine.release(attention_demand=0.8, arousal=0.7)
    print(f"✓ 注意需求后浓度: {acetylcholine.state.concentration:.3f}")
    print(f"✓ 注意水平: {acetylcholine.attention_level:.3f}")
    
    enhanced_signal, suppressed_noise = acetylcholine.modulate_attention(
        signal_strength=0.5, noise_level=0.3
    )
    print(f"✓ 信号增强: {enhanced_signal:.3f}")
    print(f"✓ 噪声抑制: {suppressed_noise:.3f}")
    
    print("\n血清素系统:")
    serotonin.release(stress_level=0.6)
    print(f"✓ 压力后浓度: {serotonin.state.concentration:.3f}")
    print(f"✓ 情绪状态: {serotonin.mood_state:.3f}")
    print(f"✓ 冲动性: {serotonin.impulsivity:.3f}")
    
    print("\n去甲肾上腺素系统:")
    norepinephrine.release(novelty=0.8, salience=0.7)
    print(f"✓ 新异刺激后浓度: {norepinephrine.state.concentration:.3f}")
    print(f"✓ 警觉水平: {norepinephrine.vigilance:.3f}")
    print(f"✓ 相位模式: {norepinephrine.phasic_mode}")
    
    print("\n完整神经调质系统:")
    nm_system = NeuromodulatorySystem()
    
    nm_system.process_event('reward', {'reward': 1.0, 'prediction_error': 0.5})
    nm_system.process_event('attention', {'attention': 0.8, 'arousal': 0.7})
    
    nm_system.update(1.0)
    
    global_state = nm_system.get_global_state()
    print(f"✓ 多巴胺浓度: {global_state['dopamine']['concentration']:.3f}")
    print(f"✓ 乙酰胆碱浓度: {global_state['acetylcholine']['concentration']:.3f}")
    print(f"✓ 系统摘要: 动机={global_state['summary']['motivation']:.3f}, "
          f"注意={global_state['summary']['attention']:.3f}")
    
    return True


def test_synaptic_plasticity():
    """测试突触可塑性"""
    print("\n" + "="*60)
    print("测试7: 突触可塑性规则")
    print("="*60)
    
    stdp_rule = SynapticPlasticityRule(rule_type='stdp')
    
    print(f"✓ 可塑性规则类型: {stdp_rule.rule_type}")
    print(f"✓ LTP幅度: {stdp_rule.A_plus:.3f}")
    print(f"✓ LTD幅度: {stdp_rule.A_minus:.3f}")
    print(f"✓ LTP时间常数: {stdp_rule.tau_plus:.1f} ms")
    print(f"✓ LTD时间常数: {stdp_rule.tau_minus:.1f} ms")
    
    delta_w_ltp = stdp_rule.compute_weight_change(
        pre_spike_time=10.0,
        post_spike_time=10.5,
        current_weight=0.5,
        neuromodulator_level=0.7
    )
    print(f"✓ LTP权重变化 (Δt=0.5ms): {delta_w_ltp:.5f}")
    
    delta_w_ltd = stdp_rule.compute_weight_change(
        pre_spike_time=10.5,
        post_spike_time=10.0,
        current_weight=0.5,
        neuromodulator_level=0.7
    )
    print(f"✓ LTD权重变化 (Δt=-0.5ms): {delta_w_ltd:.5f}")
    
    plasticity_manager = PlasticityManager()
    plasticity_manager.add_rule('stdp', stdp_rule)
    
    print(f"✓ 可塑性管理器规则: {list(plasticity_manager.rules.keys())}")
    
    return True


def test_integrated_simulation():
    """测试集成仿真"""
    print("\n" + "="*60)
    print("测试8: 集成神经元-集群-调质仿真")
    print("="*60)
    
    neurons = [
        Neuron(neuron_id=f"integrated_neuron_{i}", neuron_type="pyramidal")
        for i in range(50)
    ]
    
    ensemble = NeuralEnsemble(
        ensemble_id="integrated_ensemble",
        neurons=neurons,
        connection_probability=0.1
    )
    
    nm_system = NeuromodulatorySystem()
    
    print(f"✓ 创建神经元集群: {len(neurons)}个神经元")
    print(f"✓ 初始化神经调质系统")
    
    simulation_time = 100.0
    dt = 1.0
    current_time = 0.0
    
    results = []
    
    for step in range(int(simulation_time / dt)):
        input_pattern = np.random.rand(50) * 0.3
        
        if step % 20 == 0:
            nm_system.process_event('reward', {'reward': 1.0})
        
        if step % 15 == 0:
            nm_system.process_event('attention', {'attention': 0.8})
        
        nm_system.update(dt)
        
        activity = ensemble.activate(input_pattern, current_time, dt)
        
        for neuron in ensemble.neurons:
            neuron.neuromodulator_levels['dopamine'] = nm_system.dopamine.state.concentration
            neuron.neuromodulator_levels['acetylcholine'] = nm_system.acetylcholine.state.concentration
        
        results.append({
            'time': current_time,
            'ensemble_activity': activity.activity_level,
            'dopamine': nm_system.dopamine.state.concentration,
            'acetylcholine': nm_system.acetylcholine.state.concentration,
            'synchrony': activity.synchrony_index,
        })
        
        current_time += dt
    
    print(f"✓ 仿真完成: {simulation_time}ms")
    print(f"✓ 平均集群活动: {np.mean([r['ensemble_activity'] for r in results]):.3f}")
    print(f"✓ 平均同步指数: {np.mean([r['synchrony'] for r in results]):.3f}")
    print(f"✓ 平均多巴胺浓度: {np.mean([r['dopamine'] for r in results]):.3f}")
    print(f"✓ 平均乙酰胆碱浓度: {np.mean([r['acetylcholine'] for r in results]):.3f}")
    
    return True


def run_all_tests():
    """运行所有测试"""
    print("\n" + "="*80)
    print(" "*20 + "神经元级别仿真完整测试套件")
    print("="*80)
    
    tests = [
        ("离子通道动力学", test_ion_channel),
        ("突触传递与可塑性", test_synapse),
        ("完整神经元模型", test_neuron),
        ("神经元集群", test_neural_ensemble),
        ("皮层柱架构", test_cortical_column),
        ("神经调质系统", test_neuromodulation),
        ("突触可塑性规则", test_synaptic_plasticity),
        ("集成仿真", test_integrated_simulation),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            start_time = time.time()
            success = test_func()
            elapsed_time = time.time() - start_time
            
            results[test_name] = {
                'success': success,
                'time': elapsed_time
            }
            
            print(f"\n✓ {test_name} - 通过 ({elapsed_time:.3f}s)")
            
        except Exception as e:
            results[test_name] = {
                'success': False,
                'error': str(e),
                'time': 0
            }
            print(f"\n✗ {test_name} - 失败: {str(e)}")
    
    print("\n" + "="*80)
    print(" "*30 + "测试总结")
    print("="*80)
    
    passed = sum(1 for r in results.values() if r['success'])
    total = len(results)
    
    print(f"\n总计: {passed}/{total} 测试通过")
    print(f"成功率: {passed/total*100:.1f}%")
    
    if passed == total:
        print("\n🎉 所有测试通过！神经元级别仿真系统运行正常。")
    else:
        print("\n⚠️  部分测试失败，请检查错误信息。")
    
    print("\n" + "="*80)
    
    return results


if __name__ == "__main__":
    results = run_all_tests()
