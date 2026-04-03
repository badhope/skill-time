@echo off
chcp 65001 >nul
echo ============================================
echo   RandomAgent v0.3.0 - 一键启动器
echo ============================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到 Python，请先安装 Python 3.8+
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [1/4] 检查 RandomAgent 是否已安装...
pip show random-agent >nul 2>&1
if errorlevel 1 (
    echo.
    echo RandomAgent 尚未安装，正在安装...
    echo.
    cd /d "%~dp0"
    pip install -e .
    if errorlevel 1 (
        echo [错误] 安装失败，请检查 Python 和 pip 是否正常
        pause
        exit /b 1
    )
    echo.
    echo ✓ RandomAgent 安装成功！
) else (
    echo ✓ RandomAgent 已安装
)

echo.
echo [2/4] 检查配置...
if not exist "%USERPROFILE%\.random-agent\config.json" (
    echo.
    echo 首次使用，启动配置向导...
    echo.
    random-agent setup
) else (
    echo ✓ 配置文件已存在
)

echo.
echo [3/4] 选择启动模式:
echo.
echo   1. 交互式模式 (推荐新手)
echo      引导式界面，逐步生成提示词
echo.
echo   2. AI 对话模式
echo      直接与 AI 对话 (需要 Ollama 或 API Key)
echo.
echo   3. 效果演示
echo      查看不同模式的效果对比
echo.
echo   4. 命令行帮助
echo      查看所有可用命令
echo.
echo   0. 退出
echo.

set /p choice="请选择 (0-4): "

if "%choice%"=="1" goto interactive
if "%choice%"=="2" goto chat
if "%choice%"=="3" goto demo
if "%choice%"=="4" goto help
if "%choice%"=="0" goto end

echo 无效选择
pause
goto end

:interactive
echo.
echo 启动交互式模式...
echo.
random-agent interactive
goto end

:chat
echo.
echo 启动 AI 对话模式...
echo.
random-agent chat
goto end

:demo
echo.
echo 启动效果演示...
echo.
random-agent demo
goto end

:help
echo.
echo 显示帮助信息...
echo.
random-agent --help
goto end

:end
echo.
echo ============================================
echo   感谢使用 RandomAgent！
echo ============================================
echo.
echo 反馈和建议: https://github.com/badhope/skill-time/issues
echo 文档: https://github.com/badhope/skill-time#readme
echo.
pause
