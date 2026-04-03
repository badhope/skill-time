"""
意识涌现系统 - 全局工作空间理论和意识整合
基于2024-2025最新神经科学研究
"""

import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

from random_agent.brain_inspired.ensemble import NeuralEnsemble
from random_agent.brain_inspired.neuron import Neuron


class ConsciousnessLevel(Enum):
    """意识水平"""
    UNCONSCIOUS = 0
    PRECONSCIOUS = 1
    CONSCIOUS = 2
    SELF_CONSCIOUS = 3


@dataclass
class ConsciousContent:
    """意识内容"""
    content: Any
    salience: float
    access_count: int
    broadcast_strength: float
    timestamp: float


@dataclass
class GlobalWorkspaceState:
    """全局工作空间状态"""
    active_contents: List[ConsciousContent]
    total_activity: float
    consciousness_level: ConsciousnessLevel
    integration_degree: float


class GlobalWorkspace:
    """全局工作空间 - 意识的核心"""
    
    def __init__(self, capacity: int = 4):
        self.capacity = capacity
        self.workspace: List[ConsciousContent] = []
        self.broadcast_strength = 0.8
        self.access_threshold = 0.5
        
    def broadcast(self, content: Any, salience: float, current_time: float = 0.0) -> bool:
        """广播内容到全局工作空间"""
        if salience < self.access_threshold:
            return False
        
        if len(self.workspace) >= self.capacity:
            self._evict_lowest_salience()
        
        conscious_content = ConsciousContent(
            content=content,
            salience=salience,
            access_count=1,
            broadcast_strength=self.broadcast_strength * salience,
            timestamp=current_time
        )
        
        self.workspace.append(conscious_content)
        
        return True
    
    def access(self, query: Any = None) -> Optional[ConsciousContent]:
        """访问工作空间内容"""
        if not self.workspace:
            return None
        
        if query is None:
            return max(self.workspace, key=lambda x: x.salience)
        
        best_match = None
        best_score = 0.0
        
        for item in self.workspace:
            score = self._compute_relevance(item.content, query)
            if score > best_score:
                best_score = score
                best_match = item
        
        if best_match:
            best_match.access_count += 1
        
        return best_match
    
    def _compute_relevance(self, content: Any, query: Any) -> float:
        """计算相关性"""
        if content == query:
            return 1.0
        return 0.5
    
    def _evict_lowest_salience(self):
        """驱逐最低显著性内容"""
        if self.workspace:
            min_idx = min(range(len(self.workspace)), key=lambda i: self.workspace[i].salience)
            self.workspace.pop(min_idx)
    
    def get_state(self) -> GlobalWorkspaceState:
        """获取状态"""
        total_activity = sum(item.salience for item in self.workspace)
        
        if total_activity > 2.0:
            level = ConsciousnessLevel.SELF_CONSCIOUS
        elif total_activity > 1.0:
            level = ConsciousnessLevel.CONSCIOUS
        elif total_activity > 0.5:
            level = ConsciousnessLevel.PRECONSCIOUS
        else:
            level = ConsciousnessLevel.UNCONSCIOUS
        
        integration = self._compute_integration()
        
        return GlobalWorkspaceState(
            active_contents=self.workspace.copy(),
            total_activity=total_activity,
            consciousness_level=level,
            integration_degree=integration
        )
    
    def _compute_integration(self) -> float:
        """计算整合度"""
        if len(self.workspace) < 2:
            return 0.0
        
        saliences = [item.salience for item in self.workspace]
        variance = np.var(saliences)
        
        integration = 1.0 / (1.0 + variance)
        
        return integration


class ThalamocorticalSystem:
    """丘脑皮层系统 - 意识的闸门"""
    
    def __init__(self):
        self.thalamic_nuclei = self._create_thalamic_nuclei()
        self.cortical_connections = {}
        self.arousal_level = 0.5
        
    def _create_thalamic_nuclei(self) -> Dict[str, NeuralEnsemble]:
        """创建丘脑核团"""
        nuclei = {}
        
        nuclei_names = ['intralaminar', 'reticular', 'medial_dorsal', 'pulvinar']
        
        for name in nuclei_names:
            neurons = [Neuron(f"thalamus_{name}_{i}", "thalamic") for i in range(50)]
            nuclei[name] = NeuralEnsemble(f"thalamus_{name}", neurons)
        
        return nuclei
    
    def regulate_arousal(self, arousal_input: float):
        """调节唤醒水平"""
        self.arousal_level = np.clip(arousal_input, 0, 1)
    
    def gate_information(self, information: Any, salience: float) -> bool:
        """门控信息"""
        gate_threshold = 1.0 - self.arousal_level
        
        return salience > gate_threshold
    
    def broadcast_to_cortex(self, content: Any, target_regions: List[str]) -> Dict[str, Any]:
        """广播到皮层"""
        broadcast_result = {}
        
        for region in target_regions:
            broadcast_result[region] = {
                'content': content,
                'strength': self.arousal_level,
                'received': True
            }
        
        return broadcast_result
    
    def get_state(self) -> Dict[str, Any]:
        """获取状态"""
        return {
            'arousal_level': self.arousal_level,
            'n_nuclei': len(self.thalamic_nuclei)
        }


