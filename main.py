def ReadFile():
    with open(name,'r') as attendee:
        
        data = attendee.read()
        print(data)


def validation():
    try:
        if open(name,'r'):
            return True
    except FileNotFoundError:
        print("Try Entering the Correct Name of the Attendance File")
        main()
        
        
def main():
    global name
    name = input('Enter the name : ')
    name = name+'.txt'
    
    if validation():
        ReadFile()

if __name__ == '__main__':
    
    main()
    