@echo off

:: 1. 清理昨天的旧日志（解决你的强迫症）
if exist tunnel_log.txt del tunnel_log.txt

:: 2. 自动清理被占用的 8000 端口（注意 python 的拼写！）
echo Cleaning up port 8000...
taskkill /F /IM python.exe >nul 2>&1

:: 3. 启动 FastAPI 后端
echo Starting FastAPI Backend...
start cmd /k "python -m uvicorn main:app --host 127.0.0.1 --port 8000"

:: 4. 启动 Cloudflared 隧道
echo Starting Cloudflared Tunnel...
start /b cmd /c "..\code_tools\cloudflared.exe tunnel --url http://127.0.0.1:8000 --protocol http2 > tunnel_log.txt 2>&1"

:: 5. 延迟 3 秒启动看门狗
echo Starting Watchdog...
start /b cmd /c "timeout /t 3 >nul && python watchdog.py"

echo ====================================================
echo Services Started.
echo 1. Backend is running in a new window. Check it for errors!
echo 2. Please check tunnel_log.txt to find your public URL.
echo ====================================================
pause