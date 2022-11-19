from selenium.webdriver.common.by import By
from selenium.webdriver.common import keys 
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
import time

def login_details(email,password,driver):

    try:
        getEmail = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//input[@id='o1-input']"))
        )
        getPassword = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//input[@id='current-password']"))
        )

        getLogin = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//button[@class='zp-button zp_1TrB3 zp_3m2tW zp_2z1mP']"))
        )
        getEmail.send_keys(email)
        getPassword.send_keys(password)
        getLogin.click()


    except TimeoutException as ex:
        print(ex.message)



def get_the_right_company(companyName,driver):

    chooseCompany = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH,"//input[@placeholder='Search...']"))
    )
    chooseCompany.send_keys(companyName)

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
        print("Unable to fetch the revenue info")



def login_to_new_window(driver,companyName):
    driver.execute_script("window.open('https://app.apollo.io/#/login','new window')")
    driver.switch_to.window(driver.window_handles[1])
    login_details("thapaanjan40@gmail.com","@asdfqwer1234@",driver)
    get_the_right_company(companyName,driver)
    if (check_if_revenue_matches_criteria(driver) == False):
        driver.switch_to.window(driver.window_handles[0])
        return driver





