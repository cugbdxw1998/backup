'''
with open('C') as file_object:
    #contents= file_object.read()
    for line in file_object:
        print(line.rstrip())
        #print(line)
#print(contents.rstrip())

#filename= './python_exercise/contents.txt'
 
with open('python_exercise\contents.txt') as file_object:
    lines=file_object.readlines()

pi_string=' '
for line in lines:
    pi_string += line.strip()
print(pi_string)
print(len(pi_string))
'''
filename='python_exercise\programming.txt'
with open(filename,'w') as file_project:
    file_project.write("I like programming!\n")
    file_project.write("I love creating new games!\n")
    
with open(filename) as f:
    lines = f.readlines()
    for line in lines:
        print(line.rstrip())