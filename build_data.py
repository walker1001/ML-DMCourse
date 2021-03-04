import os
import json

CRAWL_FOLDER = 'data/crawl_data'
OUTPUT = 'data/news_vnexpress'

os.makedirs(OUTPUT, exist_ok=False)

for filename in os.listdir(CRAWL_FOLDER):
    label = filename.split('.txt')[0]
    label_folder = os.path.join(OUTPUT, label)
    os.makedirs(label_folder, exist_ok=False)
    samples = open(os.path.join(CRAWL_FOLDER, filename)).readlines()
    
    n = 0
    for sample in samples:
        s = json.loads(sample)
        content = s['contents']
        with open(os.path.join(label_folder, str(n).zfill(5) + ".txt"), 'w') as f:
            f.writelines(content)
            f.write('\n')
        n += 1

print("Completed")
