#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Refactor 项目状态检查工具
用于监控项目的完整性、质量和统计信息
"""

import os
import re
import json
from datetime import datetime
from pathlib import Path
from collections import defaultdict

class ProjectStatusChecker:
    def __init__(self):
        self.root_dir = Path(__file__).parent.parent
        self.stats = {
            'total_files': 0,
            'total_dirs': 0,
            'total_lines': 0,
            'broken_links': 0,
            'missing_files': 0,
            'format_issues': 0,
            'sections': {},
            'last_updated': datetime.now().isoformat()
        }
        
    def scan_project(self):
        """扫描整个项目"""
        print("🔍 扫描项目结构...")
        
        for item in self.root_dir.rglob('*'):
            if item.is_file() and item.suffix == '.md':
                self.analyze_file(item)
            elif item.is_dir() and not item.name.startswith('.'):
                self.analyze_directory(item)
                
        return self.stats
    
    def analyze_file(self, file_path):
        """分析单个文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            relative_path = file_path.relative_to(self.root_dir)
            self.stats['total_files'] += 1
            self.stats['total_lines'] += len(content.split('\n'))
            
            # 检查文件格式
            self.check_file_format(file_path, content)
            
            # 检查链接
            self.check_links(file_path, content)
            
            # 统计章节信息
            self.analyze_section(file_path, content)
            
        except Exception as e:
            print(f"❌ 分析文件 {file_path} 时出错: {e}")
    
    def analyze_directory(self, dir_path):
        """分析目录"""
        if dir_path != self.root_dir:
            self.stats['total_dirs'] += 1
    
    def check_file_format(self, file_path, content):
        """检查文件格式"""
        issues = []
        
        # 检查标题层级
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if line.startswith('#'):
                level = len(line) - len(line.lstrip('#'))
                if level > 5:
                    issues.append(f"标题层级过深: {line.strip()}")
        
        # 检查代码块格式
        code_blocks = re.findall(r'```(\w+)?\n(.*?)```', content, re.DOTALL)
        for lang, code in code_blocks:
            if not lang and code.strip():
                issues.append("代码块缺少语言标识")
        
        if issues:
            self.stats['format_issues'] += len(issues)
            print(f"⚠️  {file_path}: {len(issues)} 个格式问题")
    
    def check_links(self, file_path, content):
        """检查链接有效性"""
        links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
        
        for text, link in links:
            if link.startswith(('http', 'https', '#')):
                continue
                
            # 检查相对链接
            link_path = file_path.parent / link
            if not link_path.exists():
                self.stats['broken_links'] += 1
                print(f"🔗 损坏链接: {file_path} -> {link}")
    
    def analyze_section(self, file_path, content):
        """分析章节信息"""
        relative_path = file_path.relative_to(self.root_dir)
        
        # 提取章节编号
        match = re.match(r'^(\d+)\.', relative_path.parts[0] if relative_path.parts else '')
        if match:
            section_num = match.group(1)
            if section_num not in self.stats['sections']:
                self.stats['sections'][section_num] = {
                    'name': relative_path.parts[0] if relative_path.parts else '',
                    'files': 0,
                    'lines': 0,
                    'subsections': {}
                }
            
            self.stats['sections'][section_num]['files'] += 1
            self.stats['sections'][section_num]['lines'] += len(content.split('\n'))
            
            # 分析子章节
            if len(relative_path.parts) > 1:
                sub_match = re.match(r'^(\d+\.\d+)', relative_path.parts[1])
                if sub_match:
                    sub_num = sub_match.group(1)
                    if sub_num not in self.stats['sections'][section_num]['subsections']:
                        self.stats['sections'][section_num]['subsections'][sub_num] = {
                            'name': relative_path.parts[1],
                            'files': 0,
                            'lines': 0
                        }
                    self.stats['sections'][section_num]['subsections'][sub_num]['files'] += 1
                    self.stats['sections'][section_num]['subsections'][sub_num]['lines'] += len(content.split('\n'))
    
    def generate_report(self):
        """生成项目状态报告"""
        print("\n📊 生成项目状态报告...")
        
        report = f"""# Refactor 项目状态报告

> 自动生成的项目状态报告，更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 📈 总体统计

- **总文件数**: {self.stats['total_files']} 个 Markdown 文件
- **总目录数**: {self.stats['total_dirs']} 个目录
- **总代码行数**: {self.stats['total_lines']} 行
- **损坏链接数**: {self.stats['broken_links']} 个
- **格式问题数**: {self.stats['format_issues']} 个

## 📚 章节统计

"""
        
        for section_num in sorted(self.stats['sections'].keys()):
            section = self.stats['sections'][section_num]
            report += f"### {section_num}. {section['name']}\n"
            report += f"- **文件数**: {section['files']} 个\n"
            report += f"- **代码行数**: {section['lines']} 行\n"
            
            if section['subsections']:
                report += "- **子章节**:\n"
                for sub_num in sorted(section['subsections'].keys()):
                    sub = section['subsections'][sub_num]
                    report += f"  - {sub_num} {sub['name']}: {sub['files']} 文件, {sub['lines']} 行\n"
            report += "\n"
        
        # 添加质量评估
        report += self.generate_quality_assessment()
        
        # 添加建议
        report += self.generate_recommendations()
        
        return report
    
    def generate_quality_assessment(self):
        """生成质量评估"""
        quality_score = 100
        
        # 根据问题数量扣分
        if self.stats['broken_links'] > 0:
            quality_score -= min(self.stats['broken_links'] * 2, 20)
        if self.stats['format_issues'] > 0:
            quality_score -= min(self.stats['format_issues'], 15)
        if self.stats['total_files'] < 30:
            quality_score -= 10
            
        quality_level = "优秀" if quality_score >= 90 else "良好" if quality_score >= 80 else "一般" if quality_score >= 70 else "需要改进"
        
        return f"""## 🎯 质量评估

- **质量评分**: {quality_score}/100 ({quality_level})
- **完整性**: {'✅ 完整' if self.stats['total_files'] >= 30 else '⚠️ 需要补充'}
- **链接质量**: {'✅ 良好' if self.stats['broken_links'] == 0 else f'⚠️ {self.stats["broken_links"]} 个损坏链接'}
- **格式规范**: {'✅ 规范' if self.stats['format_issues'] == 0 else f'⚠️ {self.stats["format_issues"]} 个格式问题'}

"""
    
    def generate_recommendations(self):
        """生成改进建议"""
        recommendations = []
        
        if self.stats['broken_links'] > 0:
            recommendations.append("🔗 修复损坏的链接")
        if self.stats['format_issues'] > 0:
            recommendations.append("📝 修正格式问题")
        if self.stats['total_files'] < 30:
            recommendations.append("📚 补充更多技术专题")
            
        # 检查章节完整性
        expected_sections = ['1', '2', '3', '4', '5', '6']
        missing_sections = [s for s in expected_sections if s not in self.stats['sections']]
        if missing_sections:
            recommendations.append(f"📂 补充缺失的章节: {', '.join(missing_sections)}")
        
        if not recommendations:
            recommendations.append("🎉 项目状态良好，继续保持！")
        
        return f"""## 💡 改进建议

{chr(10).join(f"- {rec}" for rec in recommendations)}

## 📅 更新历史

- **本次更新**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **上次更新**: {self.stats['last_updated']}

---
> 本报告由自动化工具生成，用于监控项目状态和质量。
"""
    
    def save_report(self, report):
        """保存报告"""
        report_path = self.root_dir / '项目状态报告.md'
        try:
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(report)
            print("✅ 项目状态报告已保存")
        except Exception as e:
            print(f"❌ 保存报告失败: {e}")
    
    def export_stats(self):
        """导出统计数据为JSON"""
        stats_path = self.root_dir / 'tools' / 'project_stats.json'
        try:
            with open(stats_path, 'w', encoding='utf-8') as f:
                json.dump(self.stats, f, ensure_ascii=False, indent=2)
            print("✅ 统计数据已导出")
        except Exception as e:
            print(f"❌ 导出统计数据失败: {e}")
    
    def run(self):
        """运行状态检查"""
        print("🚀 开始项目状态检查...\n")
        
        try:
            # 扫描项目
            self.scan_project()
            
            # 生成报告
            report = self.generate_report()
            
            # 保存报告
            self.save_report(report)
            
            # 导出统计数据
            self.export_stats()
            
            # 打印摘要
            print(f"\n📊 项目状态摘要:")
            print(f"   📁 总文件数: {self.stats['total_files']}")
            print(f"   📂 总目录数: {self.stats['total_dirs']}")
            print(f"   📝 总代码行数: {self.stats['total_lines']}")
            print(f"   🔗 损坏链接数: {self.stats['broken_links']}")
            print(f"   ⚠️ 格式问题数: {self.stats['format_issues']}")
            
            print("\n✅ 项目状态检查完成！")
            
        except Exception as e:
            print(f"❌ 状态检查过程中出现错误: {e}")

def main():
    """主函数"""
    checker = ProjectStatusChecker()
    checker.run()

if __name__ == '__main__':
    main() 