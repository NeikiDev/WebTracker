import hashlib
import requests
import os
import json
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin, quote_plus

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0";

def fetch_page(url):
    try:
        with requests.Session() as session:
            session.headers.update({"User-Agent": user_agent})
            resp = session.get(url, timeout=5)
            content_type = resp.headers.get("Content-Type", "text/html")
            if "text/html" not in content_type:
                return resp.status_code, content_type, ""
            return resp.status_code, content_type, resp.text
    except Exception as error:
        return None, None, error
    
def extract_metadata(soup):
    og_data = {}
    for tag in soup.find_all("meta"):
        prop = tag.get("property")
        content = tag.get("content")
        if prop and content and prop.startswith("og:"):
            og_data[prop[3:]] = content
    return og_data

def sha256_of_html(html):
    return hashlib.sha256(html.encode("utf-8")).hexdigest()

def url_as_md5(url):
    return hashlib.md5(url.encode("utf-8")).hexdigest()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def countdown(t):
    while t:
        mins, secs = divmod(t, 60)
        timer = 'Next crawl in: {:02d}:{:02d}'.format(mins, secs)
        print(timer, end="\r")
        time.sleep(1)
        t -= 1

def main_crawl():
    urls = "urls.txt"
    webhook_url = "<YOUR DISCORD WEBHOOK URL>"
    crawl_interval = 5 * 60  

    while True:
        url_list = open(urls, "r").read().split("\n")
        url_count = len([u for u in url_list if u])
        
        clear_screen()
        print(f"Starting WebCrawler Pro 3000\nCurrently tracking {url_count} URLs. Please wait...")
        
        for url in url_list:
            if not url:
                continue
            old_url_data_loaded = {}
            url_hash = url_as_md5(url)
            file_path = f"./tracked/{url_hash}.json"

            if not os.path.exists("./tracked"):
                os.makedirs("./tracked")

            if os.path.exists(file_path):
                with open(file_path, "r") as f:
                    old_url_data_loaded = json.load(f)

            status, content_type, html = fetch_page(url)
            soup = BeautifulSoup(html, "html.parser")
            metadata = extract_metadata(soup)

            website_data = {
                "status": status,
                "content_type": content_type,
                "metadata_length": len(str(metadata)),
                "sha256": sha256_of_html(html)
            }

            change_detected = old_url_data_loaded and (old_url_data_loaded["sha256"] != website_data["sha256"] or old_url_data_loaded["status"] != website_data["status"])
            
            if not old_url_data_loaded or change_detected:
                embed_color = 0x00ff00 if not old_url_data_loaded else 0xff0000
                action = "First crawl" if not old_url_data_loaded else "Changes detected"
                xdata = {
                    "content": f"{action} of {url} - {url_hash}",
                    "username": "Webtracker",
                    "embeds": [{
                        "title": "Website Data",
                        "description": f"Status Code: {website_data['status']}\nBody Hash: {website_data['sha256']}\nBody Length: {len(html)}\nMetadata Length: {len(metadata)}",
                        "color": embed_color
                    }]
                }
                
                with open(file_path, "w") as f:
                    json.dump(website_data, f, indent=4)

                response = requests.post(webhook_url, json=xdata)
                print(f"Sent {url} to webhook with status code {response.status_code}")

        countdown(crawl_interval)

if __name__ == '__main__':
    main_crawl()