"""
配置管理系统 (Configuration Management)

提供统一的配置管理：
- 配置文件支持 (YAML/JSON)
- 环境变量支持
- 默认配置
- 配置验证
"""

import os
import json
from typing import Any, Dict, Optional, List
from dataclasses import dataclass, field, asdict
from pathlib import Path


@dataclass
class RandomnessConfig:
    """随机性配置"""
    seed: Optional[int] = None
    base_level: float = 0.5
    quantum_enabled: bool = True
    neural_noise_enabled: bool = True
    creative_enabled: bool = True
    
    noise_config: Dict[str, float] = field(default_factory=lambda: {
        "base_level": 0.1,
        "signal_to_noise_ratio": 0.8,
        "fluctuation_amplitude": 0.2,
        "spontaneous_rate": 0.05
    })


@dataclass
class MemoryConfig:
    """记忆配置"""
    working_memory_capacity: int = 7
    long_term_memory_limit: int = 10000
    decay_rate: float = 0.1
    consolidation_threshold: float = 0.7
    retrieval_limit: int = 10


@dataclass
class ConsciousnessConfig:
    """意识配置"""
    enable_layers: bool = True
    enable_stream: bool = True
    enable_dmn: bool = True
    dmn_activation_threshold: float = 0.3
    stream_flow_rate: float = 0.5


@dataclass
class PersonalityConfig:
    """性格配置"""
    openness: float = 0.6
    conscientiousness: float = 0.5
    extraversion: float = 0.5
    agreeableness: float = 0.5
    neuroticism: float = 0.4
    
    def to_dict(self) -> Dict[str, float]:
        return asdict(self)


@dataclass
class AIProviderConfig:
    """AI 提供商配置"""
    provider: str = "openai"
    model: str = "gpt-4"
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 2000
    timeout: int = 30


@dataclass
class LoggingConfig:
    """日志配置"""
    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file: Optional[str] = None
    console: bool = True


