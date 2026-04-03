#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RandomAgent 预设场景模板

提供开箱即用的使用场景配置，
让用户无需理解复杂参数即可快速开始使用。

使用方式:
    from random_agent.templates import TEMPLATES, get_template
    
    template = get_template("creative_writing")
    config = template.get_config()
"""

from typing import Dict, Any, Optional


TEMPLATES = {
    # ==================== 内容创作类 ====================
    
    "creative_writing": {
        "name": "创意写作",
        "description": "用于小说、诗歌、剧本等文学创作",
        "category": "内容创作",
        "randomness": 0.8,
        "mode": "creative",
        "system_prompt_addition": """你是一位富有创造力的作家。你的文字应该：
- 充满想象力和独特的视角
- 使用生动的比喻和隐喻
- 展现意想不到的转折
- 让读者感到惊喜和启发""",
        "examples": [
            "写一个关于时间旅行的科幻故事开头",
            "创作一首关于春天的现代诗",
            "写一段悬疑小说的情节"
        ],
        "tips": [
            "适合需要突破创作瓶颈时使用",
            "可以多次生成获取不同灵感",
            "结合具体主题效果更好"
        ]
    },
    
    "copywriting": {
        "name": "营销文案",
        "description": "用于广告、产品描述、推广文案",
        "category": "内容创作",
        "randomness": 0.6,
        "mode": "divergent",
        "system_prompt_addition": """你是一位资深文案策划。你的文案应该：
- 抓住目标受众的注意力
- 突出产品的独特卖点（USP）
- 使用有说服力的语言
- 创造情感共鸣""",
        "examples": [
            "为一款智能手表写广告文案",
            "撰写咖啡店的开业推广文案",
            "为在线课程写销售页面文案"
        ],
        "tips": [
            "提供产品特点和目标受众信息",
            "可以要求不同风格：正式/幽默/感性",
            "适合 A/B 测试不同版本"
        ]
    },
    
    "blog_post": {
        "name": "博客文章",
        "description": "用于技术博客、个人博客、行业文章",
        "category": "内容创作",
        "randomness": 0.5,
        "mode": "balanced",
        "system_prompt_addition": """你是一位专业的博主。你的文章应该：
- 结构清晰，易于阅读
- 提供有价值的信息或见解
- 使用恰当的例子和数据
- 引发读者的思考和讨论""",
        "examples": [
            "写一篇关于远程工作技巧的博客",
            "探讨 AI 对未来职业的影响",
            "分享学习编程的经验心得"
        ],
        "tips": [
            "指定目标读者群体",
            "提供关键词或主题方向",
            "可要求包含具体案例"
        ]
    },
    
    "social_media": {
        "name": "社交媒体",
        "description": "用于 Twitter、微博、小红书等平台内容",
        "category": "内容创作",
        "randomness": 0.7,
        "mode": "creative",
        "system_prompt_addition": """你是一位社交媒体运营专家。你的内容应该：
- 简洁有力，适合平台特性
- 容易引起互动和分享
- 使用适当的 emoji 和话题标签
- 展现个性化和人性化""",
        "examples": [
            "写一条关于工作效率的推文",
            "创作一条产品发布的微博",
            "写一篇小红书种草笔记"
        ],
        "tips": [
            "指定平台类型会有更好的适配",
            "控制字数在合适范围",
            "鼓励加入个人观点和经历"
        ]
    },
    
    # ==================== 问题解决类 ====================
    
    "brainstorming": {
        "name": "头脑风暴",
        "description": "用于产生多样化的想法和解决方案",
        "category": "问题解决",
        "randomness": 0.9,
        "mode": "divergent",
        "system_prompt_addition": """你是一位创新思维教练。在头脑风暴中你应该：
- 追求数量而非质量（先发散后收敛）
- 欢迎看似荒谬的想法
- 在他人想法基础上构建
- 延迟评判，鼓励大胆思考""",
        "examples": [
            "如何提高团队的工作效率？",
            "为新餐厅想一些创意菜单",
            "设计一款创新的智能家居产品"
        ],
        "tips": [
            "不要限制想法的范围",
            "可以分多轮进行，每轮聚焦不同角度",
            "记录所有想法后再筛选"
        ]
    },
    
    "problem_solving": {
        "name": "问题分析",
        "description": "用于系统性分析和解决复杂问题",
        "category": "问题解决",
        "randomness": 0.4,
        "mode": "analytical",
        "system_prompt_addition": """你是一位问题解决专家。你的分析应该：
