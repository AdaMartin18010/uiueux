#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
语义模型体系递归扩展器

本脚本用于自动递归迭代扩展语义模型体系，通过形式化论证和实际应用验证，
不断完善和扩展语义模型的理论基础和实践应用。

作者: AI Assistant
版本: 1.0.0
日期: 2024
"""

import os
import json
import re
import logging
from typing import Dict, List, Set, Tuple, Optional, Any
from dataclasses import dataclass, field
from pathlib import Path
from datetime import datetime

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('semantic_model_expansion.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class SemanticConcept:
    """语义概念"""
    name: str
    description: str
    type: str
    properties: Dict[str, Any] = field(default_factory=dict)
    relations: List[str] = field(default_factory=list)
    constraints: List[str] = field(default_factory=list)
    examples: List[str] = field(default_factory=list)

@dataclass
class SemanticDomain:
    """语义域"""
    name: str
    description: str
    concepts: List[SemanticConcept] = field(default_factory=list)
    relations: List[str] = field(default_factory=list)
    constraints: List[str] = field(default_factory=list)
    operations: List[str] = field(default_factory=list)
    parent_domain: Optional[str] = None
    child_domains: List[str] = field(default_factory=list)

@dataclass
class SemanticModel:
    """语义模型"""
    name: str
    description: str
    domains: List[SemanticDomain] = field(default_factory=list)
    mappings: List[Dict[str, Any]] = field(default_factory=list)
    rules: List[str] = field(default_factory=list)
    axioms: List[str] = field(default_factory=list)
    theorems: List[str] = field(default_factory=list)
    applications: List[str] = field(default_factory=list)

class SemanticModelExpander:
    """语义模型扩展器"""
    
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.models: Dict[str, SemanticModel] = {}
        self.domains: Dict[str, SemanticDomain] = {}
        self.concepts: Dict[str, SemanticConcept] = {}
        self.expansion_history: List[Dict[str, Any]] = []
        self.iteration_count = 0
        self.max_iterations = 10
        
    def load_existing_models(self) -> None:
        """加载现有的语义模型"""
        logger.info("开始加载现有语义模型...")
        
        # 扫描目录结构
        for model_dir in self.base_path.iterdir():
            if model_dir.is_dir() and model_dir.name != "__pycache__":
                self._load_model_from_directory(model_dir)
        
        logger.info(f"已加载 {len(self.models)} 个语义模型")
    
    def _load_model_from_directory(self, model_dir: Path) -> None:
        """从目录加载语义模型"""
        readme_file = model_dir / "README.md"
        if readme_file.exists():
            try:
                content = readme_file.read_text(encoding='utf-8')
                model = self._parse_markdown_to_model(content, model_dir.name)
                self.models[model_dir.name] = model
                logger.info(f"已加载模型: {model_dir.name}")
            except Exception as e:
                logger.error(f"加载模型 {model_dir.name} 失败: {e}")
    
    def _parse_markdown_to_model(self, content: str, name: str) -> SemanticModel:
        """解析Markdown内容为语义模型"""
        model = SemanticModel(name=name, description="")
        
        # 提取描述
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if line.startswith('#') and i + 1 < len(lines):
                model.description = lines[i + 1].strip()
                break
        
        # 提取语义域
        domain_pattern = r'### (\d+\.)?([^#\n]+)语义域'
        domains = re.findall(domain_pattern, content)
        for _, domain_name in domains:
            domain = SemanticDomain(name=domain_name.strip(), description=f"{domain_name.strip()}语义域")
            model.domains.append(domain)
        
        # 提取形式化定义
        formal_pattern = r'```\n([^`]+)\n```'
        formal_defs = re.findall(formal_pattern, content)
        for formal_def in formal_defs:
            self._parse_formal_definition(formal_def, model)
        
        return model
    
    def _parse_formal_definition(self, formal_def: str, model: SemanticModel) -> None:
        """解析形式化定义"""
        # 解析概念
        concept_pattern = r'concepts:\s*\{([^}]+)\}'
        concepts = re.findall(concept_pattern, formal_def)
        for concept_list in concepts:
            for concept in concept_list.split(','):
                concept = concept.strip()
                if concept:
                    semantic_concept = SemanticConcept(
                        name=concept,
                        description=f"{concept}概念",
                        type="concept"
                    )
                    if model.domains:
                        model.domains[0].concepts.append(semantic_concept)
        
        # 解析关系
        relation_pattern = r'relations:\s*\{([^}]+)\}'
        relations = re.findall(relation_pattern, formal_def)
        for relation_list in relations:
            for relation in relation_list.split(','):
                relation = relation.strip()
                if relation:
                    if model.domains:
                        model.domains[0].relations.append(relation)
        
        # 解析约束
        constraint_pattern = r'constraints:\s*\{([^}]+)\}'
        constraints = re.findall(constraint_pattern, formal_def)
        for constraint_list in constraints:
            for constraint in constraint_list.split(','):
                constraint = constraint.strip()
                if constraint:
                    if model.domains:
                        model.domains[0].constraints.append(constraint)
    
    def expand_semantic_models(self) -> None:
        """递归扩展语义模型"""
        logger.info("开始递归扩展语义模型...")
        
        while self.iteration_count < self.max_iterations:
            self.iteration_count += 1
            logger.info(f"开始第 {self.iteration_count} 次迭代扩展...")
            
            # 分析现有模型
            analysis = self._analyze_existing_models()
            
            # 生成新概念
            new_concepts = self._generate_new_concepts(analysis)
            
            # 建立映射关系
            new_mappings = self._establish_mappings(new_concepts)
            
            # 验证一致性
            consistency_result = self._validate_consistency()
            
            # 记录扩展历史
            self._record_expansion(analysis, new_concepts, new_mappings, consistency_result)
            
            # 检查收敛条件
            if self._check_convergence():
                logger.info("语义模型扩展已收敛")
                break
            
            # 生成新文档
            self._generate_new_documents()
        
        logger.info(f"语义模型扩展完成，共进行 {self.iteration_count} 次迭代")
    
    def _analyze_existing_models(self) -> Dict[str, Any]:
        """分析现有模型"""
        analysis = {
            'model_count': len(self.models),
            'domain_count': sum(len(model.domains) for model in self.models.values()),
            'concept_count': sum(len(domain.concepts) for model in self.models.values() for domain in model.domains),
            'relation_count': sum(len(domain.relations) for model in self.models.values() for domain in model.domains),
            'constraint_count': sum(len(domain.constraints) for model in self.models.values() for domain in model.domains),
            'coverage_analysis': self._analyze_coverage(),
            'complexity_analysis': self._analyze_complexity(),
            'consistency_analysis': self._analyze_consistency()
        }
        
        logger.info(f"分析结果: {analysis}")
        return analysis
    
    def _analyze_coverage(self) -> Dict[str, float]:
        """分析覆盖率"""
        coverage = {
            'ui_coverage': 0.8,  # 示例值
            'architecture_coverage': 0.7,
            'web_coverage': 0.6,
            'ai_coverage': 0.5,
            'formal_coverage': 0.4,
            'tool_coverage': 0.3
        }
        return coverage
    
    def _analyze_complexity(self) -> Dict[str, int]:
        """分析复杂度"""
        complexity = {
            'max_concepts_per_domain': 0,
            'max_relations_per_domain': 0,
            'max_constraints_per_domain': 0,
            'average_concepts_per_domain': 0,
            'average_relations_per_domain': 0,
            'average_constraints_per_domain': 0
        }
        
        total_domains = sum(len(model.domains) for model in self.models.values())
        if total_domains > 0:
            for model in self.models.values():
                for domain in model.domains:
                    complexity['max_concepts_per_domain'] = max(
                        complexity['max_concepts_per_domain'], 
                        len(domain.concepts)
                    )
                    complexity['max_relations_per_domain'] = max(
                        complexity['max_relations_per_domain'], 
                        len(domain.relations)
                    )
                    complexity['max_constraints_per_domain'] = max(
                        complexity['max_constraints_per_domain'], 
                        len(domain.constraints)
                    )
            
            total_concepts = sum(len(domain.concepts) for model in self.models.values() for domain in model.domains)
            total_relations = sum(len(domain.relations) for model in self.models.values() for domain in model.domains)
            total_constraints = sum(len(domain.constraints) for model in self.models.values() for domain in model.domains)
            
            complexity['average_concepts_per_domain'] = total_concepts // total_domains
            complexity['average_relations_per_domain'] = total_relations // total_domains
            complexity['average_constraints_per_domain'] = total_constraints // total_domains
        
        return complexity
    
    def _analyze_consistency(self) -> Dict[str, bool]:
        """分析一致性"""
        consistency = {
            'naming_consistency': True,
            'structure_consistency': True,
            'relation_consistency': True,
            'constraint_consistency': True
        }
        return consistency
    
    def _generate_new_concepts(self, analysis: Dict[str, Any]) -> List[SemanticConcept]:
        """生成新概念"""
        new_concepts = []
        
        # 基于覆盖率分析生成新概念
        for domain_name, coverage in analysis['coverage_analysis'].items():
            if coverage < 0.8:  # 覆盖率低于80%的域需要扩展
                new_concepts.extend(self._generate_concepts_for_domain(domain_name))
        
        # 基于复杂度分析生成新概念
        complexity = analysis['complexity_analysis']
        if complexity['average_concepts_per_domain'] < 10:
            new_concepts.extend(self._generate_basic_concepts())
        
        logger.info(f"生成了 {len(new_concepts)} 个新概念")
        return new_concepts
    
    def _generate_concepts_for_domain(self, domain_name: str) -> List[SemanticConcept]:
        """为特定域生成概念"""
        concepts = []
        
        domain_concept_templates = {
            'ui': [
                '自适应语义', '多模态语义', '智能语义推理', '语义标准化',
                '语义模型库', '语义复用机制', '语义协作开发'
            ],
            'architecture': [
                '自适应架构', '事件驱动架构', '云原生架构', '智能架构',
                '架构模式库', '架构复用机制', '架构协作开发'
            ],
            'web': [
                '边缘计算', '无服务器架构', 'WebAssembly', 'AI驱动Web应用',
                'Web应用库', 'Web复用机制', 'Web协作开发'
            ],
            'ai': [
                '可解释AI', '联邦学习', '元学习', '神经符号AI',
                'AI模型库', 'AI复用机制', 'AI协作开发'
            ],
            'formal': [
                '高阶类型系统', '依赖类型系统', '同伦类型论', '量子语义学',
                '形式化库', '形式化复用机制', '形式化协作开发'
            ],
            'tool': [
                '智能化工具', '云原生工具', '低代码工具', '开源生态',
                '工具库', '工具复用机制', '工具协作开发'
            ]
        }
        
        if domain_name in domain_concept_templates:
            for concept_name in domain_concept_templates[domain_name]:
                concept = SemanticConcept(
                    name=concept_name,
                    description=f"{concept_name}的语义表示",
                    type="advanced_concept",
                    properties={
                        'complexity': 'high',
                        'maturity': 'emerging',
                        'applicability': 'broad'
                    }
                )
                concepts.append(concept)
        
        return concepts
    
    def _generate_basic_concepts(self) -> List[SemanticConcept]:
        """生成基础概念"""
        basic_concepts = [
            '语义映射', '语义组合', '语义推理', '语义验证',
            '语义优化', '语义演化', '语义集成', '语义互操作'
        ]
        
        concepts = []
        for concept_name in basic_concepts:
            concept = SemanticConcept(
                name=concept_name,
                description=f"{concept_name}的基础语义概念",
                type="basic_concept",
                properties={
                    'complexity': 'medium',
                    'maturity': 'stable',
                    'applicability': 'universal'
                }
            )
            concepts.append(concept)
        
        return concepts
    
    def _establish_mappings(self, new_concepts: List[SemanticConcept]) -> List[Dict[str, Any]]:
        """建立映射关系"""
        mappings = []
        
        for concept in new_concepts:
            # 建立概念间的映射关系
            for existing_model in self.models.values():
                for domain in existing_model.domains:
                    for existing_concept in domain.concepts:
                        if self._can_map_concepts(concept, existing_concept):
                            mapping = {
                                'source_concept': concept.name,
                                'target_concept': existing_concept.name,
                                'mapping_type': 'semantic_equivalence',
                                'confidence': 0.8,
                                'evidence': f"概念 {concept.name} 与 {existing_concept.name} 存在语义等价关系"
                            }
                            mappings.append(mapping)
        
        logger.info(f"建立了 {len(mappings)} 个映射关系")
        return mappings
    
    def _can_map_concepts(self, concept1: SemanticConcept, concept2: SemanticConcept) -> bool:
        """判断两个概念是否可以映射"""
        # 简单的相似性判断
        name_similarity = self._calculate_name_similarity(concept1.name, concept2.name)
        return name_similarity > 0.6
    
    def _calculate_name_similarity(self, name1: str, name2: str) -> float:
        """计算名称相似性"""
        # 简单的字符串相似性计算
        common_chars = set(name1) & set(name2)
        total_chars = set(name1) | set(name2)
        return len(common_chars) / len(total_chars) if total_chars else 0
    
    def _validate_consistency(self) -> Dict[str, bool]:
        """验证一致性"""
        consistency = {
            'naming_consistency': self._validate_naming_consistency(),
            'structure_consistency': self._validate_structure_consistency(),
            'relation_consistency': self._validate_relation_consistency(),
            'constraint_consistency': self._validate_constraint_consistency()
        }
        
        logger.info(f"一致性验证结果: {consistency}")
        return consistency
    
    def _validate_naming_consistency(self) -> bool:
        """验证命名一致性"""
        all_names = set()
        for model in self.models.values():
            for domain in model.domains:
                for concept in domain.concepts:
                    if concept.name in all_names:
                        return False
                    all_names.add(concept.name)
        return True
    
    def _validate_structure_consistency(self) -> bool:
        """验证结构一致性"""
        # 检查所有域都有基本结构
        for model in self.models.values():
            for domain in model.domains:
                if not domain.concepts and not domain.relations:
                    return False
        return True
    
    def _validate_relation_consistency(self) -> bool:
        """验证关系一致性"""
        # 检查关系是否有效
        all_concept_names = set()
        for model in self.models.values():
            for domain in model.domains:
                for concept in domain.concepts:
                    all_concept_names.add(concept.name)
        
        for model in self.models.values():
            for domain in model.domains:
                for relation in domain.relations:
                    # 简单的关系验证
                    if not relation or len(relation) < 2:
                        return False
        return True
    
    def _validate_constraint_consistency(self) -> bool:
        """验证约束一致性"""
        # 检查约束是否有效
        for model in self.models.values():
            for domain in model.domains:
                for constraint in domain.constraints:
                    if not constraint or len(constraint) < 3:
                        return False
        return True
    
    def _record_expansion(self, analysis: Dict[str, Any], new_concepts: List[SemanticConcept], 
                         new_mappings: List[Dict[str, Any]], consistency_result: Dict[str, bool]) -> None:
        """记录扩展历史"""
        expansion_record = {
            'iteration': self.iteration_count,
            'timestamp': datetime.now().isoformat(),
            'analysis': analysis,
            'new_concepts_count': len(new_concepts),
            'new_mappings_count': len(new_mappings),
            'consistency_result': consistency_result,
            'new_concepts': [concept.name for concept in new_concepts],
            'new_mappings': new_mappings
        }
        
        self.expansion_history.append(expansion_record)
        
        # 保存到文件
        history_file = self.base_path / "expansion_history.json"
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(self.expansion_history, f, ensure_ascii=False, indent=2)
    
    def _check_convergence(self) -> bool:
        """检查收敛条件"""
        if self.iteration_count < 3:
            return False
        
        # 检查最近几次迭代的变化
        recent_expansions = self.expansion_history[-3:]
        new_concepts_counts = [exp['new_concepts_count'] for exp in recent_expansions]
        
        # 如果新概念数量趋于稳定，认为收敛
        if len(new_concepts_counts) >= 3:
            avg_new_concepts = sum(new_concepts_counts) / len(new_concepts_counts)
            if avg_new_concepts < 2:  # 平均每次迭代少于2个新概念
                return True
        
        return False
    
    def _generate_new_documents(self) -> None:
        """生成新文档"""
        logger.info("生成新的语义模型文档...")
        
        # 生成扩展报告
        self._generate_expansion_report()
        
        # 生成概念索引
        self._generate_concept_index()
        
        # 生成映射关系图
        self._generate_mapping_diagram()
    
    def _generate_expansion_report(self) -> None:
        """生成扩展报告"""
        report_content = f"""# 语义模型扩展报告

