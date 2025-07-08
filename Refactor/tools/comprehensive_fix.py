#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全面项目修复脚本
修复链接、完善内容、规范格式
"""

import os
import re
import glob
from pathlib import Path

def build_file_mapping():
    """构建文件映射"""
    mapping = {}
    for root, dirs, files in os.walk('..'):
        for file in files:
            if file.endswith('.md'):
                full_path = os.path.join(root, file)
                # 相对路径映射
                rel_path = os.path.relpath(full_path, '..')
                mapping[file] = rel_path
                # 不带扩展名的映射
                name_without_ext = os.path.splitext(file)[0]
                mapping[name_without_ext] = rel_path
    return mapping

def fix_links_in_file(file_path, file_mapping):
    """修复单个文件中的链接"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 修复相对路径链接
        link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        
        def fix_link(match):
            text = match.group(1)
            link = match.group(2)
            
            # 跳过外部链接
            if link.startswith('http'):
                return match.group(0)
            
            # 修复相对路径
            if link.startswith('./'):
                link = link[2:]
            elif link.startswith('../'):
                # 计算正确的相对路径
                current_dir = os.path.dirname(file_path)
                target_path = os.path.normpath(os.path.join(current_dir, link))
                rel_path = os.path.relpath(target_path, os.path.dirname(file_path))
                link = rel_path.replace('\\', '/')
            
            return f'[{text}]({link})'
        
        content = re.sub(link_pattern, fix_link, content)
        
        # 修复锚点链接
        anchor_pattern = r'\[([^\]]+)\]\(([^#]+)#([^)]+)\)'
        
        def fix_anchor(match):
            text = match.group(1)
            file_link = match.group(2)
            anchor = match.group(3)
            
            # 查找对应的文件
            if file_link in file_mapping:
                correct_path = file_mapping[file_link]
                return f'[{text}]({correct_path}#{anchor})'
            return match.group(0)
        
        content = re.sub(anchor_pattern, fix_anchor, content)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"修复文件 {file_path} 时出错: {e}")
        return False

def enhance_content(file_path):
    """增强文件内容"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否缺少标题
        if not content.strip().startswith('#'):
            filename = os.path.basename(file_path)
            title = os.path.splitext(filename)[0]
            content = f'# {title}\n\n{content}'
        
        # 检查是否缺少目录
        if '## ' in content and not '## 目录' in content[:500]:
            # 生成简单的目录
            lines = content.split('\n')
            toc_lines = ['## 目录\n']
            for line in lines:
                if line.startswith('### '):
                    title = line[4:].strip()
                    anchor = title.lower().replace(' ', '-')
                    toc_lines.append(f'- [{title}](#{anchor})')
            
            if len(toc_lines) > 1:
                content = content.replace('\n\n', '\n\n' + '\n'.join(toc_lines) + '\n\n', 1)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
    except Exception as e:
        print(f"增强文件 {file_path} 时出错: {e}")
        return False

def format_markdown(file_path):
    """格式化markdown文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 修复代码块
        content = re.sub(r'```\n', '```\n', content)
        
        # 修复标题格式
        content = re.sub(r'^([^#\n].*?)$', r'# \1', content, flags=re.MULTILINE)
        
        # 修复列表格式
        content = re.sub(r'^\s*[-*]\s*([^\n]+)', r'- \1', content, flags=re.MULTILINE)
        
        # 修复表格格式
        content = re.sub(r'\|([^|]+)\|([^|]+)\|', r'| \1 | \2 |', content)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
    except Exception as e:
        print(f"格式化文件 {file_path} 时出错: {e}")
        return False

def main():
    """主函数"""
    print("🚀 开始全面项目修复...")
    
    # 构建文件映射
    print("📋 构建文件映射...")
    file_mapping = build_file_mapping()
    print(f"   映射文件数: {len(file_mapping)}")
    
    # 获取所有markdown文件
    md_files = glob.glob('../**/*.md', recursive=True)
    
    fixed_files = 0
    enhanced_files = 0
    formatted_files = 0
    
    print("🔧 开始修复文件...")
    
    for file_path in md_files:
        print(f"   处理: {file_path}")
        
        # 修复链接
        if fix_links_in_file(file_path, file_mapping):
            fixed_files += 1
        
        # 增强内容
        if enhance_content(file_path):
            enhanced_files += 1
        
        # 格式化
        if format_markdown(file_path):
            formatted_files += 1
    
    print(f"\n✅ 修复完成!")
    print(f"   修复文件数: {fixed_files}")
    print(f"   增强文件数: {enhanced_files}")
    print(f"   格式化文件数: {formatted_files}")

if __name__ == '__main__':
    main() 