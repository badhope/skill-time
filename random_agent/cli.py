#!/usr/bin/env python3
"""
RandomAgent CLI - 命令行工具

使用方法：
    python -m random_agent.cli "你的问题"
    python -m random_agent.cli --prompt "问题" --randomness 0.7
    python -m random_agent.cli --system-prompt --mode creative
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def main():
    parser = argparse.ArgumentParser(
        description="RandomAgent - 模拟人类直觉跳跃思维的提示词工程框架",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  # 生成提示词
  python -m random_agent.cli "什么是创造力？"
  
  # 指定随机性和模式
  python -m random_agent.cli "如何创新？" --randomness 0.8 --mode creative
  
  # 仅获取系统提示词
  python -m random_agent.cli --system-prompt --mode balanced
  
  # 精简版提示词
  python -m random_agent.cli "问题" --style concise
  
  # 调用 AI（需要设置 API Key）
  python -m random_agent.cli "问题" --call-ai --provider openai --model gpt-4
        """
    )
    
    parser.add_argument(
        "question",
        nargs="?",
        help="要思考的问题"
    )
    
    parser.add_argument(
        "--randomness", "-r",
        type=float,
        default=0.5,
        help="随机性水平 (0.0-1.0)，默认 0.5"
    )
    
    parser.add_argument(
        "--mode", "-m",
        choices=["divergent", "convergent", "balanced", "creative", "analytical"],
        default="balanced",
        help="思维模式，默认 balanced"
    )
    
    parser.add_argument(
        "--style", "-s",
        choices=["detailed", "concise"],
        default="detailed",
        help="提示词风格，默认 detailed"
    )
    
    parser.add_argument(
        "--system-prompt",
        action="store_true",
        help="仅输出系统提示词"
    )
    
    parser.add_argument(
        "--call-ai",
        action="store_true",
        help="调用真实 AI API"
    )
    
    parser.add_argument(
        "--provider", "-p",
        choices=["openai", "anthropic", "ollama"],
        default="openai",
        help="AI 提供商，默认 openai"
    )
    
    parser.add_argument(
        "--model",
        default=None,
        help="AI 模型名称"
    )
    
    parser.add_argument(
        "--api-key",
        default=None,
        help="API Key（也可通过环境变量设置）"
    )
    
    parser.add_argument(
        "--output", "-o",
        choices=["text", "json"],
        default="text",
        help="输出格式，默认 text"
    )
    
    args = parser.parse_args()
    
    from random_agent.prompt_templates import create_prompt, get_system_prompt_only
    from random_agent.ai_integration import create_ai_agent
    
    if args.system_prompt:
        system_prompt = get_system_prompt_only(
            randomness=args.randomness,
            mode=args.mode
        )
        print(system_prompt)
        return
    
    if not args.question:
        parser.print_help()
        print("\n❌ 错误：请提供问题，或使用 --system-prompt 获取系统提示词")
        sys.exit(1)
    
    if args.call_ai:
        try:
            agent = create_ai_agent(
                provider=args.provider,
                model=args.model,
                api_key=args.api_key,
                randomness=args.randomness,
                thinking_mode=args.mode
            )
            
            print(f"🤖 正在调用 {args.provider} ({args.model or 'default'})...")
            print(f"   随机性: {args.randomness:.0%}, 模式: {args.mode}")
            print("-" * 60)
            
            result = agent.think(args.question)
            
            if args.output == "json":
                import json
                print(json.dumps(result, ensure_ascii=False, indent=2))
            else:
                print(result["answer"])
                print("\n" + "-" * 60)
                print(f"⏱️  耗时: {result['elapsed_time']:.2f}s")
            
        except Exception as e:
            print(f"❌ 调用失败: {e}")
            sys.exit(1)
    else:
        prompt = create_prompt(
            task=args.question,
            randomness=args.randomness,
            mode=args.mode,
            style=args.style
        )
        
        if args.output == "json":
            import json
            output = {
                "question": args.question,
                "randomness": args.randomness,
                "mode": args.mode,
                "style": args.style,
                "prompt": prompt
            }
            print(json.dumps(output, ensure_ascii=False, indent=2))
        else:
            print("=" * 60)
            print(f"📝 RandomAgent 提示词")
            print(f"   问题: {args.question}")
            print(f"   随机性: {args.randomness:.0%}")
            print(f"   模式: {args.mode}")
            print("=" * 60)
            print()
            print(prompt)
            print()
            print("=" * 60)
            print("💡 提示：使用 --call-ai 可以直接调用 AI API")
            print("=" * 60)


if __name__ == "__main__":
    main()
