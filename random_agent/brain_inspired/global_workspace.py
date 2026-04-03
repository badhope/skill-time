"""
全局工作空间 - 意识涌现的核心机制
基于全局工作空间理论（Global Workspace Theory）
"""

import numpy as np
from typing import Dict, List, Any, Optional, Tuple, Callable
from dataclasses import dataclass, field
from datetime import datetime
import threading
import queue
import time


@dataclass
class InformationPacket:
    """信息包数据结构"""
    source: str
    content: Any
    salience: float
    modality: str
    timestamp: float = field(default_factory=lambda: time.time())
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ConsciousContent:
    """意识内容数据结构"""
    content: Any
    sources: List[str]
    integration_level: float
    broadcast_range: List[str]
    duration: float
    timestamp: float = field(default_factory=lambda: time.time())


@dataclass
class WorkspaceState:
    """工作空间状态数据结构"""
    active_content: Optional[ConsciousContent]
    competing_inputs: List[InformationPacket]
    attention_focus: float
    processing_load: float
    timestamp: float = field(default_factory=lambda: time.time())


class InformationIntegrator:
    """信息整合器 - 从多个模块收集和整合信息"""
    
    def __init__(self, integration_threshold: float = 0.5):
        self.integration_threshold = integration_threshold
        self.input_buffers: Dict[str, List[InformationPacket]] = {}
        self.integration_history = []
        
    def register_source(self, source_name: str):
        """注册信息源"""
        if source_name not in self.input_buffers:
            self.input_buffers[source_name] = []
    
    def receive(self, packet: InformationPacket):
        """接收信息包"""
        self.register_source(packet.source)
        self.input_buffers[packet.source].append(packet)
        
        if len(self.input_buffers[packet.source]) > 100:
            self.input_buffers[packet.source] = self.input_buffers[packet.source][-50:]
    
    def integrate(self) -> List[InformationPacket]:
        """整合所有输入"""
        all_packets = []
        
        for source, packets in self.input_buffers.items():
            all_packets.extend(packets)
        
        if not all_packets:
            return []
        
        all_packets.sort(key=lambda p: p.salience, reverse=True)
        
        integrated = []
        for packet in all_packets[:20]:
            if packet.salience > self.integration_threshold:
                integrated.append(packet)
        
        self._record_integration(integrated)
        
        return integrated
    
    def clear_buffers(self):
        """清空输入缓冲区"""
        for source in self.input_buffers:
            self.input_buffers[source] = []
    
    def _record_integration(self, integrated: List[InformationPacket]):
        """记录整合事件"""
        self.integration_history.append({
            'integrated_count': len(integrated),
            'sources': list(set(p.source for p in integrated)),
            'avg_salience': np.mean([p.salience for p in integrated]) if integrated else 0.0,
            'timestamp': datetime.now().timestamp(),
        })
        
        if len(self.integration_history) > 500:
            self.integration_history = self.integration_history[-250:]
    
    def get_buffer_stats(self) -> Dict[str, Any]:
        """获取缓冲区统计"""
        return {
            'source_count': len(self.input_buffers),
            'total_packets': sum(len(buf) for buf in self.input_buffers.values()),
            'sources': {src: len(buf) for src, buf in self.input_buffers.items()},
        }


