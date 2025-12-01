'''
This is an initializer file which only needs to be run when setting up the Email Id and Password for the canvas,
so that they can be used by selenium to get logged in to a account and mark attendance.
The data would be stored in a .json file for which would be saved as config.json
'''

#Import functions for the utitlity of the program

'''json module to interact and create json file'''
import json
#To make the code prettier and make the output in the terminal colorful
from colorama import Fore as color
'''pyinput plus is a module to automated input handeling to look for a specific type of input without usuing if else
to verify the correctness of the input, especially in case of emial ID, choices'''
import pyinputplus as pyin

def initializer():
    
    print(color.WHITE + "Hello Welcome to Intitalizer for Automated Attendance Marking System")
    print("You can Enter your id and passwords here, they'll be then stored in a json file for future use.")

    '''eid stores the gisma email id'''
    eid = pyin.inputEmail(color.CYAN + "Enter your GISMA email id : ")
    '''powd variable stores the password'''
    pwd = input("Enter the password : ")

    '''After that, the email and passowrd would be stored in a .json file using the following line of code.'''
    with open("config.json",'w') as credentitals:
        data = {
            "id":eid, 
            "password":pwd
            }
        json.dump(data, credentitals)
    
def config_validation():
    '''
    conifg_validation verifies the creation of .json file and then prints a confirmation message otherwise
    prints and Error message if file is not found or if there is some other issues witht the program.
    '''
    try:
        open('config.json')
        print(color.GREEN+"Details safed Successfully.\nYou can now take advantage of Attendance automation.")
    except FileNotFoundError:
            print(color.RED+"Opps! file has not been created due to some reasons. Please try again.")
            initializer()
    except:
        print(color.RED+"There is some issue with the program. Please check and resolve it.")


def main():
    #main() calls the subsequent functions sequentially
    initializer()
    config_validation()


    
