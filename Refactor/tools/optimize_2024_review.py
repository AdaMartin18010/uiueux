#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
2024年度技术回顾.md 格式优化脚本
优化文件格式，修复过多的空行问题
"""

import re
import os

def optimize_markdown_format(file_path):
    """优化markdown格式"""
    print(f"🔧 开始优化文件: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # 1. 修复过多的空行
    # 将3个或更多连续空行替换为2个空行
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    # 2. 修复列表项之间的空行
    # 列表项之间应该只有一个空行
    content = re.sub(r'(\n- [^\n]+)\n{2,}(- [^\n]+)', r'\1\n\2', content)
    
    # 3. 修复标题前后的空行
    # 标题前后应该只有一个空行
    content = re.sub(r'\n{2,}(#{1,6} [^\n]+)\n{2,}', r'\n\1\n', content)
    
    # 4. 修复表格前后的空行
    # 表格前后应该只有一个空行
    content = re.sub(r'\n{2,}(\|[^\n]+\|)\n{2,}', r'\n\1\n', content)
    
    # 5. 修复引用块前后的空行
    # 引用块前后应该只有一个空行
    content = re.sub(r'\n{2,}(>[^\n]+)\n{2,}', r'\n\1\n', content)
    
    # 6. 修复分隔线前后的空行
    # 分隔线前后应该只有一个空行
    content = re.sub(r'\n{2,}(---)\n{2,}', r'\n\1\n', content)
    
    # 7. 修复代码块前后的空行
    # 代码块前后应该只有一个空行
    content = re.sub(r'\n{2,}(```[^\n]*\n.*?```)\n{2,}', r'\n\1\n', content, flags=re.DOTALL)
    
    # 8. 修复段落之间的空行
    # 段落之间应该只有一个空行
    content = re.sub(r'([^\n])\n{2,}([^\n])', r'\1\n\2', content)
    
    # 9. 修复文件开头和结尾的空行
    # 文件开头和结尾不应该有多余的空行
    content = content.strip() + '\n'
    
    # 检查是否有变化
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ 优化完成: {file_path}")
        return True
    else:
        print(f"✅ 无需优化: {file_path}")
        return False

def main():
    """主函数"""
    file_path = "../年度技术回顾/2024年度技术回顾.md"
    
    if not os.path.exists(file_path):
        print(f"❌ 文件不存在: {file_path}")
        return
    
    print("🚀 开始优化2024年度技术回顾.md文件...")
    
    try:
        optimized = optimize_markdown_format(file_path)
        if optimized:
            print("✅ 文件优化完成！")
        else:
            print("✅ 文件格式良好，无需优化！")
    except Exception as e:
        print(f"❌ 优化过程中出现错误: {e}")
        return

if __name__ == "__main__":
    main() 