class ConsciousnessEmergence:
    """意识涌现机制 - 通过竞争产生意识内容"""
    
    def __init__(self, 
                 competition_threshold: float = 0.6,
                 attention_capacity: int = 7):
        self.competition_threshold = competition_threshold
        self.attention_capacity = attention_capacity
        self.competition_history = []
        self.current_conscious_content: Optional[ConsciousContent] = None
        
    def compete(self, packets: List[InformationPacket]) -> Optional[ConsciousContent]:
        """竞争产生意识内容
        
        Args:
            packets: 竞争的信息包列表
            
        Returns:
            胜出的意识内容
        """
        if not packets:
            return None
        
        scored_packets = []
        for packet in packets:
            score = self._calculate_competition_score(packet)
            scored_packets.append((packet, score))
        
        scored_packets.sort(key=lambda x: x[1], reverse=True)
        
        top_packets = scored_packets[:self.attention_capacity]
        
        if not top_packets:
            return None
        
        winner_packet, winner_score = top_packets[0]
        
        if winner_score < self.competition_threshold:
            return None
        
        conscious_content = ConsciousContent(
            content=winner_packet.content,
            sources=[p[0].source for p in top_packets[:3]],
            integration_level=winner_score,
            broadcast_range=self._determine_broadcast_range(top_packets),
            duration=self._estimate_duration(winner_score),
        )
        
        self.current_conscious_content = conscious_content
        
        self._record_competition(scored_packets, conscious_content)
        
        return conscious_content
    
    def _calculate_competition_score(self, packet: InformationPacket) -> float:
        """计算竞争分数"""
        base_score = packet.salience
        
        recency_bonus = self._calculate_recency_bonus(packet.timestamp)
        
        modality_bonus = self._get_modality_bonus(packet.modality)
        
        final_score = base_score * 0.6 + recency_bonus * 0.2 + modality_bonus * 0.2
        
        return min(final_score, 1.0)
    
    def _calculate_recency_bonus(self, timestamp: float) -> float:
        """计算时间新近性加成"""
        current_time = time.time()
        time_diff = current_time - timestamp
        
        if time_diff < 1.0:
            return 1.0
        elif time_diff < 5.0:
            return 0.8
        elif time_diff < 10.0:
            return 0.5
        else:
            return 0.2
    
    def _get_modality_bonus(self, modality: str) -> float:
        """获取模态加成"""
        modality_priorities = {
            'threat': 1.0,
            'emotion': 0.9,
            'attention': 0.85,
            'memory': 0.75,
            'perception': 0.7,
            'thought': 0.65,
            'default': 0.5,
        }
        
        return modality_priorities.get(modality, 0.5)
    
    def _determine_broadcast_range(self, top_packets: List[Tuple[InformationPacket, float]]) -> List[str]:
        """确定广播范围"""
        broadcast_targets = set()
        
        for packet, score in top_packets:
            if score > 0.7:
                broadcast_targets.add('all')
            elif score > 0.5:
                broadcast_targets.add('executive')
                broadcast_targets.add('memory')
        
        if not broadcast_targets:
            broadcast_targets.add('local')
        
        return list(broadcast_targets)
    
    def _estimate_duration(self, score: float) -> float:
        """估计意识持续时间（秒）"""
        base_duration = 2.0
        max_duration = 10.0
        
        duration = base_duration + (score * (max_duration - base_duration))
        
        return duration
    
    def _record_competition(self, 
                           scored_packets: List[Tuple[InformationPacket, float]],
                           winner: Optional[ConsciousContent]):
        """记录竞争事件"""
        self.competition_history.append({
            'participant_count': len(scored_packets),
            'winner_source': winner.sources[0] if winner else None,
            'winner_score': winner.integration_level if winner else 0.0,
            'timestamp': datetime.now().timestamp(),
        })
        
        if len(self.competition_history) > 500:
            self.competition_history = self.competition_history[-250:]
    
    def get_conscious_state(self) -> Dict[str, Any]:
        """获取意识状态"""
        return {
            'has_conscious_content': self.current_conscious_content is not None,
            'content': self.current_conscious_content.content if self.current_conscious_content else None,
            'integration_level': self.current_conscious_content.integration_level if self.current_conscious_content else 0.0,
            'sources': self.current_conscious_content.sources if self.current_conscious_content else [],
        }


