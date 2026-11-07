import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ZHIPU_API_KEY")
if not API_KEY:
    raise ValueError("⚠️找不到API_KEY！请检查 .env 文件是否正确配置。")

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
            {"role": "system", "content": "你是一个专业的新闻分析助手。请用一句话精炼总结以下新闻的核心要点，不超过100个字。"},
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
        return "⚠️ AI 摘要生成失败"

def is_news_related(keyword: str) -> bool:
    url= "https://open.bigmodel.cn/api/paas/v4/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""
        你是一个严格的新闻检索系统审核员。
        请判断用户输入的词汇是否为适合在“严肃新闻网站”检索的话题（如科技、经济、社会、政治、体育赛事等）。
        如果是游戏、动漫、网络热梗、虚拟主播或无意义的词（例如：奶龙、战锤、原神、丁真），请判定为非新闻。
    
        用户输入：{keyword}
    
        请只输出一个词：YES 或 NO。不要输出任何其他解释或标点符号。
        """

    payload = {
        "model": "glm-4-flash",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.1, 
        "max_tokens": 5
}

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=5)
        response.raise_for_status()
        result = response.json()['choices'][0]['message']['content'].strip().upper()
        return "YES" in result
    except Exception as e:
        print(f"⚠️ AI 意图判定失败 (已默认放行): {e}")
        return True 