- 明确定义问题的本质
- 从多个角度分析原因
- 提供结构化的解决方案
- 考虑实施的可行性和风险""",
        "examples": [
            "分析公司利润下降的原因",
            "解决项目延期的问题",
            "改善客户满意度低的现状"
        ],
        "tips": [
            "提供具体的背景信息和数据",
            "明确约束条件和资源限制",
            "要求分步骤给出解决方案"
        ]
    },
    
    "decision_making": {
        "name": "决策辅助",
        "description": "帮助做出重要决策，权衡利弊",
        "category": "问题解决",
        "randomness": 0.3,
        "mode": "convergent",
        "system_prompt_addition": """你是一位决策顾问。你的建议应该：
- 全面列出各选项的优缺点
- 考虑短期和长期影响
- 提供决策框架和方法论
- 帮助理清思路而非直接给答案""",
        "examples": [
            "是否应该接受新的工作offer？",
            "选择哪个技术栈来开发新产品？",
            "是否要创业还是继续打工？"
        ],
        "tips": [
            "提供所有相关因素和信息",
            "说明个人的价值观和优先级",
            "可以要求给出推荐但保留最终决定权"
        ]
    },
    
    # ==================== 学习研究类 ====================
    
    "learning_explanation": {
        "name": "概念解释",
        "description": "用简单易懂的方式解释复杂概念",
        "category": "学习研究",
        "randomness": 0.5,
        "mode": "balanced",
        "system_prompt_addition": """你是一位优秀的老师。你的解释应该：
- 用简单的语言解释复杂概念
- 使用类比和生活中的例子
- 循序渐进，由浅入深
- 检查理解程度并适时总结""",
        "examples": [
            "用量子力学的原理解释什么是量子计算",
            "像对5岁孩子一样解释区块链",
            "用日常例子说明机器学习的工作原理"
        ],
        "tips": [
            "指定目标受众的知识水平",
            "可以要求用特定领域类比",
            "适合学习和教学场景"
        ]
    },
    
    "research_assistant": {
        "name": "研究助手",
        "description": "协助进行文献综述、理论分析、假设生成",
        "category": "学习研究",
        "randomness": 0.4,
        "mode": "analytical",
        "system_prompt_addition": """你是一位学术研究助手。你的支持应该：
- 基于现有知识和逻辑推理
- 提供多个视角和理论框架
- 指出知识空白和研究机会
- 保持客观和批判性思维""",
        "examples": [
            "分析人工智能伦理的主要争议",
            "探讨远程工作对组织文化的影响",
            "评估可持续发展的技术路径"
        ],
        "tips": [
            "明确研究领域和具体问题",
            "可以要求引用相关理论和研究",
            "适合学术论文写作的前期准备"
        ]
    },
    
    "idea_development": {
        "name": "想法深化",
        "description": "将初步想法发展成完整的方案或计划",
        "category": "学习研究",
        "randomness": 0.6,
        "mode": "divergent",
        "system_prompt_addition": """你是一位创意开发专家。在深化想法时你应该：
- 探索想法的各种可能性
- 识别潜在的挑战和机遇
- 提供实施的具体步骤
- 连接相关的概念和资源""",
        "examples": [
            "将'做一个AI写作助手'的想法发展为完整的产品方案",
            '深化"社区共享厨房"的创业想法',
            "探索'个性化教育平台'的实现路径"
        ],
        "tips": [
            "清晰描述初始想法的核心",
            "说明目标和期望成果",
            "可以要求考虑不同的商业模式"
        ]
    },
    
    # ==================== 日常生活类 ====================
    
    "daily_chat": {
        "name": "日常聊天",
        "description": "更有趣、更有人情味的日常对话",
        "category": "日常生活",
        "randomness": 0.6,
        "mode": "balanced",
        "system_prompt_addition": """你是一个有趣的聊天伙伴。在对话中你应该：
