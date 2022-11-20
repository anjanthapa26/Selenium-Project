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
from apolloLogins import login_to_new_window
from apolloScraper import find_if_eligible_company



list_of_valid_companies_Details =[['Sesamy', 'N/A', 'Estimated $62.1K - $78.6K a year', 'Does not have a source link on OpsWorks Co.'], ['Booz Allen Hamilton', 'N/A', 'Estimated $72.7K - $92K a year', 'https://www.indeed.com/cmp/Booz-Allen-Hamilton'], ['Shtudy', 'N/A', '$60,000 - $400,000 a year', 'Does not have a source link on Shtudy'], ['Capgemini', 'N/A', 'Estimated $95.5K - $121K a year', 'https://www.indeed.com/cmp/Capgemini'], ['Piper Companies', 'N/A', 
'$125,000 - $150,000 a year', 'https://www.indeed.com/cmp/Piper-Companies'], ['No company name available', 'N/A', None, 'Does not have a source link on No company name available'], ['Federal Reserve Bank of Kansas City', 'N/A', 'Estimated $95.8K - $121K a year', 'https://www.indeed.com/cmp/Federal-Reserve-Bank-of-Kansas-City'], ['Premier Inc.', 'N/A', '$64,000 - $118,000 a year', 'https://www.indeed.com/cmp/Premier-Inc.-4'], ['Zoom Video Communications, Inc.', 'N/A', 'Estimated $95.9K - $121K a year', 'https://www.indeed.com/cmp/Zoom-Video-Communications-4'], ['Koch Ag & Energy Solutions', '2 years', '$100,000 - $140,000 a year', 'Does not have a source link on Koch Ag & Energy Solutions'], ['Tista Science and Technology Corporation', 'N/A', 'Estimated $95.5K - $121K a year', 'https://www.indeed.com/cmp/Tista-Science-and-Technology-Corporation'], ['No company name available', 'N/A', None, 'Does not have a source link on No company name available'], ['Remote Jobs', '3 years', 'Estimated $83.2K - $105K a year', 'https://www.indeed.com/cmp/Remote-Jobs'], ['eXp Realty', 'N/A', 'Full-time', 'https://www.indeed.com/cmp/Exp-Realty'], ['Concentrix Catalyst', 'N/A', 'Estimated $58K - $73.4K a year', 'https://www.indeed.com/cmp/Concentrix-Catalyst-1'],['CloudRay Inc', 'N/A', 'Estimated $118K - $150K a year', 'Does not have a source link on CloudRay Inc']]
def launchBrowser():
    path = './chromedriver.exe'
    chrome_options = Options()
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_argument("--allow-running-insecure-content")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36");
    chrome_options.add_argument('start-maximized')
    chrome_options.add_experimental_option('detach',True)
    driver = webdriver.Chrome(path,chrome_options=chrome_options)
    return driver


driver = launchBrowser()
driver = login_to_new_window(driver)
find_if_eligible_company(driver,list_of_valid_companies_Details)