"""
随机底层引擎 (Randomness Engine)

设计理念：世界的底层是随机的，大脑的底层也是随机的
- 量子力学视角：微观世界具有根本性的随机性
- 神经科学视角：神经元活动存在固有噪声
- 创造性视角：随机性是创造力的源泉

模块结构：
1. 量子随机模拟层 - 模拟量子不确定性
2. 神经噪声模拟层 - 模拟神经系统的随机活动
3. 创造性随机层 - 用于创造性思维的随机机制
"""

import random
import math
from typing import List, Dict, Any, Optional, Tuple, Callable
from dataclasses import dataclass, field
from enum import Enum
import hashlib
import time


class RandomnessType(Enum):
    """随机性类型"""
    QUANTUM = "quantum"
    NEURAL_NOISE = "neural_noise"
    CREATIVE = "creative"
    THERMAL = "thermal"


@dataclass
class SuperpositionState:
    """叠加态 - 同时保持多种可能性"""
    possibilities: List[Any]
    weights: List[float]
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        if len(self.possibilities) != len(self.weights):
            raise ValueError("可能性数量与权重数量不匹配")
        total = sum(self.weights)
        if total > 0:
            self.weights = [w / total for w in self.weights]


@dataclass
class NoiseConfig:
    """噪声配置"""
    base_level: float = 0.1
    signal_to_noise_ratio: float = 0.8
    fluctuation_amplitude: float = 0.2
    spontaneous_rate: float = 0.05


class QuantumRandomLayer:
    """
    量子随机模拟层
    
    模拟量子力学中的不确定性：
    - 概率波：状态以概率分布存在
    - 波函数坍塌：观测时从概率分布中选择一个确定状态
    - 叠加态：同时保持多种可能性的状态
    """
    
    def __init__(self, seed: Optional[int] = None):
        if seed is not None:
            random.seed(seed)
        self._entropy_pool: List[float] = []
        self._last_collapse_time = time.time()
    
    def _generate_entropy(self) -> float:
        """生成熵值 - 使用多种来源增加随机性"""
        sources = [
            random.random(),
            time.time() % 1,
            hash(str(time.time_ns())) % 10000 / 10000,
        ]
        combined = sum(sources) / len(sources)
        return combined
    
    def quantum_choice(
        self, 
        options: List[Any], 
        weights: Optional[List[float]] = None,
        collapse_context: Optional[Dict] = None
    ) -> Any:
        """
        量子选择 - 从概率分布中"坍塌"到一个结果
        
        Args:
            options: 可选项列表
            weights: 各选项的权重（概率）
            collapse_context: 坍塌上下文，可能影响坍塌结果
        
        Returns:
            选择的结果
        """
        if not options:
            raise ValueError("选项列表不能为空")
        
        if len(options) == 1:
            return options[0]
        
        if weights is None:
            weights = [1.0] * len(options)
        
        if collapse_context:
            weights = self._apply_context_influence(weights, collapse_context)
        
        total = sum(weights)
        if total <= 0:
            weights = [1.0] * len(options)
            total = len(options)
        
        normalized_weights = [w / total for w in weights]
        
        entropy = self._generate_entropy()
        threshold = (random.random() + entropy) / 2
        
        cumulative = 0.0
        for i, weight in enumerate(normalized_weights):
            cumulative += weight
            if threshold <= cumulative:
                self._last_collapse_time = time.time()
                return options[i]
        
        return options[-1]
    
    def _apply_context_influence(
        self, 
        weights: List[float], 
        context: Dict
    ) -> List[float]:
        """应用上下文影响 - 环境可能影响概率分布"""
        influence_factor = context.get("influence_factor", 0.1)
        influenced_weights = []
        
        for i, w in enumerate(weights):
            noise = random.gauss(0, influence_factor * w)
            influenced_weights.append(max(0.01, w + noise))
        
        return influenced_weights
    
    def create_superposition(
        self, 
        possibilities: List[Any], 
        weights: Optional[List[float]] = None
    ) -> SuperpositionState:
        """
        创建叠加态 - 同时保持多种可能性
        
        Args:
            possibilities: 可能的状态列表
            weights: 各状态的权重
        
        Returns:
            叠加态对象
        """
        if weights is None:
            weights = [1.0] * len(possibilities)
        
        return SuperpositionState(
            possibilities=possibilities,
            weights=weights,
            metadata={"created_at": time.time()}
        )
    
    def collapse_superposition(
        self, 
        superposition: SuperpositionState,
        context: Optional[Dict] = None
    ) -> Any:
        """
        坍塌叠加态 - 从叠加态中选择一个确定状态
        
        Args:
            superposition: 叠加态对象
            context: 坍塌上下文
        
        Returns:
            坍塌后的确定状态
        """
        return self.quantum_choice(
            superposition.possibilities,
            superposition.weights,
            context
        )
    
    def probability_wave(
        self, 
        x: float, 
        center: float = 0.5, 
        spread: float = 0.2
    ) -> float:
        """
        概率波函数 - 计算某个位置的概率密度
        
        使用高斯分布模拟概率波
        
        Args:
            x: 位置
            center: 波峰中心
            spread: 波的展宽
        
        Returns:
            概率密度
        """
        coefficient = 1 / (spread * math.sqrt(2 * math.pi))
        exponent = -((x - center) ** 2) / (2 * spread ** 2)
        return coefficient * math.exp(exponent)


