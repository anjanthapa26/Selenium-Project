from selenium.webdriver.common.by import By
from selenium.webdriver.common import keys 
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
import time


def get_the_right_company(companyName,driver):

    chooseCompany = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH,"//input[@placeholder='Search...']"))
    )

    try:
        getRightCompany = WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH,"//*[contains(text(),'"+companyName+"')]/..//div[contains(text(),'Information technology & services')]/../../../..")))
        #getRightCompany = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,"//*[[contains(text(),f'{companyName}')] and [contains(text(),'Information technology & services')]]")))
        getRightCompany.click()
    except Exception as e:
        print('Could not get the rightcompany information',e)


def check_if_revenue_matches_criteria(driver):
    try:
        checkRevenue = WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH,"//*[contains(text(),'Annual Revenue')]/../div[2]"))).text
        if checkRevenue[-1] == 'B' or (checkRevenue[-1] == 'M' and int(checkRevenue[0:len(checkRevenue)-1]) > 50):
            print('entered false')
            return False
        else:
            return True

    except Exception as e:
        return True



def find_if_eligible_company(driver,list_of_companiesDetails):

    for com_details in list_of_companiesDetails:

        # should fix this issue of not getting the company name 

        if com_details[0] != 'No company name available':

            get_the_right_company(com_details[0],driver)
            
            if (check_if_revenue_matches_criteria(driver) == False):
                return driver





