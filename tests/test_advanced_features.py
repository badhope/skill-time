#!/usr/bin/env python3
"""
RandomAgent 新功能测试

测试：
- 配置管理
- 日志系统
- 异常处理
- 缓存机制
- 持久化存储
"""

import unittest
import sys
import os
import tempfile
import shutil

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from random_agent.config import (
    RandomAgentConfig,
    ConfigManager,
    load_config,
    RandomnessConfig,
    MemoryConfig,
)
from random_agent.logger import (
    RandomAgentLogger,
    setup_logging,
    get_logger,
)
from random_agent.exceptions import (
    RandomAgentError,
    ConfigurationError,
    ValidationError,
    handle_errors,
)
from random_agent.cache import (
    LRUCache,
    PromptCache,
    cached,
)
from random_agent.storage import (
    JSONStorage,
    SQLiteStorage,
    SessionManager,
    Session,
)


class TestConfiguration(unittest.TestCase):
    """测试配置管理"""
    
    def test_default_config(self):
        """测试默认配置"""
        config = RandomAgentConfig()
        
        self.assertEqual(config.version, "0.1.0")
        self.assertEqual(config.randomness.base_level, 0.5)
        self.assertEqual(config.memory.working_memory_capacity, 7)
        self.assertEqual(config.personality.openness, 0.6)
    
    def test_config_validation(self):
        """测试配置验证"""
        config = RandomAgentConfig()
        config.randomness.base_level = 1.5  # 无效值
        
        manager = ConfigManager(config)
        errors = manager.validate()
        
        self.assertGreater(len(errors), 0)
    
    def test_config_save_load(self):
        """测试配置保存和加载"""
        config = RandomAgentConfig()
        config.randomness.base_level = 0.8
        
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "config.json")
            
            manager = ConfigManager(config)
            manager.save_to_file(filepath)
            
            new_manager = ConfigManager()
            new_manager.load_from_file(filepath)
            
            self.assertEqual(
                new_manager.randomness.base_level,
                0.8
            )
    
    def test_config_to_dict(self):
        """测试配置转字典"""
        config = RandomAgentConfig()
        data = config.to_dict()
        
        self.assertIn("randomness", data)
        self.assertIn("memory", data)
        self.assertIn("personality", data)
        self.assertIsInstance(data["randomness"], dict)


class TestLogging(unittest.TestCase):
    """测试日志系统"""
    
    def test_setup_logging(self):
        """测试日志设置"""
        logger_manager = setup_logging(level="DEBUG", console=True)
        
        self.assertIsInstance(logger_manager, RandomAgentLogger)
    
    def test_get_logger(self):
        """测试获取 logger"""
        setup_logging(level="INFO", console=True)
        logger = get_logger("test")
        
        self.assertIsNotNone(logger)
        self.assertEqual(logger.name, "test")
    
    def test_logging_levels(self):
        """测试日志级别"""
        setup_logging(level="DEBUG", console=True)
        logger = get_logger("test_levels")
        
        logger.debug("Debug message")
        logger.info("Info message")
        logger.warning("Warning message")


class TestExceptions(unittest.TestCase):
    """测试异常处理"""
    
    def test_base_exception(self):
        """测试基础异常"""
        error = RandomAgentError("Test error")
        
        self.assertEqual(str(error), "[RA_000] Test error")
        self.assertEqual(error.error_code, "RA_000")
    
    def test_configuration_error(self):
        """测试配置错误"""
        error = ConfigurationError(
            config_key="test_key",
            expected_type="int",
            actual_value="string"
        )
        
        self.assertIn("test_key", str(error))
        self.assertEqual(error.error_code, "RA_001")
    
    def test_handle_errors_decorator(self):
        """测试错误处理装饰器"""
        @handle_errors(default_return="default", reraise=False)
        def risky_function():
            raise ValueError("Test error")
        
        result = risky_function()
        self.assertEqual(result, "default")
    
    def test_handle_errors_success(self):
        """测试错误处理装饰器（成功情况）"""
        @handle_errors(default_return=None, reraise=False)
        def normal_function():
            return "success"
        
        result = normal_function()
        self.assertEqual(result, "success")


