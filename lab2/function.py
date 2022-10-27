import shutil
import time

def table_headlines(connection, table_name):
    with connection.cursor() as cursor:
        cursor.execute(
            f"""SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}' ORDER BY ordinal_position;"""
        )
        full_fetch_headlines = cursor.fetchall()
        i = 0
        headlines = []
        for record in full_fetch_headlines:
            s: str = "".join(c for c in record if c.isalnum())  # залишаються літери та числа
            headlines.insert(i, s)
            i = i + 1
    return headlines


def show_table(connection, table_name):
    print(f"{table_name}")
    print(f"""SQL query: "SELECT * FROM "{table_name}" ;""")

    headlines = table_headlines(connection, table_name)

    from prettytable import PrettyTable
    mytable = PrettyTable()
    mytable.field_names = headlines

    with connection.cursor() as cursor:
        cursor.execute(
            f""" SELECT * FROM "{table_name}" ;"""
        )
        full_fetch = cursor.fetchall()
        for record in full_fetch:
            # print(record)
            mytable.add_row(record)
    print(mytable)
    print()


def title_table(connection):
    with connection.cursor() as cursor:
        cursor.execute(
            f"""SELECT "table_name" FROM information_schema.tables WHERE  table_schema='public';"""
        )
        full_fetch = cursor.fetchall()
        i = 0
        title = []
        for record in full_fetch:
            s: str = "".join(c for c in record if c.isalnum())  # залишаються літери та числа
            title.insert(i, s)
            i = i + 1
        return title


def show_mas(lines):
    width = shutil.get_terminal_size().columns
    position = (width - max(map(len, lines))) // 2
    i = 1
    for line in lines:  # left justtified
        print(' ' * position + f'{i}. ' + line)
        i = i + 1


def mas_pk(connection):
    with connection.cursor() as cursor:
        cursor.execute(
            f"""SELECT a.attname FROM   pg_index i JOIN   pg_attribute a ON a.attrelid = i.indrelid  AND a.attnum = ANY(i.indkey) AND    i.indisprimary;"""
            # https://wiki.postgresql.org/wiki/Retrieve_primary_key_columns
        )
        full_fetch = cursor.fetchall()
        i = 0
        pk = []
        for record in full_fetch:
            s: str = "".join(c for c in record if c.isalnum())  # залишаються літери та числа
            pk.insert(i, s)
            i = i + 1
    return pk


def fkey(connection, table_name, headline):
    with connection.cursor() as cursor:
        cursor.execute(
            f"""SELECT constraint_name FROM information_schema.key_column_usage WHERE  table_name = '{table_name}' ;"""
        )
        full_fetch = cursor.fetchall()
        for record in full_fetch:
            s: str = "".join(c for c in str(record) if c.isalnum())
            if s.find(headline) != -1:
                if s.find('fkey') != -1:
                    return 1  # fk
                else:
                    return 0  # not key


def last_value_pk(connection, table_name, headline):
    with connection.cursor() as cursor:
        cursor.execute(
            f"""SELECT "{headline}" FROM "{table_name}" ORDER BY "{headline}" ;"""
        )
        full_fetch = cursor.fetchall()
        values = []
        i = 0
        for record in full_fetch:
            s = "".join(c for c in str(record) if c.isdecimal())  # залишаються літери та числа
            values.insert(i, s)
            i = i + 1
        return values[len(values) - 1]


def find_value(connection, headline, value, skip_table):
    title = title_table(connection)
    for record in title:
        if record == skip_table:
            continue
        # print(record)
        column_names = table_headlines(connection, record)
        for record1 in column_names:
            if record1 == headline:
                with connection.cursor() as cursor:
                    cursor.execute(
                        f"""SELECT "{headline}" FROM "{record}" ;"""
                    )
                    full_fetch = cursor.fetchall()
                    i = 0
                    values = []
                    for num in full_fetch:
                        s = "".join(c for c in str(num) if c.isdecimal())  # залишаються літери та числа
                        values.insert(i, int(s))
                        i = i + 1
                    need_num = -1
                    for num in values:
                        if int(num) == int(value):
                            need_num = num
                            break
                    if need_num == -1:
                        return 0
                    else:
                        return 1

