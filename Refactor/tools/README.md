# Refactor 自动化工具

## 目录

# - [1. generate-toc.js](#1.-generate-toc.js)
# - [2. package.json](#2.-package.json)
# - [3. CI/CD 配置](#3.-ci/cd-配置)
# - [安装依赖](#安装依赖)
# - [运行所有工具](#运行所有工具)
# - [单独运行工具](#单独运行工具)
# - [目录生成](#目录生成)
# - [链接检查](#链接检查)
# - [交叉引用](#交叉引用)
# - [格式检查](#格式检查)
# - [目录扫描配置](#目录扫描配置)
# - [输出格式配置](#输出格式配置)
# - [GitHub Actions](#github-actions)
# - [本地开发](#本地开发)
# - [添加新的检查规则](#添加新的检查规则)
# - [添加新的输出格式](#添加新的输出格式)
# - [常见问题](#常见问题)
# - [调试模式](#调试模式)
# - [添加新功能](#添加新功能)
# - [报告问题](#报告问题)
# - [代码规范](#代码规范)
# - [v1.0.0 (2024-01-01)](#v1.0.0-(2024-01-01))
# - [计划功能](#计划功能)

# [返回Refactor总览](年度技术回顾/README.md)

# > 本目录包含 Refactor 知识体系的自动化工具，用于生成目录结构、检查链接、格式化文档等。

## 工具列表

### 1. generate-toc.js

# 主要的自动化工具，提供以下功能：

# - 生成目录结构
# - 更新 README.md
# - 检查链接有效性
# - 生成交叉引用索引

### 2. package.json

# 工具依赖管理，包含：

# - 开发依赖
# - 脚本命令
# - 版本信息

### 3. CI/CD 配置

# GitHub Actions 工作流，提供：

# - 自动文档检查
# - 链接验证
# - 格式检查
# - 自动部署

## 快速开始

### 安装依赖

# ```bash
# cd Refactor/tools
# npm install
# ```text
### 运行所有工具
# ```bash
# npm run all
# ```text
### 单独运行工具
# ```bash
# 生成 SUMMARY.md
# npm run toc

# 更新 README.md 目录结构
# npm run readme

# 检查链接有效性
# npm run links

# 生成交叉引用索引
# npm run refs
# ```text
## 工具功能详解

### 目录生成

# - 自动扫描目录结构
# - 生成层级化的目录树
# - 支持 Markdown 格式输出
# - 自动更新导航链接

### 链接检查

# - 检查所有 Markdown 文件中的链接
# - 验证相对路径和绝对路径
# - 报告损坏的链接
# - 支持外部链接跳过

### 交叉引用

# - 提取文档关键词
# - 生成相关文档索引
# - 帮助发现相关内容
# - 支持多文档关联

### 格式检查

# - Markdown 语法检查
# - 代码格式验证
# - 链接格式验证
# - 自动格式化修复

## 配置选项

### 目录扫描配置
# ```javascript
# // 在 generate-toc.js 中修改
# const config = {
#   rootDir: path.join(__dirname, '..'),
#   excludeDirs: ['.git', 'node_modules', 'tools'],
#   includeExtensions: ['.md'],
#   maxDepth: 5
# };
# ```text
### 输出格式配置
# ```javascript
# // 自定义输出格式
# const outputFormats = {
#   summary: true,      // 生成 SUMMARY.md
#   readme: true,       // 更新 README.md
#   crossRefs: true,    // 生成交叉引用
#   links: true         // 检查链接
# };
# ```bash
## CI/CD 集成

### GitHub Actions

# 工作流文件：`.github/workflows/docs.yml`

# 触发条件：

# - Push 到 main/develop 分支
# - Pull Request 到 main 分支
# - 每周定时检查

# 执行步骤：

# 1. 检查文档格式
# 2. 验证链接有效性
# 3. 生成目录结构
# 4. 自动提交更新
# 5. 部署到 GitHub Pages

### 本地开发
# ```bash
# 安装依赖
# npm install

# 运行检查
# npm run check

# 格式化代码
# npm run format

# 运行所有工具
# npm run all
# ```text
## 自定义扩展

### 添加新的检查规则
# ```javascript
# // 在 generate-toc.js 中添加
# class CustomValidator {
#   validate(content) {
#     // 自定义验证逻辑
#     return {
#       valid: true,
#       issues: []
#     };
#   }
# }
# ```text
### 添加新的输出格式
# ```javascript
# // 添加新的生成器
# class CustomGenerator {
#   generate(items) {
#     // 自定义生成逻辑
#     return content;
#   }
# }
# ```text
## 故障排除

### 常见问题

#### 1. 链接检查失败
# ```bash
# 检查文件路径
# ls -la Refactor/

# 验证相对路径
# node generate-toc.js links
# ```text
#### 2. 目录生成不完整
# ```bash
# 检查目录权限
# chmod -R 755 Refactor/

# 重新扫描
# node generate-toc.js toc
# ```bash
#### 3. CI/CD 失败
# ```bash
# 检查 GitHub Actions 日志
# 验证 secrets 配置
# 确认分支权限
# ```text
### 调试模式
# ```bash
# 启用详细日志
# DEBUG=* node generate-toc.js

# 只检查特定文件
# node generate-toc.js --file=README.md
# ```

## 贡献指南

### 添加新功能

# 1. Fork 项目
# 2. 创建功能分支
# 3. 实现新功能
# 4. 添加测试
# 5. 提交 Pull Request

### 报告问题

# 1. 检查现有 Issues
# 2. 创建新的 Issue
# 3. 提供详细描述
# 4. 附上错误日志

### 代码规范

# - 使用 ES6+ 语法
# - 添加 JSDoc 注释
# - 遵循 ESLint 规则
# - 编写单元测试

## 更新日志

### v1.0.0 (2024-01-01)

# - 初始版本发布
# - 基础目录生成功能
# - 链接检查功能
# - CI/CD 集成

### 计划功能

# - [ ] 支持更多文档格式
# - [ ] 添加可视化图表
# - [ ] 集成 AI 辅助功能
# - [ ] 支持多语言文档

# ---

# > 如有问题或建议，请提交 Issue 或 Pull Request。
