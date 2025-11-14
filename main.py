import csv
import re

def ReadFile():
    
    with open(name,'r') as attendee:
        reader = csv.reader(attendee)
        next(reader)
        
        data = [row for row in reader]
         
        raw_date = data[0][0]
        date = attendance_date(raw_date)
        
        print("We are marking Attendance for Date :", date)
        
        student_present = [students[-2] for students in data]
        student_present.sort()
        
        print(*student_present, sep='\n')

    print("Total Students present in class : ",len(student_present))

def validation():
    try:
        if open(name,'r'):
            return True
    except FileNotFoundError:
        print("Try Entering the Correct Name of the Attendance File")
        main()
        

def attendance_date(raw_date):
    
    pattern = re.compile(r"\d\d\d\d-\d\d-\d\d")
    date = re.search(pattern, raw_date)
    
    return date.group()
    
        
def main():
    global name
    name = input('Enter the name : ')
    name = name+'.csv'
    
    if validation():
        ReadFile()

if __name__ == '__main__':
    
    main()
    