"""
影响因素系统 (Influence Factors)

包含影响思维的各种因素：
1. 情绪系统 - 情绪状态影响思维
2. 认知偏见 - 各种认知偏见
3. 心智模型/图式 - 思维框架
4. 习惯系统 - 行为习惯
5. 性格系统 - 大五人格特质

理论基础：
- 情绪心理学
- 认知偏见研究
- 图式理论
- 习惯形成机制
- 大五人格理论
"""

import random
import time
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from random_agent.core.randomness_engine import RandomnessEngine, RandomnessType


class EmotionType(Enum):
    """情绪类型"""
    JOY = "joy"
    FEAR = "fear"
    ANGER = "anger"
    SADNESS = "sadness"
    SURPRISE = "surprise"
    DISGUST = "disgust"
    ANTICIPATION = "anticipation"
    TRUST = "trust"
    CURIOSITY = "curiosity"
    CONFUSION = "confusion"


@dataclass
class EmotionState:
    """情绪状态"""
    emotion_type: EmotionType
    intensity: float = 0.5
    duration: float = 1.0
    trigger: Optional[str] = None
    timestamp: float = field(default_factory=time.time)


class EmotionSystem:
    """
    情绪系统
    
    神经基础：杏仁核、前额叶皮层、岛叶
    
    功能：
    - 情绪生成：根据情境生成情绪
    - 情绪调节：调节情绪强度
    - 情绪影响：情绪对思维的影响
    - 情绪记忆：情绪与记忆的关联
    """
    
    def __init__(self, randomness_engine: RandomnessEngine):
        self.randomness = randomness_engine
        self._current_emotions: Dict[EmotionType, float] = {
            et: 0.3 for et in EmotionType
        }
        self._emotion_history: List[EmotionState] = []
        self._emotion_threshold = 0.5
        self._decay_rate = 0.1
    
    def generate_emotion(
        self, 
        context: Dict, 
        stimulus: Optional[str] = None
    ) -> EmotionState:
        """
        生成情绪
        
        Args:
            context: 上下文
            stimulus: 刺激因素
        
        Returns:
            生成的情绪状态
        """
        emotion_weights = self._calculate_emotion_weights(context, stimulus)
        
        emotion_type = self.randomness.random_choice(
            list(emotion_weights.keys()),
            weights=list(emotion_weights.values()),
            randomness_type=RandomnessType.QUANTUM
        )
        
        base_intensity = emotion_weights[emotion_type]
        intensity = self.randomness.inject_randomness(base_intensity, 0.2)
        
        emotion = EmotionState(
            emotion_type=emotion_type,
            intensity=intensity,
            trigger=stimulus
        )
        
        self._current_emotions[emotion_type] = intensity
        self._emotion_history.append(emotion)
        
        if len(self._emotion_history) > 200:
            self._emotion_history = self._emotion_history[-200:]
        
        return emotion
    
    def _calculate_emotion_weights(
        self, 
        context: Dict, 
        stimulus: Optional[str]
    ) -> Dict[EmotionType, float]:
        """计算情绪权重"""
        weights = {et: 0.1 for et in EmotionType}
        
        if context.get("novelty", 0) > 0.5:
            weights[EmotionType.SURPRISE] = 0.4
            weights[EmotionType.CURIOSITY] = 0.5
        
        if context.get("threat", 0) > 0.5:
            weights[EmotionType.FEAR] = 0.6
        
        if context.get("success", 0) > 0.5:
            weights[EmotionType.JOY] = 0.5
            weights[EmotionType.TRUST] = 0.4
        
        if context.get("failure", 0) > 0.5:
            weights[EmotionType.SADNESS] = 0.4
            weights[EmotionType.ANGER] = 0.3
        
        if context.get("uncertainty", 0) > 0.5:
            weights[EmotionType.CONFUSION] = 0.4
            weights[EmotionType.ANTICIPATION] = 0.3
        
        return weights
    
    def regulate(self, emotion_type: EmotionType, target_intensity: float):
        """
        调节情绪
        
        Args:
            emotion_type: 情绪类型
            target_intensity: 目标强度
        """
        current = self._current_emotions.get(emotion_type, 0.5)
        diff = target_intensity - current
        self._current_emotions[emotion_type] = current + diff * 0.5
    
    def decay(self):
        """情绪衰减"""
        for emotion_type in self._current_emotions:
            self._current_emotions[emotion_type] *= (1 - self._decay_rate)
    
    def get_dominant_emotion(self) -> Tuple[EmotionType, float]:
        """获取主导情绪"""
        dominant = max(
            self._current_emotions.items(),
            key=lambda x: x[1]
        )
        return dominant
    
    def get_emotional_influence(self) -> Dict[str, float]:
        """
        获取情绪对思维的影响
        
        Returns:
            影响因子
        """
        dominant_type, dominant_intensity = self.get_dominant_emotion()
        
        influences = {
            "creativity_boost": 0.0,
            "risk_tolerance": 0.5,
            "focus_level": 0.5,
            "exploration_tendency": 0.5,
            "decision_speed": 0.5
        }
        
        if dominant_type == EmotionType.JOY:
            influences["creativity_boost"] = dominant_intensity * 0.3
            influences["risk_tolerance"] = 0.5 + dominant_intensity * 0.3
        
        elif dominant_type == EmotionType.FEAR:
            influences["risk_tolerance"] = 0.5 - dominant_intensity * 0.4
            influences["focus_level"] = 0.5 + dominant_intensity * 0.3
        
        elif dominant_type == EmotionType.CURIOSITY:
            influences["exploration_tendency"] = 0.5 + dominant_intensity * 0.4
            influences["creativity_boost"] = dominant_intensity * 0.2
        
        elif dominant_type == EmotionType.CONFUSION:
            influences["decision_speed"] = 0.5 - dominant_intensity * 0.3
            influences["exploration_tendency"] = 0.5 + dominant_intensity * 0.2
        
        return influences
    
    def get_state(self) -> Dict[str, Any]:
        """获取情绪状态"""
        return {
            "current_emotions": {
                et.value: intensity 
                for et, intensity in self._current_emotions.items()
            },
            "dominant_emotion": self.get_dominant_emotion()[0].value,
            "history_count": len(self._emotion_history)
        }


