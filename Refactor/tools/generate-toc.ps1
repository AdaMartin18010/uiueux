# Refactor 自动化工具 PowerShell 脚本
# 设置控制台编码为UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "🚀 Refactor 自动化工具启动中..." -ForegroundColor Green

# 检查Node.js是否安装
try {
    $nodeVersion = node --version 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Node.js 版本: $nodeVersion" -ForegroundColor Green
    } else {
        throw "Node.js not found"
    }
} catch {
    Write-Host "❌ 未检测到Node.js，请先安装Node.js" -ForegroundColor Red
    Write-Host "下载地址: https://nodejs.org/" -ForegroundColor Yellow
    Read-Host "按任意键退出"
    exit 1
}

# 检查package.json是否存在
if (-not (Test-Path "package.json")) {
    Write-Host "❌ 未找到package.json文件" -ForegroundColor Red
    Read-Host "按任意键退出"
    exit 1
}

# 安装依赖
Write-Host "📦 安装依赖..." -ForegroundColor Yellow
try {
    npm install
    if ($LASTEXITCODE -ne 0) {
        throw "npm install failed"
    }
    Write-Host "✅ 依赖安装完成" -ForegroundColor Green
} catch {
    Write-Host "❌ 依赖安装失败: $($_.Exception.Message)" -ForegroundColor Red
    Read-Host "按任意键退出"
    exit 1
}

# 运行工具
Write-Host "🔧 运行自动化工具..." -ForegroundColor Yellow
try {
    if ($args.Count -eq 0) {
        Write-Host "运行所有工具..." -ForegroundColor Cyan
        node generate-toc.js
    } else {
        Write-Host "运行指定工具: $($args[0])" -ForegroundColor Cyan
        node generate-toc.js $args[0]
    }
    
    if ($LASTEXITCODE -ne 0) {
        throw "Tool execution failed"
    }
    Write-Host "✅ 任务完成！" -ForegroundColor Green
} catch {
    Write-Host "❌ 工具运行失败: $($_.Exception.Message)" -ForegroundColor Red
    Read-Host "按任意键退出"
    exit 1
}

Read-Host "按任意键退出" 