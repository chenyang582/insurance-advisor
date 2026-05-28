#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import re

def load_insurance_guide():
    """加载保险指南文件"""
    with open(r'D:\nearpy\skills\insurance-advisor\insurance_guide.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def save_insurance_guide(data):
    """保存优化后的保险指南文件"""
    with open(r'D:\nearpy\skills\insurance-advisor\insurance_guide.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def optimize_advantages(text, insurance_info):
    """优化优势描述"""
    insurance_type = insurance_info['insurance_type']
    age_group = insurance_info['age_group']
    investment_attribute = insurance_info['investment_attribute']
    coverage_period = insurance_info['coverage_period']
    
    if investment_attribute == '投资':
        return f"【核心价值观提示】投资型保险产品不是最佳选择。{text}"
    
    if '终身' in coverage_period:
        return f"【核心价值观提示】终身保障保费过高，不符合量力而行原则。{text}"
    
    return text

def optimize_disadvantages(text, insurance_info):
    """优化劣势描述"""
    insurance_type = insurance_info['insurance_type']
    age_group = insurance_info['age_group']
    investment_attribute = insurance_info['investment_attribute']
    coverage_period = insurance_info['coverage_period']
    
    if investment_attribute == '投资':
        text += "【核心价值观强调】储蓄型保险'1000元保费只能买回1200元保额'，大部分保费用于投资而非保障，违背保险的保障本质。"
    
    if '终身' in coverage_period:
        text += "【核心价值观强调】保险期间越长，保险成本越高，保费肯定就越高，应优先选择保20年或保至70岁。"
    
    if age_group == '老年' and insurance_type in ['健康险', '医疗险', '重疾险']:
        text += "【核心价值观强调】老年人风险是年轻人的几十倍，保费非常高，通过储蓄存钱可能是更好的选择。"
    
    return text

def optimize_worth_buying(reasons, insurance_info):
    """优化值得购买的理由"""
    insurance_type = insurance_info['insurance_type']
    age_group = insurance_info['age_group']
    investment_attribute = insurance_info['investment_attribute']
    coverage_period = insurance_info['coverage_period']
    
    if investment_attribute == '投资':
        return [{
            "scenario": "无合理购买场景",
            "reason": "【核心价值观明确】投资型保险不是保险的本质功能。保险的核心是风险转移和保障，不是投资或储蓄。投资型保险风险保额低，大部分保费用于投资而非保障，性价比极低。"
        }]
    
    if '终身' in coverage_period:
        return [{
            "scenario": "经济条件极其优越",
            "reason": "【核心价值观提示】终身保障'囊中羞涩'时应选择保至70岁。只有经济实力允许时才考虑终身产品。"
        }]
    
    optimized_reasons = []
    for item in reasons:
        reason_text = item['reason']
        
        if insurance_type == '房屋保险':
            reason_text = f"【核心价值观强调】房屋保险是家家户户一定要购买的财产险产品。{reason_text}"
        
        if insurance_type == '重大疾病保险':
            reason_text = f"【核心价值观强调】重大疾病治疗费会给患者家庭带来严重财务影响，重疾保额建议50万元以上。{reason_text}"
        
        if insurance_type == '定期寿险' and coverage_period == '70岁':
            reason_text = f"【核心价值观强调】定期寿险保至70岁即可，因为届时子女已成年并工作，经济独立。{reason_text}"
        
        if age_group == '老年' and insurance_type in ['医疗险', '健康险']:
            reason_text = f"【核心价值观提示】老年人优先选择惠民保和体检。{reason_text}"
        
        optimized_reasons.append({
            "scenario": item['scenario'],
            "reason": reason_text
        })
    
    return optimized_reasons

def optimize_not_worth_buying(reasons, insurance_info):
    """优化不值得购买的理由"""
    insurance_type = insurance_info['insurance_type']
    age_group = insurance_info['age_group']
    investment_attribute = insurance_info['investment_attribute']
    coverage_period = insurance_info['coverage_period']
    
    optimized_reasons = []
    
    if investment_attribute == '投资':
        optimized_reasons.append({
            "scenario": "所有普通家庭",
            "reason": "【核心价值观明确反对】储蓄型保险产品'保费很高但保障内容较低'，风险保额比较低，大部分保费用于投资而非保障。利差对保险公司利润的贡献非常大，保险公司非常欢迎这种业务。消费者应警惕'看起来是保障型但又有相对很高现金价值'的产品。"
        })
        return optimized_reasons
    
    if '终身' in coverage_period:
        optimized_reasons.append({
            "scenario": "大多数家庭",
            "reason": "【核心价值观明确反对】保险期间越长，保险成本越高，保费肯定就越高。保至70岁即可满足家庭责任需求。终身产品'囊中羞涩'时应量力而行，不追求终身保障。"
        })
        return optimized_reasons
    
    for item in reasons:
        reason_text = item['reason']
        
        if '保费返还' in reason_text or '返还型' in str(reasons):
            reason_text = f"【核心价值观明确反对】保费返还型保险本质是储蓄型保险，'羊毛出在羊身上'。保费先借给保险公司做投资，投资收入覆盖理赔成本和运营成本。{reason_text}"
        
        if age_group == '老年' and insurance_type in ['医疗险', '健康险', '重疾险']:
            reason_text = f"【核心价值观明确反对】老年人风险是年轻人的几十倍，保费非常高。对于老年人的保障，也许通过储蓄存钱是更好的选择。{reason_text}"
        
        if insurance_type == '高端医疗保险':
            reason_text = f"【核心价值观明确反对】高端医疗保险'不是必需的'。为了更好的就医体验，可以直接去相应医疗机构就诊，费用很可能比保费少。高端医疗保险动辄几百万元保额在国内用不上。不能保证续保并且费率不保证，性价比低。{reason_text}"
        
        if insurance_type == '教育金':
            reason_text = f"【核心价值观明确反对】教育金本质是储蓄型保险产品，'从所谓收益来说，不认为教育金产品会有多大的优越性'。最大优点是间接性的强制储蓄，但收益不优越。{reason_text}"
        
        optimized_reasons.append({
            "scenario": item['scenario'],
            "reason": reason_text
        })
    
    return optimized_reasons

def optimize_insurance_item(item):
    """优化单个保险条目"""
    insurance_type = item['insurance_type']
    age_group = item['age_group']
    investment_attribute = item['investment_attribute']
    coverage_period = item['coverage_period']
    
    item['advantages'] = optimize_advantages(item['advantages'], item)
    item['disadvantages'] = optimize_disadvantages(item['disadvantages'], item)
    item['worth_buying'] = optimize_worth_buying(item['worth_buying'], item)
    item['not_worth_buying'] = optimize_not_worth_buying(item['not_worth_buying'], item)
    
    return item

def optimize_all_insurances():
    """优化所有保险条目"""
    print("开始加载保险指南文件...")
    data = load_insurance_guide()
    
    print(f"开始优化 {len(data['insurance_list'])} 种保险形态...")
    
    for i, item in enumerate(data['insurance_list']):
        data['insurance_list'][i] = optimize_insurance_item(item)
        if (i + 1) % 10 == 0:
            print(f"已优化 {i + 1}/{len(data['insurance_list'])} 种保险")
    
    print("开始保存优化后的文件...")
    save_insurance_guide(data)
    
    print("优化完成！")

if __name__ == '__main__':
    optimize_all_insurances()
