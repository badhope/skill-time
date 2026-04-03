"""
感觉皮层系统 - 视觉、听觉、体感皮层的完整实现
基于2024-2025最新神经科学研究
"""

import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

from random_agent.brain_inspired.ensemble import CorticalColumn, NeuralEnsemble
from random_agent.brain_inspired.neuron import Neuron


class SensoryModality(Enum):
    """感觉模态"""
    VISUAL = "visual"
    AUDITORY = "auditory"
    SOMATOSENSORY = "somatosensory"
    OLFACTORY = "olfactory"
    GUSTATORY = "gustatory"


@dataclass
class SensoryFeature:
    """感觉特征"""
    modality: SensoryModality
    features: np.ndarray
    salience: float
    location: Optional[Tuple[float, ...]] = None
    timestamp: float = 0.0


@dataclass
class VisualFeature(SensoryFeature):
    """视觉特征"""
    edges: Optional[np.ndarray] = None
    orientations: Optional[np.ndarray] = None
    colors: Optional[np.ndarray] = None
    motion: Optional[np.ndarray] = None
    depth: Optional[np.ndarray] = None


@dataclass
class AuditoryFeature(SensoryFeature):
    """听觉特征"""
    frequencies: Optional[np.ndarray] = None
    amplitudes: Optional[np.ndarray] = None
    phase: Optional[np.ndarray] = None
    location_3d: Optional[Tuple[float, float, float]] = None


@dataclass
class SomatosensoryFeature(SensoryFeature):
    """体感特征"""
    touch_pressure: Optional[np.ndarray] = None
    temperature: Optional[np.ndarray] = None
    pain: Optional[np.ndarray] = None
    proprioception: Optional[np.ndarray] = None


class PrimaryVisualCortex:
    """初级视觉皮层（V1）"""
    
    def __init__(self):
        self.orientation_columns = self._create_orientation_columns()
        self.ocular_dominance_columns = self._create_ocular_dominance_columns()
        self.retinotopic_map = self._create_retinotopic_map()
        
        self.receptive_field_size = 1.0
        self.orientation_selectivity = 8
        
    def _create_orientation_columns(self) -> List[CorticalColumn]:
        """创建方向选择性皮层柱"""
        columns = []
        orientations = [0, 45, 90, 135]
        
        for i, ori in enumerate(orientations):
            column = CorticalColumn(column_id=f"V1_ori_{ori}")
            column.orientation_tuning = ori
            columns.append(column)
        
        return columns
    
    def _create_ocular_dominance_columns(self) -> List[CorticalColumn]:
        """创建眼优势柱"""
        columns = []
        for i in range(4):
            column = CorticalColumn(column_id=f"V1_eye_{i}")
            columns.append(column)
        return columns
    
    def _create_retinotopic_map(self) -> np.ndarray:
        """创建视网膜拓扑映射"""
        return np.zeros((100, 100))
    
    def extract_edges(self, visual_input: np.ndarray) -> np.ndarray:
        """提取边缘特征"""
        if visual_input.ndim == 1:
            size = int(np.sqrt(len(visual_input)))
            visual_input = visual_input.reshape(size, size)
        
        sobel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
        sobel_y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
        
        from scipy.ndimage import convolve
        
        edges_x = convolve(visual_input, sobel_x)
        edges_y = convolve(visual_input, sobel_y)
        edges = np.sqrt(edges_x**2 + edges_y**2)
        
        return edges
    
    def detect_orientation(self, visual_input: np.ndarray) -> Dict[str, float]:
        """检测方向"""
        orientations = {}
        
        for column in self.orientation_columns:
            ori = column.orientation_tuning
            response = self._compute_orientation_response(visual_input, ori)
            orientations[f"orientation_{ori}"] = response
        
        return orientations
    
    def _compute_orientation_response(self, visual_input: np.ndarray, orientation: float) -> float:
        """计算方向响应"""
        theta = np.radians(orientation)
        
        if visual_input.ndim == 1:
            return 0.5
        
        kernel_size = 5
        kernel = np.zeros((kernel_size, kernel_size))
        
        for i in range(kernel_size):
            for j in range(kernel_size):
                x = i - kernel_size // 2
                y = j - kernel_size // 2
                kernel[i, j] = np.cos(theta) * x + np.sin(theta) * y
        
        kernel = kernel / (np.abs(kernel).sum() + 1e-6)
        
        from scipy.ndimage import convolve
        response = np.abs(convolve(visual_input, kernel)).mean()
        
        return float(response)
    
    def process(self, visual_input: np.ndarray, current_time: float = 0.0) -> VisualFeature:
        """处理视觉输入"""
        edges = self.extract_edges(visual_input)
        orientations = self.detect_orientation(visual_input)
        
        ori_array = np.array(list(orientations.values()))
        salience = float(np.max(ori_array)) if len(ori_array) > 0 else 0.0
        
        feature = VisualFeature(
            modality=SensoryModality.VISUAL,
            features=edges.flatten() if edges.ndim > 1 else edges,
            salience=salience,
            timestamp=current_time,
            edges=edges,
            orientations=ori_array
        )
        
        return feature