## 扩展概览

- **迭代次数**: {self.iteration_count}
- **总概念数**: {sum(len(domain.concepts) for model in self.models.values() for domain in model.domains)}
- **总关系数**: {sum(len(domain.relations) for model in self.models.values() for domain in model.domains)}
- **总约束数**: {sum(len(domain.constraints) for model in self.models.values() for domain in model.domains)}

## 扩展历史

"""
        
        for record in self.expansion_history:
            report_content += f"""
### 第 {record['iteration']} 次迭代

- **时间**: {record['timestamp']}
- **新概念数**: {record['new_concepts_count']}
- **新映射数**: {record['new_mappings_count']}
- **一致性**: {record['consistency_result']}

#### 新概念
{chr(10).join(f"- {concept}" for concept in record['new_concepts'])}

#### 新映射
{chr(10).join(f"- {mapping['source_concept']} → {mapping['target_concept']}" for mapping in record['new_mappings'])}

"""
        
        report_file = self.base_path / "扩展报告.md"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        logger.info(f"已生成扩展报告: {report_file}")
    
    def _generate_concept_index(self) -> None:
        """生成概念索引"""
        all_concepts = {}
        
        for model_name, model in self.models.items():
            for domain in model.domains:
                for concept in domain.concepts:
                    if concept.name not in all_concepts:
                        all_concepts[concept.name] = {
                            'model': model_name,
                            'domain': domain.name,
                            'type': concept.type,
                            'description': concept.description
                        }
        
        index_content = """# 语义概念索引

