"""
异常处理体系 (Exception Handling)

提供统一的异常管理：
- 自定义异常类
- 错误代码
- 异常上下文
- 错误恢复建议
"""

from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field


@dataclass
class ErrorContext:
    """错误上下文"""
    operation: str
    details: Dict[str, Any] = field(default_factory=dict)
    suggestions: List[str] = field(default_factory=list)
    
    def add_suggestion(self, suggestion: str):
        """添加恢复建议"""
        self.suggestions.append(suggestion)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "operation": self.operation,
            "details": self.details,
            "suggestions": self.suggestions
        }


class RandomAgentError(Exception):
    """RandomAgent 基础异常"""
    
    error_code: str = "RA_000"
    error_message: str = "RandomAgent 发生错误"
    
    def __init__(
        self,
        message: Optional[str] = None,
        context: Optional[ErrorContext] = None,
        cause: Optional[Exception] = None
    ):
        self.message = message or self.error_message
        self.context = context
        self.cause = cause
        
        super().__init__(self.message)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        result = {
            "error_code": self.error_code,
            "error_type": self.__class__.__name__,
            "message": self.message
        }
        
        if self.context:
            result["context"] = self.context.to_dict()
        
        if self.cause:
            result["cause"] = str(self.cause)
        
        return result
    
    def __str__(self) -> str:
        parts = [f"[{self.error_code}] {self.message}"]
        
        if self.context:
            parts.append(f"操作: {self.context.operation}")
            if self.context.suggestions:
                parts.append("建议:")
                for i, suggestion in enumerate(self.context.suggestions, 1):
                    parts.append(f"  {i}. {suggestion}")
        
        return "\n".join(parts)


class ConfigurationError(RandomAgentError):
    """配置错误"""
    
    error_code = "RA_001"
    error_message = "配置错误"
    
    def __init__(
        self,
        message: Optional[str] = None,
        config_key: Optional[str] = None,
        expected_type: Optional[str] = None,
        actual_value: Optional[Any] = None
    ):
        context = ErrorContext(
            operation="配置加载",
            details={
                "config_key": config_key,
                "expected_type": expected_type,
                "actual_value": str(actual_value) if actual_value else None
            },
            suggestions=[
                "检查配置文件格式是否正确",
                "验证配置项的类型和取值范围",
                "参考文档中的配置说明"
            ]
        )
        
        super().__init__(message or f"配置项 '{config_key}' 错误", context)


class RandomnessError(RandomAgentError):
    """随机性引擎错误"""
    
    error_code = "RA_002"
    error_message = "随机性引擎错误"
    
    def __init__(
        self,
        message: Optional[str] = None,
        operation: Optional[str] = None,
        randomness_type: Optional[str] = None
    ):
        context = ErrorContext(
            operation=operation or "随机操作",
            details={"randomness_type": randomness_type},
            suggestions=[
                "检查随机性参数是否在有效范围内",
                "验证选项列表不为空",
                "检查权重配置是否正确"
            ]
        )
        
        super().__init__(message, context)


class MemoryError(RandomAgentError):
    """记忆系统错误"""
    
    error_code = "RA_003"
    error_message = "记忆系统错误"
    
    def __init__(
        self,
        message: Optional[str] = None,
        memory_type: Optional[str] = None,
        operation: Optional[str] = None
    ):
        context = ErrorContext(
            operation=operation or "记忆操作",
            details={"memory_type": memory_type},
            suggestions=[
                "检查记忆容量是否已满",
                "验证记忆类型是否正确",
                "清理过期的记忆项"
            ]
        )
        
        super().__init__(message, context)


class ConsciousnessError(RandomAgentError):
    """意识系统错误"""
    
    error_code = "RA_004"
    error_message = "意识系统错误"
    
    def __init__(
        self,
        message: Optional[str] = None,
        consciousness_level: Optional[str] = None,
        operation: Optional[str] = None
    ):
        context = ErrorContext(
            operation=operation or "意识处理",
            details={"consciousness_level": consciousness_level},
            suggestions=[
                "检查意识层次配置",
                "验证思维流状态",
                "重置意识系统"
            ]
        )
        
        super().__init__(message, context)