class CognitiveBiasType(Enum):
    """认知偏见类型"""
    CONFIRMATION_BIAS = "confirmation_bias"
    ANCHORING = "anchoring"
    AVAILABILITY_HEURISTIC = "availability_heuristic"
    REPRESENTATIVENESS = "representativeness"
    LOSS_AVERSION = "loss_aversion"
    SUNK_COST_FALLACY = "sunk_cost_fallacy"
    DUNNING_KRUGER = "dunning_kruger"
    HALO_EFFECT = "halo_effect"
    BANDWAGON_EFFECT = "bandwagon_effect"
    FRAMING_EFFECT = "framing_effect"


class CognitiveBias:
    """
    认知偏见系统
    
    模拟人类思维中的各种认知偏见
    """
    
    def __init__(self, randomness_engine: RandomnessEngine):
        self.randomness = randomness_engine
        self._active_biases: Dict[CognitiveBiasType, float] = {}
        self._bias_history: List[Dict] = []
    
    def activate_bias(
        self, 
        bias_type: CognitiveBiasType, 
        strength: float = 0.5
    ):
        """激活认知偏见"""
        self._active_biases[bias_type] = strength
    
    def apply_bias(
        self, 
        content: Any, 
        context: Optional[Dict] = None
    ) -> Any:
        """
        应用认知偏见
        
        Args:
            content: 内容
            context: 上下文
        
        Returns:
            偏见影响后的内容
        """
        if not self._active_biases:
            return content
        
        bias_type = self.randomness.random_choice(
            list(self._active_biases.keys()),
            weights=list(self._active_biases.values()),
            randomness_type=RandomnessType.QUANTUM
        )
        
        strength = self._active_biases[bias_type]
        
        result = self._apply_specific_bias(bias_type, content, context, strength)
        
        self._bias_history.append({
            "bias_type": bias_type.value,
            "strength": strength,
            "timestamp": time.time()
        })
        
        return result
    
    def _apply_specific_bias(
        self, 
        bias_type: CognitiveBiasType, 
        content: Any, 
        context: Optional[Dict],
        strength: float
    ) -> Any:
        """应用特定偏见"""
        if bias_type == CognitiveBiasType.CONFIRMATION_BIAS:
            return self._apply_confirmation_bias(content, strength)
        
        elif bias_type == CognitiveBiasType.ANCHORING:
            return self._apply_anchoring(content, context, strength)
        
        elif bias_type == CognitiveBiasType.AVAILABILITY_HEURISTIC:
            return self._apply_availability(content, strength)
        
        elif bias_type == CognitiveBiasType.LOSS_AVERSION:
            return self._apply_loss_aversion(content, strength)
        
        elif bias_type == CognitiveBiasType.FRAMING_EFFECT:
            return self._apply_framing(content, strength)
        
        return content
    
    def _apply_confirmation_bias(
        self, 
        content: Any, 
        strength: float
    ) -> Any:
        """确认偏见 - 倾向于寻找支持现有信念的信息"""
        if isinstance(content, str):
            if random.random() < strength:
                prefixes = [
                    "这证实了我的想法：",
                    "正如我所预期的：",
                    "这支持了我的观点："
                ]
                prefix = self.randomness.random_choice(prefixes)
                return f"{prefix}{content}"
        return content
    
    def _apply_anchoring(
        self, 
        content: Any, 
        context: Optional[Dict],
        strength: float
    ) -> Any:
        """锚定效应 - 过度依赖第一个信息"""
        if context and "anchor" in context:
            anchor = context["anchor"]
            if random.random() < strength:
                return f"考虑到{anchor}，{content}"
        return content
    
    def _apply_availability(
        self, 
        content: Any, 
        strength: float
    ) -> Any:
        """可得性启发 - 基于容易想到的信息判断"""
        if random.random() < strength:
            markers = ["我记得", "最近看到", "印象中"]
            marker = self.randomness.random_choice(markers)
            return f"{marker}，{content}"
        return content
    
    def _apply_loss_aversion(
        self, 
        content: Any, 
        strength: float
    ) -> Any:
        """损失厌恶 - 对损失更敏感"""
        if random.random() < strength:
            return f"需要避免损失，{content}"
        return content
    
    def _apply_framing(
        self, 
        content: Any, 
        strength: float
    ) -> Any:
        """框架效应 - 表述方式影响判断"""
        if random.random() < strength:
            frames = ["从积极角度看", "从消极角度看", "换个角度看"]
            frame = self.randomness.random_choice(frames)
            return f"{frame}，{content}"
        return content
    
    def deactivate_bias(self, bias_type: CognitiveBiasType):
        """停用认知偏见"""
        if bias_type in self._active_biases:
            del self._active_biases[bias_type]
    
    def get_active_biases(self) -> Dict[str, float]:
        """获取活跃的偏见"""
        return {
            bt.value: strength 
            for bt, strength in self._active_biases.items()
        }


