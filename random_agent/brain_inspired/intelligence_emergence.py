"""
智能涌现系统 - 从神经活动到智能行为的涌现
基于2024-2025最新神经科学和认知科学研究
"""

import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

from random_agent.brain_inspired.ensemble import NeuralEnsemble
from random_agent.brain_inspired.neuron import Neuron


class IntelligenceType(Enum):
    """智能类型"""
    FLUID = "fluid"
    CRYSTALLIZED = "crystallized"
    EMOTIONAL = "emotional"
    CREATIVE = "creative"
    PRACTICAL = "practical"


@dataclass
class CognitiveCapability:
    """认知能力"""
    capability_type: str
    strength: float
    flexibility: float
    development_stage: str


@dataclass
class EmergentBehavior:
    """涌现行为"""
    behavior_type: str
    complexity: float
    adaptiveness: float
    novelty: float
    description: str


class CognitiveFlexibility:
    """认知灵活性"""
    
    def __init__(self):
        self.switch_cost = 0.2
        self.adaptation_rate = 0.1
        self.current_strategy = None
        self.strategy_library = {}
        
    def switch_strategy(self, new_strategy: str, context: Dict[str, Any]) -> float:
        """切换策略"""
        if self.current_strategy == new_strategy:
            return 0.0
        
        cost = self.switch_cost
        
        if context.get('practice', False):
            cost *= 0.5
        
        self.current_strategy = new_strategy
        
        return cost
    
    def adapt_to_context(self, context: Dict[str, Any]) -> str:
        """适应环境"""
        if 'problem_type' in context:
            problem_type = context['problem_type']
            
            if problem_type == 'analytical':
                return 'analytical_strategy'
            elif problem_type == 'creative':
                return 'creative_strategy'
            elif problem_type == 'social':
                return 'social_strategy'
        
        return 'general_strategy'
    
    def measure_flexibility(self, task_switches: List[Tuple[str, str]]) -> float:
        """测量灵活性"""
        if not task_switches:
            return 0.5
        
        n_switches = len(task_switches)
        unique_strategies = len(set(s[1] for s in task_switches))
        
        flexibility = unique_strategies / (n_switches + 1)
        
        return float(np.clip(flexibility, 0, 1))


class ProblemSolvingEngine:
    """问题解决引擎"""
    
    def __init__(self):
        self.strategies = self._create_strategies()
        self.analogical_reasoner = AnalogicalReasoner()
        self.abstraction_engine = AbstractionEngine()
        
    def _create_strategies(self) -> Dict[str, Any]:
        """创建策略"""
        return {
            'trial_and_error': {'effectiveness': 0.3, 'speed': 0.8},
            'means_end_analysis': {'effectiveness': 0.7, 'speed': 0.5},
            'working_backwards': {'effectiveness': 0.6, 'speed': 0.6},
            'analogical': {'effectiveness': 0.8, 'speed': 0.4},
            'insight': {'effectiveness': 0.9, 'speed': 0.2}
        }
    
    def solve(self, problem: Dict[str, Any], current_time: float = 0.0) -> Dict[str, Any]:
        """解决问题"""
        problem_type = problem.get('type', 'unknown')
        complexity = problem.get('complexity', 0.5)
        
        strategy = self._select_strategy(problem_type, complexity)
        
        solution = self._apply_strategy(strategy, problem)
        
        if strategy == 'analogical':
            analogies = self.analogical_reasoner.find_analogies(problem)
            solution['analogies'] = analogies
        
        abstraction = self.abstraction_engine.abstract(problem, solution)
        solution['abstraction'] = abstraction
        
        return solution
    
    def _select_strategy(self, problem_type: str, complexity: float) -> str:
        """选择策略"""
        if complexity > 0.7:
            return 'means_end_analysis'
        elif complexity > 0.4:
            return 'analogical'
        else:
            return 'trial_and_error'
    
    def _apply_strategy(self, strategy: str, problem: Dict[str, Any]) -> Dict[str, Any]:
        """应用策略"""
        strategy_info = self.strategies.get(strategy, {'effectiveness': 0.5, 'speed': 0.5})
        
        success_probability = strategy_info['effectiveness']
        
        solution_found = np.random.rand() < success_probability
        
        return {
            'strategy': strategy,
            'success': solution_found,
            'confidence': success_probability,
            'solution': f"使用{strategy}策略的解决方案" if solution_found else None
        }