class SecondaryVisualCortex:
    """次级视觉皮层（V2）"""
    
    def __init__(self):
        self.contour_integrator = self._create_contour_integrator()
        self.texture_analyzer = self._create_texture_analyzer()
        
    def _create_contour_integrator(self) -> NeuralEnsemble:
        """创建轮廓整合器"""
        neurons = [Neuron(f"v2_contour_{i}", "pyramidal") for i in range(100)]
        return NeuralEnsemble("v2_contour_ensemble", neurons)
    
    def _create_texture_analyzer(self) -> NeuralEnsemble:
        """创建纹理分析器"""
        neurons = [Neuron(f"v2_texture_{i}", "pyramidal") for i in range(100)]
        return NeuralEnsemble("v2_texture_ensemble", neurons)
    
    def integrate_contours(self, edges: np.ndarray) -> np.ndarray:
        """整合轮廓"""
        from scipy.ndimage import binary_dilation, binary_erosion
        
        if edges.ndim == 1:
            size = int(np.sqrt(len(edges)))
            edges = edges.reshape(size, size)
        
        dilated = binary_dilation(edges > 0.5)
        eroded = binary_erosion(edges > 0.5)
        contours = dilated.astype(float) - eroded.astype(float)
        
        return contours
    
    def analyze_texture(self, visual_input: np.ndarray) -> np.ndarray:
        """分析纹理"""
        if visual_input.ndim == 1:
            return np.zeros(10)
        
        from scipy.ndimage import sobel
        
        texture_features = []
        
        grad_x = sobel(visual_input, axis=0)
        grad_y = sobel(visual_input, axis=1)
        
        texture_features.append(np.mean(np.abs(grad_x)))
        texture_features.append(np.mean(np.abs(grad_y)))
        texture_features.append(np.std(visual_input))
        texture_features.append(np.mean(visual_input))
        
        for i in range(6):
            texture_features.append(np.random.rand())
        
        return np.array(texture_features)
    
    def process(self, v1_features: VisualFeature, current_time: float = 0.0) -> VisualFeature:
        """处理V1输出"""
        edges = v1_features.edges if v1_features.edges is not None else np.zeros((10, 10))
        
        contours = self.integrate_contours(edges)
        textures = self.analyze_texture(edges)
        
        feature = VisualFeature(
            modality=SensoryModality.VISUAL,
            features=np.concatenate([contours.flatten()[:100], textures]),
            salience=v1_features.salience * 1.2,
            timestamp=current_time,
            edges=contours
        )
        
        return feature


