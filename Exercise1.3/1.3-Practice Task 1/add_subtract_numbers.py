print('\nPlease enter two integers, followed by + or - to perform \
addition or subtraction on the number.\n')

num1 = int(input('Enter the first number:' ))
num2 = int(input('Enter the second number:' ))
operator = str(input('Enter the + or - sign: '))
print('\n')

valid_operator = False

# Check that valid operator was entered
if operator == '+':
    valid_operator = True
elif operator == '-':
    valid_operator = True
else:
    print(f'Invalid operator entered : {operator}')

if valid_operator == True:
    if operator == '+':
        print(f'The sum of {num1} and {num2} is {num1 + num2}')
    else:
        print(f'The difference of {num1} and {num2} is {num1 - num2}')