class AnalogicalReasoner:
    """类比推理器"""
    
    def __init__(self):
        self.analogy_database = {}
        
    def find_analogies(self, problem: Dict[str, Any]) -> List[Dict[str, Any]]:
        """寻找类比"""
        analogies = []
        
        for i in range(3):
            analogy = {
                'source_domain': f"domain_{i}",
                'similarity': 0.5 + np.random.rand() * 0.4,
                'applicable': True
            }
            analogies.append(analogy)
        
        return analogies
    
    def transfer_solution(self, source_solution: Any, target_problem: Dict[str, Any]) -> Any:
        """迁移解决方案"""
        return source_solution


class AbstractionEngine:
    """抽象引擎"""
    
    def __init__(self):
        self.abstraction_levels = ['concrete', 'specific', 'general', 'abstract']
        
    def abstract(self, problem: Dict[str, Any], solution: Dict[str, Any]) -> Dict[str, Any]:
        """抽象"""
        return {
            'level': 'general',
            'pattern': 'problem_solution_pattern',
            'applicability': 0.7
        }


class LearningSystem:
    """学习系统"""
    
    def __init__(self):
        self.experience_buffer = []
        self.knowledge_base = {}
        self.skill_acquisition = SkillAcquisition()
        
    def learn(self, experience: Dict[str, Any], current_time: float = 0.0) -> Dict[str, Any]:
        """学习"""
        self.experience_buffer.append(experience)
        
        if len(self.experience_buffer) > 100:
            self.experience_buffer.pop(0)
        
        insight = self._extract_insight(experience)
        
        if insight:
            self._update_knowledge(insight)
        
        skill_update = self.skill_acquisition.update(experience)
        
        return {
            'insight': insight,
            'knowledge_updated': insight is not None,
            'skill_update': skill_update,
            'experience_count': len(self.experience_buffer)
        }
    
    def _extract_insight(self, experience: Dict[str, Any]) -> Optional[str]:
        """提取洞察"""
        if experience.get('success', False):
            return f"成功经验：{experience.get('strategy', 'unknown')}"
        return None
    
    def _update_knowledge(self, insight: str):
        """更新知识库"""
        category = 'general'
        if category not in self.knowledge_base:
            self.knowledge_base[category] = []
        
        self.knowledge_base[category].append(insight)
    
    def transfer_learning(self, source_domain: str, target_domain: str) -> float:
        """迁移学习"""
        transfer_efficiency = 0.5
        
        return transfer_efficiency


class SkillAcquisition:
    """技能习得"""
    
    def __init__(self):
        self.skills = {}
        self.learning_curve_rate = 0.1
        
    def update(self, experience: Dict[str, Any]) -> Dict[str, Any]:
        """更新"""
        skill_type = experience.get('skill_type', 'general')
        
        if skill_type not in self.skills:
            self.skills[skill_type] = {
                'level': 0.0,
                'practice_count': 0
            }
        
        self.skills[skill_type]['practice_count'] += 1
        
        practice = self.skills[skill_type]['practice_count']
        new_level = 1.0 - np.exp(-self.learning_curve_rate * practice)
        self.skills[skill_type]['level'] = new_level
        
        return {
            'skill': skill_type,
            'level': new_level,
            'practice_count': practice
        }


