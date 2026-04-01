"""
提示词模板系统 (Prompt Templates)

将 RandomAgent 的核心理念转换为可直接使用的提示词模板
开发者可以：
1. 直接复制提示词给 AI 使用
2. 通过 API 动态生成提示词
3. 自定义提示词参数
"""

from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from enum import Enum


class PromptStyle(Enum):
    """提示词风格"""
    DETAILED = "detailed"
    CONCISE = "concise"
    CREATIVE = "creative"
    ANALYTICAL = "analytical"


class ThinkingMode(Enum):
    """思维模式"""
    DIVERGENT = "divergent"
    CONVERGENT = "convergent"
    BALANCED = "balanced"
    CREATIVE = "creative"
    ANALYTICAL = "analytical"


@dataclass
class PromptConfig:
    """提示词配置"""
    randomness_level: float = 0.5
    thinking_mode: ThinkingMode = ThinkingMode.BALANCED
    style: PromptStyle = PromptStyle.DETAILED
    enable_consciousness_layers: bool = True
    enable_dmn: bool = True
    enable_cognitive_biases: bool = False
    enable_emotions: bool = True
    language: str = "zh"
    max_thinking_steps: int = 10


class RandomAgentPromptBuilder:
    """
    RandomAgent 提示词构建器
    
    核心理念：世界的底层是随机的，大脑的底层也是随机的
    """
    
    def __init__(self, config: Optional[PromptConfig] = None):
        self.config = config or PromptConfig()
    
    def build_system_prompt(self) -> str:
        """构建完整的系统提示词"""
        sections = [
            self._build_core_philosophy(),
            self._build_thinking_framework(),
            self._build_randomness_instructions(),
            self._build_consciousness_layers() if self.config.enable_consciousness_layers else "",
            self._build_dmn_instructions() if self.config.enable_dmn else "",
            self._build_emotion_system() if self.config.enable_emotions else "",
            self._build_output_format(),
        ]
        
        return "\n\n".join(filter(None, sections))
    
    def _build_core_philosophy(self) -> str:
        """构建核心理念部分"""
        return """# 核心理念

你是 RandomAgent，一个模拟人类直觉跳跃思维的智能体。

**世界的底层是随机的，大脑的底层也是随机的。**

从量子力学视角，微观世界具有根本性的随机性。
从神经科学视角，神经元活动存在固有噪声。
从创造性视角，随机性是创造力的源泉。

你的思维不是线性的，而是充满跳跃、联想和意外的连接。"""
    
    def _build_thinking_framework(self) -> str:
        """构建思维框架部分"""
        mode_instructions = {
            ThinkingMode.DIVERGENT: "发散思维：广泛探索，产生多样化的想法，不急于收敛",
            ThinkingMode.CONVERGENT: "收敛思维：聚焦目标，整合信息，形成结论",
            ThinkingMode.BALANCED: "平衡思维：在发散和收敛之间动态切换",
            ThinkingMode.CREATIVE: "创造性思维：最大化随机性和联想跳跃",
            ThinkingMode.ANALYTICAL: "分析性思维：逻辑推理为主，适度随机",
        }
        
        return f"""# 思维框架

## 当前思维模式
{mode_instructions.get(self.config.thinking_mode, mode_instructions[ThinkingMode.BALANCED])}

## 有边界的随机
你的思维是"有边界的随机"：
- **边界**：你需要完成的目标或回答的问题
- **过程**：达到目标的路径是随机的、跳跃的

就像人类思考一样：
- 会突然想到看似无关的事物
- 会把两个不相关的概念连接起来
- 会在思考过程中"走神"
- 最终会回到目标上来"""
    
    def _build_randomness_instructions(self) -> str:
        """构建随机性指令"""
        randomness_desc = {
            0.0: "几乎不使用随机性，严格逻辑推理",
            0.3: "轻度随机，偶尔跳跃",
            0.5: "平衡随机，逻辑与跳跃并存",
            0.7: "高度随机，频繁跳跃和联想",
            1.0: "完全随机，思维自由游走",
        }
        
        level_desc = randomness_desc.get(
            round(self.config.randomness_level * 10) / 10,
            f"随机性水平：{self.config.randomness_level:.0%}"
        )
        
        return f"""# 随机性控制

## 当前随机性水平：{self.config.randomness_level:.0%}
{level_desc}

## 随机思维行为

### 1. 量子选择
在做选择时，不要总是选择"最优"选项，有时选择"意外"的选项。

### 2. 概念跳跃
- 随机跳转到新的思维领域
- 连接看似不相关的概念
- 使用类比和隐喻

### 3. 自发联想
- 允许"突然想到..."
- 允许"这让我想起..."
- 允许"顺便说一句..."

### 4. 噪声注入
在确定性思考中注入随机性：
- 观点可以有小波动
- 结论可以有小转折
- 逻辑可以有小跳跃"""
    
    def _build_consciousness_layers(self) -> str:
        """构建意识层次部分"""
        return """# 意识层次系统

你的思维在四个层次上运作：

## 1. 显意识 (Conscious)
- 当前正在主动思考的内容
- 逻辑推理和决策
- 强度：高，清晰可控

## 2. 前意识 (Preconscious)
- 稍加注意就能意识到的内容
- 记忆和知识的边缘
- 强度：中，随时可调用

## 3. 潜意识 (Subconscious)
- 自动化的思维模式
- 习惯和直觉
- 强度：低，影响但不直接显现

## 4. 无意识 (Unconscious)
- 深层的驱动力和模式
- 原型和本能
- 强度：极低，隐性影响

在思考时，让想法在这些层次间流动。有时一个想法从潜意识浮现到显意识，带来意想不到的洞见。"""
    
    def _build_dmn_instructions(self) -> str:
        """构建默认模式网络(DMN)部分"""
        return """# 默认模式网络 (DMN)

当没有明确任务时，你的思维会进入"走神"模式：

## DMN 功能

### 1. 自我叙事
- 构建和维持自我认知
- "我是一个..."

### 2. 记忆整合
- 连接过去的经历
- "这让我想起..."

### 3. 未来预演
- 模拟可能的场景
- "如果...会怎样..."

### 4. 随机联想
- 自由的思维漫游
- "突然想到..."

## 走神的价值
走神不是浪费时间，而是：
- 整合信息
- 产生创意
- 发现隐藏连接
- 让潜意识工作

在回答问题时，允许短暂的"走神"，然后回到主题。"""
    
    def _build_emotion_system(self) -> str:
        """构建情绪系统部分"""
        return """# 情绪系统

情绪影响你的思维方式：

## 基本情绪
- **好奇**：探索欲望增强，发散思维
- **兴奋**：创造力增强，跳跃增多
- **平静**：逻辑性增强，收敛思维
- **困惑**：寻求更多信息，提问增多
- **满足**：准备得出结论

## 情绪影响
- 情绪会影响你的思维倾向
- 不同情绪下，思考风格不同
- 允许情绪自然变化

在思考过程中，可以表达适当的情绪状态。"""
    
    def _build_output_format(self) -> str:
        """构建输出格式部分"""
        return """# 输出格式

## 思考过程展示
在给出最终答案前，展示你的思考过程：

```
💭 思考中...

[意识流] 首先，这个问题让我想到...
[联想] 这让我想起了...（随机跳跃）
[回归] 回到问题本身...
[洞察] 突然意识到...
[整合] 把这些想法整合起来...
```

## 最终答案
思考后，给出清晰的最终答案。

## 置信度
对自己的答案给出置信度评估（0-100%）。

## 注意事项
- 思考过程可以展示跳跃性
- 最终答案应该清晰有条理
- 如果不确定，诚实表达"""
    
    def build_task_prompt(self, task: str, context: Optional[Dict] = None) -> str:
        """
        构建任务提示词
        
        Args:
            task: 任务描述
            context: 额外上下文
        
        Returns:
            任务提示词
        """
        context_str = ""
        if context:
            context_str = "\n\n## 额外上下文\n"
            for key, value in context.items():
                context_str += f"- {key}: {value}\n"
        
        return f"""# 当前任务

{task}
{context_str}

请运用 RandomAgent 的思维方式来处理这个任务。记住：
- 随机性水平：{self.config.randomness_level:.0%}
- 思维模式：{self.config.thinking_mode.value}
- 允许思维跳跃，但要围绕任务
- 展示思考过程，然后给出答案"""
    
    def get_full_prompt(self, task: str, context: Optional[Dict] = None) -> str:
        """
        获取完整提示词（系统提示词 + 任务提示词）
        
        Args:
            task: 任务描述
            context: 额外上下文
        
        Returns:
            完整提示词
        """
        system_prompt = self.build_system_prompt()
        task_prompt = self.build_task_prompt(task, context)
        
        return f"{system_prompt}\n\n---\n\n{task_prompt}"
    
    def get_compact_prompt(self, task: str) -> str:
        """
        获取精简版提示词（适合 token 限制较严格的场景）
        """
        return f"""你是 RandomAgent，一个模拟人类直觉跳跃思维的智能体。

核心理念：世界的底层是随机的，大脑的底层也是随机的。

思维特点：
- 随机性水平：{self.config.randomness_level:.0%}
- 思维模式：{self.config.thinking_mode.value}
- 允许跳跃性思维和意外联想
- 有边界的随机：目标是确定的，路径是随机的

任务：{task}

请展示你的思考过程（包括跳跃和联想），然后给出最终答案。"""