class VisualAreaV4:
    """视觉区域V4 - 颜色和形状处理"""
    
    def __init__(self):
        self.color_columns = self._create_color_columns()
        self.shape_columns = self._create_shape_columns()
        
    def _create_color_columns(self) -> List[CorticalColumn]:
        """创建颜色处理柱"""
        columns = []
        colors = ['red', 'green', 'blue', 'yellow']
        for color in colors:
            column = CorticalColumn(column_id=f"V4_color_{color}")
            columns.append(column)
        return columns
    
    def _create_shape_columns(self) -> List[CorticalColumn]:
        """创建形状处理柱"""
        columns = []
        shapes = ['circle', 'square', 'triangle', 'ellipse']
        for shape in shapes:
            column = CorticalColumn(column_id=f"V4_shape_{shape}")
            columns.append(column)
        return columns
    
    def process_color(self, visual_input: np.ndarray) -> np.ndarray:
        """处理颜色"""
        if visual_input.ndim == 1:
            return np.random.rand(4)
        
        color_features = np.array([
            np.mean(visual_input),
            np.std(visual_input),
            np.max(visual_input),
            np.min(visual_input)
        ])
        
        return color_features
    
    def analyze_shape(self, contours: np.ndarray) -> Dict[str, float]:
        """分析形状"""
        if contours is None or contours.ndim == 1:
            return {'circularity': 0.5, 'complexity': 0.5}
        
        if contours.ndim == 1:
            size = int(np.sqrt(len(contours)))
            contours = contours.reshape(size, size)
        
        area = np.sum(contours > 0)
        perimeter = np.sum(np.abs(np.diff(contours, axis=0)).sum() + 
                          np.abs(np.diff(contours, axis=1)).sum())
        
        circularity = 4 * np.pi * area / (perimeter ** 2 + 1e-6)
        complexity = perimeter / (area + 1e-6)
        
        return {
            'circularity': float(np.clip(circularity, 0, 1)),
            'complexity': float(np.clip(complexity / 10, 0, 1))
        }
    
    def process(self, v2_features: VisualFeature, current_time: float = 0.0) -> VisualFeature:
        """处理V2输出"""
        colors = self.process_color(v2_features.features)
        shapes = self.analyze_shape(v2_features.edges)
        
        shape_array = np.array([shapes['circularity'], shapes['complexity']])
        combined_features = np.concatenate([colors, shape_array])
        
        feature = VisualFeature(
            modality=SensoryModality.VISUAL,
            features=combined_features,
            salience=v2_features.salience * 1.3,
            timestamp=current_time
        )
        
        return feature


class InferiorTemporalCortex:
    """下颞叶皮层 - 物体识别"""
    
    def __init__(self):
        self.object_representations = {}
        self.face_area = self._create_face_area()
        
    def _create_face_area(self) -> NeuralEnsemble:
        """创建面部识别区域（FFA）"""
        neurons = [Neuron(f"ffa_{i}", "pyramidal") for i in range(200)]
        return NeuralEnsemble("ffa_ensemble", neurons)
    
    def recognize_objects(self, v4_features: VisualFeature, current_time: float = 0.0) -> Dict[str, Any]:
        """识别物体"""
        features = v4_features.features
        
        object_candidates = {}
        
        if len(features) >= 6:
            color_score = np.mean(features[:4])
            shape_score = np.mean(features[4:6])
            
            if color_score > 0.6 and shape_score > 0.5:
                object_candidates['colored_object'] = {
                    'confidence': (color_score + shape_score) / 2,
                    'category': 'object'
                }
            
            if shape_score > 0.7:
                object_candidates['simple_shape'] = {
                    'confidence': shape_score,
                    'category': 'geometric'
                }
        
        if not object_candidates:
            object_candidates['unknown'] = {
                'confidence': 0.5,
                'category': 'unknown'
            }
        
        return object_candidates
    
    def process(self, v4_features: VisualFeature, current_time: float = 0.0) -> Dict[str, Any]:
        """处理V4输出"""
        objects = self.recognize_objects(v4_features, current_time)
        
        return {
            'objects': objects,
            'salience': v4_features.salience,
            'timestamp': current_time
        }


