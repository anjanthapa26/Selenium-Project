# This file contains all the functionality that checks if the condition is meet or not 
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

def check_if_authorization(driver):

    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME,"jobsearch-JobComponent-description"))
        )
        print(element.text)
    except TimeoutException as ex:
        print(ex.message)

    return True

    