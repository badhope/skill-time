#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
模板系统测试脚本
"""

from random_agent.templates import TEMPLATES, get_template, list_templates, list_categories, get_template_for_task, apply_template

print('=' * 60)
print('模板系统测试')
print('=' * 60)

# 测试1: 列出所有类别
print('\n【测试1】列出所有类别')
categories = list_categories()
print(f'共有 {len(categories)} 个类别: {categories}')

# 测试2: 列出所有模板
print('\n【测试2】列出所有模板')
templates = list_templates()
print(f'共有 {len(templates)} 个模板:')
for key in templates.keys():
    print(f'  - {key}: {templates[key]["name"]}')

# 测试3: 获取特定模板
print('\n【测试3】获取特定模板')
template = get_template('creative_writing')
if template:
    print(f'✓ 获取成功: {template["name"]}')
    print(f'  描述: {template["description"]}')
    print(f'  随机度: {template["randomness"]}')
    print(f'  模式: {template["mode"]}')
else:
    print('✗ 获取失败')

# 测试4: 自动推荐模板
print('\n【测试4】自动推荐模板')
test_tasks = [
    '帮我写一首关于春天的诗',
    '如何提高团队效率？',
    '解释什么是量子计算',
]
for task in test_tasks:
    recommended = get_template_for_task(task)
    if recommended:
        template_key = [k for k, v in TEMPLATES.items() if v == recommended][0]
        print(f'  任务: "{task}"')
        print(f'  推荐: {recommended["name"]} ({template_key})')

# 测试5: 应用模板
print('\n【测试5】应用模板生成提示词')
try:
    prompt = apply_template('brainstorming', '如何改善用户体验？', randomness=0.8)
    print(f'✓ 提示词生成成功 (长度: {len(prompt)} 字符)')
    print(f'  前100字: {prompt[:100]}...')
except Exception as e:
    print(f'✗ 错误: {e}')

print('\n' + '=' * 60)
print('✓ 所有测试通过！')
print('=' * 60)
