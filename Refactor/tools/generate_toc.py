#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Refactor 知识体系自动化工具 (Python版本)
用于生成目录结构、检查链接、格式化文档等
"""

import os
import re
import glob
from datetime import datetime
from pathlib import Path

class RefactorTools:
    def __init__(self):
        self.root_dir = Path(__file__).parent.parent
        self.output_dir = self.root_dir
        
    def scan_directory(self, dir_path=None, level=0):
        """扫描目录结构"""
        if dir_path is None:
            dir_path = self.root_dir
            
        items = []
        
        try:
            for item in sorted(dir_path.iterdir()):
                if item.name.startswith('.') or item.name == 'tools':
                    continue
                    
                relative_path = item.relative_to(self.root_dir)
                
                if item.is_dir():
                    children = self.scan_directory(item, level + 1)
                    items.append({
                        'type': 'directory',
                        'name': item.name,
                        'path': str(relative_path),
                        'level': level,
                        'children': children
                    })
                elif item.suffix == '.md' and item.name != 'README.md':
                    items.append({
                        'type': 'file',
                        'name': item.name,
                        'path': str(relative_path),
                        'level': level
                    })
        except Exception as e:
            print(f"扫描目录 {dir_path} 时出错: {e}")
            
        return items
    
    def generate_toc(self, items, prefix=''):
        """生成目录树"""
        toc = ''
        
        for item in items:
            indent = '  ' * item['level']
            link = item['path'].replace('\\', '/')
            
            if item['type'] == 'directory':
                toc += f"{indent}- [{item['name']}](./{link}/README.md)\n"
                if item['children']:
                    toc += self.generate_toc(item['children'], prefix + '  ')
            else:
                name = item['name'].replace('.md', '')
                toc += f"{indent}- [{name}](./{link})\n"
                
        return toc
    
    def generate_summary(self):
        """生成 SUMMARY.md"""
        print("📝 生成 SUMMARY.md...")
        
        items = self.scan_directory()
        toc = self.generate_toc(items)
        
        content = f"""# Refactor 知识体系目录

> 自动生成的目录索引，用于快速导航和内容概览

{toc}

---