class NeuralNoiseLayer:
    """
    神经噪声模拟层
    
    模拟神经系统的随机活动：
    - 基础噪声：持续的低水平随机活动
    - 信号-噪声比：可调节的随机强度
    - 自发活动：随机产生的神经活动
    - 噪声注入：在确定性过程中注入随机性
    """
    
    def __init__(self, config: Optional[NoiseConfig] = None):
        self.config = config or NoiseConfig()
        self._noise_history: List[float] = []
        self._current_noise_level = self.config.base_level
    
    def generate_noise(self, intensity: Optional[float] = None) -> float:
        """
        生成神经噪声
        
        Args:
            intensity: 噪声强度，None则使用配置的默认值
        
        Returns:
            噪声值 [-1, 1]
        """
        if intensity is None:
            intensity = self._current_noise_level
        
        noise = random.gauss(0, intensity)
        noise = max(-1, min(1, noise))
        
        self._noise_history.append(noise)
        if len(self._noise_history) > 1000:
            self._noise_history = self._noise_history[-1000:]
        
        return noise
    
    def add_noise_to_signal(
        self, 
        signal: float, 
        noise_ratio: Optional[float] = None
    ) -> float:
        """
        向信号添加噪声
        
        Args:
            signal: 原始信号
            noise_ratio: 噪声比例
        
        Returns:
            带噪声的信号
        """
        if noise_ratio is None:
            noise_ratio = 1 - self.config.signal_to_noise_ratio
        
        noise = self.generate_noise()
        noisy_signal = signal * (1 - noise_ratio) + noise * noise_ratio
        
        return noisy_signal
    
    def spontaneous_activity(self) -> Optional[float]:
        """
        自发活动 - 随机产生的神经活动
        
        Returns:
            自发活动值，如果没有自发活动则返回None
        """
        if random.random() < self.config.spontaneous_rate:
            return self.generate_noise(self.config.fluctuation_amplitude)
        return None
    
    def noise_injection(
        self, 
        value: Any, 
        injection_probability: float = 0.1
    ) -> Any:
        """
        噪声注入 - 在值中注入随机性
        
        Args:
            value: 原始值
            injection_probability: 注入概率
        
        Returns:
            可能被注入噪声的值
        """
        if random.random() > injection_probability:
            return value
        
        if isinstance(value, (int, float)):
            noise = self.generate_noise(0.2)
            return value + noise * abs(value) if value != 0 else noise
        
        if isinstance(value, str):
            if len(value) > 0 and random.random() < 0.05:
                chars = list(value)
                idx = random.randint(0, len(chars) - 1)
                similar_chars = self._get_similar_chars(chars[idx])
                if similar_chars:
                    chars[idx] = random.choice(similar_chars)
                return ''.join(chars)
        
        if isinstance(value, list) and len(value) > 0:
            if random.random() < 0.1:
                idx = random.randint(0, len(value) - 1)
                value[idx] = self.noise_injection(value[idx], 0.3)
        
        return value
    
    def _get_similar_chars(self, char: str) -> List[str]:
        """获取相似字符"""
        similar_groups = [
            ['a', 'á', 'à', 'â', 'ä'],
            ['e', 'é', 'è', 'ê', 'ë'],
            ['i', 'í', 'ì', 'î', 'ï'],
            ['o', 'ó', 'ò', 'ô', 'ö'],
            ['u', 'ú', 'ù', 'û', 'ü'],
            ['n', 'ñ'],
            ['c', 'ç'],
        ]
        
        for group in similar_groups:
            if char.lower() in group:
                return [c for c in group if c != char.lower()]
        
        return []
    
    def adjust_noise_level(self, factor: float):
        """调整噪声水平"""
        self._current_noise_level = max(
            0.01, 
            min(1.0, self.config.base_level * factor)
        )
    
    def get_noise_statistics(self) -> Dict[str, float]:
        """获取噪声统计信息"""
        if not self._noise_history:
            return {"mean": 0, "std": 0, "count": 0}
        
        mean = sum(self._noise_history) / len(self._noise_history)
        variance = sum((x - mean) ** 2 for x in self._noise_history) / len(self._noise_history)
        std = math.sqrt(variance)
        
        return {
            "mean": mean,
            "std": std,
            "count": len(self._noise_history),
            "current_level": self._current_noise_level
        }


