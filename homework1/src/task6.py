import sys
sys.path.append('/home/student/CS4300')
file_name = "/home/student/CS4300/homework1/task6_read_me.txt"

#file = open("test6_read_me.py", "r")
def word_counter(file_name):
    count = 0
    with open(r'file_name', 'r') as file:
        data = file.read()
        word_list = data.split()
        count += len(word_list)
    return print(count)