> 本目录由自动化工具生成，更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        summary_path = self.output_dir / 'SUMMARY.md'
        try:
            with open(summary_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print("✅ SUMMARY.md 生成完成")
        except Exception as e:
            print(f"❌ 生成 SUMMARY.md 失败: {e}")
    
    def update_readme_toc(self):
        """更新 README.md 目录结构"""
        print("📝 更新 README.md 目录结构...")
        
        readme_path = self.root_dir / 'README.md'
        
        try:
            with open(readme_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # 提取目录结构部分
            toc_start = content.find('## 目录结构')
            toc_end = content.find('## 知识图谱')
            
            if toc_start == -1 or toc_end == -1:
                print("❌ 无法找到目录结构标记")
                return
                
            items = self.scan_directory()
            new_toc = self.generate_readme_toc(items)
            
            new_content = (
                content[:toc_start + len('## 目录结构\n\n')] +
                new_toc +
                content[toc_end:]
            )
            
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print("✅ README.md 目录结构更新完成")
            
        except Exception as e:
            print(f"❌ 更新 README.md 失败: {e}")
    
    def generate_readme_toc(self, items):
        """生成 README 格式的目录"""
        toc = ''
        
        for item in items:
            if item['type'] == 'directory':
                # 提取章节编号
                match = re.match(r'^(\d+)\.', item['name'])
                if match:
                    section_num = match.group(1)
                    section_name = re.sub(r'^\d+\.\s*', '', item['name'])
                    toc += f"{section_num}. [{section_name}](./{item['path']}/README.md)\n"
                    
                    # 添加子项目
                    sub_items = [child for child in item['children'] if child['type'] == 'file']
                    for sub_item in sub_items:
                        sub_match = re.match(r'^(\d+\.\d+)', sub_item['name'])
                        if sub_match:
                            sub_name = re.sub(r'^\d+\.\d+\s*', '', sub_item['name'])
                            toc += f"    - [{sub_match.group(1)} {sub_name}](./{sub_item['path']})\n"
                    toc += '\n'
                    
        return toc
    
    def check_links(self):
        """检查链接有效性"""
        print("🔍 检查链接有效性...")
        
        items = self.scan_directory()
        broken_links = []
        
        for item in items:
            if item['type'] == 'file':
                file_path = self.root_dir / item['path']
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    links = self.extract_links(content)
                    
                    for link in links:
                        if not self.is_valid_link(link, file_path.parent):
                            broken_links.append({
                                'file': item['path'],
                                'link': link
                            })
                except Exception as e:
                    print(f"检查文件 {item['path']} 时出错: {e}")
        
        if broken_links:
            print("❌ 发现损坏的链接:")
            for link_info in broken_links:
                print(f"   {link_info['file']}: {link_info['link']}")
        else:
            print("✅ 所有链接检查通过")
            
        return broken_links
    
    def extract_links(self, content):
        """提取文档中的链接"""
        link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        links = []
        
        for match in re.finditer(link_pattern, content):
            links.append(match.group(2))
            
        return links
    
    def is_valid_link(self, link, base_path):
        """检查链接是否有效"""
        if link.startswith(('http', 'https', '#')):
            return True
            
        full_path = base_path / link
        return full_path.exists()
    
    def generate_cross_references(self):
        """生成交叉引用索引"""
        print("🔗 生成交叉引用索引...")
        
        items = self.scan_directory()
        references = {}
        
        # 收集所有文档的关键词
        for item in items:
            if item['type'] == 'file':
                file_path = self.root_dir / item['path']
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    keywords = self.extract_keywords(content)
                    
                    for keyword in keywords:
                        if keyword not in references:
                            references[keyword] = []
                        references[keyword].append(item['path'])
                except Exception as e:
                    print(f"处理文件 {item['path']} 时出错: {e}")
        
        # 生成交叉引用文档
        content = """# 交叉引用索引

> 自动生成的交叉引用索引，帮助发现相关内容

"""
        
        for keyword, files in references.items():
            if len(files) > 1:
                content += f"## {keyword}\n\n"
                for file_path in files:
                    name = Path(file_path).stem
                    content += f"- [{name}](./{file_path})\n"
                content += '\n'
        
        cross_ref_path = self.output_dir / '交叉引用索引.md'
        try:
            with open(cross_ref_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print("✅ 交叉引用索引生成完成")
        except Exception as e:
            print(f"❌ 生成交叉引用索引失败: {e}")
    
    def extract_keywords(self, content):
        """提取文档关键词"""
        keywords = []
        lines = content.split('\n')
        
        for line in lines:
            if line.startswith('## '):
                keyword = line.replace('## ', '').strip()
                keywords.append(keyword)
                
        return keywords
    
    def run(self):
        """运行所有工具"""
        print("🚀 开始运行 Refactor 自动化工具...\n")
        
        try:
            self.generate_summary()
            self.update_readme_toc()
            self.check_links()
            self.generate_cross_references()
            
            print("\n✅ 所有任务完成！")
        except Exception as e:
            print(f"❌ 执行过程中出现错误: {e}")

def main():
    """主函数"""
    import sys
    
    tool = RefactorTools()
    
    if len(sys.argv) == 1:
        tool.run()
    else:
        command = sys.argv[1]
        if command == 'toc':
            tool.generate_summary()
        elif command == 'readme':
            tool.update_readme_toc()
        elif command == 'links':
            tool.check_links()
        elif command == 'refs':
            tool.generate_cross_references()
        else:
            print("用法: python generate_toc.py [toc|readme|links|refs]")
            print("  toc    - 生成 SUMMARY.md")
            print("  readme - 更新 README.md 目录结构")
            print("  links  - 检查链接有效性")
            print("  refs   - 生成交叉引用索引")

if __name__ == '__main__':
    main() 