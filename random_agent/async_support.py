"""
异步支持系统 (Async Support)

提供异步操作支持：
- 异步 AI 调用
- 异步存储操作
- 异步缓存操作
- 并发控制
"""

import asyncio
import time
from typing import Any, Optional, Dict, List, Callable, TypeVar, Coroutine
from functools import wraps
from concurrent.futures import ThreadPoolExecutor
import threading


T = TypeVar('T')


class AsyncManager:
    """
    异步管理器
    
    管理异步操作和并发控制
    """
    
    _instance: Optional["AsyncManager"] = None
    _lock = threading.Lock()
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(
        self,
        max_workers: int = 10,
        max_concurrent_tasks: int = 100
    ):
        if hasattr(self, '_initialized') and self._initialized:
            return
        
        self.max_workers = max_workers
        self.max_concurrent_tasks = max_concurrent_tasks
        self._executor = ThreadPoolExecutor(max_workers=max_workers)
        self._semaphore = asyncio.Semaphore(max_concurrent_tasks)
        self._loop: Optional[asyncio.AbstractEventLoop] = None
        self._initialized = True
    
    def get_event_loop(self) -> asyncio.AbstractEventLoop:
        """获取或创建事件循环"""
        try:
            loop = asyncio.get_event_loop()
            if loop.is_closed():
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            return loop
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return loop
    
    async def run_in_executor(
        self,
        func: Callable[..., T],
        *args,
        **kwargs
    ) -> T:
        """
        在线程池中运行同步函数
        
        Args:
            func: 同步函数
            *args: 位置参数
            **kwargs: 关键字参数
        
        Returns:
            函数结果
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            self._executor,
            lambda: func(*args, **kwargs)
        )
    
    async def with_semaphore(self, coro: Coroutine[Any, Any, T]) -> T:
        """
        使用信号量控制并发
        
        Args:
            coro: 协程
        
        Returns:
            协程结果
        """
        async with self._semaphore:
            return await coro
    
    async def gather_with_concurrency(
        self,
        *coros: Coroutine[Any, Any, T],
        return_exceptions: bool = False
    ) -> List[T]:
        """
        并发执行多个协程（带并发控制）
        
        Args:
            *coros: 协程列表
            return_exceptions: 是否返回异常
        
        Returns:
            结果列表
        """
        async def run_with_semaphore(coro):
            async with self._semaphore:
                return await coro
        
        return await asyncio.gather(
            *[run_with_semaphore(coro) for coro in coros],
            return_exceptions=return_exceptions
        )
    
    def shutdown(self):
        """关闭异步管理器"""
        self._executor.shutdown(wait=True)
        if self._loop and not self._loop.is_closed():
            self._loop.close()


def async_retry(
    max_retries: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: tuple = (Exception,)
):
    """
    异步重试装饰器
    
    Args:
        max_retries: 最大重试次数
        delay: 初始延迟（秒）
        backoff: 延迟增长因子
        exceptions: 需要重试的异常类型
    
    Returns:
        装饰器
    """
    def decorator(func: Callable[..., Coroutine[Any, Any, T]]) -> Callable[..., Coroutine[Any, Any, T]]:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> T:
            current_delay = delay
            last_exception = None
            
            for attempt in range(max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_retries:
                        await asyncio.sleep(current_delay)
                        current_delay *= backoff
            
            raise last_exception
        
        return wrapper
    return decorator


def async_timeout(seconds: float):
    """
    异步超时装饰器
    
    Args:
        seconds: 超时时间（秒）
    
    Returns:
        装饰器
    """
    def decorator(func: Callable[..., Coroutine[Any, Any, T]]) -> Callable[..., Coroutine[Any, Any, T]]:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> T:
            return await asyncio.wait_for(
                func(*args, **kwargs),
                timeout=seconds
            )
        
        return wrapper
    return decorator


def sync_to_async(func: Callable[..., T]) -> Callable[..., Coroutine[Any, Any, T]]:
    """
    将同步函数转换为异步函数
    
    Args:
        func: 同步函数
    
    Returns:
        异步函数
    """
    @wraps(func)
    async def wrapper(*args, **kwargs) -> T:
        manager = AsyncManager()
        return await manager.run_in_executor(func, *args, **kwargs)
    
    return wrapper


def async_to_sync(func: Callable[..., Coroutine[Any, Any, T]]) -> Callable[..., T]:
    """
    将异步函数转换为同步函数
    
    Args:
        func: 异步函数
    
    Returns:
        同步函数
    """
    @wraps(func)
    def wrapper(*args, **kwargs) -> T:
        loop = AsyncManager().get_event_loop()
        return loop.run_until_complete(func(*args, **kwargs))
    
    return wrapper


class AsyncCache:
    """异步缓存"""
    
    def __init__(self, max_size: int = 1000, ttl: Optional[int] = None):
        self.max_size = max_size
        self.ttl = ttl
        self._cache: Dict[str, Any] = {}
        self._timestamps: Dict[str, float] = {}
        self._lock = asyncio.Lock()
    
    async def get(self, key: str) -> Optional[Any]:
        """获取缓存"""
        async with self._lock:
            if key not in self._cache:
                return None
            
            if self.ttl:
                if time.time() - self._timestamps[key] > self.ttl:
                    del self._cache[key]
                    del self._timestamps[key]
                    return None
            
            return self._cache[key]
    
    async def set(self, key: str, value: Any):
        """设置缓存"""
        async with self._lock:
            if len(self._cache) >= self.max_size:
                oldest_key = min(self._timestamps, key=self._timestamps.get)
                del self._cache[oldest_key]
                del self._timestamps[oldest_key]
            
            self._cache[key] = value
            self._timestamps[key] = time.time()
    
    async def delete(self, key: str):
        """删除缓存"""
        async with self._lock:
            if key in self._cache:
                del self._cache[key]
                del self._timestamps[key]
    
    async def clear(self):
        """清空缓存"""
        async with self._lock:
            self._cache.clear()
            self._timestamps.clear()


class AsyncTaskQueue:
    """异步任务队列"""
    
    def __init__(self, max_concurrent: int = 10):
        self.max_concurrent = max_concurrent
        self._queue: asyncio.Queue = asyncio.Queue()
        self._semaphore = asyncio.Semaphore(max_concurrent)
        self._running = False
        self._workers: List[asyncio.Task] = []
    
    async def add_task(
        self,
        coro: Coroutine[Any, Any, T],
        callback: Optional[Callable[[T], None]] = None
    ):
        """添加任务"""
        await self._queue.put((coro, callback))
    
    async def _worker(self):
        """工作协程"""
        while self._running:
            try:
                coro, callback = await asyncio.wait_for(
                    self._queue.get(),
                    timeout=1.0
                )
                
                async with self._semaphore:
                    try:
                        result = await coro
                        if callback:
                            callback(result)
                    except Exception as e:
                        print(f"任务执行失败: {e}")
                
                self._queue.task_done()
            except asyncio.TimeoutError:
                continue
    
    async def start(self, num_workers: int = 3):
        """启动任务队列"""
        self._running = True
        self._workers = [
            asyncio.create_task(self._worker())
            for _ in range(num_workers)
        ]
    
    async def stop(self):
        """停止任务队列"""
        self._running = False
        await asyncio.gather(*self._workers, return_exceptions=True)
        self._workers.clear()
    
    async def wait_completion(self):
        """等待所有任务完成"""
        await self._queue.join()


_global_async_manager: Optional[AsyncManager] = None


def get_async_manager() -> AsyncManager:
    """获取全局异步管理器"""
    global _global_async_manager
    if _global_async_manager is None:
        _global_async_manager = AsyncManager()
    return _global_async_manager
