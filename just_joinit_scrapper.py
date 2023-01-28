import re
import time
from typing import AnyStr
from fp.fp import FreeProxy
from selenium import webdriver
from langdetect import detect
from googletrans import Translator
from selenium.webdriver.common.by import By
from apolloLogins import login_to_new_window
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from apolloScraper import find_if_eligible_company


list_of_valid_companies_Details = []
prox = FreeProxy(rand=True).get()

class JustJoinItScrapper:

    def __init__(self,WHAT,WHERE):
        self.__WHAT = WHAT
        self.__WHERE = WHERE
        self.URL = 'https://justjoin.it/'
        self.proxy = FreeProxy(rand=True).get()
        self.driver = self.launch_browser()
        self.scroll_value = 0
        self.initial_job_list_titles = []
        self.idx = 0

    @staticmethod
    def launch_browser():
        chrome_options = Options()
        chrome_options.add_argument('log-level=3')
        web_driver_params = {
            'options': chrome_options
        }
        chrome_options = Options()
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument('--proxy-server=%s' % prox)
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        chrome_options.add_argument("--allow-running-insecure-content")
        chrome_options.add_argument(
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/92.0.4515.107 Safari/537.36");
        chrome_options.add_argument('start-maximized')
        chrome_options.add_experimental_option('detach', True)
        return webdriver.Chrome(ChromeDriverManager().install(), **web_driver_params)

    def get_required_webpage(self):
        self.driver.maximize_window()
        self.driver.get(self.URL)
        self.driver.find_element(By.XPATH,"//input[@placeholder='Search']").click()
        input_field = self.driver.find_element(By.XPATH,"//input[@placeholder='Skill, location, company']")
        for value in [self.__WHAT,self.__WHERE]:
            input_field.send_keys(value)
            time.sleep(2)
            input_field.send_keys(Keys.RETURN)

    def get_job_title(self):
        try:
            job_title = WebDriverWait(self.driver,5).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[@class='css-1id4k1']"))).text
            return job_title
        except Exception as e:
            print(e)
            

    def get_salary(self):
        try:
            salary =  WebDriverWait(self.driver,5).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[@class='css-1wla3xl'][1]/span[1]"))).text
            return salary
        except:
            print('Could not get salary')

    def get_company_name(self):
        try:
            company_name =  WebDriverWait(self.driver,5).until(
                    EC.element_to_be_clickable((By.XPATH, "(//div[@class='css-1uvpahd'])[1]/a"))).text
            return company_name
        except:
            print('Could not get company name')


    def get_tech_stack(self):
        tech_stacks_lists = []
        try:
            tech_stacks_container = WebDriverWait(self.driver,5).until(
                    EC.presence_of_all_elements_located((By.XPATH, "//div[@class='css-1ikoimk']/div")))
            for tech_stack in tech_stacks_container:
                text = tech_stack.text
                tech_stacks_lists.append(text.split("\n")[0])
        except Exception as e:
            print(e)

        return ' '.join(tech_stacks_lists)

    def get_maximum_years_and_job_validity(self):

        try:
            overall_text_container = WebDriverWait(self.driver,10).until(
                EC.presence_of_element_located((By.XPATH,"//div[@class='css-p1hlmi']"))
            )
        except Exception as e:
            print(e)

        container_text = overall_text_container.text
        
        try:
            if detect(container_text) != 'en':
                translator = Translator()
                container_text = translator.translate(container_text).text
        except:
            print('Could not detect langauge')

        with open('demofile.txt', "w", encoding="utf-8") as f:
            f.write(container_text)

        def readFile(fileName):
            getInfo = []
            getExperience = []

            fileObj = open(fileName,'r',encoding="utf-8")
            words = fileObj.read().splitlines()

            for word in words:
                if re.findall('\d+ years',word):
                    getExperience.append(re.findall('\d+ years',word)[0])
                if re.findall('\d+ year',word):
                    getExperience.append(re.findall('\d+ year',word)[0])
                if re.findall('\d\+ years',word):
                    getExperience.append(re.findall('\d\+ years',word)[0])

            if len(getExperience) > 0:
                final_list_of_years = max(list(map(int,re.findall('\d+',' '.join(getExperience)))))
                getInfo.append(f'{final_list_of_years}'+' years')
            else:
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

    def find_if_rules_complies(self,job_title):
        job_name = job_title[0]
        count = 0
        while count <= 2:
            try:
                find_correct_div = self.driver.find_element(By.XPATH,"//*[contains(text(),'"+job_name+"')]/../../..//div[contains(text(),'"+job_title[1]+"')]/../../../div[1]")
                break
                # find_job_title_div =self.driver.find_element(By.XPATH,"//*[contains(text(),'"+job_title+"')]")
                # self.driver.execute_script("arguments[0].scrollIntoView(true)", find_job_title_div)
            except:
                count +=1
                print('Unable to find the intial div container segregating to string length',len(job_name)//2)
                job_name = job_name[:len(job_name)//2]

        try:
            actions = ActionChains(self.driver)
            actions.move_to_element(find_correct_div)
            actions.click(find_correct_div)
            actions.perform()
        except:
            print('Click event not found')

        job_title = self.get_job_title()

        company = self.get_company_name()

        salary = self.get_salary()

        source_link = self.driver.current_url

        tech_stacks = self.get_tech_stack()

        max_years,rules_complied = self.get_maximum_years_and_job_validity()

        if not rules_complied:
            list_of_valid_companies_Details.append([job_title,company,max_years,salary,source_link,tech_stacks])

        print(job_title,company,max_years,salary,source_link,tech_stacks)

        try:
            return_driver_to_pp = self.driver.find_element(By.XPATH,"(//div[@class='css-vuh3mm'])[1]/div/button[1]")
            return_driver_to_pp.click()

        except Exception as e:
            print(e)

        find_job_container =self.driver.find_element(By.XPATH,"//div[@class='css-ic7v2w']")
        self.driver.execute_script("arguments[0].scrollTop = '"+str(self.scroll_value)+"';", find_job_container)

        


    def get_list_of_jobs(self):
        job_title_container = []
        list_of_jobs = WebDriverWait(self.driver,10).until(EC.presence_of_all_elements_located((By.XPATH,"//div[@class='css-ic7v2w']/div/div")))
        for job_title in list_of_jobs:
            try:
                job_title_container.append([job_title.find_element(By.XPATH,".//div/div/div[2]/div[1]/div[1]").text,job_title.find_element(By.XPATH,".//div/div/div[2]/div[2]/div[2]/div[1]").text])
            except:
                print('unable to get the attached element after',self.idx,len(self.initial_job_list_titles))

        return job_title_container

    def update_list_of_jobs(self):
        self.get_required_webpage()
        time.sleep(5)
        initial_job_list_titles = self.get_list_of_jobs()
        print(initial_job_list_titles)
        for idx,job_title in enumerate(initial_job_list_titles):
            self.idx = idx
            self.scroll_value += 90
            self.find_if_rules_complies(job_title)
            
            if len(initial_job_list_titles) == idx + 1:
                latest_available_jobs = self.get_list_of_jobs()
                for updated_jobs in latest_available_jobs:
                    if updated_jobs not in initial_job_list_titles:
                        initial_job_list_titles += [updated_jobs]
        return self.driver

        


obj = JustJoinItScrapper('Devops','Remote')
driver = obj.update_list_of_jobs()
login_to_new_window(driver)
find_if_eligible_company(driver,list_of_valid_companies_Details)
