@echo off
echo Starting FastAPI Backend...
start /b cmd /c "uvicorn main:app --host 127.0.0.1 --port 8000"

echo Starting Cloudflared Tunnel...
start /b cmd /c "cloudflared tunnel --url http://127.0.0.1:8000 > tunnel_log.txt 2>&1"

echo ====================================================
echo Services Started. 
echo Please check tunnel_log.txt to find your public URL.
echo ====================================================