import json
import os
from tqdm import tqdm

from src.url_functions import get_all_news_urls_from_topics_links, get_content_news_from_news_url
from src.utils import read_yaml

# read list of links for each topic
topics_links = read_yaml('src/links.yaml')

# get the list of links of news for each topic
print('Get the list of links of news for each topic')
topics_links = get_all_news_urls_from_topics_links(topics_links, n_pages_per_topic=1)

# the number of news links per topic
for k, v in topics_links.items():
    print(f'topic: {k} - No.samples: {len(v)}')

# set output path
OUTPUT = 'data/crawl_data'
os.makedirs(OUTPUT, exist_ok=False)

print('\nGet news content and save to storage')
for topic, links in topics_links.items():
    print(f'topic: {topic} - No.samples: {len(links)}')

    file_path = os.path.join(OUTPUT, f'{topic}.txt')
    with open(file_path, 'w') as f:
        for link in tqdm(links):
            s = get_content_news_from_news_url(link)
            if s is not None:
                f.writelines(json.dumps(s))
                f.write('\n')

print("Completed")
