#!/usr/bin/env python3
"""
RandomAgent 版本发布脚本

使用方法：
    python scripts/release.py --version 0.1.0
    python scripts/release.py --bump patch
    python scripts/release.py --bump minor
    python scripts/release.py --bump major
"""

import os
import sys
import argparse
import subprocess
import re
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def get_current_version():
    """从 __init__.py 获取当前版本"""
    init_file = os.path.join(os.path.dirname(__file__), "..", "random_agent", "__init__.py")
    with open(init_file, "r", encoding="utf-8") as f:
        content = f.read()
        match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', content)
        if match:
            return match.group(1)
    return "0.1.0"


def bump_version(version, bump_type):
    """升级版本号"""
    major, minor, patch = map(int, version.split("."))
    if bump_type == "major":
        major += 1
        minor = 0
        patch = 0
    elif bump_type == "minor":
        minor += 1
        patch = 0
    elif bump_type == "patch":
        patch += 1
    return f"{major}.{minor}.{patch}"


def update_version(version):
    """更新版本号"""
    init_file = os.path.join(os.path.dirname(__file__), "..", "random_agent", "__init__.py")
    with open(init_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    content = re.sub(
        r'__version__\s*=\s*["\'][^"\']+["\']',
        f'__version__ = "{version}"',
        content
    )
    
    with open(init_file, "w", encoding="utf-8") as f:
        f.write(content)
    
    setup_file = os.path.join(os.path.dirname(__file__), "..", "setup.py")
    with open(setup_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    content = re.sub(
        r'version\s*=\s*["\'][^"\']+["\']',
        f'version="{version}"',
        content
    )
    
    with open(setup_file, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"✅ 版本已更新为: {version}")


def run_tests():
    """运行测试"""
    print("\n🧪 运行测试...")
    try:
        result = subprocess.run(
            [sys.executable, "tests/test_random_agent.py", "-v"],
            cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            capture_output=True,
            text=True
        )
        print(result.stdout)
        if result.returncode != 0:
            print("❌ 测试失败！")
            return False
        print("✅ 所有测试通过！")
        return True
    except Exception as e:
        print(f"❌ 测试运行失败: {e}")
        return False


def build_package():
    """构建包"""
    print("\n📦 构建包...")
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "--upgrade", "build"],
            capture_output=True,
            text=True
        )
        
        result = subprocess.run(
            [sys.executable, "-m", "build"],
            cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            capture_output=True,
            text=True
        )
        print(result.stdout)
        if result.returncode != 0:
            print("❌ 构建失败！")
            return False
        print("✅ 构建成功！")
        return True
    except Exception as e:
        print(f"❌ 构建失败: {e}")
        return False


def create_git_tag(version):
    """创建 Git 标签"""
    print(f"\n🏷️  创建 Git 标签: v{version}")
    try:
        result = subprocess.run(
            ["git", "tag", f"v{version}"],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            print(f"⚠️  创建标签失败（可能已存在）: {result.stderr}")
        else:
            print(f"✅ 标签创建成功: v{version}")
        return True
    except Exception as e:
        print(f"⚠️  Git 操作失败: {e}")
        return True


def main():
    parser = argparse.ArgumentParser(
        description="RandomAgent 版本发布脚本",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  # 指定版本
  python scripts/release.py --version 0.2.0
  
  # 自动升级版本
  python scripts/release.py --bump patch  # 0.1.0 -> 0.1.1
  python scripts/release.py --bump minor  # 0.1.0 -> 0.2.0
  python scripts/release.py --bump major  # 0.1.0 -> 1.0.0
        """
    )
    
    parser.add_argument(
        "--version",
        help="指定版本号"
    )
    
    parser.add_argument(
        "--bump",
        choices=["patch", "minor", "major"],
        help="自动升级版本"
    )
    
    parser.add_argument(
        "--skip-tests",
        action="store_true",
        help="跳过测试"
    )
    
    parser.add_argument(
        "--skip-build",
        action="store_true",
        help="跳过构建"
    )
    
    parser.add_argument(
        "--skip-tag",
        action="store_true",
        help="跳过 Git 标签"
    )
    
    args = parser.parse_args()
    
    current_version = get_current_version()
    print(f"📌 当前版本: {current_version}")
    
    if args.version:
        version = args.version
    elif args.bump:
        version = bump_version(current_version, args.bump)
    else:
        print("❌ 请指定 --version 或 --bump")
        parser.print_help()
        sys.exit(1)
    
    print(f"🚀 发布版本: {version}")
    print(f"📅 发布时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    update_version(version)
    
    if not args.skip_tests:
        if not run_tests():
            sys.exit(1)
    
    if not args.skip_build:
        if not build_package():
            sys.exit(1)
    
    if not args.skip_tag:
        create_git_tag(version)
    
    print("\n" + "=" * 60)
    print(f"🎉 版本 {version} 发布准备完成！")
    print("=" * 60)
    print("\n下一步：")
    print("1. 检查 dist/ 目录下的构建文件")
    print("2. 运行 pip install -e . 测试安装")
    print("3. Git 提交并推送标签: git push && git push --tags")


if __name__ == "__main__":
    main()
