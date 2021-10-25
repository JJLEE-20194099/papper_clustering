import os
from tqdm import tqdm
import json

from src.url_functions import get_all_new_urls, get_content_news_from_news_url
from src.utils import read_yaml

topics_links = read_yaml('./src/links.yaml')

topics_links = get_all_new_urls(topics_links, n_pages_per_topic=1)

for topic, links in topics_links.items():
    print(topic, len(links))

output = 'data/crawling_data'
os.makedirs(output, exist_ok=True)

for topic, url_list in topics_links.items():
    print(topic, len(url_list))
    
    file_path = os.path.join(output, f'{topic}.txt')
    with open(file_path, 'w') as f:
        for link in tqdm(url_list):
            s = get_content_news_from_news_url(link)
            if (s != {'None': 'None'}):
                f.writelines(json.dumps(s))
                f.write('\n')


