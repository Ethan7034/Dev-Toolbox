from fastapi import FastAPI, Request, HTTPException, Header
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.openapi.docs import get_swagger_ui_html
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from datetime import datetime, time
from routers import auth, search, history
import os

app = FastAPI(
    title="News Retriever API",
    docs_url=None,
    version="1.0.0",
    description="""
### 📖 Quick Start Guide / 操作指南

Welcome to the **News Retriever API**. For edge security, WAF and rate limiting are enabled.\n
🔒 为防止网页受到恶意攻击，必须在操作前完成安全认证。

**👇 Please follow these 3 steps / 请按照以下 3 步进行操作：**

1. 🔑 **Get Keys / 获取安全密钥**
   * Expand `POST /auth/login` below. *(点击“ POST /auth/login ”)*
   * Click **Try it out**. *(点击“Try it out”)*
   * Enter default credentials. *（输入默认账号密码）*
   * Click **Execute**. *(点击“Execute”)*
   * Copy the access_token from the `response body`. *(复制“response body”中的access_token密钥)*

2. 🛡️ **Authorize / 解锁访问权限**
   * Click the green **Authorize 🔒** button at the top right. *(点击右上角绿色“Authorize 🔒”按钮)*
   * Paste the access_token and click **Authorize**. *(粘贴access_token密钥并确认)*

3. 🔍 **Search News / 开始搜索新闻**
   * Expand `GET /api/search`. *(展开搜索接口)*
   * Click **Try it out**, enter a keyword (e.g., 经济, Tech). *(输入关键词，例如“经济”或“Tech”)*
   * Click **Execute** to view scraped and analyzed results. *(点击执行查看结果)*

---
🕒 **SLA Window / 服务时间** Daily 09:30 - 21:30 (Returns 503 outside this window / 非营业时间返回 503)\n
💡 **Language Tip** Use your browser's built-in translation tool if needed. *(如遇语言障碍，请开启浏览器翻译)*
""",
)
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html(request: Request, accept_language: str = Header(default="en")):
    lang = "zh-CN" if "zh" in accept_language.lower() else "en"
    return get_swagger_ui_html(openapi_url=app.openapi_url, title=app.title + " - Docs", swagger_ui_parameters={"lang": lang})
# --- 1. Passive Anti-Scraping (Rate Limiting) ---
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# --- 2. Edge Security Layer (Mini-WAF & SLA) ---
@app.middleware("http")
async def edge_security_and_sla_middleware(request: Request, call_next):
    
    # --- A. SLA Service Window (09:30 - 21:30) ---
    current_time = datetime.now().time()
    start_time = time(9, 30)
    end_time = time(21, 30)
    
    if not (start_time <= current_time <= end_time):
        return JSONResponse(
            status_code=503,
            content={"detail": "❌Service is currently closed. Our SLA window is 09:30 - 21:30."}
        )

    # --- B. Mini-WAF (Bot Fight Mode) ---
    user_agent = request.headers.get("user-agent", "").lower()
    
    # Block known scraping libraries and empty User-Agents (basic bot fight)
    malicious_bots = ["python-requests", "scrapy", "curl", "wget", "postman"]
    
    if not user_agent or any(bot in user_agent for bot in malicious_bots):
        return JSONResponse(
            status_code=403, 
            content={"detail": "⚠️Forbidden: Malicious bot traffic detected by WAF."}
        )

    # If passed, proceed to the endpoint
    response = await call_next(request)
    return response

# --- 3. Middleware ---
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    return response

# --- 4. API Endpoints ---
app.include_router(auth.router)
app.include_router(search.router)
app.include_router(history.router)
@app.get("/")
def read_root():
    html_path = os.path.join(os.path.dirname(__file__),"index.html")
    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)