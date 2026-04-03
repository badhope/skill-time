#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RandomAgent 命令行工具 (CLI)

让非技术用户也能轻松使用 RandomAgent！

使用方式:
    random-agent generate "问题" [选项]
    random-agent chat [选项]
    random-agent interactive
    random-agent setup
    random-agent demo
    random-agent templates

示例:
    random-agent generate "什么是创造力？" --mode creative --randomness 0.7
    random-agent chat --provider ollama --model llama2
    random-agent interactive
"""

import sys
import os
import argparse
import json
from typing import Optional, Dict, Any, List


def cmd_generate(args):
    """生成提示词命令"""
    from random_agent import create_prompt, apply_template, get_template
    
    print("\n" + "=" * 60)
    print("RandomAgent 提示词生成器")
    print("=" * 60)
    
    if args.template:
        template = get_template(args.template)
        if not template:
            print(f"\n❌ 未找到模板: {args.template}")
            print("使用 'random-agent templates' 查看可用模板")
            return
        
        print(f"\n使用模板: {template['name']}")
        
        prompt = apply_template(
            template_name=args.template,
            task=args.task,
            randomness=args.randomness or template.get('randomness', 0.5),
            mode=args.mode or template.get('mode', 'balanced')
        )
    else:
        prompt = create_prompt(
            task=args.task,
            randomness=args.randomness,
            mode=args.mode,
            language=args.language
        )
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(prompt)
        print(f"\n✅ 提示词已保存到: {args.output}")
    else:
        print("\n生成的提示词:")
        print("-" * 60)
        print(prompt)
        print("-" * 60)
        
        if args.copy:
            import pyperclip
            pyperclip.copy(prompt)
            print("\n✅ 已复制到剪贴板！")


def cmd_chat(args):
    """直接与 AI 对话"""
    from random_agent import AIAgent, AIConfig, AIProvider
    
    print("\n" + "=" * 60)
    print("RandomAgent AI 对话模式")
    print("=" * 60)
    print(f"提供商: {args.provider}")
    print(f"模型: {args.model}")
    print("输入 'quit' 或 'exit' 退出")
    print("输入 'clear' 清空对话历史")
    print("-" * 60)
    
    try:
        config = AIConfig(
            provider=AIProvider(args.provider),
            model=args.model,
            base_url=args.base_url,
            randomness_level=args.randomness,
            thinking_mode=args.mode
        )
        
        agent = AIAgent(config)
        
        while True:
            try:
                user_input = input("\n你: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("\n再见！👋")
                    break
                    
                if user_input.lower() == 'clear':
                    agent.clear_history()
                    print("✅ 对话历史已清空")
                    continue
                    
                if not user_input:
                    continue
                
                print("\nAI 正在思考...", end="", flush=True)
                
                result = agent.think(user_input)
                
                print("\r" + " " * 20 + "\r")
                print(f"\nAI:\n{result['answer']}")
                
            except KeyboardInterrupt:
                print("\n\n已中断。输入 'quit' 退出")
                
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        print("\n可能的原因:")
        print("1. 未安装对应的 AI 库 (pip install openai / pip install anthropic)")
        print("2. API Key 未配置")
        print("3. Ollama 未运行 (如果使用 ollama 提供商)")
        print("")
        print("快速开始:")
        print("  - 使用 Ollama (免费，无需 API Key):")
        print("    1. 安装 Ollama: https://ollama.ai")
        print("    2. 运行: ollama serve")
        print("    3. 下载模型: ollama pull llama2")
        print("    4. 运行: random-agent chat --provider ollama")


def cmd_interactive(args):
    """交互式模式"""
    from random_agent import create_prompt, get_system_prompt_only
    
    print("\n" + "=" * 60)
    print("RandomAgent 交互式模式")
    print("=" * 60)
    print("这是一个引导式的交互界面，帮助你生成最佳提示词")
    print("-" * 60)
    
    current_config = {
        'task': '',
        'randomness': 0.5,
        'mode': 'balanced',
        'language': 'zh'
    }
    
    def show_current_config():
        print("\n当前配置:")
        print(f"  任务: {current_config['task'] or '(未设置)'}")
        print(f"  随机性: {current_config['randomness']}")
        print(f"  模式: {current_config['mode']}")
        print(f"  语言: {current_config['language']}")
    
    def show_help():
        print("""
