"""
RandomAgent - 模拟人类直觉跳跃思维的智能体框架

安装：
    pip install -e .

使用：
    from random_agent import create_prompt, create_ai_agent
    
    # 生成提示词
    prompt = create_prompt("什么是创造力？", randomness=0.7, mode="creative")
    
    # 调用 AI
    agent = create_ai_agent(provider="openai", api_key="your-key")
    result = agent.think("什么是创造力？")
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="random-agent",
    version="0.3.0",
    author="RandomAgent Team",
    author_email="",
    description="模拟人类直觉跳跃思维的智能体框架 - 提示词工程",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/random-agent",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        # 核心依赖（无外部依赖）
    ],
    extras_require={
        "openai": ["openai>=1.0.0"],
        "anthropic": ["anthropic>=0.18.0"],
        "all": ["openai>=1.0.0", "anthropic>=0.18.0"],
    },
    entry_points={
        "console_scripts": [
            "random-agent=random_agent.cli:main",
        ],
    },
    keywords="ai agent prompt-engineering randomness consciousness llm",
)
