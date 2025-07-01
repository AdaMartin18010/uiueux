#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Refactor 链接修复工具
用于自动修复损坏的链接和路径问题
"""

import os
import re
import shutil
from pathlib import Path
from urllib.parse import unquote

class LinkFixer:
    def __init__(self):
        self.root_dir = Path(__file__).parent.parent
        self.fixed_links = 0
        self.total_links = 0
        
    def scan_and_fix_links(self):
        """扫描并修复所有损坏的链接"""
        print("🔍 扫描项目中的链接...")
        
        for file_path in self.root_dir.rglob('*.md'):
            if file_path.is_file():
                self.fix_file_links(file_path)
                
        print(f"\n✅ 链接修复完成！")
        print(f"   总链接数: {self.total_links}")
        print(f"   修复链接数: {self.fixed_links}")
    
    def fix_file_links(self, file_path):
        """修复单个文件中的链接"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            content = self.fix_links_in_content(file_path, content)
            
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✅ 修复文件: {file_path.relative_to(self.root_dir)}")
                
        except Exception as e:
            print(f"❌ 修复文件 {file_path} 时出错: {e}")
    
    def fix_links_in_content(self, file_path, content):
        """修复内容中的链接"""
        # 查找所有链接
        link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        
        def replace_link(match):
            text = match.group(1)
            link = match.group(2)
            self.total_links += 1
            
            # 跳过外部链接和锚点链接
            if link.startswith(('http', 'https', '#')):
                return match.group(0)
            
            # 修复链接
            fixed_link = self.fix_single_link(file_path, link)
            if fixed_link != link:
                self.fixed_links += 1
                return f'[{text}]({fixed_link})'
            
            return match.group(0)
        
        return re.sub(link_pattern, replace_link, content)
    
    def fix_single_link(self, file_path, link):
        """修复单个链接"""
        # 解码URL编码
        link = unquote(link)
        
        # 处理相对路径
        if link.startswith('./'):
            link = link[2:]
        elif link.startswith('../'):
            # 计算正确的相对路径
            link = self.calculate_relative_path(file_path, link)
        
        # 检查文件是否存在
        target_path = self.resolve_target_path(file_path, link)
        if target_path.exists():
            return link
        
        # 尝试修复常见的路径问题
        fixed_link = self.try_fix_path(file_path, link)
        if fixed_link:
            return fixed_link
        
        return link
    
    def calculate_relative_path(self, file_path, link):
        """计算正确的相对路径"""
        # 解析 ../ 的数量
        parts = link.split('/')
        up_count = 0
        path_parts = []
        
        for part in parts:
            if part == '..':
                up_count += 1
            else:
                path_parts.append(part)
        
        # 计算目标路径
        current_parts = list(file_path.parent.parts)
        target_parts = current_parts[:-up_count] + path_parts
        
        # 转换为相对路径
        relative_parts = []
        for i, part in enumerate(target_parts):
            if i < len(current_parts) and part == current_parts[i]:
                continue
            relative_parts.append(part)
        
        return '/'.join(relative_parts)
    
    def resolve_target_path(self, file_path, link):
        """解析目标路径"""
        if link.startswith('/'):
            return self.root_dir / link[1:]
        else:
            return file_path.parent / link
    
    def try_fix_path(self, file_path, link):
        """尝试修复路径"""
        # 常见的路径修复规则
        fixes = [
            # 修复文件名中的空格编码
            (r'%20', ' '),
            # 修复文件名中的特殊字符
            (r'%2B', '+'),
            (r'%2F', '/'),
            # 修复常见的路径错误
            (r'\.\./\.\./', '../'),
            (r'\./\./', './'),
        ]
        
        fixed_link = link
        for pattern, replacement in fixes:
            fixed_link = re.sub(pattern, replacement, fixed_link)
        
        # 检查修复后的路径是否存在
        target_path = self.resolve_target_path(file_path, fixed_link)
        if target_path.exists():
            return fixed_link
        
        # 尝试查找相似的文件名
        return self.find_similar_file(file_path, link)
    
    def find_similar_file(self, file_path, link):
        """查找相似的文件"""
        # 提取文件名
        link_name = Path(link).name
        
        # 在项目根目录中搜索
        for search_path in self.root_dir.rglob('*.md'):
            if search_path.name == link_name:
                # 计算相对路径
                relative_path = search_path.relative_to(file_path.parent)
                return str(relative_path).replace('\\', '/')
        
        return None
    
    def create_missing_files(self):
        """创建缺失的文件"""
        print("\n📝 检查缺失的文件...")
        
        missing_files = [
            # 年度技术回顾目录的README
            '年度技术回顾/README.md',
        ]
        
        for missing_file in missing_files:
            file_path = self.root_dir / missing_file
            if not file_path.exists():
                self.create_file_template(file_path)
    
    def create_file_template(self, file_path):
        """创建文件模板"""
        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # 根据文件路径生成内容
            if file_path.name == 'README.md':
                if '年度技术回顾' in str(file_path):
                    content = self.generate_annual_review_readme()
                else:
                    content = self.generate_generic_readme(file_path)
            else:
                content = self.generate_generic_content(file_path)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ 创建文件: {file_path.relative_to(self.root_dir)}")
            
        except Exception as e:
            print(f"❌ 创建文件 {file_path} 时出错: {e}")
    
    def generate_annual_review_readme(self):
        """生成年度技术回顾README"""
        return """# 年度技术回顾

[返回Refactor总览](../README.md)

> 本目录包含年度技术发展回顾和趋势分析，帮助了解技术演进历程。

## 目录结构

- [2024年度技术回顾](./2024年度技术回顾.md) - 2024年技术发展总结

## 内容特色

### 年度概览
- 技术发展主线分析
- 关键里程碑回顾
- 重要技术突破总结

### 领域分析
- 前端技术发展
- AI技术进展
- 工程化实践
- 跨端技术演进

### 趋势预测
- 短期技术趋势
- 中期发展方向
- 长期技术愿景

## 使用方法

1. **按年份浏览**：选择特定年份查看技术回顾
2. **按领域学习**：重点关注特定技术领域
3. **趋势分析**：了解技术发展方向
4. **实践指导**：结合当前项目需求

## 持续更新

- 每年更新年度技术回顾
- 及时补充重要技术事件
- 定期分析技术趋势变化
- 保持内容的时效性和准确性

---

> 通过年度回顾，我们可以更好地理解技术发展脉络，为未来的技术选型和决策提供参考。
"""
    
    def generate_generic_readme(self, file_path):
        """生成通用README模板"""
        dir_name = file_path.parent.name
        section_num = re.match(r'^(\d+)\.', dir_name)
        
        if section_num:
            num = section_num.group(1)
            name = dir_name.replace(f'{num}.', '').strip()
            
            return f"""# {num}. {name}

[返回Refactor总览](../README.md)

> 本目录包含{name}相关技术内容，提供系统化的学习和实践指导。

## 目录结构

{self.generate_section_toc(file_path.parent)}

## 学习路径

### 入门路径
1. 基础概念学习
2. 核心原理理解
3. 实践案例应用

### 进阶路径
1. 深入技术细节
2. 性能优化实践
3. 架构设计思考

### 专家路径
1. 前沿技术探索
2. 创新应用开发
3. 技术标准制定

## 技术特色

- **系统性**：完整的技术知识体系
- **实用性**：结合实际的代码示例
- **前沿性**：包含最新技术趋势
- **批判性**：深入的技术分析

## 相关主题

- [相关技术领域1](../xxx.md)
- [相关技术领域2](../xxx.md)
- [相关技术领域3](../xxx.md)

---

> 通过系统学习，掌握{name}的核心技术和最佳实践。
"""
        else:
            return self.generate_generic_content(file_path)
    
    def generate_section_toc(self, dir_path):
        """生成章节目录"""
        toc = ""
        for file_path in sorted(dir_path.glob('*.md')):
            if file_path.name != 'README.md':
                name = file_path.stem
                toc += f"- [{name}](./{file_path.name})\n"
        return toc
    
    def generate_generic_content(self, file_path):
        """生成通用内容模板"""
        return f"""# {file_path.stem}

[返回上级目录](../README.md)

## 前沿趋势

- 当前技术发展趋势
- 最新技术动态
- 未来发展方向

## 目录结构

- 主要章节概述
- 内容组织方式
- 学习路径建议

## 知识图谱

```mermaid
graph TD
    A[主题] --> B[子主题1]
    A --> C[子主题2]
```

## 核心概念

### 概念1
详细说明和示例

### 概念2
详细说明和示例

## 代码示例

```javascript
// 实际可运行的代码示例
```

## 最佳实践

- 实践建议1
- 实践建议2
- 注意事项

## 批判性分析

- 技术优缺点分析
- 适用场景讨论
- 替代方案比较

## 相关主题推荐

- [相关主题1](../xxx.md)
- [相关主题2](../xxx.md)

## 持续优化说明

- 更新计划
- 待补充内容
- 反馈渠道

---

> 本文档持续更新中，欢迎提出建议和改进意见。
"""
    
    def run(self):
        """运行链接修复工具"""
        print("🚀 开始链接修复...\n")
        
        try:
            # 创建缺失的文件
            self.create_missing_files()
            
            # 扫描并修复链接
            self.scan_and_fix_links()
            
            print("\n✅ 链接修复完成！")
            
        except Exception as e:
            print(f"❌ 链接修复过程中出现错误: {e}")

def main():
    """主函数"""
    fixer = LinkFixer()
    fixer.run()

if __name__ == '__main__':
    main() 