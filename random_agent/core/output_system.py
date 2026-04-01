"""
输出系统 (Output System)

功能：
1. 思考过程展示 - 展示思维过程
2. 最终答案生成 - 生成最终输出
3. 格式化输出 - 格式化展示结果
"""

import time
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
from random_agent.core.randomness_engine import RandomnessEngine
from random_agent.core.consciousness_layers import Thought, ConsciousnessLevel


class OutputFormat(Enum):
    """输出格式"""
    FULL = "full"               # 完整输出
    SUMMARY = "summary"         # 摘要输出
    STRUCTURED = "structured"   # 结构化输出
    NARRATIVE = "narrative"     # 叙事输出


@dataclass
class ThinkingStep:
    """思考步骤"""
    content: str
    level: str
    timestamp: float
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class OutputResult:
    """输出结果"""
    final_answer: str
    thinking_process: List[ThinkingStep]
    confidence: float
    metadata: Dict[str, Any] = field(default_factory=dict)


class ThinkingProcessDisplay:
    """
    思考过程展示
    
    展示思维过程，包括：
    - 思维轨迹
    - 意识层次标记
    - 时间戳
    - 关键决策点
    """
    
    def __init__(self, randomness_engine: RandomnessEngine):
        self.randomness = randomness_engine
        self._steps: List[ThinkingStep] = []
        self._key_decisions: List[Dict] = []
        self._max_steps = 100
    
    def add_step(
        self, 
        thought: Thought, 
        is_key_decision: bool = False
    ):
        """添加思考步骤"""
        step = ThinkingStep(
            content=str(thought.content),
            level=thought.level.value,
            timestamp=thought.timestamp,
            metadata=thought.metadata
        )
        
        self._steps.append(step)
        
        if is_key_decision:
            self._key_decisions.append({
                "step_index": len(self._steps) - 1,
                "content": step.content,
                "timestamp": time.time()
            })
        
        if len(self._steps) > self._max_steps:
            self._steps = self._steps[-self._max_steps:]
    
    def get_process(self) -> List[ThinkingStep]:
        """获取思考过程"""
        return self._steps.copy()
    
    def get_key_decisions(self) -> List[Dict]:
        """获取关键决策"""
        return self._key_decisions.copy()
    
    def format_process(
        self, 
        format_type: OutputFormat = OutputFormat.FULL
    ) -> str:
        """格式化思考过程"""
        if format_type == OutputFormat.FULL:
            return self._format_full()
        elif format_type == OutputFormat.SUMMARY:
            return self._format_summary()
        elif format_type == OutputFormat.STRUCTURED:
            return self._format_structured()
        elif format_type == OutputFormat.NARRATIVE:
            return self._format_narrative()
        return self._format_full()
    
    def _format_full(self) -> str:
        """完整格式"""
        lines = ["=== 思考过程 ==="]
        
        for i, step in enumerate(self._steps):
            level_indicator = {
                "conscious": "[显意识]",
                "preconscious": "[前意识]",
                "subconscious": "[潜意识]",
                "unconscious": "[无意识]"
            }.get(step.level, "[未知]")
            
            lines.append(f"{i+1}. {level_indicator} {step.content}")
        
        return "\n".join(lines)
    
    def _format_summary(self) -> str:
        """摘要格式"""
        if not self._steps:
            return "无思考过程"
        
        key_steps = self._steps[::max(1, len(self._steps) // 5)]
        
        lines = ["=== 思考摘要 ==="]
        for step in key_steps:
            lines.append(f"• {step.content[:50]}...")
        
        return "\n".join(lines)
    
    def _format_structured(self) -> str:
        """结构化格式"""
        levels = {
            "conscious": [],
            "preconscious": [],
            "subconscious": [],
            "unconscious": []
        }
        
        for step in self._steps:
            if step.level in levels:
                levels[step.level].append(step.content)
        
        lines = ["=== 结构化思考过程 ==="]
        
        level_names = {
            "conscious": "显意识",
            "preconscious": "前意识",
            "subconscious": "潜意识",
            "unconscious": "无意识"
        }
        
        for level, contents in levels.items():
            if contents:
                lines.append(f"\n【{level_names[level]}】")
                for content in contents[:3]:
                    lines.append(f"  - {content[:60]}")
        
        return "\n".join(lines)
    
    def _format_narrative(self) -> str:
        """叙事格式"""
        if not self._steps:
            return "没有思考过程可以叙述"
        
        story = ["思考开始了..."]
        
        for i, step in enumerate(self._steps):
            if i == 0:
                story.append(f"首先，{step.content}")
            elif i == len(self._steps) - 1:
                story.append(f"最后，{step.content}")
            else:
                connectors = ["然后", "接着", "于是", "此时", "这时"]
                connector = self.randomness.random_choice(
                    connectors
                )
                story.append(f"{connector}，{step.content}")
        
        story.append("思考结束。")
        
        return "\n".join(story)
    
    def clear(self):
        """清空思考过程"""
        self._steps.clear()
        self._key_decisions.clear()


class AnswerGenerator:
    """
    最终答案生成器
    
    生成最终输出答案
    """
    
    def __init__(self, randomness_engine: RandomnessEngine):
        self.randomness = randomness_engine
        self._answer_templates: Dict[str, List[str]] = {
            "conclusion": [
                "综上所述，{answer}",
                "因此，{answer}",
                "结论是：{answer}",
                "最终答案是：{answer}"
            ],
            "suggestion": [
                "建议：{answer}",
                "推荐方案：{answer}",
                "可以考虑：{answer}"
            ],
            "insight": [
                "洞察：{answer}",
                "发现：{answer}",
                "关键点：{answer}"
            ]
        }
    
    def generate(
        self, 
        thinking_process: List[ThinkingStep],
        goal: str,
        confidence: float = 0.5
    ) -> str:
        """
        生成最终答案
        
        Args:
            thinking_process: 思考过程
            goal: 目标
            confidence: 置信度
        
        Returns:
            最终答案
        """
        if not thinking_process:
            return "未能得出明确结论"
        
        key_points = self._extract_key_points(thinking_process)
        
        answer_type = self._determine_answer_type(thinking_process)
        
        if key_points:
            main_point = key_points[0]
            
            template = self.randomness.random_choice(
                self._answer_templates[answer_type]
            )
            
            answer = template.format(answer=main_point)
            
            if len(key_points) > 1:
                answer += f"\n\n其他要点："
                for point in key_points[1:3]:
                    answer += f"\n• {point}"
        else:
            answer = "思考过程中未发现明确的结论点"
        
        if confidence < 0.5:
            answer += f"\n\n（置信度：{confidence:.0%}，建议进一步验证）"
        
        return answer
    
    def _extract_key_points(
        self, 
        steps: List[ThinkingStep]
    ) -> List[str]:
        """提取关键点"""
        key_points = []
        
        for step in steps:
            if step.level in ["conscious", "preconscious"]:
                content = step.content
                
                if any(kw in content for kw in ["结论", "因此", "所以", "答案", "发现"]):
                    key_points.append(content)
        
        if not key_points:
            for step in steps[-5:]:
                if step.level == "conscious":
                    key_points.append(step.content)
        
        return key_points[:5]
    
    def _determine_answer_type(
        self, 
        steps: List[ThinkingStep]
    ) -> str:
        """确定答案类型"""
        content_text = " ".join(s.content for s in steps)
        
        if any(kw in content_text for kw in ["建议", "推荐", "应该"]):
            return "suggestion"
        
        if any(kw in content_text for kw in ["发现", "洞察", "关键"]):
            return "insight"
        
        return "conclusion"


class OutputSystem:
    """
    输出系统 - 整合思考过程展示和答案生成
    """
    
    def __init__(
        self, 
        randomness_engine: Optional[RandomnessEngine] = None
    ):
        self.randomness = randomness_engine or RandomnessEngine()
        
        self.display = ThinkingProcessDisplay(self.randomness)
        self.generator = AnswerGenerator(self.randomness)
        
        self._output_history: List[OutputResult] = []
    
    def record_thought(
        self, 
        thought: Thought, 
        is_key_decision: bool = False
    ):
        """记录思考"""
        self.display.add_step(thought, is_key_decision)
    
    def generate_output(
        self, 
        goal: str,
        confidence: float = 0.5,
        format_type: OutputFormat = OutputFormat.FULL
    ) -> OutputResult:
        """
        生成输出
        
        Args:
            goal: 目标
            confidence: 置信度
            format_type: 输出格式
        
        Returns:
            输出结果
        """
        thinking_process = self.display.get_process()
        
        final_answer = self.generator.generate(
            thinking_process,
            goal,
            confidence
        )
        
        result = OutputResult(
            final_answer=final_answer,
            thinking_process=thinking_process,
            confidence=confidence,
            metadata={
                "goal": goal,
                "format": format_type.value,
                "steps_count": len(thinking_process)
            }
        )
        
        self._output_history.append(result)
        
        return result
    
    def format_output(
        self, 
        result: OutputResult,
        format_type: OutputFormat = OutputFormat.FULL
    ) -> str:
        """格式化输出"""
        lines = []
        
        lines.append("=" * 50)
        lines.append("【最终答案】")
        lines.append(result.final_answer)
        lines.append("")
        
        if format_type != OutputFormat.SUMMARY:
            lines.append("=" * 50)
            lines.append("【思考过程】")
            lines.append(self.display.format_process(format_type))
        
        lines.append("")
        lines.append("=" * 50)
        lines.append(f"置信度：{result.confidence:.0%}")
        lines.append(f"思考步骤数：{len(result.thinking_process)}")
        
        return "\n".join(lines)
    
    def get_formatted_output(
        self, 
        goal: str,
        confidence: float = 0.5,
        format_type: OutputFormat = OutputFormat.FULL
    ) -> str:
        """获取格式化输出"""
        result = self.generate_output(goal, confidence, format_type)
        return self.format_output(result, format_type)
    
    def clear(self):
        """清空"""
        self.display.clear()
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            "output_count": len(self._output_history),
            "current_steps": len(self.display._steps),
            "key_decisions": len(self.display._key_decisions)
        }
