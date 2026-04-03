"""
事件驱动交互机制 - 模块间通信的核心
模拟大脑不同区域间的动态通信
"""

import numpy as np
from typing import Dict, List, Any, Optional, Callable, Set
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import threading
import queue
import time
from collections import defaultdict


class EventType(Enum):
    """事件类型枚举"""
    PERCEPTION_INPUT = "perception_input"
    PERCEPTION_PROCESSED = "perception_processed"
    
    MEMORY_ENCODE = "memory_encode"
    MEMORY_RETRIEVE = "memory_retrieve"
    MEMORY_RETRIEVED = "memory_retrieved"
    MEMORY_CONSOLIDATE = "memory_consolidate"
    
    DMN_ACTIVATE = "dmn_activate"
    DMN_DEACTIVATE = "dmn_deactivate"
    DMN_THOUGHT_GENERATED = "dmn_thought_generated"
    
    CONSCIOUSNESS_EMERGE = "consciousness_emerge"
    CONSCIOUSNESS_BROADCAST = "consciousness_broadcast"
    
    EMOTION_PROCESS = "emotion_process"
    EMOTION_RESPONSE = "emotion_response"
    
    EXECUTIVE_DECISION = "executive_decision"
    EXECUTIVE_CONTROL = "executive_control"
    
    ATTENTION_FOCUS = "attention_focus"
    ATTENTION_SHIFT = "attention_shift"
    
    LEARNING_UPDATE = "learning_update"
    PLASTICITY_CHANGE = "plasticity_change"
    
    SYSTEM_ERROR = "system_error"
    SYSTEM_RESET = "system_reset"


@dataclass
class BrainEvent:
    """脑事件数据结构"""
    event_type: EventType
    source: str
    target: Optional[str]
    data: Dict[str, Any]
    timestamp: float = field(default_factory=lambda: time.time())
    priority: float = 0.5
    propagation_delay: float = 0.0
    event_id: str = field(default_factory=lambda: f"evt_{int(time.time()*1000)}")


class EventListener:
    """事件监听器"""
    
    def __init__(self, 
                 callback: Callable[[BrainEvent], None],
                 listener_id: str,
                 priority: float = 0.5):
        self.callback = callback
        self.listener_id = listener_id
        self.priority = priority
        self.call_count = 0
        self.last_called = None
        
    def notify(self, event: BrainEvent):
        """通知监听器"""
        try:
            self.callback(event)
            self.call_count += 1
            self.last_called = datetime.now()
        except Exception as e:
            print(f"Listener {self.listener_id} error: {e}")


