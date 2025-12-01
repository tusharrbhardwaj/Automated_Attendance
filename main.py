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
#import data_comparsion module to compare the attendance data with the student list
import information
import data_comparsion
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
                        #result stores the return value from data_extraction() to ensure the progress of the function even after initial failure
                        '''if result is True, it compares the data else raises an error.'''
                        #result stores the return value from data_extraction() to ensure the progress of the function even after initial failure
                        result = False
                        '''
                        if navigation to students list is successfull, it tries to extract data from there and save it into a csv file.
                        '''
                        try:
                            #file_name is created using module_code to avoid confusion between multiple modules data files
                            file_name = module_code+"_students_list.txt"
                            automation.data_extraction(file_name)
                            print(color.GREEN+f"File saved successfully as '{file_name}'.")
                            result = True
                        except:
                            print(color.RED + "There was some error in data extraction, please try again.")
                            result = False
                    
                    else:
                        print(color.RED + "There was some error navigating to the students list.")
                    
                    if result:
                        '''
                        if data extraction is successfull, it tries to reterive information from that data using information.py
                        and then compares that data with the student list using data_comparsion.py
                        '''
                        #data_file_name takes input from user for the name of attendance list file(without extension)
                        data_file_name = input(color.WHITE + 'Enter the name of the attendance_list: ')
                        #data_file_name_txt and data_file_name_csv creates the file names with appropriate extensions
                        data_file_name_txt = data_file_name+'.txt'
                        data_file_name_csv = data_file_name+'.csv'
                        #attendance_file_name creates the attendance file name using module_code to avoid confusion between multiple modules data files
                        attendance_file_name = module_code+'_attendance_list.txt'
                        #info_reterival stores the return value from information.main() to ensure the progress of the function even after initial failure
                        info_reterival = information.main(data_file_name_csv)
                        
                        try:
                            #Renaming the generated attendance file to include module code for clarity
                            os.rename(data_file_name_txt, attendance_file_name)
                            print(color.GREEN + f"Attendance file renamed to '{attendance_file_name}' successfully.")
                        except:
                            print(color.RED + "There was some error renaming the attendance file.")
                        
                        
                        if info_reterival:
                            '''
                            info_reterival is True if information reterival is successfull otherwise, raises an error.
                            If information reterival is successfull, it compares the data using data_comparsion.comparison()    
                            '''
                            print(color.GREEN + "Information reterival successfull.")
                            try:
                                '''
                                data_comparsion.comparison() compares the data extracted from the module's student list and the attendance list provided by the user.
                                It then creates two separate files named 'present.txt' and 'absent.txt' to store the names of present and absent students respectively.
                                '''
                                data_comparsion.comparison(attendance_file_name,file_name)
                            except:
                                print(color.RED + "There was some error in data comparsion.")
                        
                        else:
                            print(color.RED + "Information reterival from information.py was not successfull.")
                        
                    else:
                        print(color.RED + "Data extraction from was not successfull, cannot proceed to information reterival.")
                        
                        
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