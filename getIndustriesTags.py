from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
import time

'''
contains_one = '//div[contains(text(),"companies")]/../following-sibling::div'
follow_siblings = '//div[contains(text(),"companies")]/../../following-sibling::div'

'''
'''
def get_the_right_company(companyName,driver):

    chooseCompany = WebDriverWait(driver, 40).until(
            EC.presence_of_element_located((By.XPATH,"//input[@placeholder='Search...']"))
    )

    chooseCompany.send_keys(companyName)
    try:
        getRightCompany = WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH,"//*[contains(text(),'"+companyName+"')]/..//div[contains(text(),'Information technology & services')]/../../../..")))
        #getRightCompany = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,"//*[[contains(text(),f'{companyName}')] and [contains(text(),'Information technology & services')]]")))
        getRightCompany.click()
    except Exception as e:
        driver.refresh()
        print('Could not get the rightcompany information',e)


'''


''' Get the lists of tags available for the input values that is being passed '''

def get_the_list_of_tags(companyName,driver):

    
    filter_industries = ['airlines/aviation','aviation & aerospace','banking','defense & space','government administration','government relations','higher education','law enforcement','law practice','legal services','legislative office','military','oil & energy']

    lists_of_companies_with_tags = []
    chooseCompany = WebDriverWait(driver, 40).until(
            EC.presence_of_element_located((By.XPATH,"//input[@placeholder='Search...']"))
    )
    chooseCompany.send_keys(companyName)
    time.sleep(5)

    try:
        get_parent_container = WebDriverWait(driver, 40).until(
            EC.presence_of_element_located((By.XPATH,"//div[@class='apolloio-css-vars-reset zp-overlay']")))
    except:
        print('unable to get parent container')
    
    get_first_company_parent = get_parent_container.find_element(By.XPATH,"//div[contains(text(),'companies')]/../following-sibling::div/div[2]/div")
    print(get_first_company_parent.text)
    get_company = get_first_company_parent.text.splitlines()[0]
    get_industry_tag = get_first_company_parent.text.splitlines()[2]

    if get_industry_tag not in filter_industries:
        lists_of_companies_with_tags.append([get_company,get_industry_tag])
        
        #print(get_company,get_industry_tag)

    ''' Getting the group of lists of elements to tally '''

    get_parent_of_sibling_companies = get_parent_container.find_elements(By.XPATH,"//div[contains(text(),'companies')]/../../following-sibling::div/div/div[2]/div")

    for sibling_parents in get_parent_of_sibling_companies:
        get_comp = sibling_parents.text
        print(get_comp.splitlines())
        get_sibling_company = sibling_parents.text.splitlines()[0]
        try:
            get_sibling_industry_tag = sibling_parents.text.splitlines()[2]
        except IndexError:
            continue
        if get_sibling_industry_tag not in filter_industries:
            lists_of_companies_with_tags.append([get_sibling_company,get_sibling_industry_tag])
            
            print(get_sibling_company,get_sibling_industry_tag)

    return lists_of_companies_with_tags
