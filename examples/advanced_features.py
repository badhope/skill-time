#!/usr/bin/env python3
"""
RandomAgent 高级功能示例

展示如何使用：
- 配置管理
- 日志系统
- 异常处理
- 缓存机制
- 持久化存储
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from random_agent import (
    create_prompt,
    create_ai_agent,
    load_config,
    setup_logging,
    get_logger,
    track_performance,
    ConfigManager,
    RandomAgentConfig,
    SessionManager,
    get_prompt_cache,
    handle_errors,
)


def example_configuration():
    """示例：配置管理"""
    print("\n" + "=" * 60)
    print("示例 1: 配置管理")
    print("=" * 60)
    
    config = RandomAgentConfig()
    config.randomness.base_level = 0.7
    config.personality.openness = 0.8
    config.memory.working_memory_capacity = 10
    
    print(f"随机性水平: {config.randomness.base_level}")
    print(f"开放性: {config.personality.openness}")
    print(f"工作记忆容量: {config.memory.working_memory_capacity}")
    
    manager = ConfigManager(config)
    manager.save_to_file("config_example.json")
    print("\n✅ 配置已保存到 config_example.json")
    
    errors = manager.validate()
    if not errors:
        print("✅ 配置验证通过")
    else:
        print(f"❌ 配置错误: {errors}")


def example_logging():
    """示例：日志系统"""
    print("\n" + "=" * 60)
    print("示例 2: 日志系统")
    print("=" * 60)
    
    setup_logging(level="DEBUG", console=True)
    logger = get_logger("example")
    
    logger.info("这是一条信息日志")
    logger.warning("这是一条警告日志")
    logger.debug("这是一条调试日志")
    
    print("\n✅ 日志系统工作正常")


@track_performance("思考操作")
def example_performance_tracking():
    """示例：性能追踪"""
    import time
    time.sleep(0.1)
    return "完成"


def example_cache():
    """示例：缓存机制"""
    print("\n" + "=" * 60)
    print("示例 3: 缓存机制")
    print("=" * 60)
    
    cache = get_prompt_cache()
    
    prompt1 = create_prompt(
        task="什么是创造力？",
        randomness=0.7,
        mode="creative"
    )
    print(f"第一次生成提示词 ({len(prompt1)} 字符)")
    
    cached = cache.get_prompt(
        task="什么是创造力？",
        randomness=0.7,
        mode="creative",
        style="detailed"
    )
    
    if cached:
        print(f"✅ 从缓存获取 ({len(cached)} 字符)")
    else:
        cache.set_prompt(
            task="什么是创造力？",
            randomness=0.7,
            mode="creative",
            style="detailed",
            prompt=prompt1
        )
        print("✅ 已缓存提示词")
    
    stats = cache.get_stats()
    print(f"\n缓存统计:")
    print(f"  - 命中率: {stats['hit_rate']:.2%}")
    print(f"  - 总请求数: {stats['total_requests']}")


def example_session_management():
    """示例：会话管理"""
    print("\n" + "=" * 60)
    print("示例 4: 会话管理")
    print("=" * 60)
    
    session_manager = SessionManager()
    
    session = session_manager.create_session(
        metadata={"user": "example", "purpose": "demo"}
    )
    
    print(f"✅ 创建会话: {session.session_id}")
    
    session_manager.update_agent_state({
        "randomness": 0.7,
        "mode": "creative"
    })
    
    session_manager.add_thinking({
        "content": "思考中...",
        "level": "conscious"
    })
    
    print("✅ 会话数据已更新")
    
    sessions = session_manager.list_sessions(limit=5)
    print(f"\n最近会话数: {len(sessions)}")


@handle_errors(default_return=None, reraise=False)
def example_error_handling():
    """示例：错误处理"""
    print("\n" + "=" * 60)
    print("示例 5: 错误处理")
    print("=" * 60)
    
    try:
        result = 1 / 0
    except Exception as e:
        print(f"❌ 捕获错误: {e}")
        print("✅ 错误处理装饰器正常工作")


def example_integrated_usage():
    """示例：集成使用"""
    print("\n" + "=" * 60)
    print("示例 6: 集成使用")
    print("=" * 60)
    
    setup_logging(level="INFO", console=True)
    logger = get_logger("integrated")
    
    logger.info("开始集成示例")
    
    config = load_config(load_env=False)
    logger.info(f"配置加载成功: v{config.version}")
    
    cache = get_prompt_cache()
    
    @track_performance("提示词生成")
    def generate_with_cache(task: str):
        cached = cache.get_prompt(task, 0.5, "balanced", "concise")
        if cached:
            logger.info("使用缓存提示词")
            return cached
        
        prompt = create_prompt(task, randomness=0.5, mode="balanced", style="concise")
        cache.set_prompt(task, 0.5, "balanced", "concise", prompt)
        logger.info("生成新提示词")
        return prompt
    
    prompt = generate_with_cache("什么是人工智能？")
    print(f"\n生成的提示词:\n{prompt[:200]}...")
    
    logger.info("集成示例完成")


def main():
    """运行所有示例"""
    print("\n" + "=" * 60)
    print("RandomAgent 高级功能示例")
    print("=" * 60)
    
    example_configuration()
    example_logging()
    
    print("\n" + "=" * 60)
    print("性能追踪示例")
    print("=" * 60)
    result = example_performance_tracking()
    print(f"✅ 性能追踪完成: {result}")
    
    example_cache()
    example_session_management()
    example_error_handling()
    example_integrated_usage()
    
    print("\n" + "=" * 60)
    print("✅ 所有示例运行完成！")
    print("=" * 60)
    
    if os.path.exists("config_example.json"):
        os.remove("config_example.json")
        print("\n🧹 清理临时文件")


if __name__ == "__main__":
    main()
