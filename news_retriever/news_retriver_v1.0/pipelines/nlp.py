import re
from snownlp import SnowNLP

def analyze_sentiment(text):
    """
    NLP 情感分析管道
    返回格式: {"score": 0.85, "label": "Positive"}
    """
    if not text or len(text.strip()) == 0:
        return {"score": 0.5, "label": "Neutral"}
        
    try:
        s = SnowNLP(text)
        score = round(s.sentiments, 4)
            
        if score > 0.7:
            label = "Positive"
        elif score < 0.3:
            label = "Negative"
        else:
            label = "Neutral"
            
        return {"score": score, "label": label}
    except Exception as e:
        print(f"⚠️ NLP Error: {e}")    
        return {"score": 0.5, "label": "Unknown"}