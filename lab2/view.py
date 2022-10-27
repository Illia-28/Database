import os
import shutil
import time
import random

from controller import conect, close
from model import table_headlines, show_table, title_table, show_mas, fkey, find_value, last_value_pk, data_type, \
    select1, select2, select3, insert, delete, update, rand, q_exit


def MainMenu():
    os.system('cls||clear')
    print("Welcome!")
    lines = ['Main menu', '1. Show one table', '2. Show all table', '3. Insert data', '4. Delete data',
             '5. Update date', '6. Select data', '7. Randomize data', '8. Exit']
    width = shutil.get_terminal_size().columns
    position = (width - max(map(len, lines))) // 2
    flag = 1
    while flag:
        for line in lines:  # left justtified
            print(' ' * position + line)
        print("Make your choice =>", end=' ')
        while 1:
            number = input()
            number = int(number)
            if 0 > number > 8:
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
            flag = menu_6()
        elif number == 7:
            flag = menu_7()
        elif number == 8:
            break
        os.system('cls||clear')
    print(' ' * position + "Goodbye!!")
    time.sleep(1)


# show one table
def menu_1():
    os.system('cls||clear')
    con = conect()
    title = title_table(con)
    show_mas(title)
    print("Make your choice =>", end=' ')
    while 1:
        number = input()
        num = int(number)

        if num > len(title) or num < 1:
            print('Incorrect number entered, please enter again =>', end=' ')
        else:
            break
    show_table(con, title[num - 1])
    close(con)
    return q_exit()


# show all table
def menu_2():
    os.system('cls||clear')
    con = conect()
    title = title_table(con)
    for table in title:
        show_table(con, table)
    close(con)
    return q_exit()


# insert data
def menu_3():
    os.system('cls||clear')
    con = conect()
    title = title_table(con)
    show_mas(title)
    print("Make your choice =>", end=' ')
    while 1:
        number = input()
        num = int(number)

        if num > len(title) or num < 1:
            print('Incorrect number entered, please enter again =>', end=' ')
        else:
            break
    headers_selected_table = table_headlines(con, title[num - 1])
    values = []
    for i in range(len(headers_selected_table)):
        error = 0
        print(headers_selected_table[i] + " = ", end=" ")
        value = input()
        if i == 0:
            value0 = int(last_value_pk(con, title[num - 1], headers_selected_table[i]))
            value0 = value0 + 1
            if int(value) != value0:
                error = 1
        if fkey(con, title[num - 1], headers_selected_table[i]) == 1:
            if find_value(con, headers_selected_table[i], value, title[num - 1]) == 0:
                error = 1

        if error == 1:
            print("Data entry error")
            close(con)
            return q_exit()
        else:
            values.insert(i, value)
    insert(headers_selected_table, con, title, num, values)
    con.commit()
    close(con)
    return q_exit()


# delete data
def menu_4():
    os.system('cls||clear')
    con = conect()
    title = title_table(con)
    show_mas(title)
    print("Make your choice =>", end=' ')
    while 1:
        number = input()
        num = int(number)

        if num > len(title) or num < 1:
            print('Incorrect number entered, please enter again =>', end=' ')
        else:
            break
    headers_selected_table = table_headlines(con, title[num - 1])
    print(f"Enter the number {headers_selected_table[0]}, which you want to delete =>", end=' ')
    while 1:

        num_id = input()
        num_id = int(num_id)

        if 0 > num_id > last_value_pk(con, title[num - 1], headers_selected_table[0]):
            print('Incorrect number entered, please enter again =>', end=' ')
        else:
            break
    print(f"You really want to remove the line where {headers_selected_table[0]} = {num_id}? Y/N =>", end=' ')
    while 1:
        c = input()
        if c == 'Y' or c == 'y':
            delete(con, title, num, headers_selected_table, num_id)
            con.commit()
            close(con)
            return q_exit()
        elif c == 'N' or c == 'n':
            close(con)
            return q_exit()
        else:
            print("The wrong value was entered, it will be entered again. Y/N =>", end=' ')


