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
            get_tech_stack = []
            tech_stacks = ['AWS', 'Azure', 'Ansible', 'Python', 'Docker', 'Kubernetes', 'Terraform',  'Jenkins',  'Puppet']
            fileObj = open(fileName,'r')
            words = fileObj.read().splitlines()

            for word in words:
                if re.findall('\d+ years',word):
                    getExperience.append(re.findall('\d+ years',word)[0])
                if re.findall('\d+ year',word):
                    getExperience.append(re.findall('\d+ year',word)[0])
                if re.findall('\d\+ years',word):
                    getExperience.append(re.findall('\d\+ years',word)[0])

                for each_char in tech_stacks:
                    if each_char in word and each_char not in get_tech_stack:
                        get_tech_stack.append(each_char)


            if len(getExperience) > 0:
                final_list_of_years = max(list(map(int,re.findall('\d+',' '.join(getExperience)))))
                getInfo.append(final_list_of_years)
            else:
                getInfo.append('N/A')

            getInfo.append(' '.join(get_tech_stack))
            
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

    