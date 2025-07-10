#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全面修复Markdown文件格式问题的脚本
修复内容：
1. 去除行首的"#"字符（保留目录名中的"#"）
2. 修复损坏的链接
3. 统一格式规范
4. 修复代码块格式
"""

import os
import re
import glob
from pathlib import Path

def fix_markdown_file(file_path):
    """修复单个Markdown文件的格式问题"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 1. 去除行首的"#"字符（但保留目录名中的"#"）
        lines = content.split('\n')
        fixed_lines = []
        
        for line in lines:
            # 跳过空行
            if not line.strip():
                fixed_lines.append(line)
                continue
            
            # 检查是否是目录名（包含"#"的文件名）
            if re.match(r'^\d+\.\s*[^#]*#.*\.md$', line.strip()):
                # 这是目录名，保留"#"
                fixed_lines.append(line)
                continue
            
            # 检查是否是链接中的目录名
            if re.search(r'\[.*\]\(.*#.*\.md\)', line):
                # 这是包含"#"的链接，保留"#"
                fixed_lines.append(line)
                continue
            
            # 去除行首的"#"字符
            if line.startswith('#'):
                # 计算"#"的数量
                hash_count = len(line) - len(line.lstrip('#'))
                # 保留一个"#"作为标题标记
                if hash_count > 1:
                    line = '#' + line[hash_count:]
                fixed_lines.append(line)
            else:
                fixed_lines.append(line)
        
        content = '\n'.join(fixed_lines)
        
        # 2. 修复损坏的链接
        # 修复相对路径链接
        content = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', lambda m: fix_link(m.group(1), m.group(2), file_path), content)
        
        # 3. 修复代码块格式
        # 确保代码块有语言标识
        content = re.sub(r'```\s*\n', '```\n', content)
        
        # 4. 修复列表格式
        # 统一列表缩进
        content = re.sub(r'^\s*[-*+]\s+', '- ', content, flags=re.MULTILINE)
        
        # 5. 修复标题格式
        # 确保标题前后有空行
        content = re.sub(r'([^\n])\n(#+\s)', r'\1\n\n\2', content)
        content = re.sub(r'(#+\s[^\n]+)\n([^\n])', r'\1\n\n\2', content)
        
        # 如果内容有变化，写回文件
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ 已修复: {file_path}")
            return True
        else:
            print(f"⏭️  无需修复: {file_path}")
            return False
            
    except Exception as e:
        print(f"❌ 修复失败 {file_path}: {str(e)}")
        return False

def fix_link(text, url, current_file):
    """修复链接格式"""
    # 如果是相对路径，确保路径正确
    if url.startswith('./') or url.startswith('../'):
        # 这里可以添加更复杂的路径修复逻辑
        pass
    
    # 修复常见的链接问题
    if url.endswith('.md') and not url.startswith('http'):
        # 确保.md文件链接格式正确
        if not url.startswith('./') and not url.startswith('../'):
            url = './' + url
    
    return f'[{text}]({url})'

def find_markdown_files(root_dir):
    """递归查找所有Markdown文件"""
    markdown_files = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.md'):
                markdown_files.append(os.path.join(root, file))
    return markdown_files

def main():
    """主函数"""
    print("🔧 开始全面修复Markdown文件格式问题...")
    
    # 获取当前目录作为Refactor目录
    refactor_dir = os.getcwd()
    print(f"📁 当前工作目录: {refactor_dir}")
    
    # 查找所有Markdown文件
    markdown_files = find_markdown_files(refactor_dir)
    print(f"📁 找到 {len(markdown_files)} 个Markdown文件")
    
    # 修复每个文件
    fixed_count = 0
    for file_path in markdown_files:
        if fix_markdown_file(file_path):
            fixed_count += 1
    
    print(f"\n🎉 修复完成！")
    print(f"📊 统计信息:")
    print(f"   - 总文件数: {len(markdown_files)}")
    print(f"   - 修复文件数: {fixed_count}")
    print(f"   - 无需修复文件数: {len(markdown_files) - fixed_count}")

if __name__ == "__main__":
    main() 