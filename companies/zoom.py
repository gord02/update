from bs4 import BeautifulSoup
from selenium import webdriver
# from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService

import sys
sys.path.insert(0,'..') #this works relative to where to program was run from 

from logic import process
from logic import notify
from logic import sqlQueries


def get_data(): 
    company =  "Zoom"
    opts = Options()
    # so that browser instance doesn't pop up
    opts.add_argument("--headless")
    jobs = []
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options = opts)

    try:
        url = "https://careers.zoom.us/global-emerging-talent"
        driver.get(url)
        content = driver.page_source
        soup = BeautifulSoup(content, "lxml")
        driver.quit()

        elements = soup.select("td.job-title a")
        for element in elements:
            jobs.append(element.contents[0])
        
        jobs = process.process_job_titles(jobs)
        if len(jobs) > 0:
            # update company in database to found
            sqlQueries.update_company(company)
        return jobs
    
    except:
        # send email about scrapping error
        notify.parsing_error(company)
        return jobs
get_data()