class CreativeRandomLayer:
    """
    创造性随机层
    
    用于创造性思维的随机机制：
    - 远距离联想：连接看似不相关的概念
    - 概念跳跃：随机跳转到新的思维领域
    - 组合创新：随机组合现有元素产生新想法
    - 类比迁移：从其他领域借用概念
    """
    
    def __init__(self):
        self._concept_domains: Dict[str, List[str]] = {
            "nature": ["水", "火", "风", "土", "树", "花", "山", "河", "海", "天"],
            "technology": ["机器", "代码", "网络", "数据", "算法", "芯片", "机器人", "AI"],
            "art": ["音乐", "绘画", "雕塑", "舞蹈", "诗歌", "故事", "色彩", "节奏"],
            "science": ["物理", "化学", "生物", "数学", "量子", "相对论", "进化", "基因"],
            "emotion": ["爱", "恐惧", "喜悦", "悲伤", "愤怒", "平静", "激情", "忧郁"],
            "action": ["跑", "跳", "飞", "游", "转", "停", "开始", "结束"],
            "time": ["过去", "现在", "未来", "瞬间", "永恒", "循环", "线性", "螺旋"],
            "space": ["上", "下", "左", "右", "内", "外", "中心", "边缘"],
        }
        
        self._association_types = [
            "相似", "对比", "因果", "部分-整体", "功能",
            "时间", "空间", "情感", "符号", "隐喻",
            "反讽", "夸张", "借代", "联想", "直觉"
        ]
        
        self._jump_styles = [
            "直接跳跃", "螺旋上升", "分岔探索", "回溯跳跃",
            "并行跳跃", "嵌套跳跃", "逆向跳跃", "随机游走"
        ]
    
    def distant_association(
        self, 
        concept_a: str, 
        concept_b: str,
        bridge_concepts: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        远距离联想 - 连接两个看似不相关的概念
        
        Args:
            concept_a: 概念A
            concept_b: 概念B
            bridge_concepts: 可选的桥梁概念
        
        Returns:
            联想结果
        """
        association_type = random.choice(self._association_types)
        
        bridges = []
        if bridge_concepts:
            num_bridges = random.randint(1, min(3, len(bridge_concepts)))
            bridges = random.sample(bridge_concepts, num_bridges)
        
        strength = random.random()
        
        return {
            "from": concept_a,
            "to": concept_b,
            "association_type": association_type,
            "bridge_concepts": bridges,
            "strength": strength,
            "description": f"通过'{association_type}'关联，强度{strength:.2f}"
        }
    
    def conceptual_jump(
        self, 
        current_domain: str,
        available_domains: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        概念跳跃 - 随机跳转到新的思维领域
        
        Args:
            current_domain: 当前领域
            available_domains: 可用领域列表
        
        Returns:
            跳跃结果
        """
        if available_domains is None:
            available_domains = list(self._concept_domains.keys())
        
        other_domains = [d for d in available_domains if d != current_domain]
        
        if not other_domains:
            other_domains = available_domains
        
        target_domain = random.choice(other_domains)
        jump_style = random.choice(self._jump_styles)
        
        concepts_in_domain = self._concept_domains.get(target_domain, [])
        target_concept = random.choice(concepts_in_domain) if concepts_in_domain else target_domain
        
        return {
            "from_domain": current_domain,
            "to_domain": target_domain,
            "target_concept": target_concept,
            "jump_style": jump_style,
            "distance": random.random()
        }
    
    def combinatorial_innovation(
        self, 
        elements: List[Any],
        num_combinations: int = 2
    ) -> Dict[str, Any]:
        """
        组合创新 - 随机组合现有元素产生新想法
        
        Args:
            elements: 元素列表
            num_combinations: 组合数量
        
        Returns:
            组合结果
        """
        if len(elements) < 2:
            return {
                "elements": elements,
                "combinations": [],
                "innovation_score": 0
            }
        
        num_to_combine = min(num_combinations, len(elements))
        selected = random.sample(elements, num_to_combine)
        
        combination_methods = [
            "融合", "叠加", "嵌套", "对比", "序列化",
            "并行化", "递归", "映射", "转换", "重构"
        ]
        method = random.choice(combination_methods)
        
        innovation_score = random.random()
        
        return {
            "elements": selected,
            "combination_method": method,
            "innovation_score": innovation_score,
            "description": f"使用'{method}'方法组合{len(selected)}个元素"
        }
    
    def analogy_migration(
        self, 
        source_domain: str,
        target_domain: str,
        concept: str
    ) -> Dict[str, Any]:
        """
        类比迁移 - 从其他领域借用概念
        
        Args:
            source_domain: 源领域
            target_domain: 目标领域
            concept: 要迁移的概念
        
        Returns:
            迁移结果
        """
        source_concepts = self._concept_domains.get(source_domain, [])
        target_concepts = self._concept_domains.get(target_domain, [])
        
        analogy_types = [
            "结构类比", "功能类比", "过程类比", "关系类比",
            "属性类比", "隐喻类比", "抽象类比"
        ]
        analogy_type = random.choice(analogy_types)
        
        mapping_strength = random.random()
        
        return {
            "source_domain": source_domain,
            "target_domain": target_domain,
            "concept": concept,
            "analogy_type": analogy_type,
            "mapping_strength": mapping_strength,
            "source_concepts": source_concepts[:3] if source_concepts else [],
            "target_concepts": target_concepts[:3] if target_concepts else []
        }
    
    def random_inspiration(self) -> Dict[str, Any]:
        """
        随机灵感 - 完全随机产生的灵感
        
        Returns:
            灵感对象
        """
        domain = random.choice(list(self._concept_domains.keys()))
        concepts = self._concept_domains[domain]
        
        if len(concepts) >= 2:
            selected = random.sample(concepts, 2)
        else:
            selected = concepts * 2
        
        inspiration_types = [
            "突然想到", "灵光一闪", "直觉告诉我", "仿佛看到",
            "隐约感觉", "意外发现", "意外连接", "梦境启示"
        ]
        
        return {
            "type": random.choice(inspiration_types),
            "domain": domain,
            "concepts": selected,
            "intensity": random.random(),
            "timestamp": time.time()
        }
    
    def add_domain(self, name: str, concepts: List[str]):
        """添加新的概念域"""
        self._concept_domains[name] = concepts
    
    def get_random_concept(self, domain: Optional[str] = None) -> str:
        """获取随机概念"""
        if domain and domain in self._concept_domains:
            return random.choice(self._concept_domains[domain])
        
        all_concepts = []
        for concepts in self._concept_domains.values():
            all_concepts.extend(concepts)
        
        return random.choice(all_concepts) if all_concepts else "未知"


class RandomnessEngine:
    """
    随机底层引擎 - 整合所有随机层
    
    这是RandomAgent的最底层，所有上层模块都依赖此引擎获取随机性
    """
    
    def __init__(
        self, 
        seed: Optional[int] = None,
        noise_config: Optional[NoiseConfig] = None
    ):
        self.quantum_layer = QuantumRandomLayer(seed)
        self.neural_noise_layer = NeuralNoiseLayer(noise_config)
        self.creative_layer = CreativeRandomLayer()
        
        self._randomness_history: List[Dict[str, Any]] = []
    
    def random_choice(
        self, 
        options: List[Any],
        weights: Optional[List[float]] = None,
        randomness_type: RandomnessType = RandomnessType.QUANTUM,
        context: Optional[Dict] = None
    ) -> Any:
        """
        随机选择 - 核心接口
        
        Args:
            options: 选项列表
            weights: 权重
            randomness_type: 随机性类型
            context: 上下文
        
        Returns:
            选择结果
        """
        result = None
        
        if randomness_type == RandomnessType.QUANTUM:
            result = self.quantum_layer.quantum_choice(options, weights, context)
        
        elif randomness_type == RandomnessType.NEURAL_NOISE:
            if weights:
                noisy_weights = [
                    self.neural_noise_layer.add_noise_to_signal(w) 
                    for w in weights
                ]
                result = self.quantum_layer.quantum_choice(options, noisy_weights, context)
            else:
                result = self.quantum_layer.quantum_choice(options, None, context)
        
        elif randomness_type == RandomnessType.CREATIVE:
            if len(options) > 1:
                jump = self.creative_layer.conceptual_jump(
                    str(options[0]) if options else "",
                    [str(o) for o in options[1:]] if len(options) > 1 else []
                )
                result = self.quantum_layer.quantum_choice(options, weights, context)
            else:
                result = options[0] if options else None
        
        else:
            result = self.quantum_layer.quantum_choice(options, weights, context)
        
        self._record_randomness(randomness_type, {"options": options, "result": result})
        
        return result
    
    def inject_randomness(
        self, 
        value: Any,
        probability: float = 0.1
    ) -> Any:
        """注入随机性"""
        return self.neural_noise_layer.noise_injection(value, probability)
    
    def creative_association(
        self, 
        concept_a: str,
        concept_b: str
    ) -> Dict[str, Any]:
        """创造性联想"""
        return self.creative_layer.distant_association(concept_a, concept_b)
    
    def creative_jump(
        self, 
        current_domain: str
    ) -> Dict[str, Any]:
        """创造性跳跃"""
        return self.creative_layer.conceptual_jump(current_domain)
    
    def get_inspiration(self) -> Dict[str, Any]:
        """获取随机灵感"""
        return self.creative_layer.random_inspiration()
    
    def create_superposition(
        self, 
        possibilities: List[Any],
        weights: Optional[List[float]] = None
    ) -> SuperpositionState:
        """创建叠加态"""
        return self.quantum_layer.create_superposition(possibilities, weights)
    
    def collapse_superposition(
        self, 
        superposition: SuperpositionState,
        context: Optional[Dict] = None
    ) -> Any:
        """坍塌叠加态"""
        return self.quantum_layer.collapse_superposition(superposition, context)
    
    def _record_randomness(self, r_type: RandomnessType, data: Dict):
        """记录随机性使用"""
        self._randomness_history.append({
            "type": r_type.value,
            "data": data,
            "timestamp": time.time()
        })
        
        if len(self._randomness_history) > 10000:
            self._randomness_history = self._randomness_history[-10000:]
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息"""
        type_counts = {}
        for record in self._randomness_history:
            r_type = record["type"]
            type_counts[r_type] = type_counts.get(r_type, 0) + 1
        
        noise_stats = self.neural_noise_layer.get_noise_statistics()
        
        return {
            "total_random_calls": len(self._randomness_history),
            "type_distribution": type_counts,
            "noise_statistics": noise_stats
        }
    
    def set_noise_level(self, level: float):
        """设置噪声水平"""
        self.neural_noise_layer.adjust_noise_level(level)
