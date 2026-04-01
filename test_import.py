"""
测试RandomAgent模块
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("Python路径:", sys.path[:5])
print("\n当前目录:", os.getcwd())
print("\n目录内容:", os.listdir("."))

try:
    import random_agent
    print("\n✅ 成功导入 random_agent")
    print("版本:", random_agent.__version__)
    
    from random_agent import Agent
    print("\n✅ 成功导入 Agent")
    
except Exception as e:
    print(f"\n❌ 导入失败: {e}")
    import traceback
    traceback.print_exc()
