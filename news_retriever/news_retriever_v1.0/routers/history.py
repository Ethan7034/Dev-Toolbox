from fastapi import APIRouter, Depends
from pipelines.database import get_user_history
from routers.auth import get_current_user

router = APIRouter(prefix="/api", tags=["History"])

@router.get("/history", summary="Search History / 获取当前用户的搜索历史")
def fetch_history(
    current_user: str = Depends(get_current_user)
):
    history_data = get_user_history(current_user, limit=5)
    
    return {
        "status": "success",
        "user": current_user,
        "count": len(history_data),
        "history": history_data
    }