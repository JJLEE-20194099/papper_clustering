from bs4 import BeautifulSoup
import requests
from tqdm import tqdm

def get_content_(url):
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

# links = []
# raw_content = get_content_("https://vnexpress.net/the-gioi/tu-lieu-p1")
# soup = BeautifulSoup(raw_content, "html.parser")


# for article in soup.find_all("article"):
#     try:
#         p = article.find('h2', class_='title_news')
#         url = p.find('a', href=True)
#         links.append(url['href'])
#     except Exception:
#         # print(e)
#         pass

# return links

print(BeautifulSoup(get_content_("https://vnexpress.net/the-gioi/tu-lieu-p1"), 'html.parser'))