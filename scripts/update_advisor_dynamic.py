import json
import os

def add_emotion_and_dynamic_generation():
    advisor_path = 'D:/nearpy/04 skillhub/insurance-advisor/scripts/insurance_advisor.py'
    
    with open(advisor_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. 在_analyze_risk_preference方法后添加情绪分析方法
    emotion_analyzer = '''
    def _analyze_user_emotion(self, input_text: str) -> Dict[str, Any]:
        emotion = {
            'tone': 'neutral',
            'urgency': 'low',
            'confidence': 'medium',
            'concern_level': 'low'
        }
        
        positive_words = ['好的', '谢谢', '感谢', '不错', '满意', '高兴', '开心', '顺利', '放心', '安心']
        negative_words = ['担心', '害怕', '焦虑', '紧张', '着急', '忧虑', '发愁', '麻烦', '困扰', '压力']
        urgent_words = ['尽快', '急', '快点', '立刻', '马上', '急需', '紧急']
        confident_words = ['确定', '肯定', '明白', '清楚', '了解', '知道']
        confused_words = ['不懂', '不明白', '不清楚', '困惑', '疑问', '什么意思']
        concerned_words = ['担心', '顾虑', '在意', '关注', '关心', '重视']
        
        emotion_score = 0
        
        for word in positive_words:
            if word in input_text:
                emotion_score += 1
        
        for word in negative_words:
            if word in input_text:
                emotion_score -= 1
        
        if emotion_score > 2:
            emotion['tone'] = 'positive'
        elif emotion_score < -2:
            emotion['tone'] = 'negative'
        else:
            emotion['tone'] = 'neutral'
        
        emotion['urgency'] = 'high' if any(word in input_text for word in urgent_words) else 'low'
        emotion['confidence'] = 'high' if any(word in input_text for word in confident_words) else \
                               'low' if any(word in input_text for word in confused_words) else 'medium'
        emotion['concern_level'] = 'high' if any(word in input_text for word in concerned_words) else 'low'
        
        return emotion

    def _determine_tone_style(self) -> str:
        emotion = self.user_info.get('emotion', {})
        tone = emotion.get('tone', 'neutral')
        
        if tone == 'positive':
            return 'warm'
        elif tone == 'negative':
            return 'empathetic'
        else:
            return 'professional'
    
    def _get_dynamic_title(self) -> str:
        name = self.user_info.get('name', '用户')
        family_count = len(self.user_info.get('family_members', []))
        tone_style = self._determine_tone_style()
        
        titles = {
            'warm': [
                f"🏠 {name}的温馨家庭保险配置方案",
                f"💝 为{name}家人量身定制的保险规划",
                f"🌟 {name}家庭专属保险保障方案"
            ],
            'empathetic': [
                f"🏠 {name}的家庭保险保障规划",
                f"🤝 为{name}家庭定制的保险方案",
                f"🛡️ {name}家庭的安心保障计划"
            ],
            'professional': [
                f"🏠 {name}的家庭保险配置方案",
                f"📋 {name}家庭保险规划报告",
                f"💼 {name}专属保险配置建议"
            ]
        }
        
        return titles[tone_style][0]

    def _get_dynamic_intro(self) -> str:
        name = self.user_info.get('name', '您')
        tone_style = self._determine_tone_style()
        
        intros = {
            'warm': [
                f"您好{name}！👋 非常开心能为您服务！根据您分享的家庭情况，我用心为您定制了这份保险配置方案，希望能给您和家人带来安心与保障~",
                f"亲爱的{name}，您好呀！😊 感谢您的信任，我已经根据您的家庭情况精心设计了一份保险规划，希望能帮助您守护最爱的家人！"
            ],
            'empathetic': [
                f"您好{name}！👋 感谢您选择我作为您的保险顾问。我理解您对家庭保障的关心，根据您提供的情况，我为您整理了一份详细的保险配置方案。",
                f"{name}您好！🤝 我知道选择保险是一个重要的决定，我会根据您的实际情况，为您推荐最适合的保障方案。"
            ],
            'professional': [
                f"您好{name}！👋 感谢您选择我作为您的保险顾问。根据您提供的家庭情况，**以最有利于投保人的原则**，我为您精心定制了以下保险配置方案：",
                f"{name}您好！根据您的家庭信息和需求分析，我为您制定了专业的保险配置建议，以下是详细方案："
            ]
        }
        
        return intros[tone_style][0]

    def _get_dynamic_insurance_intro(self) -> str:
        tone_style = self._determine_tone_style()
        
        intros = {
            'warm': """## 📚 人身险分类说明

在为您推荐具体方案之前，先和您简单聊聊人身险的基本分类吧~ 其实不管市场上的保险产品名字多花哨，主要就是这五种：

| 险种类型 | 核心作用 | 常见产品形式 |
|----------|----------|--------------|
| 🔷 **寿险** | 身故保障，为家人留下现金 | 定期寿险、终身寿险 |
| 🩺 **重疾险** | 确诊重大疾病一次性给付保险金 | 定期重疾险、终身重疾险 |
| 🏥 **医疗险** | 医疗费用实报实销 | 百万医疗险、中端医疗险 |
| ⚡ **意外险** | 意外身故/伤残保障 | 综合意外险、交通意外险 |
| 💰 **年金保险** | 退休后稳定现金流 | 养老年金、教育年金 |

简单来说，寿险守护家人未来，重疾险和医疗险守护健康，意外险应对意外，年金险规划未来~""",
            
            'empathetic': """## 📚 人身险分类说明

我知道保险产品种类很多，可能会让人感到困惑。让我为您简单解释一下人身险的基本分类，这样您能更好地理解推荐方案：

| 险种类型 | 核心作用 | 常见产品形式 |
|----------|----------|--------------|
| 🔷 **寿险** | 身故保障，为家人留下现金 | 定期寿险、终身寿险 |
| 🩺 **重疾险** | 确诊重大疾病一次性给付保险金 | 定期重疾险、终身重疾险 |
| 🏥 **医疗险** | 医疗费用实报实销 | 百万医疗险、中端医疗险 |
| ⚡ **意外险** | 意外身故/伤残保障 | 综合意外险、交通意外险 |
| 💰 **年金保险** | 退休后稳定现金流 | 养老年金、教育年金 |

每种险种都有其独特的作用，我们会根据您的情况选择最适合的组合。""",
            
            'professional': """## 📚 人身险分类说明

在了解具体方案之前，先为您介绍人身险的基本分类。无论市场上的保险产品名称如何变化，客观上人身险主要分为以下五种：

| 险种类型 | 核心作用 | 常见产品形式 |
|----------|----------|--------------|
| 🔷 **寿险** | 身故保障，为家人留下现金 | 定期寿险、终身寿险 |
| 🩺 **重疾险** | 确诊重大疾病一次性给付保险金 | 定期重疾险、终身重疾险 |
| 🏥 **医疗险** | 医疗费用实报实销 | 百万医疗险、中端医疗险 |
| ⚡ **意外险** | 意外身故/伤残保障 | 综合意外险、交通意外险 |
| 💰 **年金保险** | 退休后稳定现金流 | 养老年金、教育年金 |

不同险种针对不同风险场景，合理组合才能实现全面保障。"""
        }
        
        return intros[tone_style]

    def _get_dynamic_product_type_intro(self) -> str:
        tone_style = self._determine_tone_style()
        
        intros = {
            'warm': """---

## ⚖️ 保障型 vs 投资型产品区分

保险产品还可以按"投资属性"分为两大类，您可以根据自己的需求来选择：

### 🛡️ 保障型产品
- **特点**：现金价值低或无现金价值，保费主要用于风险保障
- **优势**：保费便宜，保障杠杆高，能以较少的保费获得较高的保额
- **适合人群**：预算有限、注重风险保障的人群
- **典型产品**：定期寿险、消费型重疾险、一年期意外险

### 📈 投资型产品
- **特点**：现金价值高，带有很强的投资性质
- **优势**：兼具保障和储蓄功能，到期可返还保费或获得分红
- **劣势**：保费较高，保障杠杆较低，大部分保费用于投资而非保障
- **适合人群**：经济条件优越、希望资产保值增值的人群
- **典型产品**：终身寿险、返还型重疾险、年金保险

简单说，保障型是"用小钱换大保障"，投资型是"保障+储蓄"二合一~""",
            
            'empathetic': """---

## ⚖️ 保障型 vs 投资型产品区分

选择保险时，了解产品类型很重要。主要分为两大类：

### 🛡️ 保障型产品
- **特点**：现金价值低或无现金价值，保费主要用于风险保障
- **优势**：保费便宜，保障杠杆高，能以较少的保费获得较高的保额
- **适合人群**：预算有限、注重风险保障的人群
- **典型产品**：定期寿险、消费型重疾险、一年期意外险

### 📈 投资型产品
- **特点**：现金价值高，带有很强的投资性质
- **优势**：兼具保障和储蓄功能，到期可返还保费或获得分红
- **劣势**：保费较高，保障杠杆较低，大部分保费用于投资而非保障
- **适合人群**：经济条件优越、希望资产保值增值的人群
- **典型产品**：终身寿险、返还型重疾险、年金保险

我们会根据您的经济状况和需求，为您推荐最适合的类型。""",
            
            'professional': """---

## ⚖️ 保障型 vs 投资型产品区分

除了按保障责任分类，保险产品还可以按"投资属性"分为两大类：

### 🛡️ 保障型产品
- **特点**：现金价值低或无现金价值，保费主要用于风险保障
- **优势**：保费便宜，保障杠杆高，能以较少的保费获得较高的保额
- **适合人群**：预算有限、注重风险保障的人群
- **典型产品**：定期寿险、消费型重疾险、一年期意外险

### 📈 投资型产品
- **特点**：现金价值高，带有很强的投资性质
- **优势**：兼具保障和储蓄功能，到期可返还保费或获得分红
- **劣势**：保费较高，保障杠杆较低，大部分保费用于投资而非保障
- **适合人群**：经济条件优越、希望资产保值增值的人群
- **典型产品**：终身寿险、返还型重疾险、年金保险

从保障本质出发，**优先推荐保障型产品**，投资型产品仅在经济条件允许时考虑。"""
        }
        
        return intros[tone_style]

    def _get_dynamic_core_values(self) -> str:
        tone_style = self._determine_tone_style()
        economic_level = self.user_info.get('economic_status', {}).get('economic_level', '一般')
        
        values = {
            'warm': {
                '一般': """---

## 💎 核心价值观提示

在为您规划保险方案时，我始终遵循以下原则：

1. 🛡️ **保险的核心是保障，不是理财** - 我们优先选择能真正转移风险的产品，而不是带有投资功能的保险
2. ⏰ **量力而行最重要** - 根据您的经济情况推荐合适的保额和保障期限，不会让保险成为负担
3. ❌ **不推荐储蓄型产品** - 这类产品看似能返还，但实际上保障杠杆很低，大部分钱都拿去投资了
4. 💝 **保障到70岁就够了** - 这个年龄段子女基本都独立了，家庭责任也减轻了，没必要追求终身保障

希望这些原则能帮助您更好地理解我们的推荐~""",
                
                '较好': """---

## 💎 核心价值观提示

为您规划保险方案时，我始终遵循以下核心原则：

1. 🛡️ **保险的核心是风险转移，不是投资** - 我们专注于保障型产品，让每一分钱都花在刀刃上
2. ⏰ **量力而行，理性规划** - 根据您的经济实力推荐合适的保障方案，既充分保障又不造成压力
3. ❌ **储蓄型产品性价比低** - 这类产品保费高、保障低，不符合保险的本质
4. 💝 **保至70岁是黄金选择** - 能覆盖主要家庭责任期，性价比最优

如果您有任何疑问，欢迎随时和我探讨！"""
            },
            
            'empathetic': {
                '一般': """---

## 💎 核心价值观提示

我理解您对保险的关心和谨慎，在为您规划方案时，我始终坚持以下原则：

1. 🛡️ **保险的核心是风险转移和保障，不是投资或储蓄** - 我们优先选择纯保障型产品，确保您花的每一分钱都能获得最大的保障
2. ⏰ **量力而行是关键** - 我会根据您的经济状况推荐合适的方案，不会给您带来经济压力
3. ❌ **不推荐储蓄型产品** - 这类产品"保费很高但保障内容较低"，性价比不高
4. 💝 **保至70岁即可满足需求** - 这个年龄段子女已成年独立，家庭责任基本完成

这些原则都是为了确保您获得最适合的保障。""",
                
                '较好': """---

## 💎 核心价值观提示

感谢您的信任，在为您规划保险方案时，我始终遵循以下核心原则：

1. 🛡️ **保险的核心是风险转移和保障** - 我们专注于保障型产品，让保障更纯粹
2. ⏰ **量力而行，合理规划** - 根据您的经济能力推荐合适的保额和期限
3. ❌ **储蓄型产品不是最佳选择** - 风险保额较低，大部分保费用于投资而非保障
4. 💝 **保至70岁是最优选择** - 能充分覆盖家庭责任期，平衡保障与成本

如果您对这些原则有任何疑问，我很乐意为您解释。"""
            },
            
            'professional': {
                '一般': """---

## 💎 核心价值观提示

本方案严格遵循保险规划的核心原则：

1. 🛡️ **保险的核心是风险转移和保障，不是投资或储蓄**
2. ⏰ **保险期间越长，保险成本越高，保费肯定就越高，应优先选择保20年或保至70岁**
3. ❌ **储蓄型保险产品"保费很高但保障内容较低"，风险保额比较低，大部分保费用于投资而非保障**
4. 💝 **保至70岁即可满足家庭责任需求，终身产品仅在经济条件极其优越时考虑**

以上原则确保推荐方案符合保险本质，为您提供最优的风险保障。""",
                
                '较好': """---

## 💎 核心价值观提示

本方案严格遵循以下核心价值观：

1. 🛡️ **保险是风险转移工具，不是投资理财工具**
2. ⏰ **量力而行选择保障期限，优先保至70岁**
3. ❌ **储蓄型保险性价比低，违背保险保障本质**
4. 💝 **纯保障型产品优于投资型产品**

所有推荐均基于保障本质优先原则，确保您获得最优质的保险配置。"""
            }
        }
        
        level_key = '较好' if economic_level in ['较好', '充裕', '非常优越'] else '一般'
        return values[tone_style][level_key]

    def _get_dynamic_conclusion(self) -> str:
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
        
        return conclusions[tone_style][0]
'''
    
    # 在_analyze_risk_preference方法后插入情绪分析方法
    content = content.replace('return preferences\n\n    def _parse_city_value', emotion_analyzer + '\n    def _parse_city_value')
    
    # 更新_format_report方法
    old_format_report = '''    def _format_report(self, recommendations: List[Dict[str, Any]]) -> str:
        name = self.user_info.get('name', '用户')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'推荐报告_{name}_{timestamp}.md'

        report = f"# 🏠 {name}的家庭保险配置方案\\n\\n"
        report += f"您好{name}！👋 感谢您选择我作为您的保险顾问。根据您提供的家庭情况，**以最有利于投保人的原则**，我为您精心定制了以下保险配置方案：\\n\\n"
        report += "---\\n\\n"
        
        report += self._get_insurance_category_intro()
        
        report += "## 📊 您的家庭概览\\n\\n"'''
    
    new_format_report = '''    def _format_report(self, recommendations: List[Dict[str, Any]]) -> str:
        name = self.user_info.get('name', '用户')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'推荐报告_{name}_{timestamp}.md'

        report = f"# {self._get_dynamic_title()}\\n\\n"
        report += f"{self._get_dynamic_intro()}\\n\\n"
        report += "---\\n\\n"
        
        report += self._get_dynamic_insurance_intro()
        report += "\\n"
        report += self._get_dynamic_product_type_intro()
        report += "\\n"
        
        report += "## 📊 您的家庭概览\\n\\n"'''
    
    content = content.replace(old_format_report, new_format_report)
    
    # 更新核心价值观和总结部分
    old_core_values = '''        report += "\\n---\\n\\n"
        report += "## 💎 核心价值观提示\\n\\n"
        report += "1. 🛡️ **保险的核心是风险转移和保障，不是投资或储蓄**\\n"
        report += "2. ⏰ **保险期间越长，保险成本越高，保费肯定就越高，应优先选择保20年或保至70岁**\\n"
        report += "3. ❌ **储蓄型保险产品\\"保费很高但保障内容较低\\"，风险保额比较低，大部分保费用于投资而非保障**\\n"
        report += "4. 📉 **储蓄型保险\\"1000元保费只能买回1200元保额\\"，违背保险的保障本质**\\n"
        report += "5. 💸 **终身保障\\'囊中羞涩\\'时应选择保至70岁，只有经济实力允许时才考虑终身产品**\\n\\n"
        report += "## 💝 写在最后\\n\\n"
        report += "以上方案是**以最有利于投保人的原则**为您量身定制的。如果您对某些险种有疑问，或者想了解为什么没有推荐某些险种，欢迎随时问我！\\n\\n"
        report += f"*📅 报告生成时间：{datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}\\n"'''
    
    new_core_values = '''        report += self._get_dynamic_core_values()
        report += "\\n"
        report += self._get_dynamic_conclusion()'''
    
    content = content.replace(old_core_values, new_core_values)
    
    # 更新_get_insurance_category_intro方法，使其兼容动态生成
    content = content.replace('def _get_insurance_category_intro(self) -> str:', 'def _get_insurance_category_intro_deprecated(self) -> str:')
    
    with open(advisor_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("保险顾问动态内容生成功能已更新完成！")

if __name__ == '__main__':
    add_emotion_and_dynamic_generation()