class EventBus:
    """事件总线 - 模块间通信的核心枢纽"""
    
    def __init__(self, max_queue_size: int = 1000):
        self.max_queue_size = max_queue_size
        self.event_queue = queue.PriorityQueue(maxsize=max_queue_size)
        self.listeners: Dict[EventType, List[EventListener]] = defaultdict(list)
        self.event_history: List[BrainEvent] = []
        self.is_running = False
        self.processing_thread: Optional[threading.Thread] = None
        
        self.stats = {
            'total_events': 0,
            'events_by_type': defaultdict(int),
            'events_by_source': defaultdict(int),
        }
        
    def subscribe(self, 
                 event_type: EventType,
                 listener: EventListener):
        """订阅事件
        
        Args:
            event_type: 事件类型
            listener: 监听器
        """
        self.listeners[event_type].append(listener)
        self.listeners[event_type].sort(key=lambda l: l.priority, reverse=True)
    
    def unsubscribe(self,
                   event_type: EventType,
                   listener_id: str):
        """取消订阅"""
        self.listeners[event_type] = [
            l for l in self.listeners[event_type] 
            if l.listener_id != listener_id
        ]
    
    def publish(self, event: BrainEvent, async_mode: bool = True):
        """发布事件
        
        Args:
            event: 脑事件
            async_mode: 是否异步处理
        """
        if async_mode:
            self.event_queue.put((-event.priority, event))
        else:
            self._process_event(event)
        
        self._update_stats(event)
    
    def start(self):
        """启动事件总线"""
        if self.is_running:
            return
        
        self.is_running = True
        self.processing_thread = threading.Thread(target=self._process_loop, daemon=True)
        self.processing_thread.start()
    
    def stop(self):
        """停止事件总线"""
        self.is_running = False
        if self.processing_thread:
            self.processing_thread.join(timeout=2.0)
    
    def _process_loop(self):
        """事件处理循环"""
        while self.is_running:
            try:
                priority, event = self.event_queue.get(timeout=0.1)
                
                if event.propagation_delay > 0:
                    time.sleep(event.propagation_delay)
                
                self._process_event(event)
                
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Event processing error: {e}")
    
    def _process_event(self, event: BrainEvent):
        """处理单个事件"""
        listeners = self.listeners.get(event.event_type, [])
        
        if event.target:
            listeners = [
                l for l in listeners 
                if l.listener_id == event.target or event.target == 'all'
            ]
        
        for listener in listeners:
            listener.notify(event)
        
        self.event_history.append(event)
        
        if len(self.event_history) > 1000:
            self.event_history = self.event_history[-500:]
    
    def _update_stats(self, event: BrainEvent):
        """更新统计信息"""
        self.stats['total_events'] += 1
        self.stats['events_by_type'][event.event_type.value] += 1
        self.stats['events_by_source'][event.source] += 1
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            'total_events': self.stats['total_events'],
            'events_by_type': dict(self.stats['events_by_type']),
            'events_by_source': dict(self.stats['events_by_source']),
            'queue_size': self.event_queue.qsize(),
            'listener_count': sum(len(lst) for lst in self.listeners.values()),
            'is_running': self.is_running,
        }


class NeuralPathway:
    """神经通路 - 模拟大脑中的神经纤维连接"""
    
    def __init__(self, 
                 source: str,
                 target: str,
                 pathway_type: str,
                 strength: float = 1.0,
                 delay: float = 0.01):
        self.source = source
        self.target = target
        self.pathway_type = pathway_type
        self.strength = strength
        self.delay = delay
        self.activation_count = 0
        self.last_activated = None
        
    def activate(self, signal_strength: float) -> float:
        """激活通路
        
        Args:
            signal_strength: 输入信号强度
            
        Returns:
            输出信号强度
        """
        output_strength = signal_strength * self.strength
        
        self.activation_count += 1
        self.last_activated = datetime.now()
        
        return output_strength
    
    def strengthen(self, amount: float = 0.05):
        """增强通路"""
        self.strength = min(self.strength + amount, 2.0)
    
    def weaken(self, amount: float = 0.01):
        """减弱通路"""
        self.strength = max(self.strength - amount, 0.1)


