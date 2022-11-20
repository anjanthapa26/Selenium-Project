from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
import time
from openpyxl import Workbook
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter
from excelsheet import get_the_header_section,extract_info_to_excel_sheet


list_of_headers = ['Company','Designation','Responsible Person','Emails','Tech stack','Experience','Salary','Source Link']
dest_filename = 'testsheet.xlsx'
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



'''Get the emails of the respective rows '''

def get_the_emails(driver,elem):
    email_tab = elem.find_elements(By.TAG_NAME,'button')
    email_tab[0].click()
    print('passed')
    time.sleep(4)
    try:
        email_container = WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH,"//div[@class='zp_9Igty']")))
        print(email_container)
        return email_container.text

    except:
        print("There is a problem in finding the email container")



''' Methods to get a different tbodies '''

def get_different_tbodies(driver,get_rows):

    try:
        table_rows_datas = get_rows.find_elements(By.XPATH,'//tr/td')
    except:
        print('no table_rows_datas')
    try:
        responsible_person = table_rows_datas[0].find_element(By.CLASS_NAME,value="zp_EqOJn")
        print(responsible_person.text)

    except:
        print('no responsible_person')

    try:
        Designation = table_rows_datas[1].text
        print(Designation)
    except:
        print('No designation')

    try:
        email = get_the_emails(driver,table_rows_datas[2])
    except:
        print('No email')

    return [Designation,responsible_person.text,email]

''' Get the items such as Name, designation and emails of the respective company'''

def get_the_precise_details_of_company(driver):
    counter = 1
    companies_precise_details = []
    try:
        get_tables =  WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH,"//tbody")))

        for get_rows in get_tables:
            if counter <= 3:
                companies_info = get_different_tbodies(driver,get_rows)
                companies_precise_details.append(companies_info)
            counter +=1
        return companies_precise_details
        

    except Exception as e:
        return e


''' Dynamic ways to find the list of people'''

def get_people_somehow(driver):
    plist = ['People','Employees']

    for people in plist:
        print(people)
        try:
            g_people = driver.find_element(By.XPATH,"//a[normalize-space()='"+people+"']")
            return g_people
        except:
            continue
        time.sleep(2)



''' Get the further details of a company once the company if verifeid ''' 
def get_details_of_company(driver):
    static_requirement_of_client = ['CTO','Talent acquisition','CFO','CRO']

    get_people = get_people_somehow(driver)
    get_people.click()

    ''' open the filter tab '''
    try:
        get_filter = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH,"//*[contains(text(),'Open Filters')]/.."))
        )
        get_filter.click()
    except:
        print('Could not get the Open filters')


    ''' click on the job title and enter the criterias for the jobs post on the search bar '''

    try:
        get_job = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH,"//*[contains(text(),'Job Titles')]/../.."))
        )
        get_job.click()
        time.sleep(2)
        try:
            get_input_select = driver.find_element(By.XPATH,"//div[contains(text(),'Search for a job title')]/../input")

        except:
            print('unable to get the Search for a job title')
        
        for job_titles in static_requirement_of_client:
            get_input_select.send_keys(job_titles)
            time.sleep(2)
            get_input_select.send_keys(Keys.RETURN)

        time.sleep(2)
        apply_filter = driver.find_element(By.XPATH,"//*[contains(text(),'Apply Filters')]/..")
        apply_filter.click()
        time.sleep(4)
        return get_the_precise_details_of_company(driver)

    except:
        print('found some error on job title section')

    '''Get the items such as name , designation and emails from the respective company '''


    
def check_if_revenue_matches_criteria(driver):
    try:
        checkRevenue = WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH,"//*[contains(text(),'Annual Revenue')]/../div[2]"))).text
        print(checkRevenue)
        if checkRevenue[-1] == 'B' or (checkRevenue[-1] == 'M' and int(checkRevenue[1:len(checkRevenue)-1]) > 50):
            return False
        else:
            return True

    except Exception as e:
        return True



def find_if_eligible_company(driver,list_of_companiesDetails):

    wb,ws = get_the_header_section(list_of_headers)
    for com_details in list_of_companiesDetails:

        # should fix this issue of not getting the company name 

        if com_details[0] != 'No company name available':

            get_the_right_company(com_details[0],driver)
            if check_if_revenue_matches_criteria(driver) == True:
                three_details_of_company = get_details_of_company(driver)
                print(three_details_of_company)
                if len(three_details_of_company) > 0:
                    ws = extract_info_to_excel_sheet(ws,three_details_of_company,com_details)

        break

    wb.save(filename = dest_filename)











