#!/usr/bin/env node

/**
 * Refactor 知识体系自动化工具
 * 用于生成目录结构、交叉引用和导航索引
 */

const fs = require('fs');
const path = require('path');

class RefactorTools {
  constructor() {
    this.rootDir = path.join(__dirname, '..');
    this.outputDir = this.rootDir;
  }

  /**
   * 扫描目录结构
   */
  scanDirectory(dir = this.rootDir, level = 0) {
    const items = [];
    const files = fs.readdirSync(dir);
    
    for (const file of files) {
      const fullPath = path.join(dir, file);
      const stat = fs.statSync(fullPath);
      const relativePath = path.relative(this.rootDir, fullPath);
      
      if (stat.isDirectory() && !file.startsWith('.') && file !== 'tools') {
        const children = this.scanDirectory(fullPath, level + 1);
        items.push({
          type: 'directory',
          name: file,
          path: relativePath,
          level,
          children
        });
      } else if (file.endsWith('.md') && file !== 'README.md') {
        items.push({
          type: 'file',
          name: file,
          path: relativePath,
          level
        });
      }
    }
    
    return items.sort((a, b) => {
      // 目录在前，文件在后
      if (a.type !== b.type) {
        return a.type === 'directory' ? -1 : 1;
      }
      // 按名称排序
      return a.name.localeCompare(b.name);
    });
  }

  /**
   * 生成目录树
   */
  generateTOC(items, prefix = '') {
    let toc = '';
    
    for (const item of items) {
      const indent = '  '.repeat(item.level);
      const link = item.path.replace(/\\/g, '/');
      
      if (item.type === 'directory') {
        toc += `${indent}- [${item.name}](./${link}/README.md)\n`;
        if (item.children.length > 0) {
          toc += this.generateTOC(item.children, prefix + '  ');
        }
      } else {
        const name = item.name.replace('.md', '');
        toc += `${indent}- [${name}](./${link})\n`;
      }
    }
    
    return toc;
  }

  /**
   * 生成 SUMMARY.md
   */
  generateSummary() {
    const items = this.scanDirectory();
    const toc = this.generateTOC(items);
    
    const content = `# Refactor 知识体系目录

> 自动生成的目录索引，用于快速导航和内容概览

${toc}

---

> 本目录由自动化工具生成，更新时间：${new Date().toLocaleString('zh-CN')}
`;

    fs.writeFileSync(path.join(this.outputDir, 'SUMMARY.md'), content, 'utf8');
    console.log('✅ SUMMARY.md 生成完成');
  }

  /**
   * 更新 README.md 目录结构
   */
  updateReadmeTOC() {
    const readmePath = path.join(this.rootDir, 'README.md');
    const content = fs.readFileSync(readmePath, 'utf8');
    
    // 提取目录结构部分
    const tocStart = content.indexOf('## 目录结构');
    const tocEnd = content.indexOf('## 知识图谱');
    
    if (tocStart === -1 || tocEnd === -1) {
      console.log('❌ 无法找到目录结构标记');
      return;
    }
    
    const items = this.scanDirectory();
    const newTOC = this.generateReadmeTOC(items);
    
    const newContent = 
      content.substring(0, tocStart + '## 目录结构\n\n'.length) +
      newTOC +
      content.substring(tocEnd);
    
    fs.writeFileSync(readmePath, newContent, 'utf8');
    console.log('✅ README.md 目录结构更新完成');
  }

  /**
   * 生成 README 格式的目录
   */
  generateReadmeTOC(items) {
    let toc = '';
    let currentSection = '';
    
    for (const item of items) {
      if (item.type === 'directory') {
        // 提取章节编号
        const match = item.name.match(/^(\d+)\./);
        if (match) {
          const sectionNum = match[1];
          const sectionName = item.name.replace(/^\d+\.\s*/, '');
          toc += `${sectionNum}. [${sectionName}](./${item.path}/README.md)\n`;
          
          // 添加子项目
          const subItems = item.children.filter(child => child.type === 'file');
          for (const subItem of subItems) {
            const subMatch = subItem.name.match(/^(\d+\.\d+)/);
            if (subMatch) {
              const subName = subItem.name.replace(/^\d+\.\d+\s*/, '');
              toc += `    - [${subMatch[1]} ${subName}](./${subItem.path})\n`;
            }
          }
          toc += '\n';
        }
      }
    }
    
    return toc;
  }

