from tqdm import tqdm
import requests
from bs4 import BeautifulSoup

def get_all_page_urls_from_sub_topic_url(sub_topic_url, pages=1) -> list:
    urls = []
    urls.append(sub_topic_url)

    for page in range(1, pages, 1):
        urls.append(sub_topic_url + f'-p{page}')
    
    return urls

def get_content_by_link(url):
    """
    Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
    Accept-Encoding:gzip, deflate, sdch
    Accept-Language:en-US,en;q=0.8,vi;q=0.6
    Connection:keep-alive
    Host:dantri.com.vn
    Referer:http://dantri.com.vn/su-kien.htm
    Upgrade-Insecure-Requests:1
    """
    domain = None
    domains = url.split('/')
    if (domains.__len__() >= 3):
        domain = domains[2]

    headers = dict()
    headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    headers['Accept-Encoding'] = 'gzip, deflate, sdch'
    headers['Accept-Language'] = 'en-US,en;q=0.8,vi;q=0.6'
    headers['Connection'] = 'keep-alive'
    headers['Host'] = domain
    headers['Referer'] = url
    headers['Upgrade-Insecure-Requests'] = '1'

    r = requests.get(url, headers=headers, timeout=10)
    r.encoding = 'utf-8'
    r.close()
    return str(r.text)

def get_content_news_from_news_url(url: str) -> dict:
    
    try:
        raw_content = get_content_by_link(url)
        beautiful_soup = BeautifulSoup(raw_content, 'html.parser')

        title_detail = beautiful_soup.find('h1', class_='title-detail').text

        description = beautiful_soup.find('p', class_='description').txt

        content = ""
        for article_tag in beautiful_soup.find_all('article', class_='fck_detail'):
            for p_element in article_tag.find_all('p', class_='Normal'):
                content += p_element.text
        
        if len(content) < 10:
            return {'None': 'None'}
        
        return {
            "title": title_detail,
            "description": description,
            "contents": content,
            "url": url
        }
    except Exception:
        return {'None': 'None'}

def get_news_links_from_sub_topic_page_link(sub_topic_page_link: str) -> list:
    links = []
    raw_content = get_content_by_link(sub_topic_page_link)
    beautiful_soup = BeautifulSoup(raw_content, 'html.parser')

    for article in beautiful_soup.find_all("article"):
        
        try:
            p = article.find('h3', class_='title-news')
            url = p.find('a', href=True)
            links.append(url['href'])
        except Exception:
            pass
   
    return links

def get_all_new_urls(topics_links: dict, n_pages_per_topic = 1) -> dict:
    res = {}

    for k, v in tqdm(topics_links.items()):
        print(f'topic: {k} - No.sub_topics: {len(v)}')
        res[k] = []
        page_links = []
        for sub_topic_link in tqdm(v):
            s = get_all_page_urls_from_sub_topic_url(sub_topic_link, pages=n_pages_per_topic)
            page_links = page_links + s
        

        for page_link in tqdm(page_links):
            news_links = get_news_links_from_sub_topic_page_link(page_link)
            res[k] = res[k] + news_links
        
    return res
