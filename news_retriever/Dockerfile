FROM python:3.11-slim
ENV TZ=Asia/Shanghai
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip && \
    apt-get update && \
    apt-get install -y --no-install-recommends gcc build-essential tzdata && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]