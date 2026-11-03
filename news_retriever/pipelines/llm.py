import requests

# 👇 把这里换成你刚才从智谱复制的 Key
API_KEY = "51d907fcdaa44a7a84272860e27812e2.YExdW68diEJYtC8d"

def generate_ai_summary(news_title):
    """调用智谱 GLM-4-Flash 模型进行新闻总结"""
    url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "glm-4-flash", 
        "messages": [
            {"role": "system", "content": "你是一个专业的新闻分析助手。请用一句话精炼总结以下新闻的核心要点，不超过50个字。"},
            {"role": "user", "content": news_title}
        ],
        "temperature": 0.3
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"⚠️ AI Summary Error: {e}")
        return "⚠️AI 摘要生成失败"