from fastapi import APIRouter, Depends, HTTPException, Query
from pipelines.scraper import search_all_sources
from pipelines.nlp import analyze_sentiment 
from routers.auth import get_current_user
from pipelines.database import log_search

router = APIRouter(prefix="/api", tags=["Search"])

@router.get("/search", summary="Retrieve news & analyze sentiment / 新闻检索与NLP情感分析")
def search_news(
    keyword: str = Query(..., min_length=1, max_length=50, description="搜索关键词"),
    current_user: str = Depends(get_current_user)
):
    try:
        results = search_all_sources(keyword)
        
        if not results:
            return {"status": "success", "message": "No news found.", "count": 0, "data": []}
            
        for news in results:

            sentiment_data = analyze_sentiment(news["title"])

            news["sentiment_score"] = sentiment_data["score"]
            news["sentiment_label"] = sentiment_data["label"]
            
        return {
            "status": "success",
            "user": current_user,
            "keyword": keyword,
            "count": len(results),
            "data": results
        }
        
    except Exception as e:
        print(f"⚠️ Search Error: {e}")
        raise HTTPException(status_code=500, detail="❌Internal Server Error.")