'''
This script contains two main functions: comparison() and organizer().
comparison() compares the data extracted from the module's student list and the attendance list provided by the user.
It then creates two separate files named 'present.txt' and 'absent.txt' to store
the names of present and absent students respectively.
organizer() creates seperate folders as per the date of attendance and moves the respective files into those folders.
'''
#os is used to create folders and move files into those folders
import os
#coloorama is used to make the output in terminal colorful
from colorama import Fore as color

#present and absent are global lists to store names of present and absent students respectively.
present = []
absent=[]

def comparison(attendance_file_name,file_name):
    '''
    comparison() compares the data extracted from the module's student list and the attendance list provided by the user.
    It then creates two separate files named 'present.txt' and 'abset.txt' to store the names of present and absent students respectively.
    '''
    with open(file_name) as module_student_list:
        total_list = module_student_list.read().splitlines()
         
        with open(attendance_file_name) as attendance:
            attendance_list = attendance.read().splitlines()

            #answer stores the total number of students present in the class out of total strength
            answer = (f"total student present in class {len(attendance_list)}/{len(total_list)}")
            print(answer)
            
            for name in total_list:
                    if name in attendance_list:
                        present.append(name)
                    else:
                        absent.append(name)

    present.sort()
    absent.sort()                    
    with open(file_name+"_present.txt",'w') as present_file:
        for names in present:
            
            present_file.write(names+'\n')
        
    with open(file_name+'_absent.txt','w') as absent_file:
        for names in absent:
            absent_file.write(names+'\n')
        

def organizer(module_code,date):
    '''
    organizer() creates seperate folders as per the date of attendance and moves the respective files into those folders.
    '''
    try:
        '''
         folder_name is created using date variable passed to the function.
         If the folder already exists, it directly moves the files into that folder.
         '''
         
         #folder_name is created using date variable passed to the function.
         #If the folder already exists, it directly moves the files into that folder.
        folder_name = date
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
            for file in os.listdir():
                if file.startswith(module_code) and file.endswith('.txt'):
                    '''
                     It moves all the files starting with module_code and ending with .txt into the created folder.
                '''
                    os.rename(file,os.path.join(folder_name,file))
        else:
            for file in os.listdir():
                if file.startswith(module_code) and file.endswith('.txt'):
                    os.rename(file,os.path.join(folder_name,file))
        print(color.GREEN + "Files organized successfully.")
                
    except:
        print(color.RED + "There was some error in organizing the files.")