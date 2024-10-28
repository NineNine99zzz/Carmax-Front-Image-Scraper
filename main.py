import os
import time
from random import randint
from fake_useragent import UserAgent
import requests
import pandas as pd

# set working directory
os.chdir(r'D:\project_data\carmax')

# create folder to store images
if not os.path.exists('images'):
    os.makedirs('images')

# read data
df = pd.read_csv(r'D:\project_data\carmax\carmax_sample_img.csv')
url_list = df['image_url']
image_names = df['year'].astype(str) + '_' + df['make'] + '_' + df['model'] + '.jpg'

# set up headers
ua = UserAgent()

# change the headers if needed
headers = {
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "zh-CN,zh;q=0.9",
    "cookie": "_gcl_au=1.1.2095064638.1729758455; ai_user=m9SbjmndDMO2U2+DmOvjyt|2024-10-25T07:44:13.165Z; ...",

    # Note: For the cookie, if any part is deleted, the request might be blocked, 
    # so it is kept as is. No idea why. You can try with your own cookie.

    "referer": "https://www.carmax.com/car/26472995",
    "sec-ch-ua": '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": ua.firefox   # if your got 403 error, try to change the user agent to chrome or other
}

def main(url_list, image_names):
    start_time = time.time()
    total_images = len(url_list)

    for i, (url, image_name) in enumerate(zip(url_list, image_names), start=1):

        # Replace invalid characters in file name with underscores
        safe_image_name = image_name.replace('/', '_').replace('\\', '_').replace(':', '_') \
                                    .replace('*', '_').replace('?', '_').replace('"', '_') \
                                    .replace('<', '_').replace('>', '_').replace('|', '_')

        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()  

            with open(f'images/{safe_image_name}', 'wb') as f:
                f.write(response.content)

            print(f'[{i}/{total_images}] Successfully downloaded image: {image_name}')
        
        except requests.RequestException as e:
            print(f'[{i}/{total_images}] Failed to download image from {url}: {e}')

        # Sleep to avoid overwhelming the server
        time.sleep(randint(1, 2))
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f'Total time taken: {elapsed_time:.2f} seconds')

main(url_list, image_names)
