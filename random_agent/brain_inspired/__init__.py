"""
RandomAgent 脑启发架构模块
基于最新脑科学和神经科学研究的完整人脑模仿系统

核心模块：
- 感知觉系统 (PerceptualSystem): 模拟感觉皮层
- 默认模式网络 (DefaultModeNetwork): 意识的核心枢纽
- 海马体记忆系统 (HippocampalMemorySystem): 情景记忆核心
- 全局工作空间 (GlobalWorkspace): 意识涌现机制
- 前额叶执行系统 (PrefrontalExecutiveSystem): 高级认知控制
- 杏仁核情绪系统 (AmygdalaEmotionSystem): 情绪处理核心
- 事件驱动架构 (EventDrivenArchitecture): 模块间通信
"""

from random_agent.brain_inspired.perceptual_system import (
    PerceptualSystem,
    SensoryIntegrator,
    AttentionFilter,
    FeatureExtractor,
    PatternRecognizer,
    PerceptualFeatures,
)

from random_agent.brain_inspired.dmn import (
    DefaultModeNetwork,
    NarrativeSelf,
    TimeIntegrator,
    SpontaneousThought,
    MetaCognition,
    ThoughtTrace,
    NarrativeState,
    TimeWindow,
)

from random_agent.brain_inspired.hippocampus import (
    HippocampalMemorySystem,
    EpisodicEncoder,
    PatternSeparator,
    PatternCompleter,
    MemoryConsolidation,
    SynapticPlasticity,
    EpisodicTrace,
)

from random_agent.brain_inspired.global_workspace import (
    GlobalWorkspace,
    ConsciousnessEmergence,
    InformationIntegrator,
    GlobalBroadcaster,
    AttentionController,
    InformationPacket,
    ConsciousContent,
    WorkspaceState,
)

from random_agent.brain_inspired.prefrontal import (
    PrefrontalExecutiveSystem,
    WorkingMemory,
    CognitiveFlexibility,
    InhibitoryControl,
    DecisionMaker,
    Planner,
    Decision,
    Plan,
)

from random_agent.brain_inspired.amygdala import (
    AmygdalaEmotionSystem,
    ThreatDetector,
    FearConditioning,
    EmotionalMemorySystem,
    EmotionRegulator,
    EmotionalState,
    ThreatAssessment,
)

from random_agent.brain_inspired.event_system import (
    EventDrivenArchitecture,
    EventBus,
    ConnectionManager,
    BrainEventSystem,
    BrainEvent,
    EventType,
    EventListener,
    NeuralPathway,
)

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
    NeuronType,
    EnsembleState,
    EnsembleActivity,
)

from random_agent.brain_inspired.neuromodulation import (
    Neuromodulator,
    Dopamine,
    Acetylcholine,
    Serotonin,
    Norepinephrine,
    NeuromodulatorySystem,
    SynapticPlasticityRule,
    PlasticityManager,
    NeuromodulatorType,
    ReceptorFamily,
)

__all__ = [
    'PerceptualSystem',
    'SensoryIntegrator',
    'AttentionFilter',
    'FeatureExtractor',
    'PatternRecognizer',
    'PerceptualFeatures',
    
    'DefaultModeNetwork',
    'NarrativeSelf',
    'TimeIntegrator',
    'SpontaneousThought',
    'MetaCognition',
    'ThoughtTrace',
    'NarrativeState',
    'TimeWindow',
    
    'HippocampalMemorySystem',
    'EpisodicEncoder',
    'PatternSeparator',
    'PatternCompleter',
    'MemoryConsolidation',
    'SynapticPlasticity',
    'EpisodicTrace',
    
    'GlobalWorkspace',
    'ConsciousnessEmergence',
    'InformationIntegrator',
    'GlobalBroadcaster',
    'AttentionController',
    'InformationPacket',
    'ConsciousContent',
    'WorkspaceState',
    
    'PrefrontalExecutiveSystem',
    'WorkingMemory',
    'CognitiveFlexibility',
    'InhibitoryControl',
    'DecisionMaker',
    'Planner',
    'Decision',
    'Plan',
    
    'AmygdalaEmotionSystem',
    'ThreatDetector',
    'FearConditioning',
    'EmotionalMemorySystem',
    'EmotionRegulator',
    'EmotionalState',
    'ThreatAssessment',
    
    'EventDrivenArchitecture',
    'EventBus',
    'ConnectionManager',
    'BrainEventSystem',
    'BrainEvent',
    'EventType',
    'EventListener',
    'NeuralPathway',
    
    'Neuron',
    'IonChannel',
    'IonChannelType',
    'IonChannelKinetics',
    'Synapse',
    'SynapticReceptor',
    'ReceptorType',
    'DendriticCompartment',
    'Soma',
    'Axon',
    'NeuronMetabolism',
    
    'NeuralEnsemble',
    'CorticalLayer',
    'CorticalColumn',
    'Minicolumn',
    'Hypercolumn',
    'NeuronType',
    'EnsembleState',
    'EnsembleActivity',
    
    'Neuromodulator',
    'Dopamine',
    'Acetylcholine',
    'Serotonin',
    'Norepinephrine',
    'NeuromodulatorySystem',
    'SynapticPlasticityRule',
    'PlasticityManager',
    'NeuromodulatorType',
    'ReceptorFamily',
]

__version__ = '0.5.0'