# Update data
def menu_5():
    os.system('cls||clear')
    con = conect()
    title = title_table(con)
    show_mas(title)
    print("Make your choice =>", end=' ')
    while 1:
        number = input()
        num = int(number)

        if num > len(title) or num < 1:
            print('Incorrect number entered, please enter again =>', end=' ')
        else:
            break
    headers_selected_table = table_headlines(con, title[num - 1])
    print(f"Enter the number {headers_selected_table[0]}, which you want to change =>", end=' ')
    while 1:

        num_id = input()
        num_id = int(num_id)

        if num_id > int(last_value_pk(con, title[num - 1], headers_selected_table[0])) or num_id < 1:
            print('Incorrect number entered, please enter again =>', end=' ')
        else:
            break
    print()
    width = shutil.get_terminal_size().columns
    position = (width - max(map(len, headers_selected_table))) // 2
    for i in range(1, len(headers_selected_table)):  # left justtified
        print(' ' * position + f'{i}. ' + headers_selected_table[i])
    print("Make your choice =>", end=' ')
    while 1:
        num_item = input()
        num_item = int(num_item)

        if num_item > (len(headers_selected_table) - 1) or num_item < 1:
            print('Incorrect number entered, please enter again =>', end=' ')
        else:
            break
    print(f"New value of {headers_selected_table[num_item]} =>", end=' ')
    flag = 1
    while flag:
        value = input()
        if fkey(con, title[num - 1], headers_selected_table[num_item]) == 1:
            if find_value(con, headers_selected_table[num_item], value, title[num - 1]) == 0:
                print('Incorrect value entered, please enter again =>', end=' ')
            else:
                flag = 0
        else:
            flag = 0
    update(con, title, num,  headers_selected_table, num_item, num_id, value)
    con.commit()
    close(con)
    return q_exit()


# Select data
def menu_6():
    os.system('cls||clear')
    con = conect()
    print("1. Information about the order by the name of the customer (you can write only the first name, "
          "only the last name or first name and last name).")
    print("2. What goods were sent via _ ? Enter the name of the shipper?")
    print("3. Calculate the cost of the order.")

    print("Make your choice =>", end=' ')
    while 1:
        number = input()
        num = int(number)

        if num > 3 or num < 1:
            print('Incorrect number entered, please enter again =>', end=' ')
        else:
            break
    if num == 1:
        print()
        print("Enter first name or last name, or both first and last name =>", end=" ")
        name = input()
        select1(name, con)
    elif num == 2:
        print()
        print("Enter the name of the shipper =>", end=" ")
        name = input()
        if "Ukrposhta".find(name) != -1 or "Nova Poshta".find(name) != -1 or "Meest".find(name) != -1:
            select2(name, con)
        else:
            print("Data entry error")
    elif num == 3:
        print()
        print("Enter the order number =>", end=" ")
        while 1:
            num = input()
            if int(num) > int(last_value_pk(con, "Orders", "OrderID")):
                print('Incorrect number entered, please enter again =>', end=' ')
            else:
                break
        select3(num, con)
    close(con)
    print("Data selected successfully!")
    return q_exit()


# Randomize data
def menu_7():
    os.system('cls||clear')
    con = conect()
    title = title_table(con)
    show_mas(title)
    print("Make your choice =>", end=' ')
    while 1:
        number = input()
        num = int(number)

        if num > len(title) or num < 1:
            print('Incorrect number entered, please enter again =>', end=' ')
        else:
            break
    headers_selected_table = table_headlines(con, title[num - 1])
    mas_rand = []
    j = 0
    for i in range(0, len(headers_selected_table)):
        type_ = str(data_type(con, title[num - 1], headers_selected_table[i]))
        if type_.find("character varying") != -1:
            mas_rand.insert(j, "chr(trunc(65 + random()*25)::int)")
            j = j + 1
        elif type_.find("integer") != -1:
            mas_rand.insert(j, "random()*1000")
            j = j + 1

    columns = ' "' + str(headers_selected_table[0]) + '" '
    for i in range(1, len(headers_selected_table)):
        columns = str(columns) + ' , "' + str(headers_selected_table[i]) + '" '
    data = str(mas_rand[0])
    for i in range(1, len(mas_rand)):
        data = str(data) + " , " + str(mas_rand[i])
    number = random.randint(1, 100)
    rand(con, title, num, columns, data, number)
    con.commit()
    close(con)
    return q_exit()
