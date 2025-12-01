'''
Automation.py files contains the automation part of the program. This program, first takes the input from config.py
made using initializer.py.
Since there are multiple courses and module, the module code from the professor is asked to ensure the correct marking
of attendance.
Described following is the flow of the code:
1. Login credentials gets fetched from config.py
2. study.gisma.com is then opened through selenium
3. Login credentials are then entered in their respective placeholders and then it proceeds to login.
4. Page is then scrolled until the code of the module is found.
5. It then enters into that particular module. (Since I'm, working according to student portal of the website, 
It navigates to 'people' section of the website, there exists list of the people involved in the module in any manner.)
6. It then applies sorting filter for students'
7. Names of all the students is then fetched to a file named 'students.txt'
8. Currently, the program ends here but fill further be modified as of faculty factor to properly navigate and mark attendance
for each student.
'''

#json helps to read data from exisitng config.json file.
import json
#BeautifulSoup here is used to scrap the name of students in the module
from bs4 import BeautifulSoup as bsp
#Selenium is then imported to automate the web interaction.
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait as wbwait
from selenium.webdriver.support import expected_conditions as ec
from time import sleep
#system module is imported to use sys.exit() when the program needs to be terminated.
import sys
#To make the code prettier and make the output in the terminal colorful
from colorama import Fore as color

def startup():
    '''
    This startup() intializes all the necessary block of code for execution of selenium script.
    without this function other functions will crash and will definitely not give an output.
    '''
    global driver,wait,url
    '''Options makes selenium's browser control more flexible and user-defined.'''
    options = Options()
    '''Using Following line of code, user will not see the automation happening live on their screen.'''
    options.add_argument("--headless=new") #This line allows headless webscrapping/interaction using selenium
    
    # Browser driver is then set to establish an agent to interact with web on user's behalf  
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=options)

    #wait containts the implicit wait time for any element to load and appear before throwing any error.
    wait = wbwait(driver,15)

    #url contains the url of the website.
    url = 'https://study.gisma.com'

    driver.get(url)
    driver.maximize_window()

def login_data():
    '''
    login_data fetches login credentials from config.py and stores them in eid and pwd variable respectively
    '''
    with open('config.json') as configuration:
        data = json.load(configuration)
        eid = data["id"]
        pwd = data["password"]
    print(color.GREEN+"Login Details Fetched Successfully.")
    return eid,pwd
  

def login(eid,pwd):
    '''
    login() naviagtes to input field for id and password in study.gisma.com's login page, then selenium enters the login
    credentials at their respective place and then hit login button to enter the website. 
    '''
    #login_id navigates to login input field on the website
    login_id = wait.until(
        ec.visibility_of_element_located(
        (By.XPATH, '//*[@id="pseudonym_session_unique_id"]')))
    login_id.send_keys(eid)

    #It stops the program for some time to reduce error margin
    sleep(2)
    
    #login_pwd navigates to password input field on the website  
    login_pwd = wait.until(
        ec.visibility_of_element_located(
        (By.XPATH, '//*[@id="pseudonym_session_password"]')))
    login_pwd.send_keys(pwd)
    
    #Just a log to let user know, at what stage we are if he is running script in headless mode.  
    print(color.GREEN + "Login Credentials entered successfully")
    
    #login tries to click the login button on the website, Further error hunting is done in main()
    login = wait.until(
        ec.element_to_be_clickable(
        (By.XPATH, '//*[@id="login_form"]/div[3]/div[2]/button')))
    login.click()
    sleep(2)
            
def login_verification():
    '''
    login_verification checks if the login was successfull or not by checking for an element which is only available after login.
    In this case it has been programmed to check for image's placeholder which is visible once user has been successfully loggedin
    to the account. If not, it raises an error.
    '''
    try:
        driver.find_element(By.XPATH, '//*[@id="global_nav_profile_link"]/div[1]/div/img')
        print(color.GREEN + "Logged In Successfully")
        return True
    except:
        print(color.RED + "There was error logging into your account, please check the credentials once.")
        return False


def navigate_module(module_code):
    '''
    navigate_module() tries to find the module of which the code is entered.
    This function runs in loop to ensure scrolling until the module is found.
    If the module is found, the hyperlink is clicked otherwise, scrolling is continued.
    '''
    found = False
    loop_run = 0
    while True:
        try:
            #module_path makes the XPATH of module by taking module_code as input from the user.
            module_path = f"//*[contains(@title, '{module_code}')]"
            module = driver.find_element(By.XPATH,module_path)
            '''Following line of code is used to scrolling until "module" is found the webpage.'''
            driver.execute_script("arguments[0].scrollIntoView({behavior:'smooth', block:'center'});",module)
            module.click()
            found = True
            '''If the module us found, the loops breaks out after clicking the module's hyperlink.'''
            break
        except:
            '''Otherwise it continues to scroll in vertical direction by 300px'''
            driver.execute_script("window.scrollBy(0, 300)")
            sleep(1)
            loop_run+=1
            found = False
            if loop_run > 15:
                print(color.RED + "Could not find the module, please check the module code once and try again")
                break
            
    return found
            
            
def navigating_student():
    '''This function is supposed to be replaced by "attendance" hyperlink location/XPATH to navigate to the 
    attendance tool of that particular module.
    For now, this function navigates to "people" section of module which contains the list of all the people
    who are included in the module(including staff memebers.)
    It then filters out the student by applying the 'student' filter.
    '''
    #attendance_link stores data to navigate people section.
    attendance_link = wait.until(
        ec.visibility_of_element_located(
        (By.CLASS_NAME, 'people')))
    attendance_link.click()
    
    #student_filter stores data to sort students
    student_filter = driver.find_element(By.XPATH, '//*[@id="tab-0"]/select/option[2]')
    student_filter.click()
    return True
    

def data_extraction(file_name):
    '''
    data_extraction() reterieves the total list of students from the attendance portal of the module
    Since, study.gisma.com follows dynamic website layout, it needs to be scrolled down to bottom
    to retrieve complete data (list of students) from the website.
    '''
    driver.execute_script("window.scrollTo(0, window.scrollY + 10600)")
    sleep(2)
    
    # pgsrc contains the raw text/html format of the dynamic page
    pgsrc = driver.page_source
    
    #page soure data is then parsed using python inbuilt parser
    parsed = bsp(pgsrc,"html.parser")
    
    #names contains the list of names extracted from parsed data using class name
    names = parsed.find_all('a', class_="roster_user_name")
    
    name = [st_names.text for st_names in names]
    '''Follwoing line of code prints the reterived data to file named "student.txt"'''
    with open(file_name,'w') as data_file:
        for student_name in name:
            data_file.write(student_name)
        print(color.GREEN + "Student Data retrieved Successfully!")
    
    
def main():
    '''
    main() carries multiple try and except block to ensure error handeling at its best and rightfull termination
    of program instead of crashing program.
    '''
    '''module_code stores the code of the module to navigate it using selenium'''
    
    startup()
    try:
        '''This try-except block is nested with other try-except blocks to ensure error handeling at
        execution of every funciton.'''

        try:
            navigating_student()
            sleep(5)
            print(color.GREEN + "")
        except:
            print(color.RED + "Could not filter out students from the people's list")
        data_extraction()
        sleep(10)
        driver.quit()
        print("Everything was according to plan")
    except:
        sleep(2)
        print("Please Re-run the program.")
        
        
if __name__ == '__main__':
    pass