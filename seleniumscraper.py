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

list_of_valid_companies_Details = []
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
    driver.get('http://www.indeed.com')
    return driver





driver = launchBrowser()
whatJobs = driver.find_element(By.XPATH,"//input[@id='text-input-what']").send_keys('Devops Engineers')
whereJobs = driver.find_element(By.XPATH,"//input[@id='text-input-where']").send_keys('Remote')
searchBtn = driver.find_element(by=By.CLASS_NAME, value="yosegi-InlineWhatWhere-primaryButton")
searchBtn.click()




''' Since the source links are quite inconsistent '''

def deal_with_sourceLinks(company,job):
    try:
        sourceLink = job.find_element(By.XPATH,".//a[@class='jcs-JobTitle css-jspxzf eu4oa1w0']")
        #sourceLink = job.find_element(By.XPATH,".//h2[@class='jobTitle css-1h4a4n5 eu4oa1w0']/a")
        getLink = sourceLink.get_attribute('href')
        return getLink
    except:
        return 'None'


''' Since the payment sources are also inconsistent, handle that scenerios'''

def deal_with_estimated_salary(job):
    try:
        salaryParent = job.find_element(By.CLASS_NAME, value="estimated-salary")
        salary = salaryParent.find_element(By.TAG_NAME,'span').text
        return salary
    except:
        try:
            HourlySalary = job.find_element(By.CLASS_NAME, value="attribute_snippet")
            return HourlySalary.text
        except:
            print('None')



''' Deal with the inconsistent company Name '''


def deal_with_companyName(job):
    try:
        #companyName = WebDriverWait(driver, 10).until(
        #EC.presence_of_element_located((By.XPATH,"(//div[@class='jobsearch-InlineCompanyRating-companyHeader'])/a")))
        #companyName = job.find_element(By.CLASS_NAME,"companyName")
        companyName = job.find_element(By.XPATH,"(.//span[@class='companyName'])")
        return companyName.text
    except:
        return 'None'

''' Find if the each companies on lists complies with the rules or not '''

def find_if_complies_rules(job):
    try:
        driver.execute_script("arguments[0].scrollIntoView(true)",job)
    except Exception as e:
        print('Error on the execute_script')

    '''
    actions = ActionChains(driver)
    actions.move_to_element(job)
    actions.click(job)
    actions.perform()
    time.sleep(2)
    '''
    job.click()
    time.sleep()
    gt = job.find_element(By.CLASS_NAME,'resultContent')
    getCompanyName = deal_with_companyName(gt)
    print(getCompanyName)

    getSourceLink = deal_with_sourceLinks(getCompanyName,gt)
    print(getSourceLink)

    getSalary = deal_with_estimated_salary(gt)
    print(getSalary)

    if (getCompanyName != 'None') and (getSourceLink != 'None'):
        findExperience,check_valid = check_if_authorization(driver)
        print(findExperience,check_valid)
        if check_valid == False:
            list_of_valid_companies_Details.append([getCompanyName,findExperience,getSalary,getSourceLink])


        print(list_of_valid_companies_Details)
        print('length of list_of_valid_companies_details',len(list_of_valid_companies_Details))
        #login_to_new_window(driver,getCompanyName.text)

    


def find_list_of_jobs():
    #count = 0
    #go_to_next_page = driver.find_element(By.XPATH,"//a[@aria-label='Next Page']")
    while True:
        try:
            go_to_next_page = driver.find_element(By.XPATH,"//a[@aria-label='Next Page']")

            #count +=1
            '''
            job_lists = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//ul[@class='jobsearch-ResultsList css-0']/li")))'''
            # test1 = "//div[@class='slider_container css-g7s71f eu4oa1w0']"
            job_lists = WebDriverWait(driver,20).until(
                EC.presence_of_all_elements_located((By.XPATH,"(//div[@class='job_seen_beacon'])"))
            )


            for job in job_lists:
                find_if_complies_rules(job)

            go_to_next_page.click()

            '''
            if count == 1:
                break
            go_to_next_page.click()


            '''
        except:
            break


find_list_of_jobs()




''' just to check for the front side of indeed '''

#driver = login_to_new_window(driver)
#find_if_eligible_company(driver,list_of_valid_companies_Details)