class ConnectionManager:
    """连接管理器 - 管理模块间的动态连接"""
    
    def __init__(self):
        self.pathways: Dict[str, NeuralPathway] = {}
        self.connection_matrix: Dict[str, Dict[str, float]] = defaultdict(lambda: defaultdict(float))
        self.connection_history = []
        
    def create_pathway(self,
                      source: str,
                      target: str,
                      pathway_type: str = 'default',
                      strength: float = 1.0,
                      delay: float = 0.01) -> NeuralPathway:
        """创建神经通路
        
        Args:
            source: 源模块
            target: 目标模块
            pathway_type: 通路类型
            strength: 初始强度
            delay: 传递延迟
            
        Returns:
            创建的神经通路
        """
        pathway_id = f"{source}->{target}"
        
        pathway = NeuralPathway(
            source=source,
            target=target,
            pathway_type=pathway_type,
            strength=strength,
            delay=delay
        )
        
        self.pathways[pathway_id] = pathway
        self.connection_matrix[source][target] = strength
        
        self._record_connection('create', pathway)
        
        return pathway
    
    def remove_pathway(self, source: str, target: str):
        """移除神经通路"""
        pathway_id = f"{source}->{target}"
        
        if pathway_id in self.pathways:
            pathway = self.pathways[pathway_id]
            del self.pathways[pathway_id]
            
            if source in self.connection_matrix and target in self.connection_matrix[source]:
                del self.connection_matrix[source][target]
            
            self._record_connection('remove', pathway)
    
    def get_pathway(self, source: str, target: str) -> Optional[NeuralPathway]:
        """获取神经通路"""
        pathway_id = f"{source}->{target}"
        return self.pathways.get(pathway_id)
    
    def activate_pathway(self, 
                        source: str, 
                        target: str,
                        signal_strength: float) -> float:
        """激活通路"""
        pathway = self.get_pathway(source, target)
        
        if pathway:
            return pathway.activate(signal_strength)
        
        return 0.0
    
    def get_connected_targets(self, source: str) -> List[str]:
        """获取连接的目标模块"""
        if source in self.connection_matrix:
            return list(self.connection_matrix[source].keys())
        return []
    
    def get_connected_sources(self, target: str) -> List[str]:
        """获取连接的源模块"""
        sources = []
        for source, targets in self.connection_matrix.items():
            if target in targets:
                sources.append(source)
        return sources
    
    def strengthen_pathway(self, source: str, target: str, amount: float = 0.05):
        """增强通路"""
        pathway = self.get_pathway(source, target)
        if pathway:
            pathway.strengthen(amount)
            self.connection_matrix[source][target] = pathway.strength
    
    def weaken_pathway(self, source: str, target: str, amount: float = 0.01):
        """减弱通路"""
        pathway = self.get_pathway(source, target)
        if pathway:
            pathway.weaken(amount)
            self.connection_matrix[source][target] = pathway.strength
    
    def _record_connection(self, action: str, pathway: NeuralPathway):
        """记录连接变化"""
        self.connection_history.append({
            'action': action,
            'source': pathway.source,
            'target': pathway.target,
            'pathway_type': pathway.pathway_type,
            'strength': pathway.strength,
            'timestamp': datetime.now().timestamp(),
        })
        
        if len(self.connection_history) > 500:
            self.connection_history = self.connection_history[-250:]
    
    def get_connection_stats(self) -> Dict[str, Any]:
        """获取连接统计"""
        return {
            'total_pathways': len(self.pathways),
            'avg_strength': np.mean([p.strength for p in self.pathways.values()]) if self.pathways else 0.0,
            'pathway_types': list(set(p.pathway_type for p in self.pathways.values())),
            'connection_matrix_size': len(self.connection_matrix),
        }


