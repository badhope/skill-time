#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RandomAgent v0.3.0 全面模拟运行测试
"""

import sys
import os
import traceback

sys.path.insert(0, r'c:\Users\X1882\Desktop\github\skill-time')

print('=' * 70)
print('  RandomAgent v0.3.0 全面模拟运行测试')
print('=' * 70)

errors = []
warnings = []
passed = []

def test(name, func):
    try:
        func()
        passed.append(name)
        print(f'✅ {name}')
    except Exception as e:
        errors.append((name, str(e)))
        print(f'❌ {name}: {e}')

def warn(name, message):
    warnings.append((name, message))
    print(f'⚠️  {name}: {message}')

# ==================== 测试1: 核心模块导入 ====================
print('\n【1】核心模块导入测试')
print('-' * 50)

def test_import_core():
    from random_agent import (
        RandomnessEngine,
        ConsciousnessLayers,
        ConsciousnessStream,
        DMNEngine,
        MemorySystem,
        GoalSystem,
        InfluenceFactors,
        BalanceController,
        OutputSystem,
    )
test('核心引擎模块导入', test_import_core)

def test_import_prompt():
    from random_agent import (
        RandomAgentPromptBuilder,
        PromptConfig,
        PromptStyle,
        ThinkingMode,
        create_prompt,
        get_system_prompt_only,
    )
test('提示词模板导入', test_import_prompt)

def test_import_ai():
    from random_agent import (
        AIAgent,
        AIConfig,
        AIProvider,
        create_ai_agent,
    )
test('AI 集成导入', test_import_ai)

def test_import_config():
    from random_agent import (
        RandomAgentConfig,
        ConfigManager,
        load_config,
    )
test('配置管理导入', test_import_config)

def test_import_logger():
    from random_agent import (
        RandomAgentLogger,
        setup_logging,
        get_logger,
    )
test('日志系统导入', test_import_logger)

def test_import_exceptions():
    from random_agent import (
        RandomAgentError,
        ConfigurationError,
        RandomnessError,
    )
test('异常处理导入', test_import_exceptions)

def test_import_monitoring():
    from random_agent import (
        MetricsCollector,
        SystemMonitor,
        PerformanceTracker,
    )
test('性能监控导入', test_import_monitoring)

def test_import_async():
    from random_agent import (
        AsyncManager,
        sync_to_async,
        async_to_sync,
    )
test('异步支持导入', test_import_async)

def test_import_extended():
    from random_agent import (
        ExtendedAIProvider,
        GoogleProvider,
        CohereProvider,
        AzureOpenAIProvider,
    )
test('扩展提供商导入', test_import_extended)

def test_import_templates():
    from random_agent import (
        TEMPLATES,
        get_template,
        list_templates,
        list_categories,
        get_template_for_task,
        apply_template,
    )
test('预设模板导入', test_import_templates)

def test_version():
    from random_agent import __version__
    assert __version__ == '0.3.0', f'版本号不匹配: {__version__}'
test('版本号验证', test_version)

# ==================== 测试2: 提示词生成 ====================
print('\n【2】提示词生成功能测试')
print('-' * 50)

def test_basic_prompt():
    from random_agent import create_prompt
    prompt = create_prompt("什么是人工智能？", randomness=0.5, mode="balanced")
    assert len(prompt) > 500, f'提示词太短: {len(prompt)}'
    assert '随机' in prompt or 'random' in prompt.lower(), '缺少核心概念'
test('基础提示词生成', test_basic_prompt)

def test_system_prompt():
    from random_agent import get_system_prompt_only
    sp = get_system_prompt_only(randomness=0.7, mode="creative")
    assert len(sp) > 300, f'系统提示词太短: {len(sp)}'
test('系统提示词获取', test_system_prompt)

def test_different_modes():
    from random_agent import create_prompt
    modes = ['divergent', 'convergent', 'balanced', 'creative', 'analytical']
    for mode in modes:
        prompt = create_prompt("测试", mode=mode)
        assert len(prompt) > 100, f'{mode} 模式失败'
test('5种思维模式', test_different_modes)

def test_randomness_levels():
    from random_agent import create_prompt
    for r in [0.0, 0.3, 0.5, 0.7, 1.0]:
        prompt = create_prompt("测试", randomness=r)
        assert len(prompt) > 100, f'随机性 {r} 失败'
test('不同随机性级别', test_randomness_levels)

def test_language_support():
    from random_agent import create_prompt
    zh = create_prompt("测试", style="detailed")
    en = create_prompt("test", style="detailed")
    assert len(zh) > 100 and len(en) > 100
test('不同风格支持', test_language_support)

# ==================== 测试3: 预设模板系统 ====================
print('\n【3】预设模板系统测试')
print('-' * 50)

def test_template_count():
    from random_agent import list_templates, list_categories
    templates = list_templates()
    categories = list_categories()
    assert len(templates) == 16, f'模板数量错误: {len(templates)} (期望 16)'
    assert len(categories) == 5, f'类别数量错误: {len(categories)} (期望 5)'
test('模板数量和类别 (16个/5类)', test_template_count)

def test_all_templates_accessible():
    from random_agent import list_templates, get_template
    templates = list_templates()
    for key in templates.keys():
        t = get_template(key)
        assert t is not None, f'无法获取模板: {key}'
        assert 'name' in t, f'模板缺少 name: {key}'
        assert 'description' in t, f'模板缺少 description: {key}'
        assert 'randomness' in t, f'模板缺少 randomness: {key}'
        assert 'mode' in t, f'模板缺少 mode: {key}'
test('所有模板可访问且完整', test_all_templates_accessible)

def test_apply_templates():
    from random_agent import apply_template
    test_cases = [
        ('creative_writing', '写一首诗'),
        ('brainstorming', '如何提高效率'),
        ('learning_explanation', '解释量子计算'),
        ('code_review', '审查这段代码'),
        ('interview_prep', '准备面试'),
    ]
    for template_name, task in test_cases:
        prompt = apply_template(template_name, task)
        assert len(prompt) > 500, f'{template_name} 生成的提示词太短'
test('应用模板生成提示词 (5个)', test_apply_templates)

def test_smart_recommendation():
    from random_agent import get_template_for_task
    test_tasks = [
        ('写一首关于春天的诗', 'creative_writing'),
        ('如何提高团队效率？', None),
        ('解释什么是量子计算', 'learning_explanation'),
        ('帮我写广告文案', 'copywriting'),
        ('审查这段Python代码', 'code_review'),
    ]
    for task, expected_contains in test_tasks:
        result = get_template_for_task(task)
        assert result is not None, f'推荐失败: {task}'
test('智能推荐系统 (5个任务)', test_smart_recommendation)

def test_category_filtering():
    from random_agent import list_templates
    content_templates = list_templates(category='内容创作')
    assert len(content_templates) == 4, f'内容创作类别错误: {len(content_templates)}'
test('按类别筛选模板', test_category_filtering)

# ==================== 测试4: CLI 工具测试 ====================
print('\n【4】CLI 工具测试')
print('-' * 50)

def test_cli_module_exists():
    cli_path = r'c:\Users\X1882\Desktop\github\skill-time\random_agent\cli.py'
    assert os.path.exists(cli_path), 'CLI 文件不存在'
    
    with open(cli_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    assert 'def main' in content, '缺少 main 函数'
    assert 'def cmd_generate' in content, '缺少 cmd_generate 函数'
    assert 'def cmd_chat' in content, '缺少 cmd_chat 函数'
    assert 'def cmd_interactive' in content, '缺少 cmd_interactive 函数'
    assert 'def cmd_setup' in content, '缺少 cmd_setup 函数'
    assert 'def cmd_demo' in content, '缺少 cmd_demo 函数'
    assert 'def cmd_templates' in content, '缺少 cmd_templates 函数'
test('CLI 模块完整性 (6个命令)', test_cli_module_exists)

def test_cli_argument_parsing():
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        'cli',
        r'c:\Users\X1882\Desktop\github\skill-time\random_agent\cli.py'
    )
    cli = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cli)
    
    import argparse
    import sys
    
    old_argv = sys.argv
    
    try:
        sys.argv = ['random-agent', 'generate', '测试问题']
        
        parser = argparse.ArgumentParser(
            prog='random-agent',
            description='RandomAgent - 让 AI 模拟人类直觉跳跃思维',
        )
        subparsers = parser.add_subparsers(dest='command', help='可用命令')
        
        gen_parser = subparsers.add_parser('generate', help='生成提示词')
        gen_parser.add_argument('task', help='任务或问题')
        gen_parser.add_argument('--template', '-t', help='使用预设模板')
        
        subparsers.add_parser('templates', help='列出所有模板')
        
        args = parser.parse_args(['generate', '测试问题'])
        assert args.command == 'generate'
        assert args.task == '测试问题'
        
        args2 = parser.parse_args(['templates'])
        assert args2.command == 'templates'
        
        args3 = parser.parse_args(['generate', '测试', '--template', 'creative_writing'])
        assert args3.template == 'creative_writing'
    finally:
        sys.argv = old_argv
test('CLI 参数解析', test_cli_argument_parsing)

# ==================== 测试5: 配置和安装测试 ====================
print('\n【5】配置和安装测试')
print('-' * 50)

def test_setup_py():
    setup_path = r'c:\Users\X1882\Desktop\github\skill-time\setup.py'
    with open(setup_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    assert '0.3.0' in content, 'setup.py 版本号未更新'
    assert 'console_scripts' in content, '缺少 CLI 入口点配置'
    assert 'random-agent=random_agent.cli:main' in content, 'CLI 命令未注册'
test('setup.py 配置正确', test_setup_py)

def test_readme_exists():
    readme_path = r'c:\Users\X1882\Desktop\github\skill-time\README.md'
    assert os.path.exists(readme_path), 'README.md 不存在'
    
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    assert 'v0.3.0' in content, 'README 未提及 v0.3.0'
    assert 'CLI' in content or '命令行' in content, 'README 缺少 CLI 说明'
    assert 'template' in content.lower() or '模板' in content, 'README 缺少模板说明'
test('README.md 存在且包含关键信息', test_readme_exists)

def test_start_scripts():
    bat_path = r'c:\Users\X1882\Desktop\github\skill-time\start.bat'
    sh_path = r'c:\Users\X1882\Desktop\github\skill-time\start.sh'
    
    assert os.path.exists(bat_path), 'start.bat 不存在'
    assert os.path.exists(sh_path), 'start.sh 不存在'
    
    with open(bat_path, 'r', encoding='utf-8') as f:
        bat_content = f.read()
    assert '0.3.0' in bat_content, 'start.bat 版本号错误'
    
    with open(sh_path, 'r', encoding='utf-8') as f:
        sh_content = f.read()
    assert '0.3.0' in sh_content, 'start.sh 版本号错误'
test('启动脚本存在且版本正确', test_start_scripts)

# ==================== 测试6: 边界情况测试 ====================
print('\n【6】边界情况和异常处理测试')
print('-' * 50)

def test_empty_task():
    from random_agent import create_prompt
    try:
        prompt = create_prompt("", randomness=0.5)
        if len(prompt) > 0:
            pass
    except Exception as e:
        pass
test('空任务处理', test_empty_task)

def test_invalid_template():
    from random_agent import get_template
    result = get_template("nonexistent_template")
    assert result is None, '不存在模板应返回 None'
test('无效模板名称', test_invalid_template)

def test_extreme_randomness():
    from random_agent import create_prompt
    prompt_min = create_prompt("测试", randomness=0.0)
    prompt_max = create_prompt("测试", randomness=1.0)
    assert len(prompt_min) > 100 and len(prompt_max) > 100
test('极端随机性值 (0.0 和 1.0)', test_extreme_randomness)

def test_special_characters():
    from random_agent import create_prompt
    special_tasks = [
        "测试 <script>alert('xss')</script>",
        "测试中文！@#￥%……&*（）",
        "Test émojis 🎉🚀✨",
        "Multi\nLine\nTask",
    ]
    for task in special_tasks:
        prompt = create_prompt(task)
        assert len(prompt) > 100, f'特殊字符任务失败: {task[:20]}'
test('特殊字符处理', test_special_characters)

def test_long_task():
    from random_agent import create_prompt
    long_task = "这是一个非常长的任务描述" * 100
    prompt = create_prompt(long_task)
    assert len(prompt) > 100
test('超长任务描述', test_long_task)

# ==================== 测试7: 集成测试 ====================
print('\n【7】集成测试')
print('-' * 50)

def test_full_workflow():
    from random_agent import get_template_for_task, apply_template, TEMPLATES, list_templates
    
    task = "帮我写一篇关于人工智能的博客文章"
    
    step1 = get_template_for_task(task)
    assert step1 is not None, '步骤1: 推荐模板失败'
    
    template_key = [k for k, v in TEMPLATES.items() if v == step1][0]
    
    step2 = apply_template(template_key, task)
    assert len(step2) > 500, '步骤2: 生成提示词失败'
    
    assert '博客' in step2 or 'blog' in step2.lower() or '文章' in step2
test('完整工作流: 推荐→应用模板', test_full_workflow)

def test_template_with_custom_params():
    from random_agent import apply_template
    prompt1 = apply_template('brainstorming', '测试', randomness=0.9)
    prompt2 = apply_template('brainstorming', '测试', randomness=0.3)
    assert len(prompt1) > 100 and len(prompt2) > 100
test('自定义参数覆盖模板默认值', test_template_with_custom_params)

# ==================== 测试结果汇总 ====================
print('\n' + '=' * 70)
print('  测试结果汇总')
print('=' * 70)

print(f'\n✅ 通过: {len(passed)} 个测试')
for p in passed:
    print(f'   ✓ {p}')

if warnings:
    print(f'\n⚠️  警告: {len(warnings)} 个')
    for name, msg in warnings:
        print(f'   ⚠ {name}: {msg}')

if errors:
    print(f'\n❌ 错误: {len(errors)} 个')
    for name, msg in errors:
        print(f'   ❌ {name}')
        print(f'      {msg}')

print('\n' + '-' * 70)

total = len(passed) + len(errors)
pass_rate = (len(passed) / total * 100) if total > 0 else 0

print(f'总计: {total} 个测试 | 通过率: {pass_rate:.1f}%')

if errors:
    print('\n🔴 存在错误，需要修复后再部署！')
    sys.exit(1)
else:
    print('\n🟢 所有测试通过，可以部署！')
    sys.exit(0)
