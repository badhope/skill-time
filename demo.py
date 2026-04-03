#!/usr/bin/env python3
"""
RandomAgent 功能演示脚本

展示项目的各种使用场景
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def demo_basic_features():
    """演示基础功能"""
    print("\n" + "=" * 60)
    print("演示 1: 基础提示词生成")
    print("=" * 60)
    
    from random_agent import create_prompt, get_system_prompt_only
    
    # 生成完整提示词
    prompt = create_prompt(
        task="什么是创造力？",
        randomness=0.7,
        mode="creative"
    )
    
    print("\n生成的完整提示词（前500字符）:")
    print(prompt[:500] + "...")
    
    # 获取系统提示词
    system_prompt = get_system_prompt_only(randomness=0.5, mode="balanced")
    
    print("\n系统提示词（前300字符）:")
    print(system_prompt[:300] + "...")


def demo_config_management():
    """演示配置管理"""
    print("\n" + "=" * 60)
    print("演示 2: 配置管理系统")
    print("=" * 60)
    
    from random_agent import RandomAgentConfig, ConfigManager
    
    # 创建默认配置
    config = RandomAgentConfig()
    
    print("\n默认配置:")
    print(f"  版本: {config.version}")
    print(f"  随机性基础水平: {config.randomness.base_level}")
    print(f"  工作记忆容量: {config.memory.working_memory_capacity}")
    print(f"  人格开放性: {config.personality.openness}")
    
    # 配置验证
    manager = ConfigManager(config)
    errors = manager.validate()
    
    print(f"\n配置验证: {'通过' if not errors else '有错误'}")
    if errors:
        for error in errors:
            print(f"  - {error}")


def demo_logging_system():
    """演示日志系统"""
    print("\n" + "=" * 60)
    print("演示 3: 日志系统")
    print("=" * 60)
    
    from random_agent import setup_logging, get_logger
    
    # 设置日志
    setup_logging(level="INFO", console=True)
    
    # 获取 logger
    logger = get_logger("demo")
    
    print("\n日志记录示例:")
    logger.info("这是一条信息日志")
    logger.warning("这是一条警告日志")


def demo_cache_system():
    """演示缓存系统"""
    print("\n" + "=" * 60)
    print("演示 4: 缓存系统")
    print("=" * 60)
    
    from random_agent import LRUCache, cached
    
    # 使用 LRU 缓存
    cache = LRUCache(max_size=3)
    
    cache.set("key1", "value1")
    cache.set("key2", "value2")
    cache.set("key3", "value3")
    
    print("\n缓存操作:")
    print(f"  设置 key1, key2, key3")
    print(f"  获取 key1: {cache.get('key1')}")
    print(f"  获取 key2: {cache.get('key2')}")
    
    # 使用缓存装饰器
    @cached()
    def expensive_function(n):
        print(f"    计算中... {n}")
        return n * n
    
    print("\n缓存装饰器:")
    print(f"  第一次调用: {expensive_function(5)}")
    print(f"  第二次调用（使用缓存）: {expensive_function(5)}")


def demo_storage_system():
    """演示存储系统"""
    print("\n" + "=" * 60)
    print("演示 5: 存储系统")
    print("=" * 60)
    
    from random_agent import JSONStorage
    import tempfile
    
    # 使用临时目录
    with tempfile.TemporaryDirectory() as tmpdir:
        storage = JSONStorage(tmpdir)
        
        # 保存数据
        storage.save("test", {"name": "RandomAgent", "version": "0.2.0"})
        
        print("\n存储操作:")
        print(f"  保存数据到 test.json")
        
        # 加载数据
        data = storage.load("test")
        print(f"  加载数据: {data}")


def demo_async_support():
    """演示异步支持"""
    print("\n" + "=" * 60)
    print("演示 6: 异步支持")
    print("=" * 60)
    
    import asyncio
    from random_agent import AsyncCache, async_retry
    
    async def run_demo():
        # 异步缓存
        cache = AsyncCache(max_size=10)
        
        await cache.set("async_key", "async_value")
        value = await cache.get("async_key")
        
        print("\n异步缓存:")
        print(f"  设置 async_key")
        print(f"  获取 async_key: {value}")
        
        # 异步重试
        call_count = 0
        
        @async_retry(max_retries=3, delay=0.1)
        async def flaky_function():
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                print(f"  尝试 {call_count}: 失败")
                raise ValueError("Temporary error")
            print(f"  尝试 {call_count}: 成功")
            return "success"
        
        print("\n异步重试:")
        result = await flaky_function()
        print(f"  最终结果: {result}")
    
    asyncio.run(run_demo())


def demo_monitoring():
    """演示性能监控"""
    print("\n" + "=" * 60)
    print("演示 7: 性能监控")
    print("=" * 60)
    
    from random_agent import MetricsCollector, record_metric
    
    # 记录指标
    record_metric("response_time", 100.0)
    record_metric("response_time", 150.0)
    record_metric("response_time", 200.0)
    
    # 获取摘要
    collector = MetricsCollector()
    summary = collector.get_metric_summary("response_time")
    
    print("\n性能指标:")
    print(f"  指标名称: {summary['name']}")
    print(f"  最小值: {summary['min']}")
    print(f"  最大值: {summary['max']}")
    print(f"  平均值: {summary['avg']}")
    print(f"  样本数: {summary['count']}")


def demo_extended_providers():
    """演示扩展 AI 提供商"""
    print("\n" + "=" * 60)
    print("演示 8: 扩展 AI 提供商")
    print("=" * 60)
    
    from random_agent import ExtendedAIProvider
    
    print("\n支持的 AI 提供商:")
    for provider in ExtendedAIProvider:
        print(f"  - {provider.value}")


def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("RandomAgent v0.2.0 功能演示")
    print("=" * 60)
    
    demo_basic_features()
    demo_config_management()
    demo_logging_system()
    demo_cache_system()
    demo_storage_system()
    demo_async_support()
    demo_monitoring()
    demo_extended_providers()
    
    print("\n" + "=" * 60)
    print("演示完成！")
    print("=" * 60)
    print("\nRandomAgent 是一个功能完善的 AI Agent 框架")
    print("支持提示词生成、AI 集成、异步操作、性能监控等功能")
    print("\n更多信息请查看:")
    print("  - README.md")
    print("  - CHANGELOG.md")
    print("  - examples/ 目录")


if __name__ == "__main__":
    main()
