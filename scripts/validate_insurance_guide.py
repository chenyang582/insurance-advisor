import json

def validate_json():
    with open('D:/nearpy/04 skillhub/insurance-advisor/references/insurance_guide.json', encoding='utf-8') as f:
        data = json.load(f)
    
    print('JSON格式有效')
    print(f"总数: {data['total_count']}")
    types = set([x['insurance_type'] for x in data['insurance_list']])
    print(f"保险类型: {types}")
    
    type_counts = {}
    for item in data['insurance_list']:
        t = item['insurance_type']
        type_counts[t] = type_counts.get(t, 0) + 1
    
    print("\n各类型数量:")
    for t, cnt in type_counts.items():
        print(f"  {t}: {cnt}")

if __name__ == '__main__':
    validate_json()
