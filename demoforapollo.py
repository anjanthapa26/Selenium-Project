from selenium import webdriver
from selenium.webdriver.common import keys 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from checkAmbiguity import check_if_authorization
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from apolloLogins import login_to_new_window
from apolloScraper import find_if_eligible_company


list_of_valid_companies_Details = [['DevOps Engineer III', 'RELI Group, Inc.', '7 years', 'Full-time', 'https://www.indeed.com/rc/clk?jk=a4bae8a95f641804&fccid=380ad6d2bbbee773&vjs=3', 'Python AWS Azure Jenkins Docker Kubernetes Terraform', 'DevOps Engineer III']]
#list_of_valid_companies_Details = [ ['nClouds', '5 years', '$124K - $157K', 'https://www.indeed.com/rc/clk?jk=c45674b9f68a5d3c&fccid=c76149658a7e6a8d&vjs=3', 'AWS Terraform Kubernetes Ansible Puppet Docker Python Jenkins']]
#list_of_valid_companies_Details = [['Zignal Labs', '5 years', '$125K - $158K', 'https://www.indeed.com/rc/clk?jk=88e355409be88594&fccid=bcd185c836572b52&vjs=3', 'AWS Python Kubernetes'], ['NCube', '2 years', '$82.2K - $104K', 'https://www.indeed.com/rc/clk?jk=35ae9d3184d95f81&fccid=468ec7cc9189b378&vjs=3', 'Docker Kubernetes Terraform AWS Ansible'], ['eXp Realty', '5 years', 'Full-time', 'https://www.indeed.com/rc/clk?jk=753115185f2472b5&fccid=4492415ca5d0212e&vjs=3', 'AWS Python Docker Jenkins'], ['Compassion', 'N/A', '$96,730 - $120,910', 'https://www.indeed.com/rc/clk?jk=b3e2774ef36edab6&fccid=53ad9d0165a8fe49&vjs=3', ''], ['MD Ally Technologies, Inc.', '5 years', '$131K - $166K', 'https://www.indeed.com/rc/clk?jk=56a942271c3a5127&fccid=4ed9b44044763074&vjs=3', 'AWS Azure Docker Terraform Python'], ['Proofpoint', 'N/A', '$112K - $142K', 'https://www.indeed.com/rc/clk?jk=d436498637778fa0&fccid=69c7d55b78dc7424&vjs=3', 'Terraform Docker Kubernetes AWS Jenkins Python'], ['Zoom Video Communications, Inc.', '2 years', '$89.5K - $113K', 'https://www.indeed.com/rc/clk?jk=17b5fcc6c8a79ccb&fccid=e32d933c26e873c8&vjs=3', 'AWS Docker Terraform Kubernetes Ansible Jenkins'], ['Stellantis', 'N/A', '$90.7K - $115K', 'https://www.indeed.com/rc/clk?jk=a91cc11bdc3f3c22&fccid=f6172562f9aeed68&vjs=3', ''], ["Moody's", '1 years', '$79.8K - $101K', 'https://www.indeed.com/rc/clk?jk=aaae0ecb627d5e8c&fccid=28eefc5b86560831&vjs=3', 'AWS Azure Python'], ['Ardan Labs', 'N/A', '$101K - $128K', 'https://www.indeed.com/rc/clk?jk=c41f290e6e17ca97&fccid=34508cd7f02c1bbb&vjs=3', 'AWS Docker Terraform'], ['Nelnet', '40 years', '$120,000 - $130,000', 'https://www.indeed.com/rc/clk?jk=c256393e1981f1c4&fccid=d492310e78d122ff&vjs=3', 'AWS Azure Kubernetes Python'], ['IQVIA', '3 years', '$90.1K - $114K', 'https://www.indeed.com/rc/clk?jk=7e9b1da30f1e9857&fccid=6b7a1dfe07e7f037&vjs=3', 'Docker Terraform AWS'], ['nClouds', '5 years', '$124K - $157K', 'https://www.indeed.com/rc/clk?jk=c45674b9f68a5d3c&fccid=c76149658a7e6a8d&vjs=3', 'AWS Terraform Kubernetes Ansible Puppet Docker Python Jenkins']]
#list_of_valid_companies_Details = [['sesamy', '5 years', '$125K - $158K', 'https://www.indeed.com/rc/clk?jk=88e355409be88594&fccid=bcd185c836572b52&vjs=3']]
def launchBrowser():
    path = './chromedriver.exe'
    chrome_options = Options()
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_argument("--allow-running-insecure-content")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36");
    chrome_options.add_argument('start-maximized')
    chrome_options.add_experimental_option('detach',True)
    driver = webdriver.Chrome(path,chrome_options=chrome_options)
    return driver


driver = launchBrowser()
driver = login_to_new_window(driver)
find_if_eligible_company(driver,list_of_valid_companies_Details)
#driver.close()