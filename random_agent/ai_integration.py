"""
AI API 集成模块

支持调用真实的 AI 模型 API：
- OpenAI (GPT-4, GPT-3.5)
- Anthropic (Claude)
- 本地模型 (Ollama)
- 自定义 API

使用方式：
1. 设置 API Key
2. 创建 AI Agent
3. 调用 think() 方法
"""

import os
import json
import time
from typing import Optional, Dict, Any, List, Callable
from dataclasses import dataclass, field
from enum import Enum
from abc import ABC, abstractmethod


class AIProvider(Enum):
    """AI 提供商"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    OLLAMA = "ollama"
    CUSTOM = "custom"


@dataclass
class AIConfig:
    """AI 配置"""
    provider: AIProvider = AIProvider.OPENAI
    model: str = "gpt-4"
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 2000
    
    randomness_level: float = 0.5
    thinking_mode: str = "balanced"
    
    def __post_init__(self):
        if self.api_key is None:
            env_keys = {
                AIProvider.OPENAI: "OPENAI_API_KEY",
                AIProvider.ANTHROPIC: "ANTHROPIC_API_KEY",
            }
            env_key = env_keys.get(self.provider)
            if env_key:
                self.api_key = os.getenv(env_key)


class AIProviderBase(ABC):
    """AI 提供商基类"""
    
    def __init__(self, config: AIConfig):
        self.config = config
    
    @abstractmethod
    def call(self, system_prompt: str, user_message: str) -> str:
        """调用 AI API"""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """检查是否可用"""
        pass


class OpenAIProvider(AIProviderBase):
    """OpenAI 提供商"""
    
    def __init__(self, config: AIConfig):
        super().__init__(config)
        self._client = None
    
    def _get_client(self):
        if self._client is None:
            try:
                import openai
                self._client = openai.OpenAI(
                    api_key=self.config.api_key,
                    base_url=self.config.base_url
                )
            except ImportError:
                raise ImportError("请安装 openai: pip install openai")
        return self._client
    
    def call(self, system_prompt: str, user_message: str) -> str:
        client = self._get_client()
        
        response = client.chat.completions.create(
            model=self.config.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens
        )
        
        return response.choices[0].message.content
    
    def is_available(self) -> bool:
        return self.config.api_key is not None


class AnthropicProvider(AIProviderBase):
    """Anthropic (Claude) 提供商"""
    
    def __init__(self, config: AIConfig):
        super().__init__(config)
        self._client = None
    
    def _get_client(self):
        if self._client is None:
            try:
                import anthropic
                self._client = anthropic.Anthropic(api_key=self.config.api_key)
            except ImportError:
                raise ImportError("请安装 anthropic: pip install anthropic")
        return self._client
    
    def call(self, system_prompt: str, user_message: str) -> str:
        client = self._get_client()
        
        response = client.messages.create(
            model=self.config.model,
            max_tokens=self.config.max_tokens,
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_message}
            ]
        )
        
        return response.content[0].text
    
    def is_available(self) -> bool:
        return self.config.api_key is not None


class OllamaProvider(AIProviderBase):
    """Ollama 本地模型提供商"""
    
    def __init__(self, config: AIConfig):
        super().__init__(config)
        if config.base_url is None:
            config.base_url = "http://localhost:11434"
    
    def call(self, system_prompt: str, user_message: str) -> str:
        import urllib.request
        import urllib.error
        
        url = f"{self.config.base_url}/api/chat"
        
        data = {
            "model": self.config.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            "stream": False
        }
        
        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result['message']['content']
    
    def is_available(self) -> bool:
        try:
            import urllib.request
            req = urllib.request.Request(f"{self.config.base_url}/api/tags")
            with urllib.request.urlopen(req, timeout=2) as response:
                return response.status == 200
        except:
            return False


class CustomProvider(AIProviderBase):
    """自定义 API 提供商"""
    
    def __init__(
        self, 
        config: AIConfig,
        call_fn: Optional[Callable[[str, str], str]] = None
    ):
        super().__init__(config)
        self._call_fn = call_fn
    
    def set_call_function(self, fn: Callable[[str, str], str]):
        """设置调用函数"""
        self._call_fn = fn
    
    def call(self, system_prompt: str, user_message: str) -> str:
        if self._call_fn is None:
            raise ValueError("请通过 set_call_function 设置调用函数")
        return self._call_fn(system_prompt, user_message)
    
    def is_available(self) -> bool:
        return self._call_fn is not None


class AIProviderFactory:
    """AI 提供商工厂"""
    
    @staticmethod
    def create(config: AIConfig, call_fn: Optional[Callable] = None) -> AIProviderBase:
        providers = {
            AIProvider.OPENAI: OpenAIProvider,
            AIProvider.ANTHROPIC: AnthropicProvider,
            AIProvider.OLLAMA: OllamaProvider,
            AIProvider.CUSTOM: CustomProvider,
        }
        
        provider_class = providers.get(config.provider)
        if provider_class is None:
            raise ValueError(f"不支持的提供商: {config.provider}")
        
        if config.provider == AIProvider.CUSTOM:
            return provider_class(config, call_fn)
        
        return provider_class(config)


class AIAgent:
    """
    AI Agent - 集成真实 AI 模型
    
    结合 RandomAgent 的提示词工程和真实 AI 模型
    
    Example:
        >>> from random_agent.ai_integration import AIAgent, AIConfig, AIProvider
        >>> 
        >>> # 使用 OpenAI
        >>> config = AIConfig(
        ...     provider=AIProvider.OPENAI,
        ...     model="gpt-4",
        ...     api_key="your-api-key",
        ...     randomness_level=0.7
        ... )
        >>> agent = AIAgent(config)
        >>> result = agent.think("什么是创造力？")
        >>> print(result["answer"])
        >>> 
        >>> # 使用 Claude
        >>> config = AIConfig(
        ...     provider=AIProvider.ANTHROPIC,
        ...     model="claude-3-opus-20240229",
        ...     api_key="your-api-key"
        ... )
        >>> agent = AIAgent(config)
        >>> result = agent.think("什么是创造力？")
    """
    
    def __init__(self, config: AIConfig, custom_call_fn: Optional[Callable] = None):
        self.config = config
        self.provider = AIProviderFactory.create(config, custom_call_fn)
        
        from random_agent.prompt_templates import RandomAgentPromptBuilder, PromptConfig, ThinkingMode
        
        mode_map = {
            "divergent": ThinkingMode.DIVERGENT,
            "convergent": ThinkingMode.CONVERGENT,
            "balanced": ThinkingMode.BALANCED,
            "creative": ThinkingMode.CREATIVE,
            "analytical": ThinkingMode.ANALYTICAL,
        }
        
        prompt_config = PromptConfig(
            randomness_level=config.randomness_level,
            thinking_mode=mode_map.get(config.thinking_mode, ThinkingMode.BALANCED),
        )
        
        self.prompt_builder = RandomAgentPromptBuilder(prompt_config)
        
        self._conversation_history: List[Dict[str, str]] = []
    
    def think(
        self, 
        question: str, 
        context: Optional[Dict[str, Any]] = None,
        show_thinking: bool = True
    ) -> Dict[str, Any]:
        """
        思考问题
        
        Args:
            question: 问题
            context: 额外上下文
            show_thinking: 是否在提示词中要求展示思考过程
        
        Returns:
            思考结果
        """
        system_prompt = self.prompt_builder.build_system_prompt()
        
        user_message = self.prompt_builder.build_task_prompt(question, context)
        
        start_time = time.time()
        
        try:
            response = self.provider.call(system_prompt, user_message)
            success = True
            error = None
        except Exception as e:
            response = f"调用 AI API 失败: {str(e)}"
            success = False
            error = str(e)
        
        elapsed_time = time.time() - start_time
        
        self._conversation_history.append({
            "question": question,
            "response": response,
            "success": success,
            "elapsed_time": elapsed_time
        })
        
        return {
            "answer": response,
            "question": question,
            "success": success,
            "error": error,
            "elapsed_time": elapsed_time,
            "config": {
                "provider": self.config.provider.value,
                "model": self.config.model,
                "randomness_level": self.config.randomness_level,
                "thinking_mode": self.config.thinking_mode
            }
        }
    
    def chat(
        self, 
        message: str,
        maintain_context: bool = True
    ) -> str:
        """
        多轮对话
        
        Args:
            message: 用户消息
            maintain_context: 是否保持上下文
        
        Returns:
            AI 回复
        """
        system_prompt = self.prompt_builder.build_system_prompt()
        
        if maintain_context and self._conversation_history:
            context = "\n\n".join([
                f"用户: {h['question']}\n助手: {h['response']}"
                for h in self._conversation_history[-5:]
            ])
            message = f"之前的对话:\n{context}\n\n当前问题: {message}"
        
        try:
            response = self.provider.call(system_prompt, message)
            self._conversation_history.append({
                "question": message,
                "response": response,
                "success": True,
                "elapsed_time": 0
            })
            return response
        except Exception as e:
            return f"对话失败: {str(e)}"
    
    def set_randomness(self, level: float):
        """设置随机性水平"""
        self.config.randomness_level = level
        self.prompt_builder.config.randomness_level = level
    
    def set_thinking_mode(self, mode: str):
        """设置思维模式"""
        self.config.thinking_mode = mode
        from random_agent.prompt_templates import ThinkingMode
        mode_map = {
            "divergent": ThinkingMode.DIVERGENT,
            "convergent": ThinkingMode.CONVERGENT,
            "balanced": ThinkingMode.BALANCED,
            "creative": ThinkingMode.CREATIVE,
            "analytical": ThinkingMode.ANALYTICAL,
        }
        self.prompt_builder.config.thinking_mode = mode_map.get(mode, ThinkingMode.BALANCED)
    
    def get_prompt_only(self, question: str) -> str:
        """仅获取提示词（不调用 AI）"""
        return self.prompt_builder.get_full_prompt(question)
    
    def get_system_prompt(self) -> str:
        """获取系统提示词"""
        return self.prompt_builder.build_system_prompt()
    
    def clear_history(self):
        """清除对话历史"""
        self._conversation_history.clear()
    
    def is_available(self) -> bool:
        """检查 AI 是否可用"""
        return self.provider.is_available()
    
    def get_usage_stats(self) -> Dict[str, Any]:
        """获取使用统计"""
        if not self._conversation_history:
            return {"total_calls": 0}
        
        successful = [h for h in self._conversation_history if h.get("success")]
        total_time = sum(h.get("elapsed_time", 0) for h in successful)
        
        return {
            "total_calls": len(self._conversation_history),
            "successful_calls": len(successful),
            "total_time": total_time,
            "average_time": total_time / len(successful) if successful else 0
        }


def create_ai_agent(
    provider: str = "openai",
    model: Optional[str] = None,
    api_key: Optional[str] = None,
    randomness: float = 0.5,
    thinking_mode: str = "balanced",
    **kwargs
) -> AIAgent:
    """
    快速创建 AI Agent 的便捷函数
    
    Args:
        provider: 提供商 (openai/anthropic/ollama/custom)
        model: 模型名称
        api_key: API Key
        randomness: 随机性水平
        thinking_mode: 思维模式
        **kwargs: 其他配置
    
    Returns:
        AIAgent 实例
    
    Example:
        >>> # OpenAI
        >>> agent = create_ai_agent(
        ...     provider="openai",
        ...     model="gpt-4",
        ...     api_key="your-key",
        ...     randomness=0.7
        ... )
        >>> 
        >>> # Claude
        >>> agent = create_ai_agent(
        ...     provider="anthropic",
        ...     model="claude-3-opus-20240229",
        ...     api_key="your-key"
        ... )
        >>> 
        >>> # Ollama 本地
        >>> agent = create_ai_agent(
        ...     provider="ollama",
        ...     model="llama2"
        ... )
    """
    provider_map = {
        "openai": AIProvider.OPENAI,
        "anthropic": AIProvider.ANTHROPIC,
        "ollama": AIProvider.OLLAMA,
        "custom": AIProvider.CUSTOM,
    }
    
    default_models = {
        AIProvider.OPENAI: "gpt-4",
        AIProvider.ANTHROPIC: "claude-3-opus-20240229",
        AIProvider.OLLAMA: "llama2",
    }
    
    ai_provider = provider_map.get(provider.lower(), AIProvider.OPENAI)
    
    if model is None:
        model = default_models.get(ai_provider, "gpt-4")
    
    config = AIConfig(
        provider=ai_provider,
        model=model,
        api_key=api_key,
        randomness_level=randomness,
        thinking_mode=thinking_mode,
        **kwargs
    )
    
    return AIAgent(config)
