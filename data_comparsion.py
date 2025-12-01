import os

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
        

# comparison('B101A_students_list.txt','B101A_attendance_list.txt')
# print("Files 'present.txt' and 'absent.txt' created successfully.")