class CreativityEngine:
    """创造力引擎"""
    
    def __init__(self):
        self.idea_generator = IdeaGenerator()
        self.combiner = IdeaCombiner()
        self.evaluator = IdeaEvaluator()
        
    def generate_ideas(self, problem: Dict[str, Any], n_ideas: int = 5) -> List[Dict[str, Any]]:
        """生成想法"""
        base_ideas = self.idea_generator.generate(problem, n_ideas)
        
        combined_ideas = self.combiner.combine(base_ideas)
        
        all_ideas = base_ideas + combined_ideas
        
        evaluated_ideas = [self.evaluator.evaluate(idea) for idea in all_ideas]
        
        evaluated_ideas.sort(key=lambda x: x['score'], reverse=True)
        
        return evaluated_ideas[:n_ideas]
    
    def creative_problem_solving(self, problem: Dict[str, Any]) -> Dict[str, Any]:
        """创造性问题解决"""
        ideas = self.generate_ideas(problem, n_ideas=3)
        
        best_idea = ideas[0] if ideas else None
        
        return {
            'problem': problem,
            'ideas': ideas,
            'best_idea': best_idea,
            'creativity_score': best_idea['novelty'] if best_idea else 0.0
        }


class IdeaGenerator:
    """想法生成器"""
    
    def __init__(self):
        self.generation_strategies = ['association', 'mutation', 'random']
        
    def generate(self, problem: Dict[str, Any], n: int) -> List[Dict[str, Any]]:
        """生成"""
        ideas = []
        
        for i in range(n):
            idea = {
                'id': i,
                'description': f"想法{i+1}针对{problem.get('type', '问题')}",
                'source': self.generation_strategies[i % len(self.generation_strategies)],
                'novelty': np.random.rand()
            }
            ideas.append(idea)
        
        return ideas