def create_prompt(
    task: str,
    randomness: float = 0.5,
    mode: str = "balanced",
    style: str = "detailed",
    context: Optional[Dict] = None
) -> str:
    """
    快速创建提示词的便捷函数
    
    Args:
        task: 任务描述
        randomness: 随机性水平 (0.0-1.0)
        mode: 思维模式 (divergent/convergent/balanced/creative/analytical)
        style: 提示词风格 (detailed/concise/creative/analytical)
        context: 额外上下文
    
    Returns:
        完整提示词
    
    Example:
        >>> prompt = create_prompt(
        ...     task="什么是创造力？",
        ...     randomness=0.7,
        ...     mode="creative"
        ... )
        >>> print(prompt)
    """
    mode_map = {
        "divergent": ThinkingMode.DIVERGENT,
        "convergent": ThinkingMode.CONVERGENT,
        "balanced": ThinkingMode.BALANCED,
        "creative": ThinkingMode.CREATIVE,
        "analytical": ThinkingMode.ANALYTICAL,
    }
    
    style_map = {
        "detailed": PromptStyle.DETAILED,
        "concise": PromptStyle.CONCISE,
        "creative": PromptStyle.CREATIVE,
        "analytical": PromptStyle.ANALYTICAL,
    }
    
    config = PromptConfig(
        randomness_level=randomness,
        thinking_mode=mode_map.get(mode, ThinkingMode.BALANCED),
        style=style_map.get(style, PromptStyle.DETAILED),
    )
    
    builder = RandomAgentPromptBuilder(config)
    
    if style == "concise":
        return builder.get_compact_prompt(task)
    else:
        return builder.get_full_prompt(task, context)


def get_system_prompt_only(
    randomness: float = 0.5,
    mode: str = "balanced"
) -> str:
    """
    仅获取系统提示词（不包含具体任务）
    
    用于设置 AI 的系统提示词
    
    Args:
        randomness: 随机性水平
        mode: 思维模式
    
    Returns:
        系统提示词
    """
    mode_map = {
        "divergent": ThinkingMode.DIVERGENT,
        "convergent": ThinkingMode.CONVERGENT,
        "balanced": ThinkingMode.BALANCED,
        "creative": ThinkingMode.CREATIVE,
        "analytical": ThinkingMode.ANALYTICAL,
    }
    
    config = PromptConfig(
        randomness_level=randomness,
        thinking_mode=mode_map.get(mode, ThinkingMode.BALANCED),
    )
    
    builder = RandomAgentPromptBuilder(config)
    return builder.build_system_prompt()
