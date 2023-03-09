import re
import time
from fp.fp import FreeProxy
from selenium import webdriver
from selenium.webdriver.common.by import By
from apolloLogins import login_to_new_window
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from apolloScraper import find_if_eligible_company

list_of_valid_companies_Details = []
prox = FreeProxy(rand=True).get()

class Monster:

    def __init__(self,WHAT,WHERE):
        self.WHAT = WHAT
        self.WHERE = WHERE
        self.driver = self.launch_browser()
        self.url = 'https://www.monster.com/'
        self.idx = 0

    def launch_browser(self):
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
        self.driver.get(self.url)
        self.driver.find_element(By.ID,'horizontal-input-one-undefined').send_keys(self.WHAT)
        self.driver.find_element(By.ID,'horizontal-input-two-undefined').send_keys(self.WHERE)
        self.driver.find_element(By.CSS_SELECTOR,"button[aria-label='Search']").click()


    def get_source_link(self,com_name):
        try:
            source_link = WebDriverWait(self.driver,5).until(
                    EC.element_to_be_clickable((By.XPATH, "//h2[contains(@aria-label,'"+com_name+"')]/..")))
            
            return source_link.get_attribute('href')
        except:
            return 'None'
        

    def find_other_details(self):
        try:
            overall_text_container = WebDriverWait(self.driver,10).until(
                EC.presence_of_element_located((By.XPATH,"//h2[contains(text(),'Description')]/.."))
            )
        except Exception as e:
            return e

        with open('demofile.txt', "w", encoding="utf-8") as f:
            f.write(overall_text_container.text)


        def readFile(fileName):
            getInfo = []
            getExperience = []
            get_tech_stack = []
            tech_stacks = ['AWS', 'Azure', 'Ansible', 'Python', 'Docker', 'Kubernetes', 'Terraform',  'Jenkins',  'Puppet']
            fileObj = open(fileName,'r',encoding="utf-8")
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
                getInfo.append(f'{final_list_of_years}'+' years')
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


    def find_if_rules_complies(self,job_title):

        try:
            find_correct_article = self.driver.find_element(By.XPATH,"//a[contains(text(),'"+job_title[0]+"')]/following-sibling::h3[contains(text(),'"+job_title[1]+"')]/../..")
        except:
            print('unable to find correct article container')


        try:
            self.driver.execute_script("arguments[0].scrollIntoView(true)", find_correct_article)
        except Exception:
            print('Error on the execute_script')

        try:
            actions = ActionChains(self.driver)
            actions.move_to_element(find_correct_article)
            actions.click(find_correct_article)
            actions.perform()
        except:
            print('Click event not found')

        job_name = job_title[0]

        company_name = job_title[1]

        salary = None

        source_link = self.get_source_link(job_title[1])

        find_experience, get_tech, check_valid = self.find_other_details()

        print(job_name,salary,company_name,source_link,find_experience,get_tech)
        if not check_valid:
            list_of_valid_companies_Details.append([job_name, company_name, find_experience, salary, source_link,get_tech])
        


    def get_list_of_jobs(self):
        job_title_container = []
        list_of_jobs = WebDriverWait(self.driver,10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,"article[data-testid='svx_jobCard']")))
        for job_title in list_of_jobs:
            try:
                job_title_container.append([job_title.find_element(By.CSS_SELECTOR,"a[data-test-id='svx-job-title']").text,job_title.find_element(By.CSS_SELECTOR,"h3[data-testid='svx_jobCard-company']").text])
            except:
                print('unable to get the attached element after',self.idx,len(self.initial_job_list_titles))

        return job_title_container

    def update_list_of_jobs(self):
        self.get_required_webpage()

        initial_job_list_titles = self.get_list_of_jobs()
        print(initial_job_list_titles)

        for idx,job_title in enumerate(initial_job_list_titles):
            self.idx = idx
            try:
                 self.find_if_rules_complies(job_title)
            except:
                print('exception')

            if len(initial_job_list_titles) == idx + 1:
                latest_available_jobs = self.get_list_of_jobs()[self.idx + 1:]
                for updated_jobs in latest_available_jobs:
                        initial_job_list_titles += [updated_jobs]
        return self.driver

obj = Monster('devops','remote')
driver = obj.update_list_of_jobs()
login_to_new_window(driver)
find_if_eligible_company(driver,list_of_valid_companies_Details)