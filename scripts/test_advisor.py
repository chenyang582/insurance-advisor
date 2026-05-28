import sys
from io import StringIO
from insurance_advisor import InsuranceAdvisor

def test_insurance_advisor():
    advisor = InsuranceAdvisor()
    
    test_input = "我叫张三，35岁，在上海工作，IT行业，年收入50万，有一套价值500万的房产。我和妻子（32岁）有一个5岁的孩子，父母都在老家，身体都很健康。我希望如果发生重大疾病能得到高端治疗，也希望能为家人留下足够的保障。"
    
    print("测试输入：")
    print(test_input)
    print("\n" + "="*50)
    
    advisor.user_info = {
        'name': advisor._extract_name(test_input),
        'family_members': advisor._extract_family_members(test_input),
        'economic_status': advisor._extract_economic_status(test_input),
        'risk_preference': advisor._analyze_risk_preference(test_input)
    }
    
    print("解析结果：")
    print(f"姓名: {advisor.user_info['name']}")
    print(f"家庭成员: {advisor.user_info['family_members']}")
    print(f"经济状况: {advisor.user_info['economic_status']}")
    print(f"风险偏好: {advisor.user_info['risk_preference']}")
    print("\n" + "="*50)
    
    print("生成推荐报告...")
    report_path = advisor.generate_recommendation()
    print(f"报告已生成: {report_path}")
    
    with open(report_path, 'r', encoding='utf-8') as f:
        content = f.read()
        print("\n报告内容预览（前2000字符）:")
        print(content[:2000])

if __name__ == '__main__':
    test_insurance_advisor()