@dataclass
class RandomAgentConfig:
    """RandomAgent 主配置"""
    
    randomness: RandomnessConfig = field(default_factory=RandomnessConfig)
    memory: MemoryConfig = field(default_factory=MemoryConfig)
    consciousness: ConsciousnessConfig = field(default_factory=ConsciousnessConfig)
    personality: PersonalityConfig = field(default_factory=PersonalityConfig)
    ai_provider: AIProviderConfig = field(default_factory=AIProviderConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    
    version: str = "0.1.0"
    debug: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "randomness": asdict(self.randomness),
            "memory": asdict(self.memory),
            "consciousness": asdict(self.consciousness),
            "personality": asdict(self.personality),
            "ai_provider": asdict(self.ai_provider),
            "logging": asdict(self.logging),
            "version": self.version,
            "debug": self.debug
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RandomAgentConfig":
        """从字典创建"""
        return cls(
            randomness=RandomnessConfig(**data.get("randomness", {})),
            memory=MemoryConfig(**data.get("memory", {})),
            consciousness=ConsciousnessConfig(**data.get("consciousness", {})),
            personality=PersonalityConfig(**data.get("personality", {})),
            ai_provider=AIProviderConfig(**data.get("ai_provider", {})),
            logging=LoggingConfig(**data.get("logging", {})),
            version=data.get("version", "0.1.0"),
            debug=data.get("debug", False)
        )


class ConfigManager:
    """
    配置管理器
    
    支持多种配置来源（优先级从高到低）：
    1. 代码中直接设置
    2. 环境变量
    3. 配置文件
    4. 默认配置
    """
    
    ENV_PREFIX = "RANDOM_AGENT_"
    
    def __init__(self, config: Optional[RandomAgentConfig] = None):
        self._config = config or RandomAgentConfig()
        self._config_file: Optional[Path] = None
    
    def load_from_file(self, filepath: str) -> "ConfigManager":
        """
        从文件加载配置
        
        Args:
            filepath: 配置文件路径 (JSON/YAML)
        
        Returns:
            self (支持链式调用)
        """
        path = Path(filepath)
        
        if not path.exists():
            raise FileNotFoundError(f"配置文件不存在: {filepath}")
        
        self._config_file = path
        
        with open(path, "r", encoding="utf-8") as f:
            if path.suffix in [".yaml", ".yml"]:
                try:
                    import yaml
                    data = yaml.safe_load(f)
                except ImportError:
                    raise ImportError("需要安装 PyYAML: pip install pyyaml")
            else:
                data = json.load(f)
        
        self._config = RandomAgentConfig.from_dict(data)
        
        return self
    
    def load_from_env(self) -> "ConfigManager":
        """
        从环境变量加载配置
        
        Returns:
            self (支持链式调用)
        """
        env_mappings = {
            f"{self.ENV_PREFIX}SEED": ("randomness", "seed", int),
            f"{self.ENV_PREFIX}BASE_LEVEL": ("randomness", "base_level", float),
            f"{self.ENV_PREFIX}WORKING_MEMORY_CAPACITY": ("memory", "working_memory_capacity", int),
            f"{self.ENV_PREFIX}PROVIDER": ("ai_provider", "provider", str),
            f"{self.ENV_PREFIX}MODEL": ("ai_provider", "model", str),
            f"{self.ENV_PREFIX}API_KEY": ("ai_provider", "api_key", str),
            f"{self.ENV_PREFIX}BASE_URL": ("ai_provider", "base_url", str),
            f"{self.ENV_PREFIX}DEBUG": (None, "debug", lambda x: x.lower() == "true"),
            f"{self.ENV_PREFIX}LOG_LEVEL": ("logging", "level", str),
        }
        
        for env_key, (section, attr, converter) in env_mappings.items():
            value = os.getenv(env_key)
            if value is not None:
                try:
                    converted = converter(value)
                    if section:
                        section_obj = getattr(self._config, section)
                        setattr(section_obj, attr, converted)
                    else:
                        setattr(self._config, attr, converted)
                except (ValueError, TypeError) as e:
                    pass
        
        return self
    
    def save_to_file(self, filepath: str, format: str = "json"):
        """
        保存配置到文件
        
        Args:
            filepath: 文件路径
            format: 格式 (json/yaml)
        """
        path = Path(filepath)
        data = self._config.to_dict()
        
        with open(path, "w", encoding="utf-8") as f:
            if format == "yaml":
                try:
                    import yaml
                    yaml.dump(data, f, allow_unicode=True, default_flow_style=False)
                except ImportError:
                    raise ImportError("需要安装 PyYAML: pip install pyyaml")
            else:
                json.dump(data, f, indent=2, ensure_ascii=False)
    
    def get(self) -> RandomAgentConfig:
        """获取配置对象"""
        return self._config
    
    def update(self, **kwargs) -> "ConfigManager":
        """
        更新配置
        
        Args:
            **kwargs: 配置项
        
        Returns:
            self (支持链式调用)
        """
        for key, value in kwargs.items():
            if hasattr(self._config, key):
                setattr(self._config, key, value)
        
        return self
    
    def validate(self) -> List[str]:
        """
        验证配置
        
        Returns:
            错误消息列表（空列表表示验证通过）
        """
        errors = []
        
        if not 0 <= self._config.randomness.base_level <= 1:
            errors.append("randomness.base_level 必须在 0-1 之间")
        
        if self._config.memory.working_memory_capacity < 1:
            errors.append("memory.working_memory_capacity 必须大于 0")
        
        for trait, value in asdict(self._config.personality).items():
            if not 0 <= value <= 1:
                errors.append(f"personality.{trait} 必须在 0-1 之间")
        
        return errors
    
    def __getattr__(self, name: str) -> Any:
        """代理访问配置属性"""
        return getattr(self._config, name)


def load_config(
    config_file: Optional[str] = None,
    load_env: bool = True
) -> RandomAgentConfig:
    """
    加载配置的便捷函数
    
    Args:
        config_file: 配置文件路径
        load_env: 是否加载环境变量
    
    Returns:
        配置对象
    """
    manager = ConfigManager()
    
    if config_file:
        manager.load_from_file(config_file)
    
    if load_env:
        manager.load_from_env()
    
    errors = manager.validate()
    if errors:
        raise ValueError(f"配置验证失败: {errors}")
    
    return manager.get()


DEFAULT_CONFIG = RandomAgentConfig()
