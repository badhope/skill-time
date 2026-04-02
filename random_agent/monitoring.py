"""
性能监控系统 (Performance Monitoring)

提供全面的性能监控：
- 性能指标收集
- 资源使用监控
- 性能报告生成
- 告警机制
"""

import time
import psutil
import threading
from typing import Any, Optional, Dict, List, Callable
from dataclasses import dataclass, field
from datetime import datetime
from collections import defaultdict
import json


@dataclass
class MetricValue:
    """指标值"""
    value: float
    timestamp: float
    tags: Dict[str, str] = field(default_factory=dict)


@dataclass
class PerformanceMetric:
    """性能指标"""
    name: str
    description: str
    unit: str
    values: List[MetricValue] = field(default_factory=list)
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    avg_value: Optional[float] = None


class MetricsCollector:
    """
    指标收集器
    
    收集和管理性能指标
    """
    
    _instance: Optional["MetricsCollector"] = None
    _lock = threading.Lock()
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, max_values_per_metric: int = 1000):
        if hasattr(self, '_initialized') and self._initialized:
            return
        
        self.max_values_per_metric = max_values_per_metric
        self._metrics: Dict[str, PerformanceMetric] = {}
        self._initialized = True
    
    def register_metric(
        self,
        name: str,
        description: str = "",
        unit: str = ""
    ):
        """注册指标"""
        if name not in self._metrics:
            self._metrics[name] = PerformanceMetric(
                name=name,
                description=description,
                unit=unit
            )
    
    def record(
        self,
        name: str,
        value: float,
        tags: Optional[Dict[str, str]] = None
    ):
        """记录指标值"""
        if name not in self._metrics:
            self.register_metric(name)
        
        metric = self._metrics[name]
        metric_value = MetricValue(
            value=value,
            timestamp=time.time(),
            tags=tags or {}
        )
        
        metric.values.append(metric_value)
        
        if len(metric.values) > self.max_values_per_metric:
            metric.values = metric.values[-self.max_values_per_metric:]
        
        values = [v.value for v in metric.values]
        metric.min_value = min(values)
        metric.max_value = max(values)
        metric.avg_value = sum(values) / len(values)
    
    def get_metric(self, name: str) -> Optional[PerformanceMetric]:
        """获取指标"""
        return self._metrics.get(name)
    
    def get_all_metrics(self) -> Dict[str, PerformanceMetric]:
        """获取所有指标"""
        return self._metrics.copy()
    
    def get_metric_summary(self, name: str) -> Dict[str, Any]:
        """获取指标摘要"""
        metric = self.get_metric(name)
        if not metric:
            return {}
        
        return {
            "name": metric.name,
            "description": metric.description,
            "unit": metric.unit,
            "min": metric.min_value,
            "max": metric.max_value,
            "avg": metric.avg_value,
            "count": len(metric.values),
            "latest": metric.values[-1].value if metric.values else None
        }
    
    def clear_metric(self, name: str):
        """清除指标"""
        if name in self._metrics:
            del self._metrics[name]
    
    def clear_all(self):
        """清除所有指标"""
        self._metrics.clear()


class SystemMonitor:
    """
    系统监控器
    
    监控系统资源使用情况
    """
    
    def __init__(self, interval: float = 1.0):
        self.interval = interval
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._collector = MetricsCollector()
    
    def _monitor_loop(self):
        """监控循环"""
        while self._running:
            try:
                self._collect_system_metrics()
                time.sleep(self.interval)
            except Exception as e:
                print(f"监控错误: {e}")
    
    def _collect_system_metrics(self):
        """收集系统指标"""
        self._collector.record("cpu_percent", psutil.cpu_percent())
        self._collector.record("memory_percent", psutil.virtual_memory().percent)
        self._collector.record("disk_percent", psutil.disk_usage('/').percent)
        
        net_io = psutil.net_io_counters()
        self._collector.record("network_bytes_sent", net_io.bytes_sent)
        self._collector.record("network_bytes_recv", net_io.bytes_recv)
    
    def start(self):
        """启动监控"""
        if self._running:
            return
        
        self._running = True
        self._thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self._thread.start()
    
    def stop(self):
        """停止监控"""
        self._running = False
        if self._thread:
            self._thread.join(timeout=2.0)
            self._thread = None
    
    def get_system_status(self) -> Dict[str, Any]:
        """获取系统状态"""
        return {
            "cpu_percent": psutil.cpu_percent(),
            "memory": {
                "total": psutil.virtual_memory().total,
                "available": psutil.virtual_memory().available,
                "percent": psutil.virtual_memory().percent
            },
            "disk": {
                "total": psutil.disk_usage('/').total,
                "used": psutil.disk_usage('/').used,
                "percent": psutil.disk_usage('/').percent
            },
            "network": {
                "bytes_sent": psutil.net_io_counters().bytes_sent,
                "bytes_recv": psutil.net_io_counters().bytes_recv
            }
        }


