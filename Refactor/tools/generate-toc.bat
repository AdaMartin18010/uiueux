@echo off
chcp 65001 >nul
echo 🚀 Refactor 自动化工具启动中...

REM 检查Node.js是否安装
where node >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ 未检测到Node.js，请先安装Node.js
    echo 下载地址: https://nodejs.org/
    pause
    exit /b 1
)

REM 检查package.json是否存在
if not exist "package.json" (
    echo ❌ 未找到package.json文件
    pause
    exit /b 1
)

REM 安装依赖
echo 📦 安装依赖...
call npm install
if %errorlevel% neq 0 (
    echo ❌ 依赖安装失败
    pause
    exit /b 1
)

REM 运行工具
echo 🔧 运行自动化工具...
if "%1"=="" (
    echo 运行所有工具...
    call node generate-toc.js
) else (
    echo 运行指定工具: %1
    call node generate-toc.js %1
)

if %errorlevel% neq 0 (
    echo ❌ 工具运行失败
    pause
    exit /b 1
)

echo ✅ 任务完成！
pause 