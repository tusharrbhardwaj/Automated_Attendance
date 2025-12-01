import os
from colorama import Fore as color
import initializer
import pyinputplus as pyin
import automation

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
            login_verification = automation.login_verification() #login_verification() verfies if login happened or not by checking a random element which would only be available if login was successfull
        except:
            '''
            After login attempt raises any error, crediblity of login credentials is quentioned,
            after that the user is given a choice to change the credentials and run this program once again. 
            '''
            print(color.CYAN+f"Email Id : {eid}\nPassword : {pwd}")
            print("Is there anything wrong with your Email Id or Password?")
            re_validation = pyin.inputYesNo()
            if re_validation == 'yes':
                initializer.main()
            else:
                print("Okay ! Feel free to hopp on after checking the error whenever you want.")
        
        
    else:
        print(color.RED+ "We could not find any file named 'config.json'")
        print("I would recommend you to use initializer.py first, want to use it? : ")
        config_creation = pyin.inputYesNo(color.WHITE)
        if config_creation == 'yes':
            print()
            initializer.main()
            print(color.GREEN)
        else:
            print("It's understandable! Bye then :)")
            
except:
    print(color.RED + "There might be some missing files or modules. Please check them ones and try again.")