class EventDrivenArchitecture:
    """事件驱动架构 - 整合事件总线和连接管理"""
    
    def __init__(self):
        self.event_bus = EventBus()
        self.connection_manager = ConnectionManager()
        self.modules: Dict[str, Any] = {}
        self.is_initialized = False
        
    def register_module(self, 
                       module_name: str,
                       module_instance: Any,
                       event_handlers: Dict[EventType, Callable]):
        """注册模块
        
        Args:
            module_name: 模块名称
            module_instance: 模块实例
            event_handlers: 事件处理器字典
        """
        self.modules[module_name] = module_instance
        
        for event_type, handler in event_handlers.items():
            listener = EventListener(
                callback=handler,
                listener_id=module_name,
                priority=0.5
            )
            self.event_bus.subscribe(event_type, listener)
    
    def connect_modules(self,
                       source: str,
                       target: str,
                       pathway_type: str = 'default',
                       strength: float = 1.0):
        """连接模块
        
        Args:
            source: 源模块
            target: 目标模块
            pathway_type: 通路类型
            strength: 连接强度
        """
        self.connection_manager.create_pathway(
            source=source,
            target=target,
            pathway_type=pathway_type,
            strength=strength
        )
    
    def disconnect_modules(self, source: str, target: str):
        """断开模块连接"""
        self.connection_manager.remove_pathway(source, target)
    
    def send_event(self,
                  event_type: EventType,
                  source: str,
                  data: Dict[str, Any],
                  target: Optional[str] = None,
                  priority: float = 0.5):
        """发送事件
        
        Args:
            event_type: 事件类型
            source: 源模块
            data: 事件数据
            target: 目标模块（None表示广播）
            priority: 优先级
        """
        connected_targets = self.connection_manager.get_connected_targets(source)
        
        if target:
            if target in connected_targets or target == 'all':
                pathway = self.connection_manager.get_pathway(source, target)
                delay = pathway.delay if pathway else 0.0
                
                event = BrainEvent(
                    event_type=event_type,
                    source=source,
                    target=target,
                    data=data,
                    priority=priority,
                    propagation_delay=delay
                )
                
                self.event_bus.publish(event)
        else:
            for target_module in connected_targets:
                pathway = self.connection_manager.get_pathway(source, target_module)
                
                event = BrainEvent(
                    event_type=event_type,
                    source=source,
                    target=target_module,
                    data=data,
                    priority=priority,
                    propagation_delay=pathway.delay if pathway else 0.0
                )
                
                self.event_bus.publish(event)
    
    def start(self):
        """启动架构"""
        self.event_bus.start()
        self.is_initialized = True
    
    def stop(self):
        """停止架构"""
        self.event_bus.stop()
        self.is_initialized = False
    
    def get_architecture_stats(self) -> Dict[str, Any]:
        """获取架构统计"""
        return {
            'is_initialized': self.is_initialized,
            'module_count': len(self.modules),
            'modules': list(self.modules.keys()),
            'event_bus_stats': self.event_bus.get_stats(),
            'connection_stats': self.connection_manager.get_connection_stats(),
        }


class BrainEventSystem:
    """脑事件系统 - 完整的事件驱动脑启发系统
    
    整合所有脑模块的事件驱动交互
    """
    
    def __init__(self):
        self.architecture = EventDrivenArchitecture()
        self.event_history: List[Dict[str, Any]] = []
        
    def setup_default_connections(self):
        """设置默认连接"""
        default_connections = [
            ('perception', 'hippocampus', 'feedforward', 1.0),
            ('perception', 'global_workspace', 'feedforward', 0.9),
            ('hippocampus', 'global_workspace', 'feedforward', 0.8),
            ('dmn', 'global_workspace', 'bidirectional', 0.7),
            ('global_workspace', 'hippocampus', 'feedback', 0.6),
            ('global_workspace', 'dmn', 'feedback', 0.6),
            ('global_workspace', 'perception', 'feedback', 0.5),
        ]
        
        for source, target, pathway_type, strength in default_connections:
            self.architecture.connect_modules(source, target, pathway_type, strength)
            
            if pathway_type == 'bidirectional':
                self.architecture.connect_modules(target, source, pathway_type, strength)
    
    def process_input(self, input_data: Any) -> Dict[str, Any]:
        """处理输入
        
        Args:
            input_data: 输入数据
            
        Returns:
            处理结果
        """
        self.architecture.send_event(
            event_type=EventType.PERCEPTION_INPUT,
            source='external',
            data={'input': input_data},
            target='perception'
        )
        
        return {
            'status': 'processed',
            'input': input_data,
            'timestamp': datetime.now().timestamp(),
        }
    
    def get_event_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """获取事件历史"""
        events = self.architecture.event_bus.event_history[-limit:]
        
        return [
            {
                'event_type': e.event_type.value,
                'source': e.source,
                'target': e.target,
                'timestamp': e.timestamp,
                'priority': e.priority,
            }
            for e in events
        ]
    
    def get_system_status(self) -> Dict[str, Any]:
        """获取系统状态"""
        return {
            'architecture_stats': self.architecture.get_architecture_stats(),
            'event_history_count': len(self.architecture.event_bus.event_history),
            'is_running': self.architecture.is_initialized,
        }
    
    def start(self):
        """启动系统"""
        self.setup_default_connections()
        self.architecture.start()
    
    def stop(self):
        """停止系统"""
        self.architecture.stop()