class SchemaType(Enum):
    """图式类型"""
    SELF = "self"
    OTHERS = "others"
    WORLD = "world"
    TASK = "task"
    SOCIAL = "social"
    EMOTIONAL = "emotional"


@dataclass
class Schema:
    """心智图式"""
    schema_type: SchemaType
    content: Dict[str, Any]
    strength: float = 0.5
    flexibility: float = 0.5
    created_at: float = field(default_factory=time.time)


class MentalModel:
    """
    心智模型/图式系统
    
    理论基础：图式理论
    
    功能：
    - 图式存储：存储各种心智图式
    - 图式激活：根据情境激活相关图式
    - 图式应用：将图式应用于当前情境
    - 图式更新：根据新经验更新图式
    """
    
    def __init__(self, randomness_engine: RandomnessEngine):
        self.randomness = randomness_engine
        self._schemas: Dict[SchemaType, List[Schema]] = {
            st: [] for st in SchemaType
        }
        self._active_schemas: List[Schema] = []
        self._schema_history: List[Dict] = []
    
    def add_schema(
        self, 
        schema_type: SchemaType, 
        content: Dict[str, Any],
        strength: float = 0.5,
        flexibility: float = 0.5
    ):
        """添加图式"""
        schema = Schema(
            schema_type=schema_type,
            content=content,
            strength=strength,
            flexibility=flexibility
        )
        self._schemas[schema_type].append(schema)
    
    def activate_schema(
        self, 
        context: Dict
    ) -> List[Schema]:
        """
        激活图式
        
        Args:
            context: 上下文
        
        Returns:
            激活的图式列表
        """
        self._active_schemas.clear()
        
        for schema_type, schemas in self._schemas.items():
            for schema in schemas:
                activation_score = self._calculate_activation(schema, context)
                
                if activation_score > 0.3:
                    self._active_schemas.append(schema)
        
        if len(self._active_schemas) > 3:
            self._active_schemas = sorted(
                self._active_schemas,
                key=lambda s: s.strength,
                reverse=True
            )[:3]
        
        return self._active_schemas
    
    def _calculate_activation(
        self, 
        schema: Schema, 
        context: Dict
    ) -> float:
        """计算激活分数"""
        score = schema.strength
        
        for key, value in schema.content.items():
            if key in context:
                if context[key] == value:
                    score += 0.2
                else:
                    score -= 0.1
        
        return max(0.0, min(1.0, score))
    
    def apply_schema(
        self, 
        content: Any
    ) -> Any:
        """
        应用图式
        
        Args:
            content: 内容
        
        Returns:
            图式影响后的内容
        """
        if not self._active_schemas:
            return content
        
        schema = self.randomness.random_choice(
            self._active_schemas,
            weights=[s.strength for s in self._active_schemas],
            randomness_type=RandomnessType.QUANTUM
        )
        
        if isinstance(content, str):
            template = f"[{schema.schema_type.value}视角] {content}"
            return template
        
        return content
    
    def update_schema(
        self, 
        schema_type: SchemaType, 
        new_content: Dict[str, Any]
    ):
        """更新图式"""
        schemas = self._schemas.get(schema_type, [])
        for schema in schemas:
            for key, value in new_content.items():
                if key in schema.content:
                    schema.content[key] = (
                        schema.content[key] * 0.7 + value * 0.3
                    )
                else:
                    schema.content[key] = value
    
    def get_active_schemas_info(self) -> List[Dict]:
        """获取活跃图式信息"""
        return [
            {
                "type": s.schema_type.value,
                "strength": s.strength,
                "content_keys": list(s.content.keys())
            }
            for s in self._active_schemas
        ]