class GlobalBroadcaster:
    """全局广播器 - 将意识内容广播到整个系统"""
    
    def __init__(self):
        self.subscribers: Dict[str, Callable] = {}
        self.broadcast_history = []
        self.broadcast_queue = queue.Queue()
        
    def subscribe(self, module_name: str, callback: Callable):
        """订阅广播
        
        Args:
            module_name: 模块名称
            callback: 回调函数
        """
        self.subscribers[module_name] = callback
    
    def unsubscribe(self, module_name: str):
        """取消订阅"""
        if module_name in self.subscribers:
            del self.subscribers[module_name]
    
    def broadcast(self, conscious_content: ConsciousContent):
        """广播意识内容"""
        if not conscious_content:
            return
        
        broadcast_targets = self._filter_targets(conscious_content.broadcast_range)
        
        broadcast_record = {
            'content': conscious_content.content,
            'targets': list(broadcast_targets.keys()),
            'integration_level': conscious_content.integration_level,
            'timestamp': datetime.now().timestamp(),
        }
        
        self.broadcast_history.append(broadcast_record)
        
        for module_name, callback in broadcast_targets.items():
            try:
                callback(conscious_content)
            except Exception as e:
                print(f"Broadcast error to {module_name}: {e}")
        
        if len(self.broadcast_history) > 500:
            self.broadcast_history = self.broadcast_history[-250:]
    
    def _filter_targets(self, broadcast_range: List[str]) -> Dict[str, Callable]:
        """过滤广播目标"""
        if 'all' in broadcast_range:
            return self.subscribers.copy()
        
        filtered = {}
        for module_name, callback in self.subscribers.items():
            if any(target in module_name.lower() for target in broadcast_range):
                filtered[module_name] = callback
        
        return filtered
    
    def get_broadcast_stats(self) -> Dict[str, Any]:
        """获取广播统计"""
        return {
            'subscriber_count': len(self.subscribers),
            'subscribers': list(self.subscribers.keys()),
            'total_broadcasts': len(self.broadcast_history),
        }


class AttentionController:
    """注意力控制器 - 管理注意力资源分配"""
    
    def __init__(self, total_capacity: float = 100.0):
        self.total_capacity = total_capacity
        self.allocated_attention: Dict[str, float] = {}
        self.attention_history = []
        
    def allocate(self, 
                 demands: Dict[str, float]) -> Dict[str, float]:
        """分配注意力资源
        
        Args:
            demands: 各模块的注意力需求
            
        Returns:
            分配结果
        """
        total_demand = sum(demands.values())
        
        if total_demand <= self.total_capacity:
            allocation = demands.copy()
        else:
            allocation = {}
            remaining_capacity = self.total_capacity
            
            sorted_demands = sorted(demands.items(), key=lambda x: x[1], reverse=True)
            
            for module, demand in sorted_demands:
                if remaining_capacity <= 0:
                    allocation[module] = 0.0
                else:
                    allocated = min(demand, remaining_capacity)
                    allocation[module] = allocated
                    remaining_capacity -= allocated
        
        self.allocated_attention = allocation
        
        self._record_allocation(allocation)
        
        return allocation
    
    def get_attention_focus(self) -> Tuple[str, float]:
        """获取注意力焦点"""
        if not self.allocated_attention:
            return 'none', 0.0
        
        focused_module = max(self.allocated_attention.items(), key=lambda x: x[1])
        
        return focused_module
    
    def release(self, module_name: str):
        """释放注意力资源"""
        if module_name in self.allocated_attention:
            del self.allocated_attention[module_name]
    
    def _record_allocation(self, allocation: Dict[str, float]):
        """记录分配事件"""
        self.attention_history.append({
            'allocation': allocation.copy(),
            'total_allocated': sum(allocation.values()),
            'timestamp': datetime.now().timestamp(),
        })
        
        if len(self.attention_history) > 500:
            self.attention_history = self.attention_history[-250:]
    
    def get_attention_stats(self) -> Dict[str, Any]:
        """获取注意力统计"""
        focused_module, focused_amount = self.get_attention_focus()
        
        return {
            'total_capacity': self.total_capacity,
            'allocated_capacity': sum(self.allocated_attention.values()),
            'available_capacity': self.total_capacity - sum(self.allocated_attention.values()),
            'focused_module': focused_module,
            'focused_amount': focused_amount,
            'allocation_count': len(self.allocated_attention),
        }


