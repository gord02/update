from bs4 import BeautifulSoup
from selenium import webdriver
from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService

def get_data():  
    opts = Options()
    # so that browser instance doesn't pop up
    opts.add_argument("--headless")

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options = opts)
    url = "https://www.quora.com/careers/engineering"
    driver.get(url)
    content = driver.page_source
    soup = BeautifulSoup(content, "lxml")
    driver.quit()
    print(content)

    jobs = []
    # titles = soup.select("td div")
    title = soup.select("td div")
    print(title)
    # for title in titles:
        # jobs.append(title.contents[0])