class HabitSystem:
    """
    习惯系统
    
    管理行为习惯的形成和执行
    """
    
    def __init__(self, randomness_engine: RandomnessEngine):
        self.randomness = randomness_engine
        self._habits: Dict[str, Dict] = {}
        self._execution_log: List[Dict] = []
    
    def form_habit(
        self, 
        name: str, 
        trigger: Dict, 
        action: str,
        initial_strength: float = 0.3
    ):
        """形成习惯"""
        self._habits[name] = {
            "trigger": trigger,
            "action": action,
            "strength": initial_strength,
            "execution_count": 0,
            "created_at": time.time()
        }
    
    def check_triggers(
        self, 
        context: Dict
    ) -> List[Dict]:
        """检查习惯触发"""
        triggered = []
        
        for name, habit in self._habits.items():
            if self._match_trigger(context, habit["trigger"]):
                if random.random() < habit["strength"]:
                    triggered.append({
                        "name": name,
                        "action": habit["action"],
                        "strength": habit["strength"]
                    })
                    habit["execution_count"] += 1
                    habit["strength"] = min(1.0, habit["strength"] + 0.02)
        
        if triggered:
            self._execution_log.append({
                "triggered_habits": [h["name"] for h in triggered],
                "context": str(context)[:50],
                "timestamp": time.time()
            })
        
        return triggered
    
    def _match_trigger(self, context: Dict, trigger: Dict) -> bool:
        """匹配触发条件"""
        matches = 0
        for key, value in trigger.items():
            if key in context:
                if context[key] == value:
                    matches += 1
        return matches > 0
    
    def break_habit(self, name: str) -> bool:
        """打破习惯"""
        if name in self._habits:
            del self._habits[name]
            return True
        return False
    
    def weaken_habit(self, name: str, amount: float = 0.1):
        """削弱习惯"""
        if name in self._habits:
            self._habits[name]["strength"] = max(
                0.0,
                self._habits[name]["strength"] - amount
            )
    
    def get_habits(self) -> Dict[str, Dict]:
        """获取所有习惯"""
        return self._habits.copy()


class PersonalityTrait(Enum):
    """大五人格特质"""
    OPENNESS = "openness"                    # 开放性
    CONSCIENTIOUSNESS = "conscientiousness"  # 尽责性
    EXTRAVERSION = "extraversion"            # 外向性
    AGREEABLENESS = "agreeableness"          # 宜人性
    NEUROTICISM = "neuroticism"              # 神经质


