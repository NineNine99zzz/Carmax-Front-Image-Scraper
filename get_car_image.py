import time
import random
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



# set up Selenium
driver = webdriver.Chrome()
base_url = "https://www.carmax.com/cars/all"
driver.get(base_url)
time.sleep(2)  # Wait for the page to load
driver.maximize_window()
time.sleep(2)  # Wait for the window to maximize


page_num = 50 #change the number of pages to scrape more
index = 0
max_retries = 5
wait = WebDriverWait(driver, 10)  # Set up explicit wait

for i in tqdm(range(page_num)):
    retries = 0
    while retries < max_retries:
        try:
            '''wait for the button to be clickable'''
            button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="see-more"]/div/hzn-button')))
            button.click()  # Click the "See More" button
            time.sleep(2 + random.uniform(0, 1)) 
            index += 1


            if index == page_num:
                # Save the HTML content of the page
                html = driver.page_source
                with open(r'D:\project_data\carmax\carmax_webpage.html', 'w', encoding='utf-8') as f:
                    f.write(html)

                print(f'Total clicks: {index}')
                driver.quit()
                exit()
            break
        except NoSuchElementException as e:
            '''Handle the case where the button is not found'''

            print(f'Failed to click the button, retrying in 5 seconds. Attempt {retries + 1} of {max_retries}')
            retries += 1
            time.sleep(5)
            html = driver.page_source

    if retries == max_retries:
        # If max retries reached, save the HTML and exit
        print(f'Failed to click the button after {max_retries} attempts. Saving HTML and exiting, break 2')  
        html = driver.page_source
        with open(r'D:\project_data\carmax\carmax_webpage.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print(f'Total clicks: {index}')
        driver.quit()
        exit()

# Save the final HTML content of the page
html = driver.page_source
with open(r'D:\project_data\carmax\carmax_webpagel.html', 'w', encoding='utf-8') as f:
    f.write(html)
print(f'Total clicks: {index}')
driver.quit()