class VisualCortex:
    """完整视觉皮层系统"""
    
    def __init__(self):
        self.V1 = PrimaryVisualCortex()
        self.V2 = SecondaryVisualCortex()
        self.V4 = VisualAreaV4()
        self.IT = InferiorTemporalCortex()
        
        self.processing_history = []
        
    def process(self, visual_input: np.ndarray, current_time: float = 0.0) -> Dict[str, Any]:
        """完整视觉处理流程"""
        v1_features = self.V1.process(visual_input, current_time)
        v2_features = self.V2.process(v1_features, current_time)
        v4_features = self.V4.process(v2_features, current_time)
        it_results = self.IT.process(v4_features, current_time)
        
        result = {
            'modality': 'visual',
            'v1_features': v1_features,
            'v2_features': v2_features,
            'v4_features': v4_features,
            'objects': it_results['objects'],
            'salience': it_results['salience'],
            'timestamp': current_time
        }
        
        self.processing_history.append(result)
        
        return result


class PrimaryAuditoryCortex:
    """初级听觉皮层（A1）"""
    
    def __init__(self):
        self.tonotopic_map = self._create_tonotopic_map()
        self.frequency_columns = self._create_frequency_columns()
        
    def _create_tonotopic_map(self) -> np.ndarray:
        """创建音调拓扑映射"""
        frequencies = np.logspace(1, 4, 100)
        return frequencies
    
    def _create_frequency_columns(self) -> List[CorticalColumn]:
        """创建频率选择性柱"""
        columns = []
        freq_bands = ['low', 'mid_low', 'mid_high', 'high']
        
        for band in freq_bands:
            column = CorticalColumn(column_id=f"A1_freq_{band}")
            columns.append(column)
        
        return columns
    
    def analyze_frequencies(self, auditory_input: np.ndarray) -> np.ndarray:
        """分析频率成分"""
        if len(auditory_input) < 2:
            return np.zeros(10)
        
        fft_result = np.fft.fft(auditory_input)
        frequencies = np.fft.fftfreq(len(auditory_input))
        
        magnitude = np.abs(fft_result[:len(fft_result)//2])
        
        n_features = min(10, len(magnitude))
        features = np.zeros(10)
        features[:n_features] = magnitude[:n_features]
        
        if features.max() > 0:
            features = features / features.max()
        
        return features
    
    def process(self, auditory_input: np.ndarray, current_time: float = 0.0) -> AuditoryFeature:
        """处理听觉输入"""
        frequencies = self.analyze_frequencies(auditory_input)
        
        salience = float(np.max(frequencies)) if len(frequencies) > 0 else 0.0
        
        feature = AuditoryFeature(
            modality=SensoryModality.AUDITORY,
            features=frequencies,
            salience=salience,
            timestamp=current_time,
            frequencies=frequencies
        )
        
        return feature


class AuditoryCortex:
    """完整听觉皮层系统"""
    
    def __init__(self):
        self.A1 = PrimaryAuditoryCortex()
        self.processing_history = []
        
    def process(self, auditory_input: np.ndarray, current_time: float = 0.0) -> Dict[str, Any]:
        """完整听觉处理流程"""
        a1_features = self.A1.process(auditory_input, current_time)
        
        result = {
            'modality': 'auditory',
            'a1_features': a1_features,
            'frequencies': a1_features.frequencies,
            'salience': a1_features.salience,
            'timestamp': current_time
        }
        
        self.processing_history.append(result)
        
        return result


class PrimarySomatosensoryCortex:
    """初级体感皮层（S1）"""
    
    def __init__(self):
        self.body_map = self._create_body_map()
        self.sensory_columns = self._create_sensory_columns()
        
    def _create_body_map(self) -> Dict[str, np.ndarray]:
        """创建身体感觉图谱"""
        body_parts = ['hand', 'face', 'foot', 'trunk']
        body_map = {}
        
        for part in body_parts:
            body_map[part] = np.random.rand(10, 10)
        
        return body_map
    
    def _create_sensory_columns(self) -> List[CorticalColumn]:
        """创建感觉柱"""
        columns = []
        modalities = ['touch', 'pressure', 'temperature', 'pain']
        
        for modality in modalities:
            column = CorticalColumn(column_id=f"S1_{modality}")
            columns.append(column)
        
        return columns
    
    def process_touch(self, somatosensory_input: np.ndarray) -> np.ndarray:
        """处理触觉"""
        if len(somatosensory_input) < 2:
            return np.zeros(4)
        
        touch_features = np.array([
            np.mean(somatosensory_input),
            np.std(somatosensory_input),
            np.max(somatosensory_input),
            np.min(somatosensory_input)
        ])
        
        return touch_features
    
    def process(self, somatosensory_input: np.ndarray, current_time: float = 0.0) -> SomatosensoryFeature:
        """处理体感输入"""
        touch = self.process_touch(somatosensory_input)
        
        salience = float(np.max(np.abs(touch))) if len(touch) > 0 else 0.0
        
        feature = SomatosensoryFeature(
            modality=SensoryModality.SOMATOSENSORY,
            features=touch,
            salience=salience,
            timestamp=current_time,
            touch_pressure=touch
        )
        
        return feature


class SomatosensoryCortex:
    """完整体感皮层系统"""
    
    def __init__(self):
        self.S1 = PrimarySomatosensoryCortex()
        self.processing_history = []
        
    def process(self, somatosensory_input: np.ndarray, current_time: float = 0.0) -> Dict[str, Any]:
        """完整体感处理流程"""
        s1_features = self.S1.process(somatosensory_input, current_time)
        
        result = {
            'modality': 'somatosensory',
            's1_features': s1_features,
            'touch': s1_features.touch_pressure,
            'salience': s1_features.salience,
            'timestamp': current_time
        }
        
        self.processing_history.append(result)
        
        return result


class SensoryCortex:
    """完整感觉皮层系统"""
    
    def __init__(self):
        self.visual = VisualCortex()
        self.auditory = AuditoryCortex()
        self.somatosensory = SomatosensoryCortex()
        
        self.multisensory_integration = MultisensoryIntegration()
        
    def process(self, 
                visual_input: Optional[np.ndarray] = None,
                auditory_input: Optional[np.ndarray] = None,
                somatosensory_input: Optional[np.ndarray] = None,
                current_time: float = 0.0) -> Dict[str, Any]:
        """处理所有感觉输入"""
        results = {}
        
        if visual_input is not None:
            results['visual'] = self.visual.process(visual_input, current_time)
        
        if auditory_input is not None:
            results['auditory'] = self.auditory.process(auditory_input, current_time)
        
        if somatosensory_input is not None:
            results['somatosensory'] = self.somatosensory.process(somatosensory_input, current_time)
        
        integrated = self.multisensory_integration.integrate(results, current_time)
        results['integrated'] = integrated
        
        return results


class MultisensoryIntegration:
    """多感觉整合"""
    
    def __init__(self):
        self.integration_weights = {
            'visual': 0.4,
            'auditory': 0.3,
            'somatosensory': 0.3
        }
        
    def integrate(self, sensory_results: Dict[str, Any], current_time: float) -> Dict[str, Any]:
        """整合多感觉信息"""
        total_salience = 0.0
        dominant_modality = None
        max_salience = 0.0
        
        for modality, weight in self.integration_weights.items():
            if modality in sensory_results:
                salience = sensory_results[modality].get('salience', 0.0)
                total_salience += salience * weight
                
                if salience > max_salience:
                    max_salience = salience
                    dominant_modality = modality
        
        return {
            'total_salience': total_salience,
            'dominant_modality': dominant_modality,
            'integration_strength': total_salience / (sum(self.integration_weights.values()) + 1e-6),
            'timestamp': current_time
        }
