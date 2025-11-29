'''
This is the information file and provides the main file with main information like data, date and validation of both.
'''

import csv #To read data from csv file
import re #To search and print regular expression
from colorama import Fore as color #To make the code prettier and make the output in the terminal colorful
from datetime import date

'''
In this file color.red is used to showcase warning or error messages to the user and color.green represents the successfullness of the funciton.
Moreover, color.white is used to showcase normal texts or input texts.
'''

def ReadFile():
    
    '''
    The vairbale "name" refers to the name of the file that containts the attendance list.
    
    ReadFile() pickes the name and read the file, further it takes date information from date_validation().
    Furthermore, it prints the the list of studentes who were present sorted alphabatically,
    printing the toatal stength of the class is also achieved by this function.
    
    It then compares the current_date to the date of the data to ensure that the user is marking the attendance for the correct
    date.
    If the date of the data and the current data does not matches, it gets a confirmation choice from the user asking
    if he still wants to continue with old date data.
    '''
    with open(name,'r') as attendee:
        reader = csv.reader(attendee)
        next(reader)
        
        #data contains all the data which is actually in the csv file, unflitered and non-formatted.
        data = [row for row in reader]

        #raw_data contains the 'date' column of the csv file indexed from data
        global raw_date
        raw_date = data[0][0]

        #validated_date contains the returned tuple of values from date_validation ie data_date and choice respectively.
        validated_date = date_validation()

        global data_date
        data_date = validated_date[0]
        current_date = validated_date[1]
        
        print(color.WHITE + "We are marking Attendance for Date :", data_date)
        
        #student_present containts the name column of the csv file indexed from data
        student_present = [students[-2] for students in data]
        student_present.sort()
        
        #The sorted list of student name is then printed line by line in the terminal
        # print(*student_present, sep='\n')
        with open(f"{data_date}.txt",'w') as attendee:
            for names in student_present:
                attendee.write(names+'\n')

    #len(student_present) counts the number of students who were present in the class and then prints them out
    print(color.CYAN + "Total Students present in class : ",len(student_present))
    
    #Following logic block compares the dates from current_date() and attendance_date()
    if (current_date != data_date):
        print(color.RED + "The Date of the data does not matches to today's date !")
        print(color.RED + f"Today's Date is {current_date}, While the data we are working with is of date {data_date}")
        choice = input(color.RED + "Are you sure you still want to continue with the current Data-File? : ")
        #choice is indexed from the returned value from date_validation() to ensure the progress of the function even after date mismatch
        if choice in 'Yy':
            #Dummy data print, later would be replaced by selenium execution in main.py
            print(color.GREEN + "Opening the broswer to mark the attendance")



def validation():
    '''
    validation() validates the file and looks if that exists.
    If the file given as inputed by the user does not exists, it raises an error instead of crashing the program and then,
    reexuctes the program.
    Or if there is some other problem, it returns with specified error message.
    '''
    try:
        if open(name,'r'):
            return True
    except FileNotFoundError:
        print(color.RED + "Oops ! No such file in the folder, try Entering the Correct Name of the Attendance File")
        main()
    except:
        print(color.RED + "There is some problem with the program in validation() or main().")
 
 
   
def date_validation():
    '''
    date_validation() have to subfunctions, current_date() which uses date module to find out current date to compare with
    the date of the data and attendance_date() which takes raw_date as positional parameter and then returns the date of the
    data.
    
    The date of the data is extracted out from the csv file using re as in csv file the data is in regular expression for date.
    
    both current_date and attendance_date are treated as return value of the function.
    '''
    def current_date():
        #todays_date contains current date using date functon 
        todays_date = date.today()
        return todays_date
    
    #current_date calls current_date() and stores the return value to ensure better reusablity of function without recalling it multiple times.
    current_date = current_date()
    
    def attendance_date(raw_date):
        #attendance_date() uses regular expression pattern matching to find the date of the current data from the pile of unfiltered coloumn of date.

        #pattern stores the regular expression of date to match the pattern and find the date
        pattern = re.compile(r"\d\d\d\d-\d\d-\d\d")
        
        #The pattern is then searched in the raw-unfiltered data
        data_date = re.search(pattern, raw_date)
        
        #The searched data is then grouped to reach the result
        return data_date.group()
    
    #attendance_date calls attendance_date() and stores the return value to ensure better reusablity of function without recalling it multiple times.
    attendance_date = attendance_date(raw_date)

    return attendance_date, current_date
     

    
def main():
    '''
    main() calls the other functions of the programs and ensure the conditional and respectful execution of each function. 
    '''
    global name
    name = input(color.WHITE + 'Enter the name : ')
    name = name+'.csv'
    
    
    if validation():
        ReadFile()
        

if __name__ == '__main__':
    
    main()
    