class AIProviderError(RandomAgentError):
    """AI 提供商错误"""
    
    error_code = "RA_005"
    error_message = "AI 提供商错误"
    
    def __init__(
        self,
        message: Optional[str] = None,
        provider: Optional[str] = None,
        model: Optional[str] = None,
        api_error: Optional[str] = None
    ):
        context = ErrorContext(
            operation="AI API 调用",
            details={
                "provider": provider,
                "model": model,
                "api_error": api_error
            },
            suggestions=[
                "检查 API Key 是否正确",
                "验证网络连接",
                "检查 API 配额和限制",
                "尝试使用其他模型或提供商"
            ]
        )
        
        super().__init__(message, context)


class PromptError(RandomAgentError):
    """提示词错误"""
    
    error_code = "RA_006"
    error_message = "提示词生成错误"
    
    def __init__(
        self,
        message: Optional[str] = None,
        task: Optional[str] = None,
        mode: Optional[str] = None
    ):
        context = ErrorContext(
            operation="提示词生成",
            details={
                "task": task,
                "mode": mode
            },
            suggestions=[
                "检查任务描述是否清晰",
                "验证思维模式是否有效",
                "使用默认参数重试"
            ]
        )
        
        super().__init__(message, context)


class ValidationError(RandomAgentError):
    """验证错误"""
    
    error_code = "RA_007"
    error_message = "输入验证错误"
    
    def __init__(
        self,
        message: Optional[str] = None,
        field: Optional[str] = None,
        value: Optional[Any] = None,
        constraints: Optional[Dict[str, Any]] = None
    ):
        context = ErrorContext(
            operation="输入验证",
            details={
                "field": field,
                "value": str(value) if value else None,
                "constraints": constraints
            },
            suggestions=[
                "检查输入值的类型和格式",
                "验证输入是否满足约束条件",
                "参考 API 文档中的参数说明"
            ]
        )
        
        super().__init__(message, context)


class StorageError(RandomAgentError):
    """存储错误"""
    
    error_code = "RA_008"
    error_message = "数据存储错误"
    
    def __init__(
        self,
        message: Optional[str] = None,
        operation: Optional[str] = None,
        filepath: Optional[str] = None
    ):
        context = ErrorContext(
            operation=operation or "存储操作",
            details={"filepath": filepath},
            suggestions=[
                "检查文件路径是否存在",
                "验证文件权限",
                "检查磁盘空间",
                "确保文件未被其他程序占用"
            ]
        )
        
        super().__init__(message, context)


class PerformanceError(RandomAgentError):
    """性能错误"""
    
    error_code = "RA_009"
    error_message = "性能问题"
    
    def __init__(
        self,
        message: Optional[str] = None,
        operation: Optional[str] = None,
        elapsed_time: Optional[float] = None,
        threshold: Optional[float] = None
    ):
        context = ErrorContext(
            operation=operation or "性能监控",
            details={
                "elapsed_time": elapsed_time,
                "threshold": threshold
            },
            suggestions=[
                "减少迭代次数",
                "优化算法复杂度",
                "使用缓存机制",
                "降低随机性水平"
            ]
        )
        
        super().__init__(message, context)


def handle_errors(
    default_return: Any = None,
    reraise: bool = False,
    log_error: bool = True
):
    """
    错误处理装饰器
    
    Args:
        default_return: 发生错误时的默认返回值
        reraise: 是否重新抛出异常
        log_error: 是否记录错误日志
    
    Example:
        @handle_errors(default_return=None, reraise=False)
        def risky_operation():
            ...
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except RandomAgentError as e:
                if log_error:
                    from random_agent.logger import get_logger
                    logger = get_logger()
                    logger.error(f"RandomAgent 错误: {e}")
                
                if reraise:
                    raise
                
                return default_return
            except Exception as e:
                if log_error:
                    from random_agent.logger import get_logger
                    logger = get_logger()
                    logger.error(f"未知错误: {e}")
                
                if reraise:
                    raise RandomAgentError(
                        message=f"操作失败: {str(e)}",
                        cause=e
                    )
                
                return default_return
        
        return wrapper
    return decorator


from functools import wraps
