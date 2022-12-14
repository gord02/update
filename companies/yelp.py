from bs4 import BeautifulSoup
from selenium import webdriver
from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService

import time

from logic import process

def get_data():  
    start_time = time.time()
    opts = Options()
    # so that browser instance doesn't pop up
    opts.add_argument("--headless")
    opts.add_argument('--disable-blink-features=AutomationControlled')
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options = opts)
    url = "https://www.yelp.careers/us/en/search-results"

    driver.get(url)
    content = driver.page_source
    soup = BeautifulSoup(content, "lxml")
    driver.quit()

    titles = set()

    # Page has pagination
    usedLinks = set()
    q = []
    # skipping the prev button, there is hidden prev link that will be first in the list so skip to index 1
    firstLink = soup.select("ul.pagination li a")[1]['href']

    q.append(firstLink)
    while len(q) > 0:
        link = q.pop()
        usedLinks.add(link)
        # have to re-initialize new web driver for new calls
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options = opts)
        driver.get(link)
        page = driver.page_source
        driver.quit()
        soup = BeautifulSoup(page, "lxml") 
        
        jobTitles =  soup.select("div.job-title span")
        for jobT in jobTitles:
            titles.add(jobT.contents[0])
        
        links = soup.select("ul.pagination li a")
        for newLink in links:
            urlLink =  newLink['href'] 
            if urlLink not in usedLinks and len(urlLink) > 0:
                    q.insert(0, urlLink) 
                    # prevents repeated addition of the same url to the q
                    usedLinks.add(urlLink)
                    
    jobs = process.process_job_titles(titles)
    if len(jobs) > 0:
        # update company in database to found
        pass  
         
                         
    print("--- %s seconds ---" % (time.time() - start_time))
    print("minutes: ", (time.time() - start_time)/60)
    
  