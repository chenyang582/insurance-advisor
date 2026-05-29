import os

def fix_dynamic_conclusion():
    advisor_path = 'D:/nearpy/04 skillhub/insurance-advisor/scripts/insurance_advisor.py'
    
    with open(advisor_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 找到并修复_get_dynamic_conclusion方法
    old_conclusion = '''    def _get_dynamic_conclusion(self) -> str:
        name = self.user_info.get('name', '您')
        tone_style = self._determine_tone_style()
        
        conclusions = {
            'warm': [
                f"## 💝 写在最后\n\n{name}，这份方案是我根据您的家庭情况用心定制的，希望能帮助您和家人建立起坚实的保障防线~ 如果您对某些险种有疑问，或者想了解更多细节，随时都可以问我！\n\n祝您和家人身体健康，生活愉快！🌸\n\n*📅 报告生成时间：{datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}*",
                f"## 💝 写在最后\n\n亲爱的{name}，希望这份保险配置方案能让您更安心！保险是对家人爱的承诺，希望这份方案能帮助您守护最珍贵的人~ 有任何问题随时联系我哦！\n\n*📅 报告生成时间：{datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}*"
            ],
            'empathetic': [
                f"## 💝 写在最后\n\n{name}，以上方案是**以最有利于投保人的原则**为您量身定制的。我知道选择保险是一个重要的决定，如果您有任何疑问或担忧，都可以告诉我，我会耐心为您解答。\n\n希望这份方案能为您和家人带来安心与保障。\n\n*📅 报告生成时间：{datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}*",
                f"## 💝 写在最后\n\n感谢您的信任，{name}。这份方案考虑了您的实际情况和需求，如果您对某些部分有疑虑，欢迎随时和我沟通。选择合适的保险是对家庭的责任，希望这份方案能帮助您做出最适合的选择。\n\n*📅 报告生成时间：{datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}*"
            ],
            'professional': [
                f"## 💝 写在最后\n\n以上方案是**以最有利于投保人的原则**为您量身定制的。如果您对某些险种有疑问，或者想了解为什么没有推荐某些险种，欢迎随时咨询。\n\n保险规划是一个持续的过程，建议定期审视保障需求并适时调整。\n\n*📅 报告生成时间：{datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}*",
                f"## 💝 写在最后\n\n{name}您好，这份保险配置方案基于您的实际情况和保险规划原则制定。如有任何疑问或需要进一步调整，请随时联系。\n\n祝您和家人身体健康，生活顺利！\n\n*📅 报告生成时间：{datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}*"
            ]
        }
        
        return conclusions[tone_style][0]'''
    
    new_conclusion = '''    def _get_dynamic_conclusion(self) -> str:
        name = self.user_info.get('name', '您')
        tone_style = self._determine_tone_style()
        timestamp = datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')
        
        if tone_style == 'warm':
            return f"""## 💝 写在最后

{name}，这份方案是我根据您的家庭情况用心定制的，希望能帮助您和家人建立起坚实的保障防线~ 如果您对某些险种有疑问，或者想了解更多细节，随时都可以问我！

祝您和家人身体健康，生活愉快！🌸

*📅 报告生成时间：{timestamp}*"""
        elif tone_style == 'empathetic':
            return f"""## 💝 写在最后

{name}，以上方案是**以最有利于投保人的原则**为您量身定制的。我知道选择保险是一个重要的决定，如果您有任何疑问或担忧，都可以告诉我，我会耐心为您解答。

希望这份方案能为您和家人带来安心与保障。

*📅 报告生成时间：{timestamp}*"""
        else:
            return f"""## 💝 写在最后

以上方案是**以最有利于投保人的原则**为您量身定制的。如果您对某些险种有疑问，或者想了解为什么没有推荐某些险种，欢迎随时咨询。

保险规划是一个持续的过程，建议定期审视保障需求并适时调整。

*📅 报告生成时间：{timestamp}*"""'''
    
    content = content.replace(old_conclusion, new_conclusion)
    
    with open(advisor_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("已修复_get_dynamic_conclusion方法！")

if __name__ == '__main__':
    fix_dynamic_conclusion()