class GlobalWorkspace:
    """全局工作空间 - 意识涌现的核心机制
    
    基于全局工作空间理论，实现：
    - 信息整合：从多个专门模块收集信息
    - 意识涌现：通过竞争产生意识内容
    - 全局广播：将意识内容广播到整个系统
    - 注意力控制：管理注意力资源分配
    """
    
    def __init__(self, 
                 integration_threshold: float = 0.5,
                 competition_threshold: float = 0.6,
                 attention_capacity: int = 7):
        
        self.integrator = InformationIntegrator(integration_threshold)
        self.consciousness = ConsciousnessEmergence(competition_threshold, attention_capacity)
        self.broadcaster = GlobalBroadcaster()
        self.attention = AttentionController()
        
        self.workspace_state = WorkspaceState(
            active_content=None,
            competing_inputs=[],
            attention_focus=0.5,
            processing_load=0.0,
        )
        
        self.processing_history = []
        self.is_active = False
        
    def register_module(self, module_name: str, callback: Callable):
        """注册模块到全局工作空间
        
        Args:
            module_name: 模块名称
            callback: 接收广播的回调函数
        """
        self.integrator.register_source(module_name)
        self.broadcaster.subscribe(module_name, callback)
    
    def submit(self, packet: InformationPacket):
        """提交信息到工作空间
        
        Args:
            packet: 信息包
        """
        self.integrator.receive(packet)
    
    def process(self) -> Optional[ConsciousContent]:
        """处理工作空间中的信息
        
        Returns:
            产生的意识内容
        """
        self.is_active = True
        
        integrated_packets = self.integrator.integrate()
        
        self.workspace_state.competing_inputs = integrated_packets
        
        conscious_content = self.consciousness.compete(integrated_packets)
        
        if conscious_content:
            self.workspace_state.active_content = conscious_content
            
            self.broadcaster.broadcast(conscious_content)
            
            attention_demands = self._calculate_attention_demands(integrated_packets)
            self.attention.allocate(attention_demands)
            
            focused_module, focused_amount = self.attention.get_attention_focus()
            self.workspace_state.attention_focus = focused_amount
        
        self.workspace_state.processing_load = len(integrated_packets) / 20.0
        
        self._record_processing(conscious_content)
        
        return conscious_content
    
    def run_cycle(self, timeout: float = 1.0) -> Optional[ConsciousContent]:
        """运行一个处理周期
        
        Args:
            timeout: 超时时间（秒）
            
        Returns:
            产生的意识内容
        """
        start_time = time.time()
        
        result = self.process()
        
        elapsed = time.time() - start_time
        if elapsed < timeout:
            time.sleep(timeout - elapsed)
        
        return result
    
    def get_state(self) -> WorkspaceState:
        """获取工作空间状态"""
        return self.workspace_state
    
    def get_conscious_content(self) -> Optional[ConsciousContent]:
        """获取当前意识内容"""
        return self.consciousness.current_conscious_content
    
    def _calculate_attention_demands(self, packets: List[InformationPacket]) -> Dict[str, float]:
        """计算注意力需求"""
        demands = {}
        
        for packet in packets:
            if packet.source not in demands:
                demands[packet.source] = 0.0
            
            demands[packet.source] += packet.salience * 10
        
        return demands
    
    def _record_processing(self, conscious_content: Optional[ConsciousContent]):
        """记录处理事件"""
        self.processing_history.append({
            'had_conscious_content': conscious_content is not None,
            'content_sources': conscious_content.sources if conscious_content else [],
            'integration_level': conscious_content.integration_level if conscious_content else 0.0,
            'processing_load': self.workspace_state.processing_load,
            'timestamp': datetime.now().timestamp(),
        })
        
        if len(self.processing_history) > 500:
            self.processing_history = self.processing_history[-250:]
    
    def get_workspace_stats(self) -> Dict[str, Any]:
        """获取工作空间统计信息"""
        return {
            'is_active': self.is_active,
            'buffer_stats': self.integrator.get_buffer_stats(),
            'conscious_state': self.consciousness.get_conscious_state(),
            'broadcast_stats': self.broadcaster.get_broadcast_stats(),
            'attention_stats': self.attention.get_attention_stats(),
            'processing_history_length': len(self.processing_history),
        }
    
    def reset(self):
        """重置工作空间"""
        self.integrator.clear_buffers()
        self.consciousness.current_conscious_content = None
        self.workspace_state = WorkspaceState(
            active_content=None,
            competing_inputs=[],
            attention_focus=0.5,
            processing_load=0.0,
        )
        self.is_active = False
