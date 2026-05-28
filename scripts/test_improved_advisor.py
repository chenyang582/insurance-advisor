import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from insurance_advisor import InsuranceAdvisor


def test_improved_advisor():
    print("=" * 70)
    print("测试优化后的保险顾问")
    print("=" * 70)

    advisor = InsuranceAdvisor()

    # 模拟用户输入 - 一次性输入完整信息
    test_input = """我叫张三，今年35岁，在上海工作，从事IT行业，年收入50万，有一套价值500万的房产。
我的妻子叫李四，32岁，是一名教师，工作稳定。我们有一个5岁的儿子，叫张小宝。
我的父亲今年62岁，母亲58岁，身体都还健康，他们在老家生活。
我希望为家人提供全面的保障，对重大疾病的治疗比较关注，希望能够获得优质的医疗资源。
我对保险的预算比较充足，希望能够建立一个完整的保障体系。"""

    print("\n模拟用户输入：")
    print("-" * 70)
    print(test_input)
    print("-" * 70)

    # 处理用户输入
    advisor.process_user_input(test_input)
    
    # 强制设置信息收集完成状态，以便测试
    advisor.info_status['name_collected'] = True
    advisor.info_status['family_collected'] = True
    advisor.info_status['economic_collected'] = True
    advisor.info_status['risk_collected'] = True

    print("\n" + "=" * 70)
    print("信息收集完成，检查解析结果：")
    print("=" * 70)

    # 输出解析的用户信息
    print(f"\n姓名: {advisor.user_info.get('name', '未获取')}")
    print(f"\n家庭成员:")
    for member in advisor.user_info.get('family_members', []):
        print(f"  - {member.get('role')}: {member.get('age')}岁, 健康状况: {member.get('health')}, 年龄组: {member.get('age_group')}")

    print(f"\n经济状况:")
    economic = advisor.user_info.get('economic_status', {})
    print(f"  - 收入: {economic.get('income')}万/年")
    print(f"  - 资产: {economic.get('assets')}万")
    print(f"  - 城市: {economic.get('city')}")
    print(f"  - 职业: {economic.get('occupation')}")
    print(f"  - 经济水平: {economic.get('economic_level')}")

    print(f"\n风险偏好:")
    risk = advisor.user_info.get('risk_preference', {})
    for key, value in risk.items():
        print(f"  - {key}: {value}")

    print(f"\n识别的场景:")
    scenarios = advisor.user_info.get('scenarios', [])
    for scenario in scenarios:
        print(f"  - {scenario}")

    print(f"\n隐藏需求:")
    hidden = advisor.user_info.get('hidden_needs', {})
    for key, value in hidden.items():
        print(f"  - {key}: {value}")

    print("\n" + "=" * 70)
    print("测试规则匹配:")
    print("=" * 70)

    if advisor.user_info.get('family_members'):
        for member in advisor.user_info.get('family_members', []):
            print(f"\n为 {member.get('role')} 匹配规则:")
            matched_rules = advisor._match_worth_buying_rules(
                member,
                advisor.user_info.get('scenarios', []),
                advisor.user_info.get('risk_preference', {})
            )

            if matched_rules:
                for i, match in enumerate(matched_rules, 1):
                    rule = match.get('rule', {})
                    print(f"\n  匹配规则 {i}:")
                    print(f"    - 保险类型: {rule.get('insurance_type')}")
                    print(f"    - 年龄组: {rule.get('age_group')}")
                    print(f"    - 保障期限: {rule.get('coverage_period')}")
                    print(f"    - 属性: {rule.get('investment_attribute')}")
                    print(f"    - 优势: {rule.get('advantages')[:100]}...")

                    base_amount = advisor._extract_recommended_amount(rule.get('worth_buying', []))
                    adjusted_amount = advisor._adjust_recommended_amount(
                        base_amount,
                        advisor.user_info.get('economic_status', {})
                    )
                    print(f"    - 推荐保额: {base_amount} -> {adjusted_amount}")

                    print(f"    - 匹配的场景: {match.get('matched_scenarios', [])}")
            else:
                print("  没有匹配到合适的规则")

    print("\n" + "=" * 70)
    print("生成推荐报告:")
    print("=" * 70)

    report_path = advisor.generate_recommendation()
    print(f"\n报告已生成: {report_path}")

    # 读取并显示报告内容的一部分（不打印以避免编码问题
    print(f"\n报告已成功保存至: {report_path}")
    print("报告生成完成。")

    print("\n" + "=" * 70)
    print("测试完成！")
    print("=" * 70)


if __name__ == '__main__':
    test_improved_advisor()
