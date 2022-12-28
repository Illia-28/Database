import os
import shutil
import time
import model

def MainMenu():
    os.system('cls||clear')
    print("Welcome!")
    lines = ['Main menu', '1. Show one table', '2. Show all table', '3. Insert data', '4. Delete data',
             '5. Update date', '6. Exit']
    width = shutil.get_terminal_size().columns
    position = (width - max(map(len, lines))) // 2
    flag = 1
    while flag:
        for line in lines:
            print(' ' * position + line)
        print("Make your choice =>", end=' ')
        while 1:
            number = input()
            number = int(number)
            if 0 > number > 6:
                print('Incorrect number entered, please enter again =>', end=' ')
            else:
                break
        if number == 1:
            flag = menu_1()
        elif number == 2:
            flag = menu_2()
        elif number == 3:
            flag = menu_3()
        elif number == 4:
            flag = menu_4()
        elif number == 5:
            flag = menu_5()
        elif number == 6:
            break
        os.system('cls||clear')
    print(' ' * position + "Goodbye!!")
    time.sleep(1)


# show one table
def menu_1():
    os.system('cls||clear')
    tables = ['Customers', 'OrderDetails', 'Orders', 'Products', 'Shippers']
    width = shutil.get_terminal_size().columns
    position = (width - max(map(len, tables))) // 2

    print(" ")
    for line in range(5):
        print(' ' * position + f'{line + 1}. ' + tables[line])
    print("Make your choice =>", end=' ')
    while 1:
        number = input()
        number = int(number)
        if 0 > number > 5:
            print('Incorrect number entered, please enter again =>', end=' ')
        else:
            break

    if number == 1:
        model.show(model.Customers)
    elif number == 2:
        model.show(model.OrderDetails)
    elif number == 3:
        model.show(model.Orders)
    elif number == 4:
        model.show(model.Products)
    elif number == 5:
        model.show(model.Shippers)
    return model.q_exit()


# show all table
def menu_2():
    model.show_all()
    return model.q_exit()


# insert data
def menu_3():
    os.system('cls||clear')
    tables = ['Customers', 'OrderDetails', 'Orders', 'Products', 'Shippers']
    width = shutil.get_terminal_size().columns
    position = (width - max(map(len, tables))) // 2

    print(" ")
    for line in range(5):
        print(' ' * position + f'{line + 1}. ' + tables[line])
    print("Make your choice =>", end=' ')
    while 1:
        number = input()
        number = int(number)
        if 0 > number > 5:
            print('Incorrect number entered, please enter again =>', end=' ')
        else:
            break
    if number == 1:
        model.insert_customers()
    elif number == 2:
        model.insert_order_details()
    elif number == 3:
        model.insert_orders()
    elif number == 4:
        model.insert_products()
    elif number == 5:
        model.insert_shippers()
    return model.q_exit()


# delete data
def menu_4():
    os.system('cls||clear')
    model.delete()
    return model.q_exit()


# Update data
def menu_5():
    model.update()
    return model.q_exit()


MainMenu()
