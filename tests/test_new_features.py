#!/usr/bin/env python3
"""
RandomAgent 新功能测试

测试：
- 异步支持
- 性能监控
- 扩展 AI 提供商
"""

import unittest
import asyncio
import time
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from random_agent.async_support import (
    AsyncManager,
    AsyncCache,
    AsyncTaskQueue,
    async_retry,
    async_timeout,
    sync_to_async,
    async_to_sync,
    get_async_manager,
)

from random_agent.monitoring import (
    MetricsCollector,
    PerformanceTracker,
    AlertManager,
    PerformanceReporter,
    get_metrics_collector,
    get_performance_tracker,
    record_metric,
)


class TestAsyncSupport(unittest.TestCase):
    """测试异步支持"""
    
    def test_async_manager_singleton(self):
        """测试异步管理器单例"""
        manager1 = get_async_manager()
        manager2 = get_async_manager()
        
        self.assertIs(manager1, manager2)
    
    def test_async_cache(self):
        """测试异步缓存"""
        async def run_test():
            cache = AsyncCache(max_size=3, ttl=1)
            
            await cache.set("key1", "value1")
            result = await cache.get("key1")
            
            self.assertEqual(result, "value1")
            
            await cache.delete("key1")
            result = await cache.get("key1")
            
            self.assertIsNone(result)
        
        asyncio.run(run_test())
    
    def test_sync_to_async(self):
        """测试同步转异步"""
        def sync_func(x):
            return x * 2
        
        async_func = sync_to_async(sync_func)
        
        async def run_test():
            result = await async_func(5)
            self.assertEqual(result, 10)
        
        asyncio.run(run_test())
    
    def test_async_to_sync(self):
        """测试异步转同步"""
        async def async_func(x):
            await asyncio.sleep(0.01)
            return x * 2
        
        sync_func = async_to_sync(async_func)
        
        result = sync_func(5)
        self.assertEqual(result, 10)
    
    def test_async_retry(self):
        """测试异步重试"""
        call_count = 0
        
        @async_retry(max_retries=3, delay=0.01)
        async def flaky_function():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ValueError("Temporary error")
            return "success"
        
        async def run_test():
            result = await flaky_function()
            self.assertEqual(result, "success")
            self.assertEqual(call_count, 3)
        
        asyncio.run(run_test())
    
    def test_async_timeout(self):
        """测试异步超时"""
        @async_timeout(0.1)
        async def slow_function():
            await asyncio.sleep(1)
            return "done"
        
        async def run_test():
            with self.assertRaises(asyncio.TimeoutError):
                await slow_function()
        
        asyncio.run(run_test())


class TestMonitoring(unittest.TestCase):
    """测试性能监控"""
    
    def test_metrics_collector_singleton(self):
        """测试指标收集器单例"""
        collector1 = get_metrics_collector()
        collector2 = get_metrics_collector()
        
        self.assertIs(collector1, collector2)
    
    def test_record_metric(self):
        """测试记录指标"""
        collector = MetricsCollector()
        
        collector.record("test_metric", 10.0)
        collector.record("test_metric", 20.0)
        collector.record("test_metric", 30.0)
        
        metric = collector.get_metric("test_metric")
        
        self.assertIsNotNone(metric)
        self.assertEqual(metric.min_value, 10.0)
        self.assertEqual(metric.max_value, 30.0)
        self.assertEqual(metric.avg_value, 20.0)
    
    def test_metric_summary(self):
        """测试指标摘要"""
        collector = MetricsCollector()
        
        collector.record("cpu_usage", 50.0)
        collector.record("cpu_usage", 60.0)
        collector.record("cpu_usage", 70.0)
        
        summary = collector.get_metric_summary("cpu_usage")
        
        self.assertEqual(summary["min"], 50.0)
        self.assertEqual(summary["max"], 70.0)
        self.assertEqual(summary["avg"], 60.0)
        self.assertEqual(summary["count"], 3)
    
    def test_performance_tracker(self):
        """测试性能追踪器"""
        tracker = PerformanceTracker()
        
        tracker.start_trace("test_operation")
        time.sleep(0.01)
        duration = tracker.end_trace("test_operation")
        
        self.assertGreater(duration, 0)
        
        metric = tracker._collector.get_metric("test_operation_duration")
        self.assertIsNotNone(metric)
    
    def test_alert_manager(self):
        """测试告警管理器"""
        alert_manager = AlertManager()
        collector = MetricsCollector()
        
        alert_manager.add_rule(
            metric_name="cpu_percent",
            threshold=80.0,
            comparison="greater",
            message="CPU 使用率过高"
        )
        
        collector.record("cpu_percent", 90.0)
        alert_manager.check_alerts(collector)
        
        alerts = alert_manager.get_alerts()
        self.assertEqual(len(alerts), 1)
        self.assertEqual(alerts[0]["value"], 90.0)
    
    def test_performance_reporter(self):
        """测试性能报告生成器"""
        collector = MetricsCollector()
        
        collector.record("response_time", 100.0)
        collector.record("response_time", 200.0)
        
        reporter = PerformanceReporter(collector)
        report = reporter.generate_report()
        
        self.assertIn("generated_at", report)
        self.assertIn("metrics", report)
        self.assertIn("response_time", report["metrics"])


class TestExtendedProviders(unittest.TestCase):
    """测试扩展 AI 提供商"""
    
    def test_extended_provider_enum(self):
        """测试扩展提供商枚举"""
        from random_agent.extended_providers import ExtendedAIProvider
        
        self.assertEqual(ExtendedAIProvider.GOOGLE.value, "google")
        self.assertEqual(ExtendedAIProvider.COHERE.value, "cohere")
        self.assertEqual(ExtendedAIProvider.AZURE_OPENAI.value, "azure_openai")
    
    def test_provider_factory(self):
        """测试提供商工厂"""
        from random_agent.extended_providers import ExtendedAIProviderFactory
        from random_agent.ai_integration import AIConfig
        
        config = AIConfig(model="test-model")
        
        with self.assertRaises(ValueError):
            ExtendedAIProviderFactory.create(config, "invalid_provider")


if __name__ == "__main__":
    unittest.main(verbosity=2)
