# 🏗️ News Retriever: Full-Stack Cloud-Native Architecture

## 📌 Overview
The **News Retriever** is a microservice-based data pipeline designed for real-time news scraping, NLP sentiment analysis, and secure public exposure. The architecture strictly follows a top-down, decoupled approach, ensuring high availability, security, and scalability.

## 🗺️ System Architecture (Layered Breakdown)

### 🛡️ 1. Edge Security & Network Access Layer
*   **Cloudflare WAF (Web Application Firewall)**: Intercepts malicious traffic, prevents DDoS attacks, and blocks automated bots at the edge.
*   **Cloudflared Tunnel**: Establishes a secure, outbound-only connection to expose the local FastAPI service to the public internet without opening inbound ports.
*   **SLA Management**: The service operates within a predefined Service Level Agreement (e.g., 10:30 - 22:30 daily) to ensure resource efficiency.

### 🌐 2. Frontend Presentation Layer
*   **Minimalist Web UI**: Built with pure HTML and Vanilla JavaScript (no heavy frontend frameworks).
*   **Dynamic Language Toggle**: Implements i18n (Internationalization) with a bilingual UI (EN/ZH) to cater to different user demographics.
*   **API Integration**: Communicates with the backend via asynchronous `fetch` API calls, rendering JSON responses into user-friendly data cards.

### ⚙️ 3. Application & Middleware Layer
*   **FastAPI Core**: Serves as the high-performance API Gateway, handling asynchronous HTTP requests.
*   **Authentication Middleware**: Inherits JWT/session validation from the legacy `User Login System V4.0` to secure the `/search` endpoint.
*   **Latency Monitoring Middleware**: Intercepts requests to measure processing time and logs performance metrics for system observability.

### 🧠 4. Data Pipeline & NLP Layer (Core Engine)
1.  **Scraping**: Utilizes `Requests` and `BeautifulSoup` to dynamically fetch news content based on user-defined keywords.
2.  **Cleaning**: Applies `Regular Expressions (Regex)` to strip HTML tags, advertisements, and irrelevant noise.
3.  **Structuring**: Employs `Pandas` to normalize the unstructured text into structured DataFrames, handling deduplication and formatting.
4.  **Analysis**: Integrates `jieba` for Chinese word segmentation and frequency analysis, and `SnowNLP` for sentiment polarity scoring (Positive/Negative).

### 💾 5. Persistence & Logging Layer
*   **JSON-based Data Store**: Temporarily caches query history and high-frequency keywords, acting as a growing local corpus.
*   *(Future Extension)*: Planned migration to SQLite/PostgreSQL for scalable relational data storage.

### 🐳 6. Cloud-Native Deployment Layer
*   **Docker Containerization**: Encapsulates the application and its dependencies into immutable images to guarantee environment consistency.
*   **Background Daemonization**: Deploys via NSSM (Windows) or VBS scripts to ensure the service runs silently and independently of the IDE terminal.

---

## 📂 Project Structure
```text
news_retriever/
├── main.py               # FastAPI entry point & Middleware configurations
├── scraper.py            # Web scraping and data extraction modules
├── nlp_pipeline.py       # Pandas data processing & jieba/SnowNLP analysis
├── static/
│   └── index.html        # Frontend UI with bilingual toggle logic
├── data/
│   └── history.json      # Local persistence for query logs
├── requirements.txt      # Python dependencies
└── Dockerfile            # Container build instructions