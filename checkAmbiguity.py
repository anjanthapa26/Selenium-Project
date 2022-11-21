# This file contains all the functionality that checks if the condition is meet or not 
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import re

def check_if_authorization(driver):

    try:
        element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME,"jobsearch-JobComponent-description"))
        )

        f = open('demofile.txt','w')
        f.write(element.text)

        # check if there is persence of given datas available
        def readFile(fileName):
            getInfo = []
            getExperience = []
            fileObj = open(fileName,'r')
            words = fileObj.read().splitlines()

            for i in words:
                if re.findall('\d+ years',i):
                    getExperience.append(re.findall('\d+ years',i)[0])
                    getInfo.append(getExperience[0])
                    break
                elif re.findall('\d+ year',i):
                    getExperience.append(re.findall('\d+ year',i)[0])
                    getInfo.append(getExperience[0])
                    break

            if len(getExperience) < 1:
                getInfo.append('N/A')

            for word in words:
                if word.find('U.S') != -1 or word.find('U.S work permit') != -1 or word.find('USA') != -1 or word.find('U.S permit') != -1:
                    getInfo.append(True)
                    return getInfo


            getInfo.append(False)
            fileObj.close()

            return getInfo


        f.close()
        return readFile('demofile.txt')



    except TimeoutException as ex:
        print('Entered into an exception')

    