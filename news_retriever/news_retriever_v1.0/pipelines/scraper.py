import requests
import re
import xml.etree.ElementTree as ET

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def fetch_news_local_filter(keyword):
    print(f"[*] Fetching RSS feed and searching for: {keyword}")
    
    url = "https://www.chinanews.com.cn/rss/scroll-news.xml"
    
    results = []
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        response.encoding = 'utf-8'
        
        root = ET.fromstring(response.content)
        
        for item in root.findall('.//item'):
            title = item.find('title').text
            link = item.find('link').text
            
            if title:
                if keyword in title:
                    results.append({
                        "title": title,
                        "source": "China News (中新网)",
                        "url": link
                    })
    except Exception as e:
        print(f"⚠️RSS Error: {e}")
        
    if not results:
        print("  ⚠️No exact match found. Returning latest headlines instead.")
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            root = ET.fromstring(response.content)
            for item in root.findall('.//item')[:5]:
                results.append({
                    "title": item.find('title').text,
                    "source": "China News (Latest)",
                    "url": item.find('link').text
                })
        except:
            pass
            
    return results[:10]

def search_all_sources(keyword):
    return fetch_news_local_filter(keyword)

if __name__ == "__main__":
    test = search_all_sources("经济")
    print(f"\n✅ Total Results: {len(test)}")
    for i, r in enumerate(test):
        print(f"[{i+1}] {r['title']} ({r['source']})")