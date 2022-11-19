from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.common import keys 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
from checkAmbiguity import check_if_authorization
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from apolloScraper import login_to_new_window


def launchBrowser():
    path = './chromedriver.exe'
    chrome_options = Options()
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--allow-running-insecure-content")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36");
    chrome_options.add_argument('start-maximized')
    chrome_options.add_experimental_option('detach',True)
    driver = webdriver.Chrome(path,chrome_options=chrome_options)
    driver.get('http://www.indeed.com')
    return driver

driver = launchBrowser()
whatJobs = driver.find_element(By.XPATH,"//input[@id='text-input-what']").send_keys('Devops Engineer')
whereJobs = driver.find_element(By.XPATH,"//input[@id='text-input-where']").send_keys('Remote')
searchBtn = driver.find_element(by=By.CLASS_NAME, value="yosegi-InlineWhatWhere-primaryButton")
searchBtn.click()


''' Find if the each companies on lists complies with the rules or not '''

def find_if_complies_rules(job):
    try:
        driver.execute_script("arguments[0].scrollIntoView(true)",job)
    except Exception as e:
        print(e)
    actions = ActionChains(driver)
    actions.move_to_element(job)
    actions.click(job)
    actions.perform()
    getCompanyName = driver.find_element(by=By.CLASS_NAME, value="companyName")
    if check_if_authorization(driver) == True:
        login_to_new_window(driver,getCompanyName.text)

    


def find_list_of_jobs():
    job_lists = driver.find_elements(By.XPATH,"//ul[@class='jobsearch-ResultsList css-0']/li")
    for job in job_lists:
        find_if_complies_rules(job)

find_list_of_jobs()