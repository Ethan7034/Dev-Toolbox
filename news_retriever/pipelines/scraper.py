import requests
import xml.etree.ElementTree as ET
import re
from concurrent.futures import ThreadPoolExecutor

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def fetch_rss_source(url, source_name, lang, keyword):
    print(f"[*] Fetching from {source_name} [{lang}]...")
    results = []
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        
        root = ET.fromstring(response.content)
        
        for item in root.findall('.//item'):
            title_node = item.find('title')
            link_node = item.find('link')
            
            if title_node is not None and link_node is not None:
                title = title_node.text or ""
                link = link_node.text or ""
                
                if keyword.lower() in title.lower():
                    results.append({
                        "title": title.strip(),
                        "source": source_name,
                        "url": link.strip(),
                        "lang": lang
                    })
    except Exception as e:
        print(f"⚠️Error fetching {source_name}: {e}")
    
    return results

def search_all_sources(keyword):
    print(f"\n========== 🚀 Starting Bilingual Search for: '{keyword}' ==========")
    
    sources = [
        ("https://www.chinanews.com.cn/rss/scroll-news.xml", "China News (中新网)", "zh"),
        ("https://36kr.com/feed", "36Kr (36氪)", "zh"),
        
        ("http://feeds.bbci.co.uk/news/world/rss.xml", "BBC News", "en"),
        ("https://hnrss.org/frontpage", "Hacker News", "en"),
        ("https://www.theguardian.com/world/rss", "The Guardian", "en")
    ]
    
    all_results = []
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(fetch_rss_source, url, name, lang, keyword) for url, name, lang in sources]
        
        for future in futures:
            all_results.extend(future.result())
            
    seen_titles = set()
    unique_results = []
    for item in all_results:
        if item["title"] not in seen_titles:
            seen_titles.add(item["title"])
            unique_results.append(item)
            
    print(f"========== ✅ Found {len(unique_results)} articles ==========\n")
    return unique_results[:15]

if __name__ == "__main__":
    test_results = search_all_sources("AI")
    for idx, res in enumerate(test_results, 1):
        print(f"{idx}. [{res['source']} - {res['lang']}] {res['title']}")