class IdeaCombiner:
    """想法组合器"""
    
    def __init__(self):
        self.combination_methods = ['synthesis', 'integration', 'transformation']
        
    def combine(self, ideas: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """组合"""
        if len(ideas) < 2:
            return []
        
        combined = []
        
        for i in range(min(2, len(ideas) - 1)):
            new_idea = {
                'id': f"combined_{i}",
                'description': f"组合想法：{ideas[i]['description']} + {ideas[i+1]['description']}",
                'source': 'combination',
                'novelty': (ideas[i]['novelty'] + ideas[i+1]['novelty']) / 2 * 1.2
            }
            combined.append(new_idea)
        
        return combined


class IdeaEvaluator:
    """想法评估器"""
    
    def __init__(self):
        self.criteria = {
            'novelty': 0.3,
            'usefulness': 0.4,
            'feasibility': 0.3
        }
        
    def evaluate(self, idea: Dict[str, Any]) -> Dict[str, Any]:
        """评估"""
        novelty = idea.get('novelty', np.random.rand())
        usefulness = np.random.rand()
        feasibility = np.random.rand()
        
        score = (novelty * self.criteria['novelty'] +
                usefulness * self.criteria['usefulness'] +
                feasibility * self.criteria['feasibility'])
        
        evaluated = idea.copy()
        evaluated.update({
            'novelty': novelty,
            'usefulness': usefulness,
            'feasibility': feasibility,
            'score': score
        })
        
        return evaluated


class EmergenceDetector:
    """涌现检测器"""
    
    def __init__(self):
        self.emergence_threshold = 0.6
        self.emergence_history = []
        
    def detect(self, system_state: Dict[str, Any]) -> Optional[EmergentBehavior]:
        """检测涌现"""
        complexity = self._measure_complexity(system_state)
        adaptiveness = self._measure_adaptiveness(system_state)
        novelty = self._measure_novelty(system_state)
        
        emergence_score = (complexity + adaptiveness + novelty) / 3
        
        if emergence_score > self.emergence_threshold:
            behavior = EmergentBehavior(
                behavior_type=self._classify_emergence(system_state),
                complexity=complexity,
                adaptiveness=adaptiveness,
                novelty=novelty,
                description=f"涌现行为：复杂度{complexity:.2f}，适应性{adaptiveness:.2f}，新颖性{novelty:.2f}"
            )
            
            self.emergence_history.append(behavior)
            
            return behavior
        
        return None
    
    def _measure_complexity(self, state: Dict[str, Any]) -> float:
        """测量复杂度"""
        n_components = state.get('n_components', 1)
        interactions = state.get('n_interactions', 0)
        
        complexity = min(1.0, interactions / (n_components * 2 + 1))
        
        return complexity
    
    def _measure_adaptiveness(self, state: Dict[str, Any]) -> float:
        """测量适应性"""
        return state.get('adaptiveness', 0.5)
    
    def _measure_novelty(self, state: Dict[str, Any]) -> float:
        """测量新颖性"""
        return state.get('novelty', 0.5)
    
    def _classify_emergence(self, state: Dict[str, Any]) -> str:
        """分类涌现"""
        return 'adaptive_behavior'


class IntelligenceEmergence:
    """智能涌现系统"""
    
    def __init__(self):
        self.cognitive_flexibility = CognitiveFlexibility()
        self.problem_solving = ProblemSolvingEngine()
        self.learning_system = LearningSystem()
        self.creativity_engine = CreativityEngine()
        self.emergence_detector = EmergenceDetector()
        
        self.capabilities: List[CognitiveCapability] = []
        self.emergence_history = []
        
    def process(self, input_data: Dict[str, Any], current_time: float = 0.0) -> Dict[str, Any]:
        """完整处理流程"""
        problem_solving_result = None
        if 'problem' in input_data:
            problem_solving_result = self.problem_solving.solve(input_data['problem'], current_time)
        
        learning_result = None
        if 'experience' in input_data:
            learning_result = self.learning_system.learn(input_data['experience'], current_time)
        
        creativity_result = None
        if 'creative_task' in input_data:
            creativity_result = self.creativity_engine.creative_problem_solving(input_data['creative_task'])
        
        flexibility_result = None
        if 'context' in input_data:
            strategy = self.cognitive_flexibility.adapt_to_context(input_data['context'])
            flexibility_result = {
                'selected_strategy': strategy,
                'flexibility_score': 0.7
            }
        
        system_state = {
            'n_components': 5,
            'n_interactions': 3,
            'adaptiveness': 0.7,
            'novelty': creativity_result['creativity_score'] if creativity_result else 0.5
        }
        emergent_behavior = self.emergence_detector.detect(system_state)
        
        result = {
            'problem_solving': problem_solving_result,
            'learning': learning_result,
            'creativity': creativity_result,
            'flexibility': flexibility_result,
            'emergent_behavior': {
                'detected': emergent_behavior is not None,
                'behavior': emergent_behavior.__dict__ if emergent_behavior else None
            },
            'timestamp': current_time
        }
        
        result['intelligence_level'] = self._compute_intelligence_level(result)
        
        self.emergence_history.append(result)
        
        return result
    
    def _compute_intelligence_level(self, result: Dict[str, Any]) -> float:
        """计算智能水平"""
        components = []
        
        if result.get('problem_solving'):
            components.append(result['problem_solving'].get('confidence', 0.5))
        
        if result.get('learning'):
            components.append(0.7)
        
        if result.get('creativity'):
            components.append(result['creativity'].get('creativity_score', 0.5))
        
        if result.get('flexibility'):
            components.append(result['flexibility'].get('flexibility_score', 0.5))
        
        if not components:
            return 0.5
        
        return float(np.mean(components))
    
    def solve_problem(self, problem: Dict[str, Any], current_time: float = 0.0) -> Dict[str, Any]:
        """解决问题"""
        return self.problem_solving.solve(problem, current_time)
    
    def learn_from_experience(self, experience: Dict[str, Any], current_time: float = 0.0) -> Dict[str, Any]:
        """从经验学习"""
        return self.learning_system.learn(experience, current_time)
    
    def generate_creative_solution(self, problem: Dict[str, Any]) -> Dict[str, Any]:
        """生成创造性解决方案"""
        return self.creativity_engine.creative_problem_solving(problem)
    
    def get_capabilities(self) -> List[CognitiveCapability]:
        """获取能力"""
        return self.capabilities
