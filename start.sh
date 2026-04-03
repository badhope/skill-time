#!/bin/bash
echo "============================================"
echo "  RandomAgent v0.3.0 - 一键启动器"
echo "============================================"
echo ""

if ! command -v python3 &> /dev/null; then
    echo "[错误] 未检测到 Python，请先安装 Python 3.8+"
    echo "下载地址: https://www.python.org/downloads/"
    exit 1
fi

echo "[1/4] 检查 RandomAgent 是否已安装..."
if ! pip3 show random-agent &> /dev/null; then
    echo ""
    echo "RandomAgent 尚未安装，正在安装..."
    echo ""
    cd "$(dirname "$0")"
    pip3 install -e .
    if [ $? -ne 0 ]; then
        echo "[错误] 安装失败，请检查 Python 和 pip 是否正常"
        exit 1
    fi
    echo ""
    echo "✓ RandomAgent 安装成功！"
else
    echo "✓ RandomAgent 已安装"
fi

echo ""
echo "[2/4] 检查配置..."
if [ ! -f "$HOME/.random-agent/config.json" ]; then
    echo ""
    echo "首次使用，启动配置向导..."
    echo ""
    random-agent setup
else
    echo "✓ 配置文件已存在"
fi

echo ""
echo "[3/4] 选择启动模式:"
echo ""
echo "  1. 交互式模式 (推荐新手)"
echo "     引导式界面，逐步生成提示词"
echo ""
echo "  2. AI 对话模式"
echo "     直接与 AI 对话 (需要 Ollama 或 API Key)"
echo ""
echo "  3. 效果演示"
echo "     查看不同模式的效果对比"
echo ""
echo "  4. 命令行帮助"
echo "     查看所有可用命令"
echo ""
echo "  0. 退出"
echo ""

read -p "请选择 (0-4): " choice

case $choice in
    1)
        echo ""
        echo "启动交互式模式..."
        echo ""
        random-agent interactive
        ;;
    2)
        echo ""
        echo "启动 AI 对话模式..."
        echo ""
        random-agent chat
        ;;
    3)
        echo ""
        echo "启动效果演示..."
        echo ""
        random-agent demo
        ;;
    4)
        echo ""
        echo "显示帮助信息..."
        echo ""
        random-agent --help
        ;;
    0)
        exit 0
        ;;
    *)
        echo "无效选择"
        exit 1
        ;;
esac

echo ""
echo "============================================"
echo "  感谢使用 RandomAgent！"
echo "============================================"
echo ""
echo "反馈和建议: https://github.com/badhope/skill-time/issues"
echo "文档: https://github.com/badhope/skill-time#readme"
echo ""
