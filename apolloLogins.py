from selenium.webdriver.common.by import By
from selenium.webdriver.common import keys 
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
import time


def login_details(email,password,driver):

    try:
        getEmail = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//input[@id='o1-input']"))
        )
        getPassword = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//input[@id='current-password']"))
        )

        getLogin = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//button[@class='zp-button zp_1TrB3 zp_3m2tW zp_2z1mP']"))
        )
        getEmail.send_keys(email)
        getPassword.send_keys(password)
        getLogin.click()


    except TimeoutException as ex:
        print(ex.message)


def login_to_new_window(driver):

    driver.get('https://app.apollo.io/#/login')

    ''' applying the demo for the apolloscraper'''
    '''
    driver.execute_script("window.open('https://app.apollo.io/#/login','new window')")
    driver.switch_to.window(driver.window_handles[1])
    '''
    login_details("thapaanjan40@gmail.com","@asdfqwer1234@",driver)
    return driver
