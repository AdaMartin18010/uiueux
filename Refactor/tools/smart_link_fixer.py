#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能链接修复工具
自动修复Markdown文件中的相对路径链接问题
"""

import os
import re
from pathlib import Path

class SmartLinkFixer:
    def __init__(self):
        self.root_dir = Path(__file__).parent.parent
        self.fixed_files = 0
        self.fixed_links = 0
        self.file_map = {}
        
    def build_file_map(self):
        """构建文件名到路径的映射"""
        print("📋 构建文件映射...")
        
        for file_path in self.root_dir.rglob('*.md'):
            if file_path.is_file():
                # 使用文件名作为键
                filename = file_path.name
                self.file_map[filename] = file_path
                
                # 也使用不带扩展名的文件名作为键
                name_without_ext = file_path.stem
                self.file_map[name_without_ext] = file_path
                
        print(f"   映射文件数: {len(self.file_map)}")
    
    def fix_all_files(self):
        """修复所有文件中的链接"""
        print("🔧 开始修复链接...")
        
        for file_path in self.root_dir.rglob('*.md'):
            if file_path.is_file():
                self.fix_file_links(file_path)
                
        print(f"\n✅ 链接修复完成！")
        print(f"   修复文件数: {self.fixed_files}")
        print(f"   修复链接数: {self.fixed_links}")
    
    def fix_file_links(self, file_path):
        """修复单个文件中的链接"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            content = self.fix_relative_links(content, file_path)
            content = self.fix_broken_links(content, file_path)
            
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✅ 修复文件: {file_path.relative_to(self.root_dir)}")
                self.fixed_files += 1
                
        except Exception as e:
            print(f"❌ 修复文件 {file_path} 时出错: {e}")
    
    def fix_relative_links(self, content, current_file):
        """修复相对路径链接"""
        # 匹配Markdown链接模式
        link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        
        def fix_link(match):
            link_text = match.group(1)
            link_url = match.group(2)
            
            # 跳过外部链接和锚点链接
            if link_url.startswith('http') or link_url.startswith('#') or link_url.startswith('mailto:'):
                return match.group(0)
            
            # 处理相对路径
            if link_url.startswith('../') or link_url.startswith('./'):
                fixed_url = self.resolve_relative_path(link_url, current_file)
                if fixed_url:
                    self.fixed_links += 1
                    return f'[{link_text}]({fixed_url})'
            
            # 处理文件名直接引用
            if link_url.endswith('.md') or not link_url.startswith('/'):
                fixed_url = self.resolve_filename(link_url, current_file)
                if fixed_url:
                    self.fixed_links += 1
                    return f'[{link_text}]({fixed_url})'
            
            return match.group(0)
        
        return re.sub(link_pattern, fix_link, content)
    
    def resolve_relative_path(self, relative_path, current_file):
        """解析相对路径"""
        try:
            # 构建目标文件的绝对路径
            target_path = current_file.parent / relative_path
            
            # 如果目标文件存在，计算相对于根目录的路径
            if target_path.exists():
                return str(target_path.relative_to(self.root_dir))
            
            # 尝试解析包含文件名的路径
            if relative_path.endswith('.md'):
                filename = Path(relative_path).name
                if filename in self.file_map:
                    return str(self.file_map[filename].relative_to(self.root_dir))
            
            return None
            
        except Exception:
            return None
    
    def resolve_filename(self, filename, current_file):
        """根据文件名解析路径"""
        # 确保文件名有.md扩展名
        if not filename.endswith('.md'):
            filename += '.md'
        
        if filename in self.file_map:
            target_path = self.file_map[filename]
            return str(target_path.relative_to(self.root_dir))
        
        return None
    
    def fix_broken_links(self, content, current_file):
        """修复损坏的链接"""
        # 修复常见的损坏链接模式
        fixes = [
            # 修复URL编码的空格
            (r'%20', ' '),
            # 修复模板占位符
            (r'\[([^\]]+)\]\(xxx\.md\)', r'[\1](#)'),
            (r'\[([^\]]+)\]\(链接地址\)', r'[\1](#)'),
            # 修复错误的路径分隔符
            (r'\\\\', '/'),
            (r'\\', '/'),
        ]
        
        for pattern, replacement in fixes:
            if re.search(pattern, content):
                content = re.sub(pattern, replacement, content)
                self.fixed_links += 1
        
        return content
    
    def run(self):
        """运行链接修复工具"""
        print("🚀 开始智能链接修复...\n")
        
        try:
            self.build_file_map()
            self.fix_all_files()
            print("\n✅ 智能链接修复完成！")
            
        except Exception as e:
            print(f"❌ 链接修复过程中出现错误: {e}")

def main():
    """主函数"""
    fixer = SmartLinkFixer()
    fixer.run()

if __name__ == '__main__':
    main() 