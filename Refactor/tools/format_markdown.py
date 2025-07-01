#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Refactor Markdown 自动格式化工具
用于修复代码块语言标识、标题层级等格式问题
"""

import os
import re
from pathlib import Path

class MarkdownFormatter:
    def __init__(self):
        self.root_dir = Path(__file__).parent.parent
        self.fixed_files = 0
        self.total_issues = 0
        
    def format_all_files(self):
        """格式化所有Markdown文件"""
        print("🔧 开始格式化Markdown文件...")
        
        for file_path in self.root_dir.rglob('*.md'):
            if file_path.is_file():
                self.format_file(file_path)
                
        print(f"\n✅ 格式化完成！")
        print(f"   修复文件数: {self.fixed_files}")
        print(f"   修复问题数: {self.total_issues}")
    
    def format_file(self, file_path):
        """格式化单个文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            content = self.fix_code_blocks(content)
            content = self.fix_heading_levels(content)
            content = self.fix_links(content)
            content = self.fix_formatting(content)
            
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✅ 格式化文件: {file_path.relative_to(self.root_dir)}")
                self.fixed_files += 1
                
        except Exception as e:
            print(f"❌ 格式化文件 {file_path} 时出错: {e}")
    
    def fix_code_blocks(self, content):
        """修复代码块语言标识"""
        # 查找没有语言标识的代码块
        pattern = r'```\n(.*?)```'
        
        def add_language(match):
            code = match.group(1).strip()
            # 根据代码内容推断语言
            language = self.infer_language(code)
            self.total_issues += 1
            return f'```{language}\n{code}\n```'
        
        return re.sub(pattern, add_language, content, flags=re.DOTALL)
    
    def infer_language(self, code):
        """根据代码内容推断语言"""
        code_lower = code.lower()
        
        # JavaScript/TypeScript
        if any(keyword in code_lower for keyword in ['function', 'const', 'let', 'var', 'console.log', 'import', 'export']):
            if 'interface' in code_lower or 'type' in code_lower:
                return 'typescript'
            return 'javascript'
        
        # Python
        if any(keyword in code_lower for keyword in ['def ', 'import ', 'from ', 'class ', 'print(', 'if __name__']):
            return 'python'
        
        # Rust
        if any(keyword in code_lower for keyword in ['fn ', 'let ', 'mut ', 'pub ', 'impl ', 'struct ']):
            return 'rust'
        
        # HTML
        if '<' in code and '>' in code:
            return 'html'
        
        # CSS
        if '{' in code and '}' in code and ':' in code:
            return 'css'
        
        # JSON
        if code.strip().startswith('{') and code.strip().endswith('}'):
            return 'json'
        
        # YAML
        if ':' in code and '\n' in code and not '{' in code:
            return 'yaml'
        
        # Shell
        if any(keyword in code_lower for keyword in ['#!/', 'cd ', 'ls ', 'git ', 'npm ', 'python ']):
            return 'bash'
        
        # 默认返回text
        return 'text'
    
    def fix_heading_levels(self, content):
        """修复标题层级"""
        lines = content.split('\n')
        fixed_lines = []
        
        for line in lines:
            if line.startswith('#'):
                level = len(line) - len(line.lstrip('#'))
                if level > 5:
                    # 将超过5级的标题降级
                    new_level = 5
                    new_line = '#' * new_level + line[level:]
                    fixed_lines.append(new_line)
                    self.total_issues += 1
                else:
                    fixed_lines.append(line)
            else:
                fixed_lines.append(line)
        
        return '\n'.join(fixed_lines)
    
    def fix_links(self, content):
        """修复链接格式"""
        # 修复模板占位符链接
        content = re.sub(r'\[([^\]]+)\]\(xxx\.md\)', r'[\1](#)', content)
        content = re.sub(r'\[([^\]]+)\]\(链接地址\)', r'[\1](#)', content)
        
        # 修复URL编码的空格
        content = re.sub(r'%20', ' ', content)
        
        return content
    
    def fix_formatting(self, content):
        """修复其他格式问题"""
        # 确保文件末尾有换行符
        if not content.endswith('\n'):
            content += '\n'
        
        # 修复多余的空行
        content = re.sub(r'\n{3,}', '\n\n', content)
        
        # 修复行尾空格
        lines = content.split('\n')
        fixed_lines = [line.rstrip() for line in lines]
        content = '\n'.join(fixed_lines)
        
        return content
    
    def run(self):
        """运行格式化工具"""
        print("🚀 开始Markdown格式化...\n")
        
        try:
            self.format_all_files()
            print("\n✅ Markdown格式化完成！")
            
        except Exception as e:
            print(f"❌ 格式化过程中出现错误: {e}")

def main():
    """主函数"""
    formatter = MarkdownFormatter()
    formatter.run()

if __name__ == '__main__':
    main() 