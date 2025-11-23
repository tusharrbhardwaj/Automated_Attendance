import csv
import re
from datetime import date

def ReadFile():
    
    with open(name,'r') as attendee:
        reader = csv.reader(attendee)
        next(reader)
        
        data = [row for row in reader]
        global raw_date
        raw_date = data[0][0]
        validated_date = date_validation()

        data_date = validated_date[0]
        choice = validated_date[1]
        
        print("We are marking Attendance for Date :", data_date)
        
        student_present = [students[-2] for students in data]
        student_present.sort()
        
        print(*student_present, sep='\n')

    print("Total Students present in class : ",len(student_present))
    
    if choice in 'Yy':
        print("Opening the broswer to mark the attendance")

def validation():
    try:
        if open(name,'r'):
            return True
    except FileNotFoundError:
        print("Try Entering the Correct Name of the Attendance File")
        main()
    
def date_validation():
    def current_date():
        todays_date =   date.today()
        return todays_date
    current_date = current_date()
    
    def attendance_date(raw_date):
        pattern = re.compile(r"\d\d\d\d-\d\d-\d\d")
        data_date = re.search(pattern, raw_date)
        return data_date.group()
    attendance_date = attendance_date(raw_date)
    
    if (current_date != attendance_date):
        print("The Date of the data does not matches to today's date !")
        print(f"Today's Date is {current_date}, While the data we are working with is of date {attendance_date}")
        choice = input("Are you sure you still want to continue with the current Data-File? : ")
        
    return attendance_date, choice
    
        
def main():
    global name
    name = input('Enter the name : ')
    name = name+'.csv'
    
    
    if validation():
        ReadFile()
        

if __name__ == '__main__':
    
    main()
    