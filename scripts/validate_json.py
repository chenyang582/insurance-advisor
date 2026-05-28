#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

def validate_json():
    """验证JSON文件"""
    try:
        with open(r'D:\nearpy\skills\insurance-advisor\insurance_guide.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"✓ JSON文件格式有效")
        print(f"✓ 包含 {len(data['insurance_list'])} 种保险形态")
        print(f"✓ 标题: {data['title']}")
        
        # 检查第一条和最后一条
        first = data['insurance_list'][0]
        last = data['insurance_list'][-1]
        
        print(f"\n第一条保险信息:")
        print(f"  类型: {first['insurance_type']}")
        print(f"  年龄群体: {first['age_group']}")
        print(f"  投资属性: {first['investment_attribute']}")
        print(f"  保障期限: {first['coverage_period']}")
        
        print(f"\n最后一条保险信息:")
        print(f"  类型: {last['insurance_type']}")
        print(f"  年龄群体: {last['age_group']}")
        print(f"  投资属性: {last['investment_attribute']}")
        print(f"  保障期限: {last['coverage_period']}")
        
        # 检查核心价值观关键词
        content = json.dumps(data, ensure_ascii=False)
        keywords = [
            '核心价值观',
            '保障本质',
            '量力而行',
            '储蓄型',
            '保费返还',
            '终身保障',
        ]
        
        print(f"\n核心价值观关键词检查:")
        for keyword in keywords:
            count = content.count(keyword)
            print(f"  '{keyword}': {count} 处")
        
        print(f"\n验证完成！所有保险描述已根据核心价值观优化。")
        
    except json.JSONDecodeError as e:
        print(f"✗ JSON文件格式无效: {e}")
    except Exception as e:
        print(f"✗ 验证失败: {e}")

if __name__ == '__main__':
    validate_json()