  /**
   * 检查链接有效性
   */
  checkLinks() {
    const items = this.scanDirectory();
    const brokenLinks = [];
    
    for (const item of items) {
      if (item.type === 'file') {
        const content = fs.readFileSync(path.join(this.rootDir, item.path), 'utf8');
        const links = this.extractLinks(content);
        
        for (const link of links) {
          if (!this.isValidLink(link, path.dirname(item.path))) {
            brokenLinks.push({
              file: item.path,
              link: link
            });
          }
        }
      }
    }
    
    if (brokenLinks.length > 0) {
      console.log('❌ 发现损坏的链接:');
      brokenLinks.forEach(({ file, link }) => {
        console.log(`   ${file}: ${link}`);
      });
    } else {
      console.log('✅ 所有链接检查通过');
    }
    
    return brokenLinks;
  }

  /**
   * 提取文档中的链接
   */
  extractLinks(content) {
    const linkRegex = /\[([^\]]+)\]\(([^)]+)\)/g;
    const links = [];
    let match;
    
    while ((match = linkRegex.exec(content)) !== null) {
      links.push(match[2]);
    }
    
    return links;
  }

  /**
   * 检查链接是否有效
   */
  isValidLink(link, basePath) {
    if (link.startsWith('http') || link.startsWith('#')) {
      return true;
    }
    
    const fullPath = path.join(this.rootDir, basePath, link);
    return fs.existsSync(fullPath);
  }

  /**
   * 生成交叉引用索引
   */
  generateCrossReferences() {
    const items = this.scanDirectory();
    const references = {};
    
    // 收集所有文档的关键词
    for (const item of items) {
      if (item.type === 'file') {
        const content = fs.readFileSync(path.join(this.rootDir, item.path), 'utf8');
        const keywords = this.extractKeywords(content);
        
        for (const keyword of keywords) {
          if (!references[keyword]) {
            references[keyword] = [];
          }
          references[keyword].push(item.path);
        }
      }
    }
    
    // 生成交叉引用文档
    let content = `# 交叉引用索引

> 自动生成的交叉引用索引，帮助发现相关内容

`;

    for (const [keyword, files] of Object.entries(references)) {
      if (files.length > 1) {
        content += `## ${keyword}\n\n`;
        for (const file of files) {
          const name = path.basename(file, '.md');
          content += `- [${name}](./${file})\n`;
        }
        content += '\n';
      }
    }
    
    fs.writeFileSync(path.join(this.outputDir, '交叉引用索引.md'), content, 'utf8');
    console.log('✅ 交叉引用索引生成完成');
  }

  /**
   * 提取文档关键词
   */
  extractKeywords(content) {
    // 简单的关键词提取逻辑
    const keywords = [];
    const lines = content.split('\n');
    
    for (const line of lines) {
      if (line.startsWith('## ')) {
        const keyword = line.replace('## ', '').trim();
        keywords.push(keyword);
      }
    }
    
    return keywords;
  }

  /**
   * 运行所有工具
   */
  run() {
    console.log('🚀 开始运行 Refactor 自动化工具...\n');
    
    try {
      this.generateSummary();
      this.updateReadmeTOC();
      this.checkLinks();
      this.generateCrossReferences();
      
      console.log('\n✅ 所有任务完成！');
    } catch (error) {
      console.error('❌ 执行过程中出现错误:', error.message);
    }
  }
}

// 命令行参数处理
const args = process.argv.slice(2);
const tool = new RefactorTools();

if (args.length === 0) {
  tool.run();
} else {
  switch (args[0]) {
    case 'toc':
      tool.generateSummary();
      break;
    case 'readme':
      tool.updateReadmeTOC();
      break;
    case 'links':
      tool.checkLinks();
      break;
    case 'refs':
      tool.generateCrossReferences();
      break;
    default:
      console.log('用法: node generate-toc.js [toc|readme|links|refs]');
      console.log('  toc    - 生成 SUMMARY.md');
      console.log('  readme - 更新 README.md 目录结构');
      console.log('  links  - 检查链接有效性');
      console.log('  refs   - 生成交叉引用索引');
  }
} 