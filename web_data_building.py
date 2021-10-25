import json
import os

crawling_data_folder = 'data/crawling_data'
output = 'data/vnexpress_news'

os.makedirs(output, exist_ok=True)

for file in os.listdir(crawling_data_folder):
    topic = file.split('.txt')[0]
    topic_folder = os.path.join(output, topic)
    os.makedirs(topic_folder, exist=True)
    samples = open(os.path.join(crawling_data_folder, file)).readlines()

    auto_filename_generator = 0
    for sample in samples:
        data = json.load(sample)
        content = data['content']
        with open(os.path.join(topic_folder, str(auto_filename_generator).zfill(5) + ".txt"), 'w') as f:
            f.writelines(content)
            f.write('\n')
        auto_filename_generator += 1
