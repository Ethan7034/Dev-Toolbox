import re
import nltk
from snownlp import SnowNLP
from nltk.sentiment import SentimentIntensityAnalyzer

try:
    sia = SentimentIntensityAnalyzer()
except LookupError:
    print("⚠️ Downloading NLTK vader_lexicon...")
    nltk.download('vader_lexicon', quiet=True)
    sia = SentimentIntensityAnalyzer()

def analyze_sentiment(text):
    if not text or len(text.strip()) == 0:
        return {"score": 0.5, "label": "Neutral"}
        
    try:
        zh_chars = len(re.findall(r'[\u4e00-\u9fa5]', text))
        
        if zh_chars > 0:
            s = SnowNLP(text)
            score = round(s.sentiments, 4)
        else:
            sentiment_dict = sia.polarity_scores(text)
            compound = sentiment_dict['compound']
            score = round((compound + 1) / 2, 4)
            
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