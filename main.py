'''
main.py is the combined file which uses all the other modules to create a complete automated 
attendance marking system.
It first checks for the existence of config.json to retrieve login credentials from it using 
automation.login_data().
Then it calls automation.startup() to awaken all the necessary utilities required by 
selenium to execute browser automation.
Then it calls automation.login() to navigate to and enter data into website's login input feilds.
After that it calls automation.login_verification() to verfies if login happened or not by checking a 
random element which would only be available if login was successfull.
If login is successfull, it asks for module code input from user and calls automation.navigate_module() 
to navigate to that module.
Then it calls automation.navigating_student() to navigate to the students list of that module.
After that it calls automation.data_extraction() to extract the students data and save it into a csv file.
If at any point there is an error, it prints appropriate error message to the user.
If config.json does not exist, it asks the user if they want to use initializer.py to create it.
If user agrees, it calls initializer.main() to create config.json.  
'''

#import os module to check for existence of config.json
import os
#import color module from colorama for colored terminal outputs
from colorama import Fore as color
#import initializer module to create config.json if it does not exist and retrieve login credentials from it
import initializer
#import automation module to perform all the browser automation tasks
import automation
#import pyinputplus module to take validated inputs from user.
import pyinputplus as pyin


try:
    '''
    The first and formost thing in the program is to check whether config.json exists to reterieve login
    credentials from it.
    '''
    if os.path.exists('config.json'):
        #executed if config.json exists otherwise, sent to else block for creation of config.json
        eid,pwd = automation.login_data()
        try:
            #automation.startup() only needs to be called once in whole program
            automation.startup() #startup() awkens all the necessary utilities required by selenium to execute browser automation
            automation.login(eid,pwd) #login() navigates to and enter data into website's login input feilds (refer to automation.py)
            #login_verification() verfies if login happened or not by checking a random element which would only be available if login was successfull
            login_verification = automation.login_verification() #login_verification() returns True if login is successfull otherwise, raises an error
        
            if login_verification == True:
                '''
                if login is successfull, the program asks for module code input from user and calls
                navigate_module() to navigate to that module.
                Then it calls navigating_student() to navigate to the students list of that module.
                After that it calls data_extraction() to extract the students data and save it into a csv file.
                '''
                #module_code takes module code input from user in uppercase format to avoid case sensitivity issues
                module_code = input(color.WHITE + "Hello Professor ! Please Enter the Module Code You want to mark attendance for : ").upper()
                try:
                    print(color.CYAN+"Navigating to the module ...")
                    navigated_module = automation.navigate_module(module_code)
                    '''
                    navigate_module() tries to navigate to the module specified by module_code input from user and returns True 
                    if navigation is successfull otherwise, raises an error
                    '''
                except:
                    print(color.RED + "Could not find the module, please check the module code once and try again")
            
                if navigated_module:
                    '''
                    if module navigation is successfull, it tries to navigate to students list and extract data from there.
                    '''
                    print(color.GREEN+ f"Navigated to the module {module_code} successfully.")
                    try:
                        #navigating_student() tries to navigate to the students list of the module and returns True if navigation is successfull otherwise, raises an error
                        navigated_students = automation.navigating_student()
                        print(color.GREEN+ "Navigated to the students list sucessfully.")
                    except:
                        print(color.RED+ " There was some error navigating to the students list, please try again.")

                    
                    if navigated_students:
                        '''
                        if navigation to students list is successfull, it tries to extract data from there and save it into a csv file.
                        '''
                        try:
                            #file_name is created using module_code to avoid confusion between multiple modules data files
                            file_name = module_code+"_students_list.csv"
                            automation.data_extraction(file_name)
                            print(color.GREEN+f"File saves successfully as '{file_name}'.")
                        except:
                            print(color.RED + "There was some error in data extraction, please try again.")
                    else:
                        print(color.RED + "There was some error navigating to the students list.")
                    
                else:
                    module_code = input(color.WHITE + "Hello Professor ! Please Enter the Module Code You want to mark attendance for : ")
                    #navigaed_module stores the return value from navigate_module() to ensure the progress of the function even after initial failure
                    navigated_module =automation.navigate_module(module_code)
            
            else:
                '''
                After login attempt raises any error, crediblity of login credentials is quentioned,
                after that the user is given a choice to change the credentials and run this program once again. 
                '''
                print(color.CYAN+f"Email Id : {eid}\nPassword : {pwd}")
                print("Is there anything wrong with your Email Id or Password?")
                re_validation = pyin.inputYesNo()
                if re_validation == 'yes':
                    initializer.main()
                    print(color.WHITE+"You can now rerun this program to hopp back on automated attendance marking system.")
                else:
                    print("Okay ! Feel free to hopp on after checking the error whenever you want.")
        
        except:
            print(color.RED + "There was some issue with the program in main automation block.")
        
    else:
        print(color.RED+ "We could not find any file named 'config.json'")
        print("I would recommend you to use initializer.py first, want to use it? : ")
        #config_creation takes validated yes/no input from user using pyinputplus module
        config_creation = pyin.inputYesNo(color.WHITE)
        if config_creation == 'yes':
            print()
            initializer.main()
            print(color.GREEN)
        else:
            print("It's understandable! Bye then :)")
            
except:
    print(color.RED + "There might be some missing files or modules. Please check them ones and try again.")