import json
import os
import re
from datetime import datetime
from typing import Dict, List, Any, Optional


class InsuranceAdvisor:
    def __init__(self):
        self.insurance_rules = self._load_insurance_rules()
        self.user_info = {
            'name': '',
            'family_members': [],
            'economic_status': {},
            'risk_preference': {}
        }
        self.conversation_history = []
        self.output_dir = os.path.join(os.path.dirname(__file__), '..', 'output')
        os.makedirs(self.output_dir, exist_ok=True)
        self.info_status = {
            'name_collected': False,
            'family_collected': False,
            'economic_collected': False,
            'risk_collected': False
        }

    def _load_insurance_rules(self) -> List[Dict[str, Any]]:
        rules_path = os.path.join(os.path.dirname(__file__), '..', 'references', 'insurance_guide.json')
        if not os.path.exists(rules_path):
            raise FileNotFoundError(f"保险规则文件未找到: {rules_path}")
        with open(rules_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get('insurance_list', [])

    def _get_age_group(self, age: int) -> str:
        if age <= 12:
            return "儿童"
        elif age <= 18:
            return "青少"
        elif age <= 50:
            return "中年"
        else:
            return "老年"

    def _analyze_risk_preference(self, input_text: str) -> Dict[str, Any]:
        preferences = {
            'high_end_treatment': 0,
            'income_protection': 0,
            'family_protection': 0,
            'budget_level': 'medium',
            'return_premium_preference': False,
            'inflation_concern': False
        }

        keywords_high_end = ['高端', '优质', '最好', '顶级', '专家', 'VIP', '特需', '好的医院', '好的医生']
        keywords_income = ['收入', '工资', '工作', '稳定', '持续', '维持', '保障生活']
        keywords_family = ['家人', '孩子', '配偶', '父母', '家庭', '保障', '留下', '照顾', '责任']
        keywords_budget_high = ['充裕', '充足', '足够', '愿意投入', '不介意价格', '预算充足', '非常优越']
        keywords_budget_low = ['有限', '紧张', '节约', '性价比', '便宜', '预算有限', '一般']
        keywords_return = ['返还', '不出险要还我', '存钱', '储蓄', '返还型', '分红', '储蓄型']
        keywords_inflation = ['通货膨胀', '贬值', '购买力', '几十年后']

        for kw in keywords_high_end:
            if kw in input_text:
                preferences['high_end_treatment'] += 1

        for kw in keywords_income:
            if kw in input_text:
                preferences['income_protection'] += 1

        for kw in keywords_family:
            if kw in input_text:
                preferences['family_protection'] += 1

        if any(kw in input_text for kw in keywords_budget_high):
            preferences['budget_level'] = 'high'
        elif any(kw in input_text for kw in keywords_budget_low):
            preferences['budget_level'] = 'low'

        preferences['return_premium_preference'] = any(kw in input_text for kw in keywords_return)
        preferences['inflation_concern'] = any(kw in input_text for kw in keywords_inflation)

        
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
        emotion['confidence'] = 'high' if any(word in input_text for word in confident_words) else                                'low' if any(word in input_text for word in confused_words) else 'medium'
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

*📅 报告生成时间：{timestamp}*"""

    def _parse_city_value(self, city: str) -> float:
        tier1_cities = ['北京', '上海', '广州', '深圳']
        tier2_cities = ['杭州', '南京', '成都', '武汉', '重庆', '西安', '天津', '苏州', '郑州', '长沙']

        if any(c in city for c in tier1_cities):
            return 1.3
        elif any(c in city for c in tier2_cities):
            return 1.1
        return 1.0

    def _parse_occupation_stability(self, occupation: str) -> str:
        stable_jobs = ['公务员', '教师', '医生', '国企', '事业单位', '体制内', '银行', '金融']
        unstable_jobs = ['IT', '互联网', '创业', '自由职业', '销售', '市场']

        if any(job in occupation for job in stable_jobs):
            return 'stable'
        elif any(job in occupation for job in unstable_jobs):
            return 'unstable'
        return 'medium'

    def _extract_name(self, text: str) -> Optional[str]:
        name_patterns = [
            r'我叫(.*?)[,，。、\s]',
            r'我是(.*?)[,，。、\s]',
            r'本人(.*?)[,，。、\s]',
            r'(.*?)，您好',
            r'(.*?)你好'
        ]
        for pattern in name_patterns:
            match = re.search(pattern, text)
            if match:
                name = match.group(1).strip()
                if name and len(name) <= 4:
                    return name
        return None

    def _extract_family_members(self, text: str) -> List[Dict[str, Any]]:
        members = []

        health_status = '健康' if any(h in text for h in ['健康', '身体好', '没毛病', '良好']) else '一般'
        if any(ill in text for ill in ['高血压', '糖尿病', '心脏病', '癌症', '病史', '患病', '遗传']) :
            health_status = '需要关注'

        # 先找到所有的年龄数字
        age_pattern = r'(\d+)岁'
        all_ages = [int(m.group(1)) for m in re.finditer(age_pattern, text)]
        age_index = 0

        # 先找本人
        if '我' in text or '本人' in text or '自己' in text:
            if age_index < len(all_ages):
                members.append({
                    'role': '本人',
                    'age': all_ages[age_index],
                    'health': health_status,
                    'age_group': self._get_age_group(all_ages[age_index])
                })
                age_index += 1

        # 再找配偶
        spouse_terms = ['妻子', '丈夫', '配偶', '爱人', '太太', '先生']
        if any(term in text for term in spouse_terms):
            if age_index < len(all_ages):
                members.append({
                    'role': '配偶',
                    'age': all_ages[age_index],
                    'health': health_status,
                    'age_group': self._get_age_group(all_ages[age_index])
                })
                age_index += 1

        # 再找孩子
        child_terms = ['孩子', '儿子', '女儿', '宝宝', '小孩']
        child_count = sum(text.count(term) for term in child_terms)
        for i in range(child_count):
            if age_index < len(all_ages):
                members.append({
                    'role': f'孩子{i+1}' if i > 0 else '孩子',
                    'age': all_ages[age_index],
                    'health': health_status,
                    'age_group': self._get_age_group(all_ages[age_index])
                })
                age_index += 1

        # 再找父母
        parent_terms = ['父母', '父亲', '母亲', '爸妈', '爸', '妈']
        if any(term in text for term in parent_terms):
            parent_count = text.count('父母') + text.count('爸') + text.count('妈')
            for i in range(min(parent_count, 2)):
                if age_index < len(all_ages):
                    parent_age = all_ages[age_index]
                    age_index += 1
                else:
                    parent_age = 60 if i == 0 else 58
                members.append({
                    'role': '父亲' if i == 0 else '母亲',
                    'age': parent_age,
                    'health': health_status,
                    'age_group': self._get_age_group(parent_age)
                })

        return members

    def _extract_economic_status(self, text: str) -> Dict[str, Any]:
        status = {
            'income': 0,
            'assets': 0,
            'city': '',
            'occupation': '',
            'debt': 0,
            'economic_level': '一般'
        }

        income_patterns = [
            r'年收入(\d+)(万)?',
            r'年薪(\d+)(万)?',
            r'月收入(\d+)(万)?',
            r'月薪(\d+)(万)?'
        ]
        for pattern in income_patterns:
            match = re.search(pattern, text)
            if match:
                amount = int(match.group(1))
                unit = match.group(2)
                if '月' in pattern:
                    # 注意：我们不重复乘以10000，因为已经是万元单位了
                    if unit:
                        status['income'] = amount * 12
                    else:
                        status['income'] = amount / 10000 * 12
                else:
                    if unit:
                        status['income'] = amount
                    else:
                        status['income'] = amount / 10000
                break

        asset_patterns = [
            r'(房产|资产|价值|房子|存款)(\d+)(万)?',
            r'(\d+)(万)?(房产|资产|价值|房子)'
        ]
        for pattern in asset_patterns:
            match = re.search(pattern, text)
            if match:
                amount_str = match.group(2)
                unit = match.group(3) if len(match.groups()) >= 3 else match.group(1)
                if '万' in str(match.group(0)):
                    status['assets'] = int(amount_str)
                else:
                    status['assets'] = int(amount_str) / 10000
                break

        cities = ['北京', '上海', '广州', '深圳', '杭州', '南京', '成都', '武汉', '重庆', '西安', '天津', '苏州', '郑州', '长沙']
        for city in cities:
            if city in text:
                status['city'] = city
                break

        occupations = ['IT', '互联网', '公务员', '教师', '医生', '国企', '创业', '销售', '体制内', '金融', '银行', '工程师']
        for occupation in occupations:
            if occupation in text:
                status['occupation'] = occupation
                break

        debt_pattern = r'(房贷|贷款|负债)(\d+)(万)?'
        match = re.search(debt_pattern, text)
        if match:
            amount_str = match.group(2)
            unit = match.group(3) if len(match.groups()) >= 3 else None
            if unit:
                status['debt'] = int(amount_str)
            else:
                status['debt'] = int(amount_str) / 10000

        # 简化经济水平判断（使用万元单位
        if status['income'] > 100 or status['assets'] > 1000:
            status['economic_level'] = '非常优越'
        elif status['income'] > 30 or status['assets'] > 300:
            status['economic_level'] = '较好'
        elif status['income'] == 0 and status['assets'] == 0:
            status['economic_level'] = '不确定'

        return status

    def _analyze_sentiment_and_hidden_needs(self, text: str) -> Dict[str, Any]:
        sentiment = {
            'concern_level': 0,
            'family_orientation': 0,
            'security_seeking': 0,
            'quality_conscious': 0,
            'hereditary_concern': False,
            'job_mobility_concern': False,
            'only_parent_concern': False
        }

        concern_keywords = ['担心', '害怕', '忧虑', '不安', '焦虑', '压力', '责任', '怕', '担心自己']
        family_keywords = ['家人', '孩子', '配偶', '父母', '家庭', '照顾', '陪伴', '为了']
        security_keywords = ['保障', '安全', '稳定', '安心', '放心', '可靠', '万一', '意外']
        quality_keywords = ['好', '优质', '高端', '专业', '最好', '顶级', '品质', '质量']
        hereditary_keywords = ['遗传', '病史', '家族', '遗传病史']
        mobility_keywords = ['工作变动', '流动性大', '换工作', '不稳定', '工作调动']
        only_parent_keywords = ['独生子女', '只有我', '一个人', '没人照顾']

        for kw in concern_keywords:
            if kw in text:
                sentiment['concern_level'] += 1

        for kw in family_keywords:
            if kw in text:
                sentiment['family_orientation'] += 1

        for kw in security_keywords:
            if kw in text:
                sentiment['security_seeking'] += 1

        for kw in quality_keywords:
            if kw in text:
                sentiment['quality_conscious'] += 1

        sentiment['hereditary_concern'] = any(kw in text for kw in hereditary_keywords)
        sentiment['job_mobility_concern'] = any(kw in text for kw in mobility_keywords)
        sentiment['only_parent_concern'] = any(kw in text for kw in only_parent_keywords)

        return sentiment

    def _determine_user_scenarios(self, user_info: Dict[str, Any]) -> List[str]:
        scenarios = []
        economic_level = user_info.get('economic_status', {}).get('economic_level', '一般')
        risk_pref = user_info.get('risk_preference', {})
        hidden_needs = user_info.get('hidden_needs', {})

        if economic_level == '一般':
            scenarios.append('家庭经济条件一般')
        elif economic_level == '较好':
            scenarios.append('家庭经济条件较好')
        elif economic_level == '非常优越':
            scenarios.append('经济条件非常优越')

        if hidden_needs.get('family_orientation', 0) > 0:
            scenarios.append('希望为家人提供保障')

        if hidden_needs.get('hereditary_concern', False):
            scenarios.append('家庭中有遗传性疾病史')

        if hidden_needs.get('job_mobility_concern', False):
            scenarios.append('父母工作流动性大')

        if hidden_needs.get('only_parent_concern', False):
            scenarios.append('是独生子女')

        if risk_pref.get('return_premium_preference', False):
            scenarios.append('持有强烈保费返还心理')

        if risk_pref.get('inflation_concern', False):
            scenarios.append('担心通货膨胀影响保额实际购买力')

        return scenarios

    def _match_worth_buying_rules(self, member: Dict[str, Any], scenarios: List[str], risk_preference: Dict[str, Any]) -> List[Dict[str, Any]]:
        age_group = member.get('age_group', '')
        economic_level = risk_preference.get('budget_level', 'medium')

        matched_rules = []

        for rule in self.insurance_rules:
            if rule['age_group'] != age_group:
                continue

            if rule['investment_attribute'] == '投资':
                continue

            # 简化匹配逻辑：只要有worth_buying的规则都考虑
            if rule.get('worth_buying'):
                # 检查这个规则是否至少有一个适用场景
                applicable = False
                matched_scenarios = []
                for worth_scenario in rule.get('worth_buying', []):
                    scenario_text = worth_scenario.get('scenario', '')

                    # 检查是否有匹配的场景
                    if scenarios:
                        for user_scenario in scenarios:
                            if user_scenario in scenario_text:
                                applicable = True
                                matched_scenarios.append(user_scenario)
                                break

                    # 如果没有明确匹配的场景，至少保留一些基础规则
                    if not applicable and ('经济条件一般' in scenario_text or '经济条件较好' in scenario_text):
                        applicable = True
                        matched_scenarios.append('基础保障')

                if applicable:
                    matched_rules.append({
                        'rule': rule,
                        'matched_scenarios': matched_scenarios,
                        'worth_buying': True
                    })

        matched_rules.sort(key=lambda x: self._calculate_rule_score(x['rule'], economic_level), reverse=True)
        return matched_rules[:3]

    def _calculate_rule_score(self, rule: Dict[str, Any], budget_level: str) -> int:
        score = 0

        if rule['investment_attribute'] == '保障':
            score += 10

        if rule['coverage_period'] == '70岁':
            score += 8
        elif rule['coverage_period'] == '60岁':
            score += 5
        elif rule['coverage_period'] == '30岁':
            score += 3

        if budget_level == 'high' and rule['coverage_period'] in ['70岁', '终身']:
            score += 3

        return score

    def _extract_recommended_amount(self, worth_buying_list: List[Dict[str, Any]]) -> Optional[str]:
        for wb in worth_buying_list:
            reason = wb.get('reason', '')
            match = re.search(r'建议保额(\d+)-(\d+)万元', reason)
            if match:
                return f"{match.group(1)}-{match.group(2)}万元"
        return "根据实际情况确定"

    def _adjust_recommended_amount(self, base_amount: str, economic_status: Dict[str, Any]) -> str:
        amount_match = re.search(r'(\d+)-(\d+)万元', base_amount)
        if not amount_match:
            return base_amount

        min_val = int(amount_match.group(1))
        max_val = int(amount_match.group(2))

        city_multiplier = self._parse_city_value(economic_status.get('city', ''))
        occupation = economic_status.get('occupation', '')
        occupation_stability = self._parse_occupation_stability(occupation)

        if occupation_stability == 'unstable':
            city_multiplier *= 1.2

        adjusted_min = int(min_val * city_multiplier)
        adjusted_max = int(max_val * city_multiplier)

        return f"{adjusted_min}-{adjusted_max}万元"

    def process_user_input(self, user_input: str) -> Dict[str, Any]:
        self.conversation_history.append({
            'role': 'user',
            'content': user_input,
            'timestamp': datetime.now().isoformat()
        })

        name = self._extract_name(user_input)
        if name:
            self.user_info['name'] = name
            self.info_status['name_collected'] = True

        members = self._extract_family_members(user_input)
        if members:
            existing_roles = set(m['role'] for m in self.user_info.get('family_members', []))
            for member in members:
                if member['role'] not in existing_roles:
                    self.user_info.setdefault('family_members', []).append(member)
            self.info_status['family_collected'] = len(self.user_info.get('family_members', [])) > 0

        economic = self._extract_economic_status(user_input)
        if economic.get('income') > 0 or economic.get('city') or economic.get('occupation'):
            self.user_info['economic_status'] = {**self.user_info.get('economic_status', {}), **economic}
            self.info_status['economic_collected'] = True

        risk = self._analyze_risk_preference(user_input)
        if any(v > 0 for k, v in risk.items() if k not in ['budget_level', 'return_premium_preference', 'inflation_concern']) or \
           risk['budget_level'] != 'medium' or \
           risk['return_premium_preference'] or \
           risk['inflation_concern']:
            self.user_info['risk_preference'] = {**self.user_info.get('risk_preference', {}), **risk}
            self.info_status['risk_collected'] = True

        hidden_needs = self._analyze_sentiment_and_hidden_needs(user_input)
        self.user_info['hidden_needs'] = hidden_needs

        self.user_info['scenarios'] = self._determine_user_scenarios(self.user_info)

        return self.user_info

    def _generate_question(self, missing_info: str, context: str = "") -> str:
        questions = {
            'name': [
                "还没请教您贵姓呢？方便告诉我您的称呼吗？",
                "对了，我还不知道怎么称呼您呢？",
                "请问怎么称呼您比较合适？"
            ],
            'family': [
                "您可以和我说说您的家庭成员吗？比如有没有孩子、配偶或者需要照顾的父母？",
                "关于您的家人，您方便分享一下吗？比如配偶、孩子的年龄和健康状况？",
                "除了您自己，家里还有哪些成员需要考虑保障呢？"
            ],
            'economic': [
                "为了更好地了解您的情况，您方便说说您的年收入大概在什么范围吗？您在哪个城市生活呢？",
                "您目前从事什么职业呀？收入情况大概是怎样的？这对我了解您的情况很有帮助哦~",
                "您有固定资产吗？比如房产之类的？大概价值多少呢？"
            ],
            'risk': [
                "如果发生健康问题，您更倾向于接受什么样的治疗呢？是希望能享受更好的医疗服务，还是更注重性价比？",
                "您最关心的是家人的哪些方面呢？比如孩子的成长、家人的健康，还是未来的生活保障？",
                "您对未来的生活有什么规划吗？比如希望达到什么样的生活水平？"
            ]
        }

        import random
        return random.choice(questions.get(missing_info, questions['family']))

    def _determine_missing_info(self) -> Optional[str]:
        if not self.user_info.get('name'):
            return 'name'
        if not self.user_info.get('family_members') or len(self.user_info['family_members']) == 0:
            return 'family'
        if not self.user_info.get('economic_status') or not self.user_info['economic_status'].get('income'):
            return 'economic'
        if not self.user_info.get('risk_preference'):
            return 'risk'
        return None

    def get_response(self, user_input: str = "") -> str:
        if not user_input:
            return "您好！我是您的专属顾问。很高兴为您服务！您可以和我聊聊您的家庭情况，比如家人的年龄、工作、收入等，我会为您提供专业的建议~"

        self.process_user_input(user_input)

        missing_info = self._determine_missing_info()

        if missing_info:
            return self._generate_question(missing_info, user_input)

        return self.generate_recommendation()

    def is_info_complete(self) -> bool:
        return all(self.info_status.values())

    def _validate_against_core_values(self, recommendations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        validated = []
        
        for rec in recommendations:
            rule = rec['rule']
            is_valid = True
            
            if rule['investment_attribute'] == '投资':
                if self.user_info.get('economic_status', {}).get('economic_level') != '非常优越':
                    continue
            
            if rule['coverage_period'] == '终身':
                if self.user_info.get('economic_status', {}).get('economic_level') != '非常优越':
                    continue
            
            if rule['insurance_type'] == '年金':
                has_basic_coverage = any(r['insurance_type'] in ['寿险', '重疾险', '医疗险', '意外'] for r in recommendations)
                if not has_basic_coverage:
                    continue
            
            validated.append(rec)
        
        return validated

    def _optimize_recommendations(self, recommendations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        member_recs = {}
        for rec in recommendations:
            role = rec['member']['role']
            if role not in member_recs:
                member_recs[role] = []
            member_recs[role].append(rec)
        
        for role, recs in member_recs.items():
            recs.sort(key=lambda x: self._calculate_rule_score(x['rule'], self.user_info.get('risk_preference', {}).get('budget_level', 'medium')), reverse=True)
            member_recs[role] = recs
        
        return [rec for role in member_recs for rec in member_recs[role]]

    def generate_recommendation(self) -> str:
        recommendations = []

        for member in self.user_info.get('family_members', []):
            matched_rules = self._match_worth_buying_rules(
                member,
                self.user_info.get('scenarios', []),
                self.user_info.get('risk_preference', {})
            )

            for match in matched_rules:
                rule = match['rule']
                base_amount = self._extract_recommended_amount(rule.get('worth_buying', []))
                adjusted_amount = self._adjust_recommended_amount(
                    base_amount,
                    self.user_info.get('economic_status', {})
                )

                recommendations.append({
                    'member': member,
                    'rule': rule,
                    'insurance_type': rule['insurance_type'],
                    'coverage_period': rule['coverage_period'],
                    'investment_attribute': rule['investment_attribute'],
                    'coverage': adjusted_amount,
                    'advantages': rule['advantages'],
                    'product_names': rule.get('product_names', []),
                    'matched_scenarios': match.get('matched_scenarios', [])
                })

        recommendations = self._validate_against_core_values(recommendations)
        recommendations = self._optimize_recommendations(recommendations)

        report_content = self._format_report(recommendations)
        self._save_report_to_file(report_content)
        
        name = self.user_info.get('name', '用户')
        return f"您好{name}！我已经为您完成了家庭情况分析，并生成了专属的保险配置方案报告。报告已保存至 output 文件夹，您可以查看详细内容。"

    def _save_report_to_file(self, report_content: str) -> None:
        name = self.user_info.get('name', '用户')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'推荐报告_{name}_{timestamp}.md'
        
        output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output')
        os.makedirs(output_dir, exist_ok=True)
        
        file_path = os.path.join(output_dir, filename)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"报告已生成: {file_path}")

    def _determine_policy_type(self, coverage_period: str) -> str:
        if coverage_period in ['终身']:
            return '长期型'
        elif coverage_period in ['60岁', '70岁', '30年', '20年']:
            return '长期型'
        elif coverage_period == '一年期':
            return '一年期'
        return '长期型'

    def _determine_payment_period(self, age: int, coverage_period: str) -> str:
        if age <= 30:
            return '30年缴'
        elif age <= 40:
            return '20年缴'
        elif age <= 50:
            return '15年缴'
        else:
            return '10年缴'

    def _calculate_premium(self, insurance_type: str, coverage: str, age: int, payment_period: str) -> str:
        amount_match = re.search(r'(\d+)-(\d+)万元', coverage)
        if not amount_match:
            return '需根据具体产品测算'

        avg_amount = (int(amount_match.group(1)) + int(amount_match.group(2))) / 2
        
        base_rates = {
            '寿险': 0.012,
            '健康': 0.025,
            '意外': 0.002
        }
        
        rate = base_rates.get(insurance_type, 0.01)
        base_premium = avg_amount * 10000 * rate
        
        age_factor = 1.0
        if age > 50:
            age_factor = 2.5
        elif age > 45:
            age_factor = 2.0
        elif age > 40:
            age_factor = 1.6
        elif age > 35:
            age_factor = 1.3
        elif age > 30:
            age_factor = 1.1
        
        premium = base_premium * age_factor
        
        payment_years = int(payment_period.replace('年缴', ''))
        annual_premium = premium / payment_years
        
        min_premium = int(annual_premium * 0.9)
        max_premium = int(annual_premium * 1.2)
        
        if min_premium < 100:
            return f"{min_premium}-{max_premium}元"
        return f"{int(min_premium / 100) * 100}-{int(max_premium / 100) * 100}元"

    def _get_insurance_category_intro_deprecated(self) -> str:
        intro = "## 📚 人身险分类说明\n\n"
        intro += "在了解具体方案之前，先为您简单介绍一下人身险的基本分类。无论市场上的保险产品名称如何变化，客观上人身险主要分为以下四种：\n\n"
        intro += "| 险种类型 | 核心作用 | 常见产品形式 |\n"
        intro += "|----------|----------|--------------|\n"
        intro += "| 🔷 **寿险** | 身故保障，为家人留下现金 | 定期寿险、终身寿险 |\n"
        intro += "| 🩺 **重疾险** | 确诊重大疾病一次性给付保险金 | 定期重疾险、终身重疾险 |\n"
        intro += "| 🏥 **医疗险** | 医疗费用实报实销 | 百万医疗险、中端医疗险 |\n"
        intro += "| ⚡ **意外险** | 意外身故/伤残保障 | 综合意外险、交通意外险 |\n"
        intro += "| 💰 **年金保险** | 退休后稳定现金流 | 养老年金、教育年金 |\n\n"
        intro += "---\n\n"
        intro += "## ⚖️ 保障型 vs 投资型产品区分\n\n"
        intro += "除了按保障责任分类，保险产品还可以按\"投资属性\"分为两大类：\n\n"
        intro += "### 🛡️ 保障型产品\n"
        intro += "- **特点**：现金价值低或无现金价值，保费主要用于风险保障\n"
        intro += "- **优势**：保费便宜，保障杠杆高，能以较少的保费获得较高的保额\n"
        intro += "- **适合人群**：预算有限、注重风险保障的人群\n"
        intro += "- **典型产品**：定期寿险、消费型重疾险、一年期意外险\n\n"
        intro += "### 📈 投资型产品\n"
        intro += "- **特点**：现金价值高，带有很强的投资性质\n"
        intro += "- **优势**：兼具保障和储蓄功能，到期可返还保费或获得分红\n"
        intro += "- **劣势**：保费较高，保障杠杆较低，大部分保费用于投资而非保障\n"
        intro += "- **适合人群**：经济条件优越、希望资产保值增值的人群\n"
        intro += "- **典型产品**：终身寿险、返还型重疾险、年金保险\n\n"
        intro += "---\n\n"
        return intro

    def _get_not_recommended_reasons(self, recommendations: List[Dict[str, Any]]) -> str:
        all_types = ['寿险', '重疾险', '医疗险', '意外', '年金']
        recommended_types = set()
        
        for rec in recommendations:
            recommended_types.add(rec['insurance_type'])
        
        not_recommended = [t for t in all_types if t not in recommended_types]
        
        if not not_recommended:
            return ""
        
        reasons = "\n---\n\n"
        reasons += "## ❌ 不推荐的险种说明\n\n"
        reasons += "基于您的家庭情况和保险规划原则，以下险种本次暂不推荐：\n\n"
        
        for insurance_type in not_recommended:
            reasons += f"### {self._get_type_emoji(insurance_type)} **【{self._get_type_full_name(insurance_type)}】**\n\n"
            reasons += self._generate_single_not_reason(insurance_type)
            reasons += "\n"
        
        return reasons

    def _get_type_emoji(self, insurance_type: str) -> str:
        emoji_map = {
            '寿险': '🔷',
            '重疾险': '🩺',
            '医疗险': '🏥',
            '意外': '⚡',
            '年金': '💰'
        }
        return emoji_map.get(insurance_type, '📋')

    def _get_type_full_name(self, insurance_type: str) -> str:
        name_map = {
            '寿险': '寿险',
            '重疾险': '重疾险',
            '医疗险': '医疗险',
            '意外': '意外险',
            '年金': '年金保险'
        }
        return name_map.get(insurance_type, insurance_type)

    def _generate_single_not_reason(self, insurance_type: str) -> str:
        reasons = {
            '寿险': """**暂不推荐理由：**
1. **家庭责任评估**：经过综合评估，您目前的家庭责任风险较低，现有保障已足够覆盖潜在风险
2. **经济成本考量**：寿险保费与年龄密切相关，当前阶段购买的机会成本较高
3. **替代方案**：建议优先完善健康保障，待家庭责任增加时再考虑配置寿险

**建议关注时机**：当家庭成员结构变化（如新增子女）或收入显著提升时，可重新评估寿险需求。""",
            
            '重疾险': """**暂不推荐理由：**
1. **已有保障评估**：您已拥有较为完善的重疾保障或其他健康保障，重复配置的边际效益较低
2. **健康状况限制**：根据您的健康告知，部分重疾险产品可能无法承保或需加费
3. **预算优先级**：建议优先配置其他更急需的保障类型

**建议**：定期审视健康状况和保障缺口，适时补充重疾险保障。建议重疾保额50万元以上【核心价值观提示】。""",
            
            '医疗险': """**暂不推荐理由：**
1. **已有保障评估**：您已拥有较为完善的医保或其他医疗费用报销保障，重复配置的边际效益较低
2. **健康状况限制**：根据您的健康告知，部分医疗险产品可能无法承保或需加费
3. **预算优先级**：建议优先配置重疾险等给付型保障，再考虑医疗险报销型保障

**建议**：定期审视健康状况和保障缺口，适时补充医疗险保障。建议选择保证续保的长期医疗险【核心价值观提示】。""",
            
            '意外': """**暂不推荐理由：**
1. **已有保障评估**：您可能已通过单位团体险或其他渠道获得了足够的意外保障
2. **风险暴露程度**：您的职业和生活方式意外风险相对较低
3. **性价比考量**：当前阶段配置意外险的性价比不高

**建议**：可考虑配置一份基础的一年期意外险作为补充，保费通常在百元左右。""",
            
            '年金': """**暂不推荐理由：**
1. **经济阶段评估**：您目前处于家庭责任较重的阶段，优先保障型产品更为重要
2. **投资效率考量**：年金保险的投资回报率相对较低，资金流动性较差
3. **机会成本**：相同预算下，配置保障型产品能获得更高的风险保障杠杆

**建议**：年金保险适合作为养老规划的补充工具，建议在完成基础保障后再考虑。"""
        }
        return reasons.get(insurance_type, f"暂不推荐{insurance_type}险，具体原因可根据您的实际情况进一步分析。")

    def _format_report(self, recommendations: List[Dict[str, Any]]) -> str:
        name = self.user_info.get('name', '用户')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'推荐报告_{name}_{timestamp}.md'

        report = f"# {self._get_dynamic_title()}\n\n"
        report += f"{self._get_dynamic_intro()}\n\n"
        report += "---\n\n"
        
        report += self._get_dynamic_insurance_intro()
        report += "\n"
        report += self._get_dynamic_product_type_intro()
        report += "\n"
        
        report += "## 📊 您的家庭概览\n\n"
        report += "| 成员 | 年龄 | 健康状况 | 年龄分组 |\n"
        report += "|------|------|----------|----------|\n"

        for member in self.user_info.get('family_members', []):
            report += f"| {member['role']} | {member['age']}岁 | {member['health']} | {member['age_group']} |\n"

        report += "\n---\n\n"
        report += "## 💼 推荐方案\n\n"

        total_premium_min = 0
        total_premium_max = 0

        if not recommendations:
            report += "**❌ 不推荐购买任何保险**\n\n"
            report += "根据专业的保险规划原则，您的情况目前不适合购买保险。以下是详细分析：\n\n"
            report += self._generate_not_recommended_reasons()
            report += "\n\n---\n\n"
            report += "## 📖 典型案例\n\n"
            report += self._generate_case_studies()
        else:
            member_recommendations = {}
            for rec in recommendations:
                role = rec['member']['role']
                if role not in member_recommendations:
                    member_recommendations[role] = []
                member_recommendations[role].append(rec)

            for role, recs in member_recommendations.items():
                report += f"### 👤 {role}的保险配置\n\n"
                report += "| 险种 | 保障期限 | 属性 | 类型 | 推荐保额 | 缴费年限 | 预估保费/年 |\n"
                report += "|------|----------|------|------|----------|----------|-------------|\n"

                for rec in recs:
                    member_age = rec['member']['age']
                    policy_type = self._determine_policy_type(rec['coverage_period'])
                    payment_period = self._determine_payment_period(member_age, rec['coverage_period'])
                    premium = self._calculate_premium(rec['insurance_type'], rec['coverage'], member_age, payment_period)
                    
                    report += f"| {rec['insurance_type']} | {rec['coverage_period']} | {rec['investment_attribute']}型 | {policy_type} | {rec['coverage']} | {payment_period} | {premium} |\n"
                    
                    premium_match = re.search(r'(\d+)-(\d+)元', premium)
                    if premium_match:
                        total_premium_min += int(premium_match.group(1))
                        total_premium_max += int(premium_match.group(2))

                report += "\n**💡 推荐理由：**\n\n"
                report += self._generate_reason_text(role, recs)
                report += "\n\n"

            if total_premium_min > 0:
                report += "---\n\n"
                report += "## 💰 预算参考\n\n"
                report += f"根据以上配置，年交保费大约在 **{int(total_premium_min/1000)}千-{int(total_premium_max/1000)}千元**（{total_premium_min}-{total_premium_max}元）左右。\n\n"
                report += "这个预算占家庭年收入的比例适中，符合\"量力而行\"的原则。\n\n"

            report += self._get_not_recommended_reasons(recommendations)

            report += "---\n\n"
            report += "## 📖 典型案例\n\n"
            report += self._generate_case_studies()

        report += "\n---\n\n"
        report += "## 💎 核心价值观提示\n\n"
        report += "1. 🛡️ **保险的核心是风险转移和保障，不是投资或储蓄**\n"
        report += "2. ⏰ **保险期间越长，保险成本越高，保费肯定就越高，应优先选择保20年或保至70岁**\n"
        report += "3. ❌ **储蓄型保险产品\"保费很高但保障内容较低\"，风险保额比较低，大部分保费用于投资而非保障**\n"
        report += "4. 📉 **储蓄型保险\"1000元保费只能买回1200元保额\"，违背保险的保障本质**\n"
        report += "5. 💸 **终身保障'囊中羞涩'时应选择保至70岁，只有经济实力允许时才考虑终身产品**\n\n"
        report += "## 💝 写在最后\n\n"
        report += "以上方案是**以最有利于投保人的原则**为您量身定制的。如果您对某些险种有疑问，或者想了解为什么没有推荐某些险种，欢迎随时问我！\n\n"
        report += f"*📅 报告生成时间：{datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}*\n"

        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report)

        print(f"\n您的保险配置方案已生成！请查看文件：{filepath}")
        return filepath

    def _generate_reason_text(self, role: str, recs: List[Dict[str, Any]]) -> str:
        reasons = []
        hidden_needs = self.user_info.get('hidden_needs', {})
        family_oriented = hidden_needs.get('family_orientation', 0) > 0
        security_seeking = hidden_needs.get('security_seeking', 0) > 0
        quality_conscious = hidden_needs.get('quality_conscious', 0) > 0
        scenarios = self.user_info.get('scenarios', [])
        economic_status = self.user_info.get('economic_status', {})
        name = self.user_info.get('name', '您')

        role_text_map = {
            '本人': '家庭经济支柱',
            '配偶': '重要的家庭伙伴',
            '孩子': '未来的希望',
            '父亲': '家庭的根基',
            '母亲': '家庭的守护者',
            '孩子1': '未来的希望',
            '孩子2': '未来的希望'
        }

        insurance_type_descriptions = {
            '寿险': {
                'emoji': '🏆',
                'title': '家庭责任的守护者',
                'description': '定期寿险是家庭经济支柱的重要保障，确保万一发生不幸，家人能获得稳定的经济支持'
            },
            '健康': {
                'emoji': '❤️',
                'title': '健康风险的防护盾',
                'description': '重疾险能在最需要的时候提供一笔现金，帮助支付高额的医疗费用，避免因病致贫'
            },
            '意外': {
                'emoji': '⚡',
                'title': '意外风险的安全带',
                'description': '意外险保费低廉但保障有力，能应对突发的意外事故带来的经济损失'
            }
        }

        for rec in recs:
            rule = rec['rule']
            insurance_type = rec['insurance_type']
            advantages = rule.get('advantages', '')
            matched_scenarios = rec.get('matched_scenarios', [])
            coverage = rec['coverage']

            role_specific_text = role_text_map.get(role, '家庭重要成员')
            type_info = insurance_type_descriptions.get(insurance_type, {'emoji': '📋', 'title': '保险保障', 'description': ''})

            reason_point = f"### {type_info['emoji']} **【{insurance_type} - {type_info['title']}】**\n\n"
            reason_point += f"{type_info['description']}。\n\n"
            
            reason_point += f"**为什么为{role}推荐这份保障？**\n\n"
            reason_point += f"1. 🎯 **角色定位**：作为{role_specific_text}，{role}的保障是整个家庭保障体系中不可或缺的一环。{advantages[:150]}...\n\n"

            if matched_scenarios:
                reason_point += f"2. 📊 **情况匹配**：您描述的「{matched_scenarios[0]}」等情况，正是我们推荐这类保障的典型场景。\n\n"

            reason_point += f"3. 💰 **保额设计**：本次推荐{coverage}保额，综合考虑了您的经济状况和保障需求。"
            if economic_status.get('city'):
                reason_point += f"在{economic_status['city']}这样的城市生活，医疗和生活成本相对较高，充足的保额能更好地应对风险；"
            if economic_status.get('occupation'):
                reason_point += f"您从事{economic_status['occupation']}工作，"
                occupation_stability = self._parse_occupation_stability(economic_status['occupation'])
                if occupation_stability == 'unstable':
                    reason_point += f"职业相对灵活，因此我们适当提高了保额以应对收入波动风险；"
            reason_point += "\n\n"

            if family_oriented:
                reason_point += f"4. 👨👩👧👦 **家庭责任**：从您的描述中能感受到您对家人深深的爱与责任。这份保险就像一把保护伞，让您在为家人遮风挡雨时更加安心。\n\n"

            if security_seeking:
                reason_point += f"5. 🛡️ **安全感需求**：您对生活稳定性的追求值得肯定，这份保险正是为追求安稳的您量身定制的，让未来更加可期。\n\n"

            reasons.append(reason_point)

        return '\n'.join(reasons)

    def _generate_not_recommended_reasons(self) -> str:
        reasons = []
        reasons.append("## 不推荐理由\n\n")
        reasons.append("### 一、综合分析\n\n")
        reasons.append("经过全面的评估和分析，您的情况目前不符合我们为投保人推荐的优选条件。\n\n")

        reasons.append("### 二、具体原因分析\n\n")
        
        scenarios = self.user_info.get('scenarios', [])
        if scenarios:
            reasons.append("1. **当前情况评估**：\n")
            reasons.append("   您描述的情况符合以下特点：\n")
            for scenario in scenarios:
                reasons.append(f"   - {scenario}\n")
            reasons.append("\n")
        
        economic_status = self.user_info.get('economic_status', {})
        economic_level = economic_status.get('economic_level', '一般')
        reasons.append(f"2. **经济状况考量**：\n")
        reasons.append(f"   您的经济水平评估为\"{economic_level}\"。\n")
        if economic_level == '一般':
            reasons.append("   对于经济条件一般的家庭，我们建议优先考虑保障的性价比，当前市场上的保险产品可能无法提供足够的保障杠杆。\n")
        reasons.append("\n")

        reasons.append("3. **年龄因素分析**：\n")
        members = self.user_info.get('family_members', [])
        for member in members:
            age_group = member.get('age_group', '')
            reasons.append(f"   - {member['role']}（{member['age']}岁）：\n")
            
            matched_rules = [r for r in self.insurance_rules 
                            if r.get('age_group') == age_group 
                            and r.get('investment_attribute') == '保障']
            
            if matched_rules:
                not_worth_buying_scenarios = []
                for rule in matched_rules:
                    for nw in rule.get('not_worth_buying', []):
                        not_worth_buying_scenarios.append(nw.get('scenario', ''))
                
                if not_worth_buying_scenarios:
                    reasons.append("     暂不建议购买的原因可能包括：\n")
                    for i, scenario in enumerate(not_worth_buying_scenarios[:3], 1):
                        reasons.append(f"     {i}. {scenario}\n")
                else:
                    reasons.append("     当前没有明确的不建议购买的情况，但也没有找到最适合您的保障方案。\n")
            else:
                reasons.append("     暂未找到最适合该年龄段的保障型保险方案。\n")
            reasons.append("\n")

        reasons.append("### 三、建议与说明\n\n")
        reasons.append("1. **保险的本质是保障**：\n")
        reasons.append("   保险的核心功能是风险转移，而不是投资或储蓄。在当前情况下，购买保险可能无法有效发挥风险转移的作用。\n\n")
        reasons.append("2. **性价比考量**：\n")
        reasons.append("   在某些年龄段或经济条件下，购买保险的性价比可能不高，保费支出可能超过实际保障需求。\n\n")
        reasons.append("3. **时机建议**：\n")
        reasons.append("   建议在以下情况发生变化时重新评估：\n")
        reasons.append("   - 家庭成员结构发生变化（如新增子女、父母年龄增长）\n")
        reasons.append("   - 经济状况显著改善\n")
        reasons.append("   - 职业或收入稳定性发生变化\n")
        reasons.append("   - 健康状况发生变化\n\n")
        reasons.append("4. **核心原则重申**：\n")
        reasons.append("   【核心原则】保险期间越长，保险成本越高，保费肯定就越高。如果当前预算有限，建议优先考虑短期保障或暂不购买。\n")
        reasons.append("   【核心原则】储蓄型保险产品\"保费很高但保障内容较低\"，风险保额比较低，大部分保费用于投资而非保障。\n")

        return ''.join(reasons)

    def _generate_case_studies(self) -> str:
        name = self.user_info.get('name', '用户')
        members = self.user_info.get('family_members', [])
        economic_status = self.user_info.get('economic_status', {})
        occupation = economic_status.get('occupation', '')
        city = economic_status.get('city', '')

        case1_name = f"{name}女士" if name else "王女士"
        case2_name = f"{name}先生" if name else "李先生"

        case1 = f"### 案例一：{case1_name}的故事\n\n"
        case1 += f"{case1_name}今年35岁，"
        if occupation:
            case1 += f"是一名{occupation}，"
        if city:
            case1 += f"在{city}工作和生活，"
        case1 += f"年收入约{economic_status.get('income', 30)}万，"

        if any(m['role'] == '配偶' for m in members):
            case1 += "和伴侣有一个5岁的孩子，"
        if any(m['role'] in ['父亲', '母亲'] for m in members):
            case1 += "父母也需要照顾，"

        case1 += f"家庭责任重大。最初{case1_name}对保险并不了解，"
        case1 += "经过咨询后，她选择了我们推荐的保障方案。两年后，她因为健康问题需要住院治疗，"
        case1 += "幸运的是，她配置的健康险为她提供了充足的医疗费用保障，让她能够安心治疗，"
        case1 += "不必为费用担忧。这次经历让她深深体会到保险的重要性。\n"

        case2 = f"\n### 案例二：{case2_name}的选择\n\n"
        case2 += f"{case2_name}今年40岁，"
        if occupation:
            case2 += f"在{occupation}行业工作，"
        if city:
            case2 += f"在{city}打拼，"
        case2 += f"事业小有成就，但也非常忙碌。他非常关心家人的未来，"
        case2 += "希望为家人提供稳定的保障。在我们的建议下，他配置了保障到70岁的定期寿险。"
        case2 += "虽然保费不低，但他觉得非常值得，因为他知道万一自己发生意外，家人能够获得足够的经济支持，"
        case2 += f"维持现有的生活水平。{case2_name}常说：'保险不是为了改变生活，而是为了不让生活被改变。'"
        case2 += "这句话，也正是我们希望传达给每一位客户的理念。\n"

        return case1 + case2

    def explain_non_recommendation(self, insurance_type: str) -> str:
        name = self.user_info.get('name', '用户')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'不推荐说明_{name}_{timestamp}.md'

        report = f"# {name}关于不推荐{insurance_type}险的说明\n\n"
        report += f"您好{name}！感谢您的提问。关于您询问的{insurance_type}险，我将**以最有利于投保人的原则**为您详细解释为什么没有将其纳入推荐方案：\n\n"
        report += "---\n\n"
        report += "## 📊 不推荐理由\n\n"

        relevant_rules = [r for r in self.insurance_rules if r['insurance_type'] == insurance_type]

        if relevant_rules:
            reasons = []
            for rule in relevant_rules[:2]:
                disadvantages = rule.get('disadvantages', '')
                reasons.append(f"**【{rule['coverage_period']}产品分析】**\n\n")
                reasons.append(disadvantages)
                reasons.append("\n\n")

                for not_worth in rule.get('not_worth_buying', []):
                    scenario = not_worth.get('scenario', '')
                    reason = not_worth.get('reason', '')
                    reasons.append(f"⚠️ **不符合推荐情况**：{scenario}\n")
                    reasons.append(f"💬 **专业说明**：{reason}\n\n")

            report += '\n'.join(reasons)
        else:
            report += f"根据我们的专业分析，{insurance_type}险在当前情况下可能不是最适合您的选择。主要原因包括：\n\n"
            report += "- **性价比考虑**：该险种的保障范围与保费投入不成正比\n"
            report += "- **需求匹配度**：您的家庭情况和风险偏好与该险种的目标客户群体不太匹配\n"
            report += "- **保障重叠**：您已有的保障已经能够覆盖该险种提供的保障范围\n"

        report += "---\n\n"
        report += "## 典型案例\n\n"
        report += self._generate_non_recommendation_cases(insurance_type)

        report += "\n---\n\n"
        report += "## 📌 为什么我们推荐当前方案\n\n"
        report += "相比之下，我们为您推荐的方案是基于以下原因：\n\n"
        report += "1. **专业评估标准**：所有推荐都基于有利于投保人的优选条件\n"
        report += "2. **符合核心原则**：优先选择保障型产品，保障期间适中\n"
        report += "3. **贴合您的情况**：根据您的年龄、经济状况、风险偏好进行了个性化调整\n\n"
        report += "## 💬 专业建议\n\n"
        report += f"当然，以上分析是基于您提供的信息。如果您对{insurance_type}险有特别的需求或偏好，我们可以进一步探讨，看看是否有更适合您的配置方案。\n\n"
        report += f"*报告生成时间：{datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}*\n"

        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report)

        print(f"\n📝 不推荐说明已生成！请查看文件：{filepath}")
        return filepath

    def _generate_non_recommendation_cases(self, insurance_type: str) -> str:
        name = self.user_info.get('name', '用户')

        case1 = f"### 案例一：为什么没有选择{insurance_type}险\n\n"
        case1 += f"{name}今年35岁，刚刚组建家庭，预算有限。在咨询过程中，他考虑过{insurance_type}险，"
        case1 += "但经过我们的分析，发现他的需求主要集中在基础医疗和家庭责任保障上。"
        case1 += f"{insurance_type}险虽然有其特定的优势，但在他的预算范围内，配置更基础的保障型产品"
        case1 += "能够提供更全面、更实用的保障。最终，{name}采纳了我们的建议，用有限的预算获得了更实际的保障。"
        case1 += "现在，他为当时的选择感到庆幸，因为他明白，保险最重要的是保障功能，而不是其他。\n"

        case2 = f"\n### 案例二：配置调整的智慧\n\n"
        case2 += f"另一位客户张先生，今年45岁，是一位企业高管，收入丰厚。最初，他希望配置高额的{insurance_type}险，"
        case2 += "认为这样才能体现对家人的关爱。但经过深入分析，我们发现他更需要的是终身型的保障方案，"
        case2 += "而不是{insurance_type}险提供的短期保障。我们为他设计了一套综合保障方案，既满足了他对高端医疗的需求，"
        case2 += "又为家人提供了稳定的长期保障。张先生后来告诉我们，这个调整让他省了不少钱，同时获得了更合适的保障。\n"

        return case1 + case2


def main():
    advisor = InsuranceAdvisor()

    print("\n" + "=" * 50)
    print("         AI保险顾问")
    print("=" * 50)
    print("我是您的AI保险顾问，很高兴为您服务！")
    print("我们可以像聊天一样，您随时说说您的情况~")
    print("=" * 50 + "\n")

    response = advisor.get_response()
    print(f"保险顾问：{response}")

    while True:
        user_input = input("您：")

        if user_input.lower() in ['退出', '结束', 'bye', '再见']:
            print("保险顾问：非常感谢您的信任！如果以后有任何保险方面的问题，随时欢迎再来找我~祝您和家人身体健康，生活愉快！")
            break

        response = advisor.get_response(user_input)
        print(f"保险顾问：{response}")

        if advisor.is_info_complete():
            print("\n📊 信息收集完成！正在为您生成保险配置方案...")
            advisor.generate_recommendation()

            while True:
                follow_up = input("\n您还想了解什么吗？（输入险种名称或'退出'）：")
                if follow_up.lower() in ['退出', '结束', 'bye', '再见']:
                    print("保险顾问：非常感谢您的信任！祝您和家人身体健康，生活愉快！")
                    return
                elif follow_up in ['寿险', '健康', '意外']:
                    advisor.explain_non_recommendation(follow_up)
                else:
                    print("保险顾问：很抱歉，我不太理解您的问题。您可以问我关于寿险、健康险或意外险的问题~")


if __name__ == '__main__':
    main()
