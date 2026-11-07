import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

PROXIES = None  

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Connection": "keep-alive"
}

def fetch_rss_source(url, source_name, lang, keyword):
    results = []
    try:
        response = requests.get(url, headers=HEADERS, proxies=PROXIES, timeout=8)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'xml')
        
        for item in soup.find_all('item'):
            title = item.find('title').text if item.find('title') else ""
            link = item.find('link').text if item.find('link') else ""
            
            if title and link:
                if keyword.lower() in title.lower():
                    results.append({
                        "title": title.strip(),
                        "source": source_name,
                        "url": link.strip(),
                        "lang": lang 
                    })
    except Exception as e:
        print(f"[!] Skip {source_name}: {e}")
    return results

def search_all_sources(keyword):
    print(f"\n========== 🚀 Starting Search for: '{keyword}' ==========")
    
    sources = [
        ("https://a.jiemian.com/index.php?m=article&a=rss", "界面新闻", "zh"),
        ("https://36kr.com/feed-newsflash", "36氪快讯", "zh"),
        ("https://36kr.com/feed", "36氪", "zh"),
        ("http://www.tmtpost.com/rss.xml", "钛媒体", "zh"),
        ("https://www.ifanr.com/feed", "爱范儿", "zh"),
        ("https://sspai.com/feed", "少数派", "zh"),
        ("https://www.solidot.org/index.rss", "Solidot", "zh"),
        ("https://plink.anyfeeder.com/cnbeta", "cnBeta", "zh"),
        ("https://www.itjuzi.com/api/telegraph.xml", "IT桔子", "zh"),
        ("http://www.chinanews.com.cn/rss/scroll-news.xml", "中新网", "zh"),
        ("https://zhidx.com/rss", "智东西", "zh"),
        ("https://www.ithome.com/rss/", "IT之家", "zh"),
    ]
    
    all_results = []
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(fetch_rss_source, url, name, lang, keyword) for url, name, lang in sources]
        for future in futures:
            all_results.extend(future.result())
            
    seen_titles = set()
    unique_results = []
    for item in all_results:
        if item["title"] not in seen_titles:
            seen_titles.add(item["title"])
            unique_results.append(item)
            
    if not unique_results:
        print("[!] No articles found or network failed.")

    print(f"========== ✅ Found {len(unique_results)} articles ==========\n")
    return unique_results[:15]