def data_type(connection,table_name, headline):
    with connection.cursor() as cursor:
        cursor.execute(
            f"""SELECT "data_type" FROM information_schema.columns WHERE  table_schema='public' and "table_name" = '{table_name}' and "column_name" ='{headline}';"""
        )
        full_fetch = cursor.fetchall()
        values = []
        i = 0
        for record in full_fetch:
            s: str = "".join(c for c in str(record) if c.isdecimal())  # залишаються літери та числа
            values.insert(i, str(s))
            i = i + 1
        return full_fetch[0]

def select1(Name, connection):

    from prettytable import PrettyTable
    mytable = PrettyTable()
    mytable.field_names = ["CustomerName", "OrderID", "OrderDate", "ShipperName", "ProductName", "Quantity"]
    beg = int(time.time() * 1000)

    with connection.cursor() as cursor:
        cursor.execute(
            f"""SELECT c."CustomerName", o."OrderID", o."OrderDate", s."ShipperName", p."ProductName", od."Quantity"  FROM "Customers" as c
                JOIN "Orders" as o ON c."CustomerID" = o."CustomerID"
                JOIN "Shippers" as s ON o."ShipperID" = s."ShipperID"
                JOIN "OrderDetails" as od ON o."OrderID" = od."OrderID"
                JOIN "Products" as p ON p."ProductID" = od."ProductID"
                WHERE "CustomerName" LIKE '%{Name}%';"""
        )
        end = int(time.time() * 1000) - beg
        full_fetch = cursor.fetchall()
        for record in full_fetch:
            # print(record)
            mytable.add_row(record)
    print(mytable)
    print()
    print('Time of request = {} ms'.format(end))

def select2(Name, connection):

    from prettytable import PrettyTable
    mytable = PrettyTable()
    mytable.field_names = ["OrderID", "ShipperName", "ProductName", "Quantity"]
    beg = int(time.time() * 1000)

    with connection.cursor() as cursor:
        cursor.execute(
            f"""SELECT o."OrderID", s."ShipperName", p."ProductName", od."Quantity"  FROM "Orders" as o
                JOIN "Shippers" as s ON o."ShipperID" = s."ShipperID"
                JOIN "OrderDetails" as od ON o."OrderID" = od."OrderID"
                JOIN "Products" as p ON p."ProductID" = od."ProductID"
                WHERE "ShipperName" LIKE '%{Name}%';;"""
        )
        end = int(time.time() * 1000) - beg
        full_fetch = cursor.fetchall()
        for record in full_fetch:
            # print(record)
            mytable.add_row(record)
    print(mytable)
    print()
    print('Time of request = {} ms'.format(end))


def select3(Number, connection):

    from prettytable import PrettyTable
    mytable = PrettyTable()
    mytable.field_names = [ "OrderID",  "Cost of order"]
    beg = int(time.time() * 1000)

    with connection.cursor() as cursor:
        cursor.execute(
            f"""SELECT o."OrderID", SUM("Price" * "Quantity") as "Cost of order" FROM "Orders" as o
                JOIN "OrderDetails" as od ON o."OrderID" = od."OrderID"
                JOIN "Products" as p ON p."ProductID" = od."ProductID"
                WHERE o."OrderID" = '{Number}'
                GROUP BY o."OrderID";"""
        )
        end = int(time.time() * 1000) - beg
        full_fetch = cursor.fetchall()
        for record in full_fetch:
            # print(record)
            mytable.add_row(record)
    print(mytable)
    print()
    print('Time of request = {} ms'.format(end))

def q_exit():
    print('Continue work with DB? Y/N =>', end=' ')
    while 1:
        c = input()
        if c == 'Y' or c == 'y':
            return 1
        elif c == 'N' or c == 'n':
            return 0
        else:
            print("The wrong value was entered, it will be entered again. Y/N =>", end=' ')
