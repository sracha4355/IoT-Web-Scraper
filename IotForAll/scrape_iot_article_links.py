from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
from bs4 import BeautifulSoup
import json
import pprint
import concurrent.futures
import os
import threading

# Get the absolute directory of the current script
id = [1]
WRITE = True
NUMBER_OF_THREADS = 20


def load_driver(service) -> webdriver.Chrome:
    options = Options()
    options.add_argument("--headless")  # Run in headless mode if needed
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    return webdriver.Chrome(service=service, options=options)


def extract_text_from_iotforall_article(links, driver, data, interval):
    start, end = interval
    print(start, end)
    link_list = list(links)
    for i in range(start, end):
        print('Scraping article', i)
        link = links[link_list[i]]["url"]
        driver.get(link)
        time.sleep(2)
        bs4 = BeautifulSoup(driver.page_source, 'html.parser')
        elements = bs4.find_all(lambda tag: 
            (tag.name == 'h2' and tag.get("class") == ["wp-block-heading"] or \
            tag.name == "p"))
        
        text = []
        for element in elements:
            text.append(element.text)
        text = "\n".join(text)
        print(text)
        data[link] = {
            "url": None,
            'annotated': False,
            "id": i,
            "text": text,
        }

IoTForAllLinks = None
FILEPATH = os.path.dirname(os.path.realpath(__file__)) + "\..\scraped-data\IoTForAllArticleLinks.json"
print("Absolute path to the file:", FILEPATH)

try:
    with open(FILEPATH, "r") as file:
        IoTForAllLinks = json.load(file)  # Deserialize JSON to Python dictionary
        print("JSON data loaded successfully:")
     
except FileNotFoundError:
    print(f"Error: The file '{FILEPATH}' does not exist.")
except json.JSONDecodeError as e:
    print(f"Error: Failed to decode JSON - {e}")

#driver = load_driver(Service(ChromeDriverManager().install()))

def divide_into_intervals(number, n):
    if n <= 0:
        raise ValueError("Number of intervals (n) must be greater than 0")
    interval_size = number / n
    intervals = [round(i * interval_size, 2) for i in range(n + 1)]
    intervals = [[intervals[i], intervals[i + 1]] for i in range(n)]
    for interval in intervals:
        interval[0] = int(interval[0])
        interval[1] = int(interval[1])
    return intervals

data = {}
intervals = divide_into_intervals(len(IoTForAllLinks), NUMBER_OF_THREADS)
print(intervals)

threads = [threading.Thread(
    target=extract_text_from_iotforall_article,
    args=(IoTForAllLinks, load_driver(Service(ChromeDriverManager().install())), data, interval))
    for interval in intervals
]

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()

#for key, item in IoTForAllLinks.items():
#    link = item["url"]
#    extract_text_from_iotforall_article(link, driver, id, data)
#    break

print(len(data))

FILEPATH = os.path.dirname(os.path.realpath(__file__)) + "\..\scraped-data\IoTForAllArticleText.json"
if WRITE: 
    json_data = json.dumps(data, indent=4)
    with open(FILEPATH, "w") as json_file:
        json_file.write(json_data)
    print('JSON data has been written to', FILEPATH)

#while True:
#    pass
