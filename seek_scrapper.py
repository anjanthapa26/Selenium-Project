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
cases = [["\$\d+K - \$\d+K"],["\$\d+,\d+ - \$\d+,\d+"],["\$\d+.\d+K - \$\d+.\d+K"],["\$\d+.\d+K - \$\d+K"],["\$\d+K - \$\d+.\d+K"],["\$\d+,\d+K - \$\d+,\d+K"]]

class Seek:

    def __init__(self,WHAT,WHERE):
        self.WHAT = WHAT
        self.WHERE = WHERE
        self.driver = self.launch_browser()
        self.url = 'https://www.seek.com.au/'
        self.count = 1

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
        self.driver.find_element(By.ID,'keywords-input').send_keys(self.WHAT)
        self.driver.find_element(By.ID,'SearchBar__Where').send_keys(self.WHERE)
        self.driver.find_element(By.XPATH,"//button[@type='submit']").click()


    def get_job_title(self):
        try:
            job_title = WebDriverWait(self.driver,5).until(
                    EC.presence_of_element_located((By.XPATH, "//h1[@data-automation='job-detail-title']"))).text
            return job_title
        except Exception as e:
            print(e)
            
    def get_company_name(self):
        try:
            company_name =  WebDriverWait(self.driver,5).until(
                    EC.presence_of_element_located((By.XPATH, "//span[@data-automation='advertiser-name']"))).text
            return company_name
        except Exception as e:
            print(e)

    def get_salary(self):
        try:
            salary = WebDriverWait(self.driver,5).until(
                    EC.presence_of_element_located((By.XPATH, "//span[@data-automation='job-detail-work-type']/../following-sibling::div"))).text
            # for case in cases:
            #     get_exact_salary = re.findall(case[0], salary)
            #     if get_exact_salary:
            #         return get_exact_salary[0]
            # if not get_exact_salary:
            #     return salary

            return salary

        except:
            return 'Not Mentioned'

    def find_other_details(self):
        try:
            overall_text_container = WebDriverWait(self.driver,10).until(
                EC.presence_of_element_located((By.XPATH,"//div[@data-automation='jobAdDetails']"))
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

    def find_if_rules_complies(self,job):
        try:
            self.driver.execute_script("arguments[0].scrollIntoView(true)", job)
        except Exception:
            print('Error on the execute_script')
        
        try:
            get_job_visit_element = job.find_element(By.XPATH,".//a[@data-automation='jobTitle']")
        except Exception as e:
            print(e)

        try:
            actions = ActionChains(self.driver)
            actions.move_to_element(get_job_visit_element)
            actions.click(get_job_visit_element)
            actions.perform()
        except:
            print('Click event not found')

        job_title = self.get_job_title()

        company_name = self.get_company_name()

        salary = self.get_salary()

        source_link = self.driver.current_url

        find_experience, get_tech, check_valid = self.find_other_details()

        print(job_title,salary,company_name,source_link,find_experience,get_tech)
        if not check_valid:
            list_of_valid_companies_Details.append([job_title,company_name,find_experience, salary, source_link,get_tech])


    def get_list_of_jobs(self,idx=1):
            jobs_container = WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH,"(//article[@data-automation='normalJob'])["+str(idx)+"]")))
            return jobs_container

    def get_all_list_of_jobs(self):
        initial_job_list = []
        self.get_required_webpage()
        time.sleep(3)
        initial_job_list.append(self.get_list_of_jobs())
        idx = 0
        while idx <= len(initial_job_list):
            self.find_if_rules_complies(initial_job_list[idx])
            self.driver.back()

            try:
                initial_job_list += [self.get_list_of_jobs(len(initial_job_list)+1)]
                idx +=1
            except:
                if len(initial_job_list) == idx + 1:
                    initial_job_list = []
                    idx = 0
                    self.count +=1
                    self.url = "https://www.seek.com.au/{}-jobs/in-{}?page={}".format(self.WHAT,self.WHERE,self.count)
                    self.driver.get(self.url)
                    try:
                        initial_job_list.append(self.get_list_of_jobs(idx+1))
                    except:
                        return self.driver


obj = Seek('Devops','Remote')
driver = obj.get_all_list_of_jobs()
login_to_new_window(driver)
find_if_eligible_company(driver,list_of_valid_companies_Details)

        