class PerformanceTracker:
    """
    性能追踪器
    
    追踪函数和代码块的性能
    """
    
    def __init__(self):
        self._collector = MetricsCollector()
        self._active_traces: Dict[str, float] = {}
        self._lock = threading.Lock()
    
    def start_trace(self, name: str):
        """开始追踪"""
        with self._lock:
            self._active_traces[name] = time.time()
    
    def end_trace(self, name: str) -> float:
        """结束追踪"""
        with self._lock:
            if name not in self._active_traces:
                return 0.0
            
            duration = time.time() - self._active_traces[name]
            del self._active_traces[name]
            
            self._collector.record(f"{name}_duration", duration)
            
            return duration
    
    def trace(self, name: str):
        """追踪装饰器"""
        def decorator(func):
            def wrapper(*args, **kwargs):
                self.start_trace(name)
                try:
                    result = func(*args, **kwargs)
                    return result
                finally:
                    self.end_trace(name)
            return wrapper
        return decorator


class AlertManager:
    """
    告警管理器
    
    管理性能告警
    """
    
    def __init__(self):
        self._alerts: List[Dict[str, Any]] = []
        self._rules: List[Dict[str, Any]] = []
        self._callbacks: List[Callable] = []
    
    def add_rule(
        self,
        metric_name: str,
        threshold: float,
        comparison: str = "greater",
        message: str = ""
    ):
        """添加告警规则"""
        self._rules.append({
            "metric_name": metric_name,
            "threshold": threshold,
            "comparison": comparison,
            "message": message
        })
    
    def check_alerts(self, collector: MetricsCollector):
        """检查告警"""
        for rule in self._rules:
            metric = collector.get_metric(rule["metric_name"])
            if not metric or not metric.values:
                continue
            
            latest_value = metric.values[-1].value
            triggered = False
            
            if rule["comparison"] == "greater" and latest_value > rule["threshold"]:
                triggered = True
            elif rule["comparison"] == "less" and latest_value < rule["threshold"]:
                triggered = True
            elif rule["comparison"] == "equal" and latest_value == rule["threshold"]:
                triggered = True
            
            if triggered:
                alert = {
                    "metric_name": rule["metric_name"],
                    "value": latest_value,
                    "threshold": rule["threshold"],
                    "message": rule["message"],
                    "timestamp": time.time()
                }
                self._alerts.append(alert)
                self._notify_callbacks(alert)
    
    def add_callback(self, callback: Callable):
        """添加告警回调"""
        self._callbacks.append(callback)
    
    def _notify_callbacks(self, alert: Dict[str, Any]):
        """通知回调"""
        for callback in self._callbacks:
            try:
                callback(alert)
            except Exception as e:
                print(f"告警回调错误: {e}")
    
    def get_alerts(self, limit: int = 100) -> List[Dict[str, Any]]:
        """获取告警"""
        return self._alerts[-limit:]
    
    def clear_alerts(self):
        """清除告警"""
        self._alerts.clear()


class PerformanceReporter:
    """
    性能报告生成器
    
    生成性能报告
    """
    
    def __init__(self, collector: MetricsCollector):
        self.collector = collector
    
    def generate_report(self) -> Dict[str, Any]:
        """生成报告"""
        metrics = self.collector.get_all_metrics()
        
        report = {
            "generated_at": datetime.now().isoformat(),
            "metrics": {}
        }
        
        for name, metric in metrics.items():
            report["metrics"][name] = {
                "description": metric.description,
                "unit": metric.unit,
                "min": metric.min_value,
                "max": metric.max_value,
                "avg": metric.avg_value,
                "count": len(metric.values),
                "latest": metric.values[-1].value if metric.values else None
            }
        
        return report
    
    def export_json(self, filepath: str):
        """导出为 JSON"""
        report = self.generate_report()
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
    
    def export_text(self, filepath: str):
        """导出为文本"""
        report = self.generate_report()
        
        lines = [
            "=" * 60,
            "RandomAgent 性能报告",
            "=" * 60,
            f"生成时间: {report['generated_at']}",
            "",
            "指标摘要:",
            "-" * 60
        ]
        
        for name, data in report["metrics"].items():
            lines.extend([
                f"\n{name}:",
                f"  描述: {data['description']}",
                f"  单位: {data['unit']}",
                f"  最小值: {data['min']:.2f}" if data['min'] else "  最小值: N/A",
                f"  最大值: {data['max']:.2f}" if data['max'] else "  最大值: N/A",
                f"  平均值: {data['avg']:.2f}" if data['avg'] else "  平均值: N/A",
                f"  最新值: {data['latest']:.2f}" if data['latest'] else "  最新值: N/A",
                f"  样本数: {data['count']}"
            ])
        
        lines.append("\n" + "=" * 60)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))


_global_collector: Optional[MetricsCollector] = None
_global_monitor: Optional[SystemMonitor] = None
_global_tracker: Optional[PerformanceTracker] = None


def get_metrics_collector() -> MetricsCollector:
    """获取全局指标收集器"""
    global _global_collector
    if _global_collector is None:
        _global_collector = MetricsCollector()
    return _global_collector


def get_system_monitor() -> SystemMonitor:
    """获取全局系统监控器"""
    global _global_monitor
    if _global_monitor is None:
        _global_monitor = SystemMonitor()
    return _global_monitor


def get_performance_tracker() -> PerformanceTracker:
    """获取全局性能追踪器"""
    global _global_tracker
    if _global_tracker is None:
        _global_tracker = PerformanceTracker()
    return _global_tracker


def record_metric(name: str, value: float, tags: Optional[Dict[str, str]] = None):
    """记录指标（便捷函数）"""
    get_metrics_collector().record(name, value, tags)


def track_performance(name: str):
    """性能追踪装饰器（便捷函数）"""
    return get_performance_tracker().trace(name)