class IntegrationCenter:
    """整合中心 - 信息整合"""
    
    def __init__(self):
        self.integration_buffer = []
        self.phi_calculator = PhiCalculator()
        
    def integrate(self, contents: List[ConsciousContent], current_time: float = 0.0) -> float:
        """整合内容"""
        if not contents:
            return 0.0
        
        integration_strength = self._compute_integration_strength(contents)
        
        self.integration_buffer.append({
            'contents': contents,
            'strength': integration_strength,
            'timestamp': current_time
        })
        
        if len(self.integration_buffer) > 10:
            self.integration_buffer.pop(0)
        
        return integration_strength
    
    def _compute_integration_strength(self, contents: List[ConsciousContent]) -> float:
        """计算整合强度"""
        if len(contents) < 2:
            return 0.0
        
        saliences = [c.salience for c in contents]
        mean_salience = np.mean(saliences)
        
        integration = mean_salience * len(contents) / self._compute_diversity(contents)
        
        return float(np.clip(integration, 0, 1))
    
    def _compute_diversity(self, contents: List[ConsciousContent]) -> float:
        """计算多样性"""
        if len(contents) < 2:
            return 1.0
        
        return 1.0
    
    def compute_phi(self, system_state: Dict[str, Any]) -> float:
        """计算整合信息（Φ）"""
        return self.phi_calculator.compute(system_state)


class PhiCalculator:
    """整合信息计算器"""
    
    def __init__(self):
        self.phi_history = []
        
    def compute(self, system_state: Dict[str, Any]) -> float:
        """计算Φ值"""
        activity = system_state.get('total_activity', 0.0)
        integration = system_state.get('integration_degree', 0.0)
        
        phi = activity * integration
        
        self.phi_history.append(phi)
        
        if len(self.phi_history) > 100:
            self.phi_history.pop(0)
        
        return phi


class AttentionSchema:
    """注意图式 - 意识的模型"""
    
    def __init__(self):
        self.attention_model = {}
        self.self_model = {}
        
    def build_attention_model(self, attention_state: Dict[str, Any]) -> Dict[str, Any]:
        """构建注意模型"""
        self.attention_model = {
            'focus': attention_state.get('focus', None),
            'intensity': attention_state.get('intensity', 0.0),
            'targets': attention_state.get('targets', [])
        }
        
        return self.attention_model
    
    def build_self_model(self, workspace_contents: List[ConsciousContent]) -> Dict[str, Any]:
        """构建自我模型"""
        self.self_model = {
            'n_contents': len(workspace_contents),
            'dominant_content': max(workspace_contents, key=lambda x: x.salience).content if workspace_contents else None,
            'total_salience': sum(c.salience for c in workspace_contents)
        }
        
        return self.self_model
    
    def generate_metacognition(self) -> Dict[str, Any]:
        """生成元认知"""
        return {
            'attention_awareness': self.attention_model,
            'self_awareness': self.self_model,
            'metacognitive_level': 0.5
        }


class ConsciousnessEmergence:
    """意识涌现系统"""
    
    def __init__(self):
        self.global_workspace = GlobalWorkspace()
        self.thalamocortical = ThalamocorticalSystem()
        self.integration_center = IntegrationCenter()
        self.attention_schema = AttentionSchema()
        
        self.consciousness_history = []
        
    def process(self, input_data: Dict[str, Any], current_time: float = 0.0) -> Dict[str, Any]:
        """处理输入并涌现意识"""
        if 'arousal' in input_data:
            self.thalamocortical.regulate_arousal(input_data['arousal'])
        
        broadcast_success = False
        if 'content' in input_data:
            salience = input_data.get('salience', 0.5)
            
            if self.thalamocortical.gate_information(input_data['content'], salience):
                broadcast_success = self.global_workspace.broadcast(
                    input_data['content'],
                    salience,
                    current_time
                )
        
        workspace_state = self.global_workspace.get_state()
        
        integration_strength = self.integration_center.integrate(
            workspace_state.active_contents,
            current_time
        )
        
        phi = self.integration_center.compute_phi({
            'total_activity': workspace_state.total_activity,
            'integration_degree': workspace_state.integration_degree
        })
        
        attention_model = self.attention_schema.build_attention_model(
            input_data.get('attention_state', {})
        )
        self_model = self.attention_schema.build_self_model(workspace_state.active_contents)
        metacognition = self.attention_schema.generate_metacognition()
        
        result = {
            'consciousness_level': workspace_state.consciousness_level.value,
            'workspace_state': {
                'n_contents': len(workspace_state.active_contents),
                'total_activity': workspace_state.total_activity,
                'integration_degree': workspace_state.integration_degree
            },
            'broadcast_success': broadcast_success,
            'integration_strength': integration_strength,
            'phi': phi,
            'attention_model': attention_model,
            'self_model': self_model,
            'metacognition': metacognition,
            'thalamocortical_state': self.thalamocortical.get_state(),
            'timestamp': current_time
        }
        
        self.consciousness_history.append(result)
        
        return result
    
    def access_consciousness(self, query: Any = None) -> Optional[ConsciousContent]:
        """访问意识内容"""
        return self.global_workspace.access(query)
    
    def get_consciousness_level(self) -> ConsciousnessLevel:
        """获取意识水平"""
        state = self.global_workspace.get_state()
        return state.consciousness_level
    
    def is_conscious(self) -> bool:
        """是否有意识"""
        level = self.get_consciousness_level()
        return level in [ConsciousnessLevel.CONSCIOUS, ConsciousnessLevel.SELF_CONSCIOUS]
