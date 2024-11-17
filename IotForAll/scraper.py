from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
from bs4 import BeautifulSoup
import json
import pprint
import concurrent.futures
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



'''
Each thread wld need its own:
 - master thread basically assigns work to other threads
 - child thread will have its own driver, and scrape the content, and store it for us in DB
'''

FILEPATH = 'c:/Users/srach/Projects/IoTNER/IoT-Web-Scraper/scraped-data/'
FILENAME = 'IoTForAllArticleLinks.json'
SCROLL_PAUSE_TIME = 10
PAGE_LOAD_TIME = 1
WRITE = True

service = Service(ChromeDriverManager().install())
URL = 'https://www.iotforall.com/articles'
def load_driver(service) -> webdriver.Chrome:
    options = Options()
    #options.add_argument("--headless")  # Run in headless mode if needed
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    return webdriver.Chrome(service=service, options=options)

def extract_text_from_iotforall_article(link, driver):
    driver.get(link)
    time.sleep(1)
    bs4 = BeautifulSoup(driver.page_source, 'html.parser')
    headers, paragraphs = [], []
    for paragraph in bs4.find_all('p'):
        paragraphs.append(paragraph.text)

    for header in bs4.find_all('h2', class_='wp-block-heading'):
        headers.append(header.text)
        
    title = bs4.find('h1').text
    return {
        'headers': headers,
        'paragraphs': paragraphs,
        'title': title
    }
   
driver = load_driver(service)
driver.get(URL)
time.sleep(PAGE_LOAD_TIME) # wait for page to load

soup = BeautifulSoup(driver.page_source, 'html.parser')
links_to_articles = set()
num_links_scraped, total_articles_available = 0, int(soup.find('div', class_='filterapp-count flexed').find('span').text)
last_height = driver.execute_script("return document.body.scrollHeight")
num_scrolls = 0


while True and num_scrolls < 10:
    print(f'on scroll: {num_scrolls}')
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    time.sleep(SCROLL_PAUSE_TIME)
    new_height = driver.execute_script("return document.body.scrollHeight")
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    if new_height == last_height:
        break
    last_height = new_height
    num_scrolls += 1

soup = BeautifulSoup(driver.page_source, 'html.parser')
driver.quit()

links = soup.find_all('div', class_='single-result-card')
links = [article.find('a')["href"] for article in links]
print(f'num of article links on the page: {len(links)}')

link_id = 1
data = {}
for link in links:
    data[link] = {
        "url": link,
        "annotated": False,
        "link_id": link_id
    }
    link_id += 1

if WRITE: 
    json_data = json.dumps(data, indent=4)
    with open(FILEPATH + FILENAME, "w") as json_file:
        json_file.write(json_data)
    print('JSON data has been written to', FILEPATH + FILENAME)


'''
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    for article in articles:
    ### click on the articles tag
        header = article.find('h5', class_='ih5')
        results.append(
            executor.submit(extract_text_from_iotforall_article,
                header.find('a')["href"], load_driver(service)
            )
        )

    for result in results:
        try:
            data = result.result()
            ### write code here to write to db once we get the results
        except Exception as exc:
            print('%r generated an exception: ', (exc))
'''

