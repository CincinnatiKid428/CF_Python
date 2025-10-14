with open('number_list.txt','w') as file:
    numlist = [file.writelines(f'{i}\n') for i in range(50,101)]