"""
RandomAgent - 模拟人类直觉跳跃思维的智能体框架

核心理念：世界的底层是随机的，大脑的底层也是随机的

主要功能：
1. 提示词工程 - 生成可直接使用的系统提示词
2. AI 集成 - 调用真实的 AI 模型 (OpenAI/Claude/Ollama)
3. 思维模拟 - 模拟人类意识流和随机思维过程
"""

from random_agent.core.randomness_engine import RandomnessEngine
from random_agent.core.consciousness_layers import ConsciousnessLayers
from random_agent.core.consciousness_stream import ConsciousnessStream
from random_agent.core.dmn_engine import DMNEngine
from random_agent.core.memory_system import MemorySystem
from random_agent.core.goal_system import GoalSystem
from random_agent.core.influence_factors import InfluenceFactors
from random_agent.core.balance_controller import BalanceController
from random_agent.core.output_system import OutputSystem
from random_agent.agent import RandomAgent as Agent

from random_agent.prompt_templates import (
    RandomAgentPromptBuilder,
    PromptConfig,
    PromptStyle,
    ThinkingMode,
    create_prompt,
    get_system_prompt_only,
)

from random_agent.ai_integration import (
    AIAgent,
    AIConfig,
    AIProvider,
    AIProviderBase,
    create_ai_agent,
)

from random_agent.config import (
    RandomAgentConfig,
    ConfigManager,
    load_config,
    RandomnessConfig,
    MemoryConfig,
    ConsciousnessConfig,
    PersonalityConfig,
    AIProviderConfig,
    LoggingConfig,
)

from random_agent.logger import (
    RandomAgentLogger,
    setup_logging,
    get_logger,
    track_performance,
)

from random_agent.exceptions import (
    RandomAgentError,
    ConfigurationError,
    RandomnessError,
    MemoryError,
    ConsciousnessError,
    AIProviderError,
    PromptError,
    ValidationError,
    StorageError,
    PerformanceError,
    handle_errors,
)

from random_agent.cache import (
    LRUCache,
    PromptCache,
    MemoryCache,
    cached,
    get_prompt_cache,
    get_memory_cache,
)

from random_agent.storage import (
    JSONStorage,
    SQLiteStorage,
    SessionManager,
    Session,
    export_session,
    import_session,
)

__version__ = "0.1.1"
__all__ = [
    # Core modules
    "RandomnessEngine",
    "ConsciousnessLayers", 
    "ConsciousnessStream",
    "DMNEngine",
    "MemorySystem",
    "GoalSystem",
    "InfluenceFactors",
    "BalanceController",
    "OutputSystem",
    "Agent",
    # Prompt templates
    "RandomAgentPromptBuilder",
    "PromptConfig",
    "PromptStyle",
    "ThinkingMode",
    "create_prompt",
    "get_system_prompt_only",
    # AI Integration
    "AIAgent",
    "AIConfig",
    "AIProvider",
    "AIProviderBase",
    "create_ai_agent",
    # Configuration
    "RandomAgentConfig",
    "ConfigManager",
    "load_config",
    "RandomnessConfig",
    "MemoryConfig",
    "ConsciousnessConfig",
    "PersonalityConfig",
    "AIProviderConfig",
    "LoggingConfig",
    # Logging
    "RandomAgentLogger",
    "setup_logging",
    "get_logger",
    "track_performance",
    # Exceptions
    "RandomAgentError",
    "ConfigurationError",
    "RandomnessError",
    "MemoryError",
    "ConsciousnessError",
    "AIProviderError",
    "PromptError",
    "ValidationError",
    "StorageError",
    "PerformanceError",
    "handle_errors",
    # Cache
    "LRUCache",
    "PromptCache",
    "MemoryCache",
    "cached",
    "get_prompt_cache",
    "get_memory_cache",
    # Storage
    "JSONStorage",
    "SQLiteStorage",
    "SessionManager",
    "Session",
    "export_session",
    "import_session",
]
