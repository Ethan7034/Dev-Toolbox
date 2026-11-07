from fastapi import APIRouter, Depends, HTTPException, Query
from pipelines.scraper import search_all_sources
from pipelines.nlp import analyze_sentiment 
from routers.auth import get_current_user
from pipelines.database import log_search
from pipelines.llm import generate_ai_summary, is_news_related

router = APIRouter(prefix="/api", tags=["Search"])

@router.get("/search", summary="Retrieve news & analyze sentiment / 新闻检索与NLP情感分析")
def search_news(
    keyword: str = Query(..., min_length=1, max_length=50, description="搜索关键词"),
    current_user: str = Depends(get_current_user)
):
    try:
        if not is_news_related(keyword):
            raise HTTPException(
                status_code=400, 
                detail=" 检索被拦截：这似乎不是新闻话题。请搜索科技、经济或时事相关的词汇。"
            )
        results = search_all_sources(keyword)
        
        if not results:
            return {
                "status": "empty", 
                "message": "未找到相关真实新闻，请尝试更宽泛的词汇。", 
                "count": 0, 
                "data": []
            }
            
        for index, news in enumerate(results):
            sentiment_data = analyze_sentiment(news["title"])
            news["sentiment_score"] = sentiment_data["score"]
            news["sentiment_label"] = sentiment_data["label"]
    
        global_ai_summary = ""
        if results:
            titles = [news["title"] for news in results[:5]]
            prompt_text = "请作为新闻主编，用不超过80个字，一句话总结以下新闻的核心趋势：" + "；".join(titles)
            global_ai_summary = generate_ai_summary(prompt_text)

        return {
            "status": "success",
            "user": current_user,
            "keyword": keyword,
            "count": len(results),
            "global_ai_summary": global_ai_summary, 
            "data": results
        }
        
    except HTTPException as he:
        raise he 
    except Exception as e:
        print(f"⚠️ Search Error: {e}")
        raise HTTPException(status_code=500, detail="❌Internal Server Error.")