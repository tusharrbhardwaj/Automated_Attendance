from colorama import Fore as color
import initializer
import pyinputplus as pyin

try:
    
    '''
    The first and formost thing in the program is to check whether config.json exists to reterieve login
    credentials from it.
    '''
    try:
        open('config.json')  
    except:
        print(color.RED+ "We could not find any file named 'config.json'")
        print("I would recommend you to use initializer.py first, want to use it? : ")
        config_creation = pyin.inputYesNo(color.WHITE)
        if config_creation == 'yes':
            print()
            initializer.main()
        else:
            print("It's understandable! Bye then :)")
            
except:
    print("There might be some missing files or modules. please check them ones and try again.")