- 展现真实的兴趣和好奇心
- 分享个人观点和经历
- 适当幽默但不刻意
- 能够进行深度的闲聊""",
        "examples": [
            "今天天气真好，你觉得呢？",
            "最近有什么有趣的事情吗？",
            "你觉得人生的意义是什么？"
        ],
        "tips": [
            "像和朋友聊天一样自然",
            "可以分享自己的感受和故事",
            "适合放松和获得新视角"
        ]
    },
    
    "life_advice": {
        "name": "生活建议",
        "description": "获得生活各方面的建议和指导",
        "category": "日常生活",
        "randomness": 0.5,
        "mode": "balanced",
        "system_prompt_addition": """你是一位睿智的生活导师。你的建议应该：
- 基于经验和智慧而非教条
- 考虑个体差异和具体情况
- 提供实用的行动建议
- 鼓励自我反思和成长""",
        "examples": [
            "如何克服拖延症？",
            "怎样维持长期的人际关系？",
            "如何在工作和生活之间找到平衡？"
        ],
        "tips": [
            "分享具体情况会得到更有针对性的建议",
            "保持开放心态，建议仅供参考",
            "可以追问深入某个方面"
        ]
    },
    
    "creative_inspiration": {
        "name": "创意灵感",
        "description": "寻找创意灵感和新思路",
        "category": "日常生活",
        "randomness": 0.85,
        "mode": "creative",
        "system_prompt_addition": """你是灵感的源泉。在激发创造力时你应该：
- 打破常规思维模式
- 连接不相关的事物
- 提出令人惊讶的问题
- 开启全新的视角""",
        "examples": [
            "给我一些关于'时间'的创意联想",
            "如果动物会说话，世界会怎样？",
            "重新定义'成功'这个概念"
        ],
        "tips": [
            "开放心态，接受所有想法",
            "适合创意工作者和设计师",
            "可以作为头脑风暴的热身"
        ]
    },
    
    # ==================== 专业领域类 ====================
    
    "business_strategy": {
        "name": "商业策略",
        "description": "制定和分析商业策略",
        "category": "专业领域",
        "randomness": 0.5,
        "mode": "analytical",
        "system_prompt_addition": """你是一位经验丰富的战略顾问。你的分析应该：
- 基于市场和竞争分析
- 考虑商业模式和盈利能力
- 评估风险和机会
- 提供可执行的策略建议""",
        "examples": [
            "为一家初创公司制定市场进入策略",
            "分析传统零售业的数字化转型",
            "评估扩张到国际市场的可行性"
        ],
        "tips": [
            "提供行业背景和公司情况",
            "明确战略目标和约束条件",
            "适合创业者和管理者"
        ]
    },
    
    "code_review": {
        "name": "代码审查",
        "description": "代码审查、重构建议、最佳实践",
        "category": "专业领域",
        "randomness": 0.3,
        "mode": "analytical",
        "system_prompt_addition": """你是一位高级软件工程师。在代码审查时你应该：
- 关注代码质量和可维护性
- 识别潜在的问题和 bug
- 建议改进和优化方案
- 分享最佳实践和设计模式""",
        "examples": [
            "审查这段 Python 代码的质量",
            "建议如何优化数据库查询性能",
            "评估这个架构设计的优劣"
        ],
        "tips": [
            "提供代码片段或详细描述",
            "说明技术栈和上下文",
            "可以要求特定关注点（安全/性能/可读性）"
        ]
    },
    
    "interview_prep": {
        "name": "面试准备",
        "description": "面试模拟、问题准备、回答优化",
        "category": "专业领域",
        "randomness": 0.4,
        "mode": "balanced",
        "system_prompt_addition": """你是一位面试教练。你的帮助应该：
