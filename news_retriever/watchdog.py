import requests
import time
import os
import re

LOCAL_URL = "http://localhost:8000"
LOG_FILE = "tunnel_log.txt"

# 🔍 核心函数：自动从日志里提取最新的公网 URL
def get_tunnel_url():
    if not os.path.exists(LOG_FILE):
        return None
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            content = f.read()
            # 用正则匹配 trycloudflare 的链接
            urls = re.findall(r'https://[a-zA-Z0-9-]+\.trycloudflare\.com', content)
            if urls:
                return urls[-1] # 返回最后一次匹配到的链接
    except Exception as e:
        print(f"⚠️ 读取日志文件失败: {e}")
    return None

print("🚀 启动保活引擎，正在自动抓取隧道链接...")

current_tunnel_url = None
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

while True:
    # 如果还没有链接，或者之前的链接挂了（比如日志更新了），就去日志里抓最新的
    if not current_tunnel_url:
        current_tunnel_url = get_tunnel_url()
        if current_tunnel_url:
            print(f"✅ 自动抓取到链接: {current_tunnel_url}")
        else:
            print(f"[{time.strftime('%H:%M:%S')}] 等待日志生成链接中... (确认 cloudflared 是否在运行)")
            time.sleep(3)
            continue

    try:
        # 踢一脚本地
        requests.get(LOCAL_URL, headers=headers, timeout=5)
        
        # 踢一脚隧道公网
        res = requests.get(current_tunnel_url, headers=headers, timeout=10)
        print(f"[{time.strftime('%H:%M:%S')}] 保活成功，状态码: {res.status_code}，目标: {current_tunnel_url}")
        
    except Exception as e:
        print(f"[{time.strftime('%H:%M:%S')}] ⚠️ 保活异常: {e}")
        
        # 如果报错，说明链接可能失效了，清空当前链接，下一轮循环重新去日志里找
        # （比如断网重连后，cloudflared 生成了新链接）
        current_tunnel_url = None 
    
    # 每 30 秒循环一次
    time.sleep(30)