class PersonalitySystem:
    """
    性格系统
    
    基于大五人格理论
    """
    
    def __init__(self, randomness_engine: RandomnessEngine):
        self.randomness = randomness_engine
        self._traits: Dict[PersonalityTrait, float] = {
            PersonalityTrait.OPENNESS: 0.6,
            PersonalityTrait.CONSCIENTIOUSNESS: 0.5,
            PersonalityTrait.EXTRAVERSION: 0.5,
            PersonalityTrait.AGREEABLENESS: 0.5,
            PersonalityTrait.NEUROTICISM: 0.4
        }
    
    def set_trait(self, trait: PersonalityTrait, value: float):
        """设置特质值"""
        self._traits[trait] = max(0.0, min(1.0, value))
    
    def get_trait(self, trait: PersonalityTrait) -> float:
        """获取特质值"""
        return self._traits.get(trait, 0.5)
    
    def get_influence_on_thinking(self) -> Dict[str, float]:
        """
        获取性格对思维的影响
        
        Returns:
            影响因子
        """
        openness = self._traits[PersonalityTrait.OPENNESS]
        conscientiousness = self._traits[PersonalityTrait.CONSCIENTIOUSNESS]
        extraversion = self._traits[PersonalityTrait.EXTRAVERSION]
        neuroticism = self._traits[PersonalityTrait.NEUROTICISM]
        
        return {
            "creativity": openness,
            "exploration_tendency": openness * 0.8,
            "persistence": conscientiousness,
            "organization": conscientiousness * 0.7,
            "social_orientation": extraversion,
            "risk_tolerance": 1 - neuroticism * 0.5,
            "emotional_stability": 1 - neuroticism,
            "randomness_acceptance": openness * 0.6 + (1 - conscientiousness) * 0.4
        }
    
    def get_profile(self) -> Dict[str, float]:
        """获取性格画像"""
        return {
            trait.value: value 
            for trait, value in self._traits.items()
        }


class InfluenceFactors:
    """
    影响因素系统 - 整合所有影响因素
    """
    
    def __init__(
        self, 
        randomness_engine: Optional[RandomnessEngine] = None
    ):
        self.randomness = randomness_engine or RandomnessEngine()
        
        self.emotion = EmotionSystem(self.randomness)
        self.cognitive_bias = CognitiveBias(self.randomness)
        self.mental_model = MentalModel(self.randomness)
        self.habit = HabitSystem(self.randomness)
        self.personality = PersonalitySystem(self.randomness)
        
        self._influence_history: List[Dict] = []
    
    def process(
        self, 
        content: Any, 
        context: Optional[Dict] = None
    ) -> Any:
        """
        处理内容 - 应用所有影响因素
        
        Args:
            content: 内容
            context: 上下文
        
        Returns:
            处理后的内容
        """
        context = context or {}
        
        if context.get("generate_emotion", False):
            self.emotion.generate_emotion(context)
        
        emotional_influence = self.emotion.get_emotional_influence()
        
        if random.random() < emotional_influence.get("creativity_boost", 0):
            content = self.randomness.inject_randomness(content, 0.1)
        
        content = self.cognitive_bias.apply_bias(content, context)
        
        self.mental_model.activate_schema(context)
        content = self.mental_model.apply_schema(content)
        
        triggered_habits = self.habit.check_triggers(context)
        if triggered_habits:
            habit = triggered_habits[0]
            if isinstance(content, str):
                content = f"[习惯:{habit['name']}] {content}"
        
        personality_influence = self.personality.get_influence_on_thinking()
        
        self._influence_history.append({
            "emotional_influence": emotional_influence,
            "personality_influence": personality_influence,
            "triggered_habits": [h["name"] for h in triggered_habits],
            "timestamp": time.time()
        })
        
        if len(self._influence_history) > 200:
            self._influence_history = self._influence_history[-200:]
        
        return content
    
    def get_state(self) -> Dict[str, Any]:
        """获取影响因素状态"""
        return {
            "emotion": self.emotion.get_state(),
            "active_biases": self.cognitive_bias.get_active_biases(),
            "active_schemas": self.mental_model.get_active_schemas_info(),
            "habits_count": len(self.habit.get_habits()),
            "personality": self.personality.get_profile()
        }
    
    def set_personality(
        self, 
        openness: float = 0.5,
        conscientiousness: float = 0.5,
        extraversion: float = 0.5,
        agreeableness: float = 0.5,
        neuroticism: float = 0.5
    ):
        """设置性格"""
        self.personality.set_trait(PersonalityTrait.OPENNESS, openness)
        self.personality.set_trait(PersonalityTrait.CONSCIENTIOUSNESS, conscientiousness)
        self.personality.set_trait(PersonalityTrait.EXTRAVERSION, extraversion)
        self.personality.set_trait(PersonalityTrait.AGREEABLENESS, agreeableness)
        self.personality.set_trait(PersonalityTrait.NEUROTICISM, neuroticism)
    
    def enable_bias(
        self, 
        bias_type: CognitiveBiasType, 
        strength: float = 0.5
    ):
        """启用认知偏见"""
        self.cognitive_bias.activate_bias(bias_type, strength)
    
    def disable_bias(self, bias_type: CognitiveBiasType):
        """禁用认知偏见"""
        self.cognitive_bias.deactivate_bias(bias_type)
    
    def decay_emotions(self):
        """衰减情绪"""
        self.emotion.decay()
