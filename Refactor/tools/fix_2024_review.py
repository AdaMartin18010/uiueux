#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
2024年度技术回顾.md 格式修复脚本
专门修复该文件的markdown格式问题
"""

import re
import os
import sys

def fix_markdown_format(file_path):
    """修复markdown格式问题"""
    print(f"🔧 开始修复文件: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # 1. 修复代码块语言标识
    # 查找没有语言标识的代码块
    code_block_pattern = r'```\n(.*?)```'
    def add_language_identifier(match):
        code_content = match.group(1)
        # 根据内容判断语言
        if 'javascript' in code_content.lower() or 'js' in code_content.lower():
            return f'```javascript\n{code_content}```'
        elif 'typescript' in code_content.lower() or 'ts' in code_content.lower():
            return f'```typescript\n{code_content}```'
        elif 'python' in code_content.lower():
            return f'```python\n{code_content}```'
        elif 'html' in code_content.lower():
            return f'```html\n{code_content}```'
        elif 'css' in code_content.lower():
            return f'```css\n{code_content}```'
        elif 'json' in code_content.lower():
            return f'```json\n{code_content}```'
        elif 'yaml' in code_content.lower() or 'yml' in code_content.lower():
            return f'```yaml\n{code_content}```'
        elif 'bash' in code_content.lower() or 'shell' in code_content.lower():
            return f'```bash\n{code_content}```'
        else:
            return f'```text\n{code_content}```'
    
    content = re.sub(code_block_pattern, add_language_identifier, content, flags=re.DOTALL)
    
    # 2. 修复表格对齐
    # 确保表格分隔符正确
    table_pattern = r'(\|[^|]+\|[^|]+\|[^|]+\|)\n(\|[\s\-:]+\|[\s\-:]+\|[\s\-:]+\|)'
    def fix_table_alignment(match):
        header = match.group(1)
        separator = match.group(2)
        # 确保分隔符有正确的对齐
        return f'{header}\n{separator}'
    
    content = re.sub(table_pattern, fix_table_alignment, content)
    
    # 3. 修复标题层级
    # 确保标题前后有空行
    heading_pattern = r'^([#]+)\s+(.+)$'
    def fix_heading_spacing(match):
        level = match.group(1)
        text = match.group(2)
        return f'\n{level} {text}\n'
    
    content = re.sub(heading_pattern, fix_heading_spacing, content, flags=re.MULTILINE)
    
    # 4. 修复列表格式
    # 确保列表项前后有空行
    list_pattern = r'^(\s*[-*+]\s+.+)$'
    def fix_list_spacing(match):
        item = match.group(1)
        return f'\n{item}\n'
    
    content = re.sub(list_pattern, fix_list_spacing, content, flags=re.MULTILINE)
    
    # 5. 修复链接格式
    # 确保链接格式正确
    link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    def fix_link_format(match):
        text = match.group(1)
        url = match.group(2)
        # 确保链接格式正确
        return f'[{text}]({url})'
    
    content = re.sub(link_pattern, fix_link_format, content)
    
    # 6. 修复空行
    # 移除多余的空行，保留适当的空行
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    # 7. 修复引用块格式
    # 确保引用块格式正确
    quote_pattern = r'^>\s*(.+)$'
    def fix_quote_format(match):
        text = match.group(1)
        return f'> {text}'
    
    content = re.sub(quote_pattern, fix_quote_format, content, flags=re.MULTILINE)
    
    # 8. 修复粗体和斜体格式
    # 确保粗体和斜体格式正确
    bold_pattern = r'\*\*([^*]+)\*\*'
    italic_pattern = r'\*([^*]+)\*'
    
    def fix_bold_format(match):
        text = match.group(1)
        return f'**{text}**'
    
    def fix_italic_format(match):
        text = match.group(1)
        return f'*{text}*'
    
    content = re.sub(bold_pattern, fix_bold_format, content)
    content = re.sub(italic_pattern, fix_italic_format, content)
    
    # 9. 修复代码内联格式
    # 确保内联代码格式正确
    inline_code_pattern = r'`([^`]+)`'
    def fix_inline_code_format(match):
        code = match.group(1)
        return f'`{code}`'
    
    content = re.sub(inline_code_pattern, fix_inline_code_format, content)
    
    # 10. 修复分隔线格式
    # 确保分隔线格式正确
    hr_pattern = r'^---+$'
    def fix_hr_format(match):
        return '\n---\n'
    
    content = re.sub(hr_pattern, fix_hr_format, content, flags=re.MULTILINE)
    
    # 检查是否有变化
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ 修复完成: {file_path}")
        return True
    else:
        print(f"✅ 无需修复: {file_path}")
        return False

def main():
    """主函数"""
    file_path = "../年度技术回顾/2024年度技术回顾.md"
    
    if not os.path.exists(file_path):
        print(f"❌ 文件不存在: {file_path}")
        return
    
    print("🚀 开始修复2024年度技术回顾.md文件...")
    
    try:
        fixed = fix_markdown_format(file_path)
        if fixed:
            print("✅ 文件修复完成！")
        else:
            print("✅ 文件格式良好，无需修复！")
    except Exception as e:
        print(f"❌ 修复过程中出现错误: {e}")
        return

if __name__ == "__main__":
    main() 