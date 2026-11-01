from fastapi import APIRouter, Depends, HTTPException, Query
from pipelines.scraper import search_all_sources
from routers.auth import get_current_user

router = APIRouter(prefix="/api", tags=["Search"])

@router.get("/search", summary="多源新闻检索")
def search_news(
    keyword: str = Query(..., min_length=1, max_length=50, description="搜索关键词"),
    current_user: str = Depends(get_current_user)
):
    try:
        results = search_all_sources(keyword)
        
        if not results:
            return {
                "status": "success",
                "message": "No news found for this keyword.",
                "count": 0,
                "data": []
            }
            
        return {
            "status": "success",
            "user": current_user,
            "keyword": keyword,
            "count": len(results),
            "data": results
        }
        
    except Exception as e:
        print(f"[!] Search Error: {e}")
        raise HTTPException(
            status_code=500, 
            detail="Internal Server Error during searching. Please try again later."
        )