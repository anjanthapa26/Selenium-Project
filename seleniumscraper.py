import time
from typing import AnyStr
from fp.fp import FreeProxy
from selenium import webdriver
from selenium.webdriver.common import keys
from selenium.webdriver.common.by import By
from apolloLogins import login_to_new_window
from checkAmbiguity import check_if_authorization
from apolloScraper import find_if_eligible_company
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

proxy = FreeProxy(rand=True).get()
list_of_valid_companies_Details = []
TARGET_URL = 'https://www.indeed.com'


def launch_browser():
    chrome_options = Options()
    # TOGGLE COMMENT FOR headless or !headless
    # chrome_options.add_argument("--headless")
    # path = './chromedriver.exe'
    chrome_options.add_argument('log-level=3')
    # if path:
    #     chrome_options.add_argument(r'user-data-dir=' + path)
    web_driver_params = {
        'options': chrome_options
    }
    chrome_options = Options()
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument('--proxy-server=%s' % proxy)
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_argument("--allow-running-insecure-content")
    chrome_options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/92.0.4515.107 Safari/537.36");
    chrome_options.add_argument('start-maximized')
    chrome_options.add_experimental_option('detach', True)
    return webdriver.Chrome(ChromeDriverManager().install(), **web_driver_params)


driver = launch_browser()
driver.get(TARGET_URL)
driver.find_element(By.XPATH, "//input[@id='text-input-what']").send_keys('Devops Engineers')
driver.find_element(By.XPATH, "//input[@id='text-input-where']").send_keys('Remote')
searchBtn = driver.find_element(by=By.CLASS_NAME, value="yosegi-InlineWhatWhere-primaryButton")
searchBtn.click()

''' Since the source links are quite inconsistent '''


def deal_with_sourceLinks(company, job):
    try:
        source_link = job.find_element(By.XPATH, ".//a[@class='jcs-JobTitle css-jspxzf eu4oa1w0']")
        # source_link = job.find_element(By.XPATH,".//h2[@class='jobTitle css-1h4a4n5 eu4oa1w0']/a")
        return source_link.get_attribute('href')
    except:
        return 'None'


''' Since the payment sources are also inconsistent, handle that scenerios'''


def deal_with_estimated_salary(job: WebElement) -> AnyStr or None:
    try:
        salary_parent = job.find_element(By.CLASS_NAME, value="estimated-salary")
        salary = salary_parent.find_element(By.TAG_NAME, 'span').text
        return salary
    except:
        try:
            hourly_salary = job.find_element(By.CLASS_NAME, value="attribute_snippet")
            return hourly_salary.text
        except:
            print('None')
            return None


''' Deal with the inconsistent company Name '''


def deal_with_company_name(job):
    try:
        # company_name = WebDriverWait(driver, 10).until(
        # EC.presence_of_element_located((By.XPATH,"(//div[@class='jobsearch-InlineCompanyRating-companyHeader'])/a")))
        # company_name = job.find_element(By.CLASS_NAME,"company_name")
        # company_name = job.find_element(By.XPATH, "(.//span[@class='company_name'])")
        company_name = job.find_element(By.XPATH, ".//a[@data-tn-element='companyName']")
        return company_name.text
    except:
        return 'None'


''' Find if the each companies on lists complies with the rules or not '''


def find_if_complies_rules(job: WebElement):
    try:
        driver.execute_script("arguments[0].scrollIntoView(true)", job)
    except Exception:
        print('Error on the execute_script')

    try:
        find_tr = job.find_element(By.CLASS_NAME, 'jobCardShelf')
        actions = ActionChains(driver)
        actions.move_to_element(find_tr)
        actions.click(find_tr)
        actions.perform()
        time.sleep(2)
    except:
        print('Click event not found')

    get_company_name = deal_with_company_name(job)
    print(get_company_name)

    get_source_link = deal_with_sourceLinks(get_company_name, job)
    print(get_source_link)

    get_salary = deal_with_estimated_salary(job)
    print(get_salary)

    if (get_company_name != 'None') and (get_source_link != 'None'):
        find_experience, check_valid = check_if_authorization(driver)
        print(find_experience, check_valid)
        if not check_valid:
            list_of_valid_companies_Details.append([get_company_name, find_experience, get_salary, get_source_link])

        print(list_of_valid_companies_Details)
        print('length of list_of_valid_companies_details', len(list_of_valid_companies_Details))
        # login_to_new_window(driver,get_company_name.text)


def find_list_of_jobs():
    # count = 0
    # go_to_next_page = driver.find_element(By.XPATH,"//a[@aria-label='Next Page']")
    while True:
        # count =0
        try:
            go_to_next_page = driver.find_element(By.XPATH, "//a[@aria-label='Next Page']")

            '''
            job_lists = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//ul[@class='jobsearch-ResultsList css-0']/li")))'''
            # test1 = "//div[@class='slider_container css-g7s71f eu4oa1w0']"
            job_lists = WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'job_seen_beacon'))
            )

            for job in job_lists:
                find_if_complies_rules(job)

            go_to_next_page.click()

            '''
            if count == 1:
                break
                '''
        except:
            break


find_list_of_jobs()

''' just to check for the front side of indeed '''
'''
driver = login_to_new_window(driver)
find_if_eligible_company(driver,list_of_valid_companies_Details)

'''