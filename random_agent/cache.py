"""
缓存机制 (Caching System)

提供智能缓存功能：
- LRU 缓存
- TTL 过期
- 缓存统计
- 缓存预热
"""

import time
import hashlib
import json
from typing import Any, Optional, Dict, List, Callable
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import OrderedDict


@dataclass
class CacheEntry:
    """缓存条目"""
    key: str
    value: Any
    created_at: float = field(default_factory=time.time)
    expires_at: Optional[float] = None
    access_count: int = 0
    size: int = 0
    
    def is_expired(self) -> bool:
        """检查是否过期"""
        if self.expires_at is None:
            return False
        return time.time() > self.expires_at
    
    def access(self):
        """访问计数"""
        self.access_count += 1


class LRUCache:
    """
    LRU (Least Recently Used) 缓存
    
    自动淘汰最久未使用的条目
    """
    
    def __init__(self, max_size: int = 1000, ttl: Optional[int] = None):
        """
        Args:
            max_size: 最大缓存条目数
            ttl: 生存时间（秒），None 表示永不过期
        """
        self.max_size = max_size
        self.ttl = ttl
        self._cache: OrderedDict[str, CacheEntry] = OrderedDict()
        self._stats = {
            "hits": 0,
            "misses": 0,
            "evictions": 0,
            "size": 0
        }
    
    def get(self, key: str) -> Optional[Any]:
        """获取缓存值"""
        if key not in self._cache:
            self._stats["misses"] += 1
            return None
        
        entry = self._cache[key]
        
        if entry.is_expired():
            self.delete(key)
            self._stats["misses"] += 1
            return None
        
        self._cache.move_to_end(key)
        entry.access()
        self._stats["hits"] += 1
        
        return entry.value
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        """设置缓存值"""
        if key in self._cache:
            self.delete(key)
        
        if len(self._cache) >= self.max_size:
            self._evict()
        
        expires_at = None
        if ttl is not None:
            expires_at = time.time() + ttl
        elif self.ttl is not None:
            expires_at = time.time() + self.ttl
        
        entry = CacheEntry(
            key=key,
            value=value,
            expires_at=expires_at,
            size=self._estimate_size(value)
        )
        
        self._cache[key] = entry
        self._stats["size"] = len(self._cache)
    
    def delete(self, key: str):
        """删除缓存"""
        if key in self._cache:
            del self._cache[key]
            self._stats["size"] = len(self._cache)
    
    def clear(self):
        """清空缓存"""
        self._cache.clear()
        self._stats["size"] = 0
    
    def _evict(self):
        """淘汰最久未使用的条目"""
        if self._cache:
            self._cache.popitem(last=False)
            self._stats["evictions"] += 1
    
    def _estimate_size(self, value: Any) -> int:
        """估算值的大小"""
        try:
            return len(json.dumps(value))
        except:
            return 1
    
    def get_stats(self) -> Dict[str, Any]:
        """获取缓存统计"""
        total_requests = self._stats["hits"] + self._stats["misses"]
        hit_rate = self._stats["hits"] / total_requests if total_requests > 0 else 0
        
        return {
            **self._stats,
            "hit_rate": hit_rate,
            "total_requests": total_requests
        }
    
    def cleanup_expired(self):
        """清理过期条目"""
        expired_keys = [
            key for key, entry in self._cache.items()
            if entry.is_expired()
        ]
        
        for key in expired_keys:
            self.delete(key)
        
        return len(expired_keys)


class PromptCache:
    """
    提示词缓存
    
    缓存生成的提示词，避免重复计算
    """
    
    def __init__(self, max_size: int = 500, ttl: int = 3600):
        """
        Args:
            max_size: 最大缓存数
            ttl: 缓存过期时间（秒）
        """
        self._cache = LRUCache(max_size=max_size, ttl=ttl)
    
    @staticmethod
    def _generate_key(
        task: str,
        randomness: float,
        mode: str,
        style: str,
        **kwargs
    ) -> str:
        """生成缓存键"""
        key_data = {
            "task": task,
            "randomness": randomness,
            "mode": mode,
            "style": style,
            **kwargs
        }
        
        key_str = json.dumps(key_data, sort_keys=True)
        return hashlib.md5(key_str.encode()).hexdigest()
    
    def get_prompt(
        self,
        task: str,
        randomness: float,
        mode: str,
        style: str,
        **kwargs
    ) -> Optional[str]:
        """获取缓存的提示词"""
        key = self._generate_key(task, randomness, mode, style, **kwargs)
        return self._cache.get(key)
    
    def set_prompt(
        self,
        task: str,
        randomness: float,
        mode: str,
        style: str,
        prompt: str,
        **kwargs
    ):
        """缓存提示词"""
        key = self._generate_key(task, randomness, mode, style, **kwargs)
        self._cache.set(key, prompt)
    
    def get_stats(self) -> Dict[str, Any]:
        """获取缓存统计"""
        return self._cache.get_stats()
    
    def clear(self):
        """清空缓存"""
        self._cache.clear()


class MemoryCache:
    """
    记忆缓存
    
    缓存频繁访问的记忆
    """
    
    def __init__(self, max_size: int = 200):
        self._cache = LRUCache(max_size=max_size, ttl=600)
    
    def get(self, memory_id: str) -> Optional[Any]:
        """获取记忆"""
        return self._cache.get(memory_id)
    
    def set(self, memory_id: str, content: Any):
        """缓存记忆"""
        self._cache.set(memory_id, content)
    
    def invalidate(self, memory_id: str):
        """使缓存失效"""
        self._cache.delete(memory_id)


def cached(
    max_size: int = 128,
    ttl: Optional[int] = None
):
    """
    缓存装饰器
    
    Args:
        max_size: 最大缓存数
        ttl: 过期时间（秒）
    
    Example:
        @cached(max_size=100, ttl=60)
        def expensive_computation(n):
            return n ** 2
    """
    cache = LRUCache(max_size=max_size, ttl=ttl)
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = hashlib.md5(
                json.dumps({
                    "args": args,
                    "kwargs": kwargs
                }, sort_keys=True).encode()
            ).hexdigest()
            
            cached_result = cache.get(key)
            if cached_result is not None:
                return cached_result
            
            result = func(*args, **kwargs)
            cache.set(key, result)
            
            return result
        
        wrapper.cache = cache
        wrapper.cache_clear = cache.clear
        wrapper.cache_stats = cache.get_stats
        
        return wrapper
    
    return decorator


_global_prompt_cache: Optional[PromptCache] = None
_global_memory_cache: Optional[MemoryCache] = None


def get_prompt_cache() -> PromptCache:
    """获取全局提示词缓存"""
    global _global_prompt_cache
    if _global_prompt_cache is None:
        _global_prompt_cache = PromptCache()
    return _global_prompt_cache


def get_memory_cache() -> MemoryCache:
    """获取全局记忆缓存"""
    global _global_memory_cache
    if _global_memory_cache is None:
        _global_memory_cache = MemoryCache()
    return _global_memory_cache