- 模拟真实面试环境
- 提供行为面试问题的 STAR 回答框架
- 帮助突出优势和成就
- 给予建设性的反馈和建议""",
        "examples": [
            "模拟一次产品经理的技术面试",
            "帮我准备'你最大的弱点是什么'这个问题",
            "优化我对领导力经验的描述"
        ],
        "tips": [
            "说明职位和公司背景",
            "分享自己的经历和成就",
            "可以进行多轮模拟练习"
        ]
    }
}


def get_template(template_name: str) -> Optional[Dict[str, Any]]:
    """
    获取指定模板
    
    Args:
        template_name: 模板名称
        
    Returns:
        模板字典，如果不存在则返回 None
    """
    return TEMPLATES.get(template_name)


def list_templates(category: Optional[str] = None) -> Dict[str, Dict[str, Any]]:
    """
    列出可用模板
    
    Args:
        category: 可选，筛选特定类别
        
    Returns:
        模板字典
    """
    if category:
        return {k: v for k, v in TEMPLATES.items() if v.get('category') == category}
    return TEMPLATES


def list_categories() -> list:
    """
    列出所有类别
    
    Returns:
        类别列表
    """
    categories = set()
    for template in TEMPLATES.values():
        if 'category' in template:
            categories.add(template['category'])
    return sorted(list(categories))


def get_template_for_task(task_description: str) -> Optional[Dict[str, Any]]:
    """
    根据任务描述自动推荐最适合的模板
    
    Args:
        task_description: 任务描述
        
    Returns:
        最匹配的模板
    """
    task_lower = task_description.lower()
    
    keywords_mapping = {
        "creative_writing": ["写", "创作", "小说", "故事", "诗", "剧本"],
        "copywriting": ["文案", "广告", "营销", "推广", "卖点"],
        "blog_post": ["博客", "文章", "教程", "分享"],
        "social_media": ["社交媒体", "推特", "微博", "小红书", "朋友圈"],
        "brainstorming": ["头脑风暴", "想法", "创意", "点子", "灵感"],
        "problem_solving": ["解决问题", "分析", "挑战", "困难"],
        "decision_making": ["决定", "选择", "决策", "取舍"],
        "learning_explanation": ["解释", "什么是", "原理", "概念", "教学"],
        "research_assistant": ["研究", "论文", "文献", "综述", "学术"],
        "idea_development": ["发展", "深化", "完善", "扩展"],
        "daily_chat": ["聊天", "对话", "闲聊"],
        "life_advice": ["建议", "怎么办", "如何", "生活"],
        "creative_inspiration": ["灵感", "创意", "联想", "想象"],
        "business_strategy": ["商业", "策略", "市场", "竞争"],
        "code_review": ["代码", "编程", "审查", "优化"],
        "interview_prep": ["面试", "求职", "简历"]
    }
    
    scores = {}
    for template_name, keywords in keywords_mapping.items():
        score = sum(1 for keyword in keywords if keyword in task_lower)
        if score > 0:
            scores[template_name] = score
    
    if scores:
        best_match = max(scores.keys(), key=lambda x: scores[x])
        return TEMPLATES.get(best_match)
    
    return None


def apply_template(template_name: str, task: str, **kwargs):
    """
    应用模板生成提示词
    
    Args:
        template_name: 模板名称
        task: 任务或问题
        **kwargs: 其他参数
        
    Returns:
        生成的提示词
    """
    from .prompt_templates import create_prompt
    
    template = get_template(template_name)
    if not template:
        raise ValueError(f"未知模板: {template_name}")
    
    randomness = kwargs.get('randomness', template.get('randomness', 0.5))
    mode = kwargs.get('mode', template.get('mode', 'balanced'))
    
    prompt = create_prompt(
        task=task,
        randomness=randomness,
        mode=mode
    )
    
    if template.get('system_prompt_addition'):
        prompt += f"\n\n{template['system_prompt_addition']}"
    
    return prompt


if __name__ == "__main__":
    print("RandomAgent 预设模板")
    print("=" * 60)
    
    categories = list_categories()
    print(f"\n共有 {len(TEMPLATES)} 个模板，分为 {len(categories)} 个类别:\n")
    
    for category in categories:
        templates = list_templates(category)
        print(f"\n【{category}】")
        for key, template in templates.items():
            print(f"  - {key}: {template['name']}")
            print(f"    {template['description']}")
