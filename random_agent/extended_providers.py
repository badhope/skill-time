"""
扩展 AI 提供商 (Extended AI Providers)

提供更多 AI 服务提供商支持：
- Google PaLM / Gemini
- Cohere
- Azure OpenAI
- Hugging Face
- Together AI
- Replicate
"""

import os
import json
import time
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from enum import Enum

from random_agent.ai_integration import AIProviderBase, AIConfig


class ExtendedAIProvider(Enum):
    """扩展的 AI 提供商"""
    GOOGLE = "google"
    COHERE = "cohere"
    AZURE_OPENAI = "azure_openai"
    HUGGINGFACE = "huggingface"
    TOGETHER = "together"
    REPLICATE = "replicate"


class GoogleProvider(AIProviderBase):
    """Google PaLM / Gemini 提供商"""
    
    def __init__(self, config: AIConfig):
        super().__init__(config)
        self._client = None
        
        if config.api_key is None:
            config.api_key = os.getenv("GOOGLE_API_KEY")
    
    def _get_client(self):
        if self._client is None:
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.config.api_key)
                self._client = genai.GenerativeModel(self.config.model)
            except ImportError:
                raise ImportError("请安装 google-generativeai: pip install google-generativeai")
        return self._client
    
    def call(self, system_prompt: str, user_message: str) -> str:
        client = self._get_client()
        
        full_prompt = f"{system_prompt}\n\n{user_message}"
        
        response = client.generate_content(
            full_prompt,
            generation_config={
                "temperature": self.config.temperature,
                "max_output_tokens": self.config.max_tokens,
            }
        )
        
        return response.text
    
    def is_available(self) -> bool:
        return self.config.api_key is not None


class CohereProvider(AIProviderBase):
    """Cohere 提供商"""
    
    def __init__(self, config: AIConfig):
        super().__init__(config)
        self._client = None
        
        if config.api_key is None:
            config.api_key = os.getenv("COHERE_API_KEY")
    
    def _get_client(self):
        if self._client is None:
            try:
                import cohere
                self._client = cohere.Client(self.config.api_key)
            except ImportError:
                raise ImportError("请安装 cohere: pip install cohere")
        return self._client
    
    def call(self, system_prompt: str, user_message: str) -> str:
        client = self._get_client()
        
        response = client.chat(
            model=self.config.model,
            message=user_message,
            preamble=system_prompt,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens
        )
        
        return response.text
    
    def is_available(self) -> bool:
        return self.config.api_key is not None


class AzureOpenAIProvider(AIProviderBase):
    """Azure OpenAI 提供商"""
    
    def __init__(self, config: AIConfig):
        super().__init__(config)
        self._client = None
        
        if config.api_key is None:
            config.api_key = os.getenv("AZURE_OPENAI_API_KEY")
        
        if config.base_url is None:
            config.base_url = os.getenv("AZURE_OPENAI_ENDPOINT")
    
    def _get_client(self):
        if self._client is None:
            try:
                from openai import AzureOpenAI
                self._client = AzureOpenAI(
                    api_key=self.config.api_key,
                    api_version="2024-02-15-preview",
                    azure_endpoint=self.config.base_url
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
        return self.config.api_key is not None and self.config.base_url is not None


class HuggingFaceProvider(AIProviderBase):
    """Hugging Face 提供商"""
    
    def __init__(self, config: AIConfig):
        super().__init__(config)
        self._client = None
        
        if config.api_key is None:
            config.api_key = os.getenv("HUGGINGFACE_API_KEY")
    
    def _get_client(self):
        if self._client is None:
            try:
                from huggingface_hub import InferenceClient
                self._client = InferenceClient(
                    model=self.config.model,
                    token=self.config.api_key
                )
            except ImportError:
                raise ImportError("请安装 huggingface-hub: pip install huggingface-hub")
        return self._client
    
    def call(self, system_prompt: str, user_message: str) -> str:
        client = self._get_client()
        
        full_prompt = f"{system_prompt}\n\n{user_message}"
        
        response = client.text_generation(
            full_prompt,
            max_new_tokens=self.config.max_tokens,
            temperature=self.config.temperature,
            return_full_text=False
        )
        
        return response
    
    def is_available(self) -> bool:
        return self.config.api_key is not None


class TogetherProvider(AIProviderBase):
    """Together AI 提供商"""
    
    def __init__(self, config: AIConfig):
        super().__init__(config)
        self._client = None
        
        if config.api_key is None:
            config.api_key = os.getenv("TOGETHER_API_KEY")
        
        if config.base_url is None:
            config.base_url = "https://api.together.xyz/v1"
    
    def _get_client(self):
        if self._client is None:
            try:
                from openai import OpenAI
                self._client = OpenAI(
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


class ReplicateProvider(AIProviderBase):
    """Replicate 提供商"""
    
    def __init__(self, config: AIConfig):
        super().__init__(config)
        self._client = None
        
        if config.api_key is None:
            config.api_key = os.getenv("REPLICATE_API_TOKEN")
    
    def _get_client(self):
        if self._client is None:
            try:
                import replicate
                self._client = replicate.Client(api_token=self.config.api_key)
            except ImportError:
                raise ImportError("请安装 replicate: pip install replicate")
        return self._client
    
    def call(self, system_prompt: str, user_message: str) -> str:
        client = self._get_client()
        
        full_prompt = f"{system_prompt}\n\n{user_message}"
        
        output = client.run(
            self.config.model,
            input={
                "prompt": full_prompt,
                "temperature": self.config.temperature,
                "max_length": self.config.max_tokens,
            }
        )
        
        return "".join(output)
    
    def is_available(self) -> bool:
        return self.config.api_key is not None


class ExtendedAIProviderFactory:
    """扩展的 AI 提供商工厂"""
    
    @staticmethod
    def create(config: AIConfig, provider_type: str = "openai") -> AIProviderBase:
        providers = {
            "google": GoogleProvider,
            "cohere": CohereProvider,
            "azure_openai": AzureOpenAIProvider,
            "huggingface": HuggingFaceProvider,
            "together": TogetherProvider,
            "replicate": ReplicateProvider,
        }
        
        provider_class = providers.get(provider_type)
        if provider_class is None:
            raise ValueError(f"不支持的提供商: {provider_type}")
        
        return provider_class(config)


def create_extended_ai_agent(
    provider_type: str,
    model: str,
    api_key: Optional[str] = None,
    **kwargs
):
    """
    创建扩展 AI Agent 的便捷函数
    
    Args:
        provider_type: 提供商类型
        model: 模型名称
        api_key: API 密钥
        **kwargs: 其他配置
    
    Returns:
        AI Agent 实例
    
    Example:
        >>> # 使用 Google Gemini
        >>> agent = create_extended_ai_agent(
        ...     provider_type="google",
        ...     model="gemini-pro",
        ...     api_key="your-google-api-key"
        ... )
        >>> result = agent.think("什么是创造力？")
        >>> 
        >>> # 使用 Cohere
        >>> agent = create_extended_ai_agent(
        ...     provider_type="cohere",
        ...     model="command",
        ...     api_key="your-cohere-api-key"
        ... )
    """
    from random_agent.ai_integration import AIProvider, AIAgent
    
    config = AIConfig(
        provider=AIProvider.CUSTOM,
        model=model,
        api_key=api_key,
        **kwargs
    )
    
    provider = ExtendedAIProviderFactory.create(config, provider_type)
    
    agent = AIAgent(config)
    agent.provider = provider
    
    return agent