class TestCache(unittest.TestCase):
    """测试缓存机制"""
    
    def test_lru_cache_basic(self):
        """测试 LRU 缓存基本功能"""
        cache = LRUCache(max_size=3)
        
        cache.set("key1", "value1")
        cache.set("key2", "value2")
        cache.set("key3", "value3")
        
        self.assertEqual(cache.get("key1"), "value1")
        self.assertEqual(cache.get("key2"), "value2")
    
    def test_lru_cache_eviction(self):
        """测试 LRU 缓存淘汰"""
        cache = LRUCache(max_size=2)
        
        cache.set("key1", "value1")
        cache.set("key2", "value2")
        cache.set("key3", "value3")  # 应该淘汰 key1
        
        self.assertIsNone(cache.get("key1"))
        self.assertEqual(cache.get("key2"), "value2")
        self.assertEqual(cache.get("key3"), "value3")
    
    def test_lru_cache_ttl(self):
        """测试 LRU 缓存 TTL"""
        cache = LRUCache(max_size=10, ttl=1)
        
        cache.set("key1", "value1")
        
        self.assertEqual(cache.get("key1"), "value1")
        
        import time
        time.sleep(1.1)
        
        self.assertIsNone(cache.get("key1"))
    
    def test_lru_cache_stats(self):
        """测试缓存统计"""
        cache = LRUCache(max_size=10)
        
        cache.set("key1", "value1")
        cache.get("key1")  # hit
        cache.get("key2")  # miss
        
        stats = cache.get_stats()
        
        self.assertEqual(stats["hits"], 1)
        self.assertEqual(stats["misses"], 1)
        self.assertEqual(stats["hit_rate"], 0.5)
    
    def test_prompt_cache(self):
        """测试提示词缓存"""
        cache = PromptCache()
        
        cache.set_prompt(
            task="test task",
            randomness=0.5,
            mode="balanced",
            style="detailed",
            prompt="Test prompt"
        )
        
        cached = cache.get_prompt(
            task="test task",
            randomness=0.5,
            mode="balanced",
            style="detailed"
        )
        
        self.assertEqual(cached, "Test prompt")
    
    def test_cached_decorator(self):
        """测试缓存装饰器"""
        call_count = [0]
        
        @cached(max_size=10)
        def expensive_function(n):
            call_count[0] += 1
            return n * 2
        
        result1 = expensive_function(5)
        result2 = expensive_function(5)
        
        self.assertEqual(result1, 10)
        self.assertEqual(result2, 10)
        self.assertEqual(call_count[0], 1)  # 只调用一次


class TestStorage(unittest.TestCase):
    """测试持久化存储"""
    
    def test_json_storage(self):
        """测试 JSON 存储"""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage = JSONStorage(tmpdir)
            
            data = {"key": "value", "number": 123}
            storage.save("test", data)
            
            loaded = storage.load("test")
            
            self.assertEqual(loaded, data)
    
    def test_json_storage_delete(self):
        """测试 JSON 存储删除"""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage = JSONStorage(tmpdir)
            
            storage.save("test", {"data": "test"})
            self.assertTrue(storage.delete("test"))
            self.assertIsNone(storage.load("test"))
    
    def test_sqlite_storage_session(self):
        """测试 SQLite 会话存储"""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = os.path.join(tmpdir, "test.db")
            storage = SQLiteStorage(db_path)
            
            session = Session(
                session_id="test-session",
                created_at=1000.0,
                updated_at=1000.0,
                agent_state={"randomness": 0.5},
                memory_data=[],
                thinking_history=[],
                metadata={}
            )
            
            self.assertTrue(storage.save_session(session))
            
            loaded = storage.load_session("test-session")
            
            self.assertIsNotNone(loaded)
            self.assertEqual(loaded.session_id, "test-session")
            self.assertEqual(loaded.agent_state["randomness"], 0.5)
            
            del storage
    
    def test_session_manager(self):
        """测试会话管理器"""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = os.path.join(tmpdir, "test.db")
            storage = SQLiteStorage(db_path)
            manager = SessionManager(storage)
            
            session = manager.create_session(
                metadata={"user": "test"}
            )
            
            self.assertIsNotNone(session.session_id)
            
            manager.update_agent_state({"state": "active"})
            
            current = manager.get_current_session()
            self.assertEqual(current.agent_state["state"], "active")
            
            del manager
            del storage


if __name__ == "__main__":
    unittest.main(verbosity=2)