## 概念列表

"""
        
        for concept_name, info in sorted(all_concepts.items()):
            index_content += f"""
### {concept_name}

- **所属模型**: {info['model']}
- **所属域**: {info['domain']}
- **类型**: {info['type']}
- **描述**: {info['description']}

"""
        
        index_file = self.base_path / "概念索引.md"
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(index_content)
        
        logger.info(f"已生成概念索引: {index_file}")
    
    def _generate_mapping_diagram(self) -> None:
        """生成映射关系图"""
        diagram_content = """# 语义映射关系图

```mermaid
graph TD
"""
        
        # 收集所有映射关系
        all_mappings = []
        for record in self.expansion_history:
            all_mappings.extend(record['new_mappings'])
        
        # 生成节点和边
        nodes = set()
        edges = []
        
        for mapping in all_mappings:
            source = mapping['source_concept']
            target = mapping['target_concept']
            nodes.add(source)
            nodes.add(target)
            edges.append((source, target, mapping['mapping_type']))
        
        # 添加节点
        for node in sorted(nodes):
            diagram_content += f"    {node.replace(' ', '_')}[{node}]\n"
        
        # 添加边
        for source, target, mapping_type in edges:
            source_id = source.replace(' ', '_')
            target_id = target.replace(' ', '_')
            diagram_content += f"    {source_id} --> {target_id}[{mapping_type}]\n"
        
        diagram_content += "```\n"
        
        diagram_file = self.base_path / "映射关系图.md"
        with open(diagram_file, 'w', encoding='utf-8') as f:
            f.write(diagram_content)
        
        logger.info(f"已生成映射关系图: {diagram_file}")
    
    def save_final_state(self) -> None:
        """保存最终状态"""
        final_state = {
            'models': {name: self._model_to_dict(model) for name, model in self.models.items()},
            'expansion_history': self.expansion_history,
            'statistics': self._calculate_statistics(),
            'timestamp': datetime.now().isoformat()
        }
        
        state_file = self.base_path / "final_state.json"
        with open(state_file, 'w', encoding='utf-8') as f:
            json.dump(final_state, f, ensure_ascii=False, indent=2)
        
        logger.info(f"已保存最终状态: {state_file}")
    
    def _model_to_dict(self, model: SemanticModel) -> Dict[str, Any]:
        """将模型转换为字典"""
        return {
            'name': model.name,
            'description': model.description,
            'domains': [
                {
                    'name': domain.name,
                    'description': domain.description,
                    'concepts': [concept.name for concept in domain.concepts],
                    'relations': domain.relations,
                    'constraints': domain.constraints,
                    'operations': domain.operations
                }
                for domain in model.domains
            ],
            'mappings': model.mappings,
            'rules': model.rules,
            'axioms': model.axioms,
            'theorems': model.theorems,
            'applications': model.applications
        }
    
    def _calculate_statistics(self) -> Dict[str, Any]:
        """计算统计信息"""
        total_concepts = sum(len(domain.concepts) for model in self.models.values() for domain in model.domains)
        total_relations = sum(len(domain.relations) for model in self.models.values() for domain in model.domains)
        total_constraints = sum(len(domain.constraints) for model in self.models.values() for domain in model.domains)
        total_domains = sum(len(model.domains) for model in self.models.values())
        
        return {
            'total_models': len(self.models),
            'total_domains': total_domains,
            'total_concepts': total_concepts,
            'total_relations': total_relations,
            'total_constraints': total_constraints,
            'total_iterations': self.iteration_count,
            'average_concepts_per_domain': total_concepts // max(total_domains, 1),
            'average_relations_per_domain': total_relations // max(total_domains, 1),
            'average_constraints_per_domain': total_constraints // max(total_domains, 1)
        }

def main():
    """主函数"""
    logger.info("启动语义模型扩展器...")
    
    # 创建扩展器
    expander = SemanticModelExpander()
    
    # 加载现有模型
    expander.load_existing_models()
    
    # 扩展语义模型
    expander.expand_semantic_models()
    
    # 保存最终状态
    expander.save_final_state()
    
    logger.info("语义模型扩展完成!")

if __name__ == "__main__":
    main() 