可用命令:
  set task <内容>      - 设置任务/问题
  set randomness <值>   - 设置随机性 (0-1)
  set mode <模式>       - 设置思维模式 (creative/balanced/analytical/divergent/convergent)
  set language <语言>   - 设置语言 (zh/en)
  generate              - 生成完整提示词
  system                - 只生成系统提示词
  preview               - 预览配置效果
  config                - 显示当前配置
  template <名称>       - 使用预设模板
  templates             - 列出所有模板
  help                  - 显示帮助
  quit/exit             - 退出
""")
    
    show_help()
    
    while True:
        try:
            user_input = input("\n> ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\n再见！👋")
                break
            
            if user_input.lower() == 'help':
                show_help()
                continue
            
            if user_input.lower() == 'config':
                show_current_config()
                continue
            
            if user_input.lower() == 'generate':
                if not current_config['task']:
                    print("❌ 请先设置任务: set task <你的任务>")
                    continue
                    
                prompt = create_prompt(
                    task=current_config['task'],
                    randomness=current_config['randomness'],
                    mode=current_config['mode'],
                    language=current_config['language']
                )
                
                print("\n" + "=" * 60)
                print("生成的提示词:")
                print("=" * 60)
                print(prompt)
                print("=" * 60)
                continue
            
            if user_input.lower() == 'system':
                if not current_config['task']:
                    print("❌ 请先设置任务: set task <你的任务>")
                    continue
                    
                system_prompt = get_system_prompt_only(
                    randomness=current_config['randomness'],
                    mode=current_config['mode']
                )
                
                print("\n系统提示词:")
                print("-" * 60)
                print(system_prompt)
                print("-" * 60)
                continue
            
            if user_input.lower() == 'templates':
                from .templates import TEMPLATES
                print("\n可用模板:")
                for key, template in TEMPLATES.items():
                    print(f"  {key}: {template['name']} - {template['description']}")
                continue
            
            if user_input.startswith('template '):
                template_name = user_input[9:].strip()
                from .templates import TEMPLATES
                
                if template_name not in TEMPLATES:
                    print(f"❌ 未知模板: {template_name}")
                    print("输入 'templates' 查看所有可用模板")
                    continue
                
                template = TEMPLATES[template_name]
                current_config.update({
                    'randomness': template.get('randomness', 0.5),
                    'mode': template.get('mode', 'balanced')
                })
                
                print(f"✅ 已应用模板: {template['name']}")
                print(f"   描述: {template['description']}")
                show_current_config()
                continue
            
            if user_input.startswith('set '):
                parts = user_input[4:].split(' ', 1)
                if len(parts) != 2:
                    print("❌ 格式错误: set <参数> <值>")
                    continue
                
                key, value = parts
                
                if key == 'task':
                    current_config['task'] = value
                    print(f"✅ 任务已设置为: {value}")
                    
                elif key == 'randomness':
                    try:
                        val = float(value)
                        if 0 <= val <= 1:
                            current_config['randomness'] = val
                            print(f"✅ 随机性已设置为: {val}")
                        else:
                            print("❌ 随机性必须在 0-1 之间")
                    except ValueError:
                        print("❌ 无效的数值")
                        
                elif key == 'mode':
                    valid_modes = ['creative', 'balanced', 'analytical', 'divergent', 'convergent']
                    if value in valid_modes:
                        current_config['mode'] = value
                        print(f"✅ 模式已设置为: {value}")
                    else:
                        print(f"❌ 无效的模式。可选: {', '.join(valid_modes)}")
                        
                elif key == 'language':
                    current_config['language'] = value
                    print(f"✅ 语言已设置为: {value}")
                    
                else:
                    print(f"❌ 未知参数: {key}")
                continue
            
            if user_input == 'preview':
                if not current_config['task']:
                    print("❌ 请先设置任务: set task <你的任务>")
                    continue
                    
                print("\n预览:")
                print(f"  任务: {current_config['task']}")
                print(f"  随机性: {current_config['randomness']} ({'低' if current_config['randomness'] < 0.3 else '中' if current_config['randomness'] < 0.7 else '高'})")
                print(f"  模式: {current_config['mode']}")
                
                mode_descriptions = {
                    'creative': '最大化创造力和联想',
                    'balanced': '平衡发散和收敛',
                    'analytical': '侧重逻辑分析',
                    'divergent': '广泛探索多种可能',
                    'convergent': '聚焦形成结论'
                }
                print(f"  效果: {mode_descriptions.get(current_config['mode'], '')}")
                continue
            
            if not user_input:
                continue
                
            print(f"❌ 未知命令: {user_input}")
            print("输入 'help' 查看帮助")
            
        except KeyboardInterrupt:
            print("\n\n已中断。输入 'quit' 退出")


def cmd_setup(args):
    """配置向导"""
    print("\n" + "=" * 60)
    print("RandomAgent 配置向导")
    print("=" * 60)
    print("这将帮助你配置 RandomAgent 的基本设置\n")
    
    config = {
        'default_provider': 'ollama',
        'default_model': 'llama2',
        'api_keys': {}
    }
    
    print("步骤 1: 选择默认的 AI 提供商")
    print("-" * 40)
    providers = [
        ('1', 'Ollama (本地模型，免费)', 'ollama'),
        ('2', 'OpenAI (GPT-4 等)', 'openai'),
        ('3', 'Anthropic Claude', 'anthropic'),
    ]
    
    for num, desc, _ in providers:
        print(f"  {num}. {desc}")
    
    choice = input("\n选择 (默认 1-Ollama): ").strip() or '1'
    
    provider_map = {p[0]: p[2] for p in providers}
    if choice in provider_map:
        config['default_provider'] = provider_map[choice]
    
    if config['default_provider'] == 'ollama':
        config['default_model'] = input("模型名称 (默认 llama2): ").strip() or 'llama2'
        config['base_url'] = input("Ollama 地址 (默认 http://localhost:11434): ").strip() or 'http://localhost:11434'
        
    elif config['default_provider'] == 'openai':
        config['default_model'] = input("模型名称 (默认 gpt-4): ").strip() or 'gpt-4'
        api_key = input("API Key (留空则从环境变量读取): ").strip()
        if api_key:
            config['api_keys']['openai'] = api_key
            
    elif config['default_provider'] == 'anthropic':
        config['default_model'] = input("模型名称 (默认 claude-3-opus-20240229): ").strip() or 'claude-3-opus-20240229'
        api_key = input("API Key (留空则从环境变量读取): ").strip()
        if api_key:
            config['api_keys']['anthropic'] = api_key
    
    print("\n步骤 2: 默认随机性水平 (0-1)")
    print("-" * 40)
    print("  0 = 完全逻辑，1 = 完全随机")
    print("  推荐: 0.5-0.7 用于日常使用")
    
    try:
        randomness = float(input("随机性 (默认 0.5): ").strip() or '0.5')
        config['default_randomness'] = max(0, min(1, randomness))
    except ValueError:
        config['default_randomness'] = 0.5
    
    print("\n步骤 3: 保存配置")
    print("-" * 40)
    
    config_dir = os.path.expanduser("~/.random-agent")
    os.makedirs(config_dir, exist_ok=True)
    config_file = os.path.join(config_dir, "config.json")
    
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print(f"✅ 配置已保存到: {config_file}")
    print("\n配置摘要:")
    print(f"  提供商: {config['default_provider']}")
    print(f"  模型: {config.get('default_model', 'N/A')}")
    print(f"  随机性: {config.get('default_randomness', 0.5)}")
    print("\n现在你可以使用:")
    print("  random-agent chat          # 开始对话")
    print("  random-agent interactive   # 交互式模式")


def cmd_demo(args):
    """演示效果对比"""
    print("\n" + "=" * 60)
    print("RandomAgent 效果演示")
    print("=" * 60)
    
    from random_agent import create_prompt
    
    demo_questions = [
        ("创意写作", "写一个关于时间旅行的故事开头"),
        ("问题解决", "如何提高团队的工作效率？"),
        ("学习研究", "解释量子纠缠的概念"),
    ]
    
    for category, question in demo_questions:
        print(f"\n{'=' * 60}")
        print(f"场景: {category}")
        print(f"问题: {question}")
        print("-" * 60)
        
        print("\n[普通模式] randomness=0.2, mode=analytical")
        prompt_normal = create_prompt(question, randomness=0.2, mode="analytical")
        print(prompt_normal[:300] + "...\n")
        
        print("[增强模式] randomness=0.8, mode=creative")
        prompt_enhanced = create_prompt(question, randomness=0.8, mode="creative")
        print(prompt_enhanced[:300] + "...")
        
        input("\n按 Enter 继续...")
    
    print("\n" + "=" * 60)
    print("演示完成！")
    print("=" * 60)
    print("\n要体验实际效果，请运行:")
    print("  random-agent chat --provider ollama")
    print("或")
    print("  random-agent interactive")


def cmd_templates(args):
    """列出所有可用模板"""
    from random_agent import list_categories, list_templates
    
    print("\n" + "=" * 60)
    print("RandomAgent 预设模板")
    print("=" * 60)
    
    categories = list_categories()
    print(f"\n共有 {len(categories)} 个类别，{len(list_templates())} 个模板\n")
    
    for category in categories:
        templates = list_templates(category)
        print(f"【{category}】")
        for key, template in templates.items():
            print(f"\n  📋 {key}")
            print(f"     名称: {template['name']}")
            print(f"     描述: {template['description']}")
            print(f"     随机度: {template.get('randomness', 'N/A')}")
            if template.get('examples'):
                print(f"     示例:")
                for example in template['examples'][:2]:
                    print(f"       - {example}")
        print()
    
    print("\n使用方式:")
    print("  random-agent generate \"你的问题\" --template <模板名称>")
    print("\n示例:")
    print('  random-agent generate "写一首诗" --template creative_writing')
    print('  random-agent generate "如何提高效率" --template brainstorming')


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        prog='random-agent',
        description='RandomAgent - 让 AI 模拟人类直觉跳跃思维',
        epilog='示例: random-agent generate "什么是创造力？" --mode creative'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # generate 命令
    gen_parser = subparsers.add_parser('generate', help='生成提示词')
    gen_parser.add_argument('task', help='任务或问题')
    gen_parser.add_argument('--template', '-t', help='使用预设模板 (如 creative_writing, brainstorming)')
    gen_parser.add_argument('--randomness', '-r', type=float, default=0.5,
                           help='随机性水平 (0-1, 默认 0.5)')
    gen_parser.add_argument('--mode', '-m', default='balanced',
                           choices=['creative', 'balanced', 'analytical', 
                                   'divergent', 'convergent'],
                           help='思维模式 (默认 balanced)')
    gen_parser.add_argument('--language', '-l', default='zh',
                           help='语言 (默认 zh)')
    gen_parser.add_argument('--output', '-o', help='输出到文件')
    gen_parser.add_argument('--copy', '-c', action='store_true',
                           help='复制到剪贴板')
    
    # chat 命令
    chat_parser = subparsers.add_parser('chat', help='与 AI 对话')
    chat_parser.add_argument('--provider', '-p', default='ollama',
                            choices=['openai', 'anthropic', 'ollama'],
                            help='AI 提供商 (默认 ollama)')
    chat_parser.add_argument('--model', '-M', default='llama2',
                            help='模型名称 (默认 llama2)')
    chat_parser.add_argument('--base-url', '-b', help='API 基础 URL')
    chat_parser.add_argument('--randomness', '-r', type=float, default=0.5,
                            help='随机性水平 (默认 0.5)')
    chat_parser.add_argument('--mode', '-m', default='balanced',
                            choices=['creative', 'balanced', 'analytical',
                                    'divergent', 'convergent'],
                            help='思维模式 (默认 balanced)')
    
    # 其他命令
    subparsers.add_parser('interactive', help='交互式模式')
    subparsers.add_parser('setup', help='配置向导')
    subparsers.add_parser('demo', help='效果演示')
    subparsers.add_parser('templates', help='列出所有模板')
    
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        print("\n快速开始:")
        print("  random-agent setup          # 首次使用：运行配置向导")
        print("  random-agent interactive   # 交互式模式（推荐新手）")
        print("  random-agent demo           # 查看效果演示")
        return
    
    command_handlers = {
        'generate': cmd_generate,
        'chat': cmd_chat,
        'interactive': cmd_interactive,
        'setup': cmd_setup,
        'demo': cmd_demo,
        'templates': cmd_templates,
    }
    
    handler = command_handlers.get(args.command)
    if handler:
        handler(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
