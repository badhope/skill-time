"""
日志系统 (Logging System)

提供统一的日志管理：
- 结构化日志
- 多级别日志
- 文件和控制台输出
- 性能追踪
"""

import logging
import sys
import time
from typing import Optional, Dict, Any, List
from pathlib import Path
from datetime import datetime
from functools import wraps
import json


class StructuredFormatter(logging.Formatter):
    """结构化日志格式化器"""
    
    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        
        if hasattr(record, "extra_data"):
            log_data["extra"] = record.extra_data
        
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        return json.dumps(log_data, ensure_ascii=False)


class ColoredFormatter(logging.Formatter):
    """彩色日志格式化器"""
    
    COLORS = {
        "DEBUG": "\033[36m",     # Cyan
        "INFO": "\033[32m",      # Green
        "WARNING": "\033[33m",   # Yellow
        "ERROR": "\033[31m",     # Red
        "CRITICAL": "\033[35m",  # Magenta
    }
    RESET = "\033[0m"
    
    def format(self, record: logging.LogRecord) -> str:
        color = self.COLORS.get(record.levelname, self.RESET)
        record.levelname = f"{color}{record.levelname}{self.RESET}"
        return super().format(record)


class RandomAgentLogger:
    """
    RandomAgent 日志管理器
    
    特点：
    - 统一的日志接口
    - 支持结构化日志
    - 支持彩色输出
    - 性能追踪
    """
    
    _instance: Optional["RandomAgentLogger"] = None
    _loggers: Dict[str, logging.Logger] = {}
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(
        self,
        level: str = "INFO",
        log_file: Optional[str] = None,
        console: bool = True,
        structured: bool = False
    ):
        if hasattr(self, "_initialized") and self._initialized:
            return
        
        self._level = getattr(logging, level.upper(), logging.INFO)
        self._log_file = log_file
        self._console = console
        self._structured = structured
        self._initialized = True
        
        self._performance_data: Dict[str, List[float]] = {}
    
    def get_logger(self, name: str = "random_agent") -> logging.Logger:
        """获取或创建 logger"""
        if name in self._loggers:
            return self._loggers[name]
        
        logger = logging.getLogger(name)
        logger.setLevel(self._level)
        logger.handlers.clear()
        
        if self._console:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(self._level)
            
            if self._structured:
                console_handler.setFormatter(StructuredFormatter())
            else:
                console_handler.setFormatter(
                    ColoredFormatter(
                        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S"
                    )
                )
            
            logger.addHandler(console_handler)
        
        if self._log_file:
            log_path = Path(self._log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            
            file_handler = logging.FileHandler(self._log_file, encoding="utf-8")
            file_handler.setLevel(self._level)
            
            if self._structured:
                file_handler.setFormatter(StructuredFormatter())
            else:
                file_handler.setFormatter(
                    logging.Formatter(
                        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S"
                    )
                )
            
            logger.addHandler(file_handler)
        
        self._loggers[name] = logger
        return logger
    
    def log_with_extra(
        self,
        logger: logging.Logger,
        level: int,
        message: str,
        **extra
    ):
        """记录带额外数据的日志"""
        record = logger.makeRecord(
            logger.name,
            level,
            "",
            0,
            message,
            (),
            None
        )
        record.extra_data = extra
        logger.handle(record)
    
    def performance_start(self, operation: str) -> float:
        """开始性能追踪"""
        start_time = time.time()
        return start_time
    
    def performance_end(
        self,
        operation: str,
        start_time: float,
        logger: Optional[logging.Logger] = None
    ):
        """结束性能追踪"""
        elapsed = time.time() - start_time
        
        if operation not in self._performance_data:
            self._performance_data[operation] = []
        
        self._performance_data[operation].append(elapsed)
        
        if logger:
            logger.debug(f"性能追踪: {operation} 耗时 {elapsed:.4f}s")
        
        return elapsed
    
    def get_performance_stats(self, operation: Optional[str] = None) -> Dict[str, Any]:
        """获取性能统计"""
        if operation:
            if operation not in self._performance_data:
                return {}
            
            times = self._performance_data[operation]
            return {
                "operation": operation,
                "count": len(times),
                "total": sum(times),
                "average": sum(times) / len(times) if times else 0,
                "min": min(times) if times else 0,
                "max": max(times) if times else 0
            }
        
        return {
            op: self.get_performance_stats(op)
            for op in self._performance_data.keys()
        }


def track_performance(operation: Optional[str] = None):
    """
    性能追踪装饰器
    
    Args:
        operation: 操作名称（默认使用函数名）
    
    Example:
        @track_performance("思考过程")
        def think(self, question):
            ...
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            op_name = operation or func.__name__
            logger_manager = RandomAgentLogger()
            logger = logger_manager.get_logger()
            
            start_time = logger_manager.performance_start(op_name)
            
            try:
                result = func(*args, **kwargs)
                elapsed = logger_manager.performance_end(op_name, start_time, logger)
                return result
            except Exception as e:
                elapsed = logger_manager.performance_end(op_name, start_time, logger)
                logger.error(f"{op_name} 执行失败: {e} (耗时 {elapsed:.4f}s)")
                raise
        
        return wrapper
    return decorator


def setup_logging(
    level: str = "INFO",
    log_file: Optional[str] = None,
    console: bool = True,
    structured: bool = False
) -> RandomAgentLogger:
    """
    设置日志系统
    
    Args:
        level: 日志级别
        log_file: 日志文件路径
        console: 是否输出到控制台
        structured: 是否使用结构化日志
    
    Returns:
        日志管理器实例
    """
    return RandomAgentLogger(
        level=level,
        log_file=log_file,
        console=console,
        structured=structured
    )


def get_logger(name: str = "random_agent") -> logging.Logger:
    """
    获取 logger 的便捷函数
    
    Args:
        name: logger 名称
    
    Returns:
        Logger 实例
    """
    manager = RandomAgentLogger()
    return manager.get_logger(name)
