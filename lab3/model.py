from sqlalchemy import create_engine, Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker, relationship
import shutil

tables = {
    1: 'Customers',
    2: 'OrderDetails',
    3: 'Orders',
    4: 'Products',
    5: 'Shippers',
}

Base = declarative_base()
engine = create_engine("postgresql+psycopg2://postgres:qwerty@localhost:5432/postgres")
Base.metadata.create_all(bind=engine)


class Customers(Base):
    __tablename__ = "Customers"

    CustomerID = Column("CustomerID", Integer, primary_key=True, nullable=False)
    CustomerName = Column("CustomerName", String, nullable=False)
    ContactName = Column("ContactName", String, nullable=False)
    Address = Column("Address", String, nullable=False)
    City = Column("City", String, nullable=False)
    PostalCode = Column("PostalCode", Integer, nullable=False)
    Country = Column("Country", String, nullable=False)

    orders = relationship('Orders')

    def __init__(self, customerid, customername, contactname, address, city, postalcode, country):
        self.CustomerID = customerid
        self.CustomerName = customername
        self.ContactName = contactname
        self.Address = address
        self.City = city
        self.PostalCode = postalcode
        self.Country = country

    def __repr__(self):
        return f"{self.CustomerID} {self.CustomerName}  {self.ContactName} {self.Address} {self.City} {self.PostalCode} {self.Country}"


class OrderDetails(Base):
    __tablename__ = "OrderDetails"

    OrderDetailID = Column("OrderDetailID", Integer, primary_key=True, nullable=False)
    OrderID = Column("OrderID", Integer, ForeignKey('Orders.OrderID'), nullable=False)
    ProductID = Column("ProductID", Integer, ForeignKey('Products.ProductID'), nullable=False)
    Quantity = Column("Quantity", Integer, nullable=False)

    products = relationship('Products')
    orders = relationship('Orders')

    def __init__(self, orderdetailid, orderid, productid, quantity):
        self.OrderDetailID = orderdetailid
        self.OrderID = orderid
        self.ProductID = productid
        self.Quantity = quantity

    def __repr__(self):
        return f"{self.OrderDetailID} {self.OrderID} {self.ProductID} {self.Quantity} "


class Orders(Base):
    __tablename__ = "Orders"

    OrderID = Column("OrderID", Integer, primary_key=True, nullable=False)
    CustomerID = Column("CustomerID", Integer, ForeignKey('Customers.CustomerID'), nullable=False)
    OrderDate = Column("OrderDate", String, nullable=False)
    ShipperID = Column("ShipperID", Integer, ForeignKey('Shippers.ShipperID'), nullable=False)

    customers = relationship('Customers')
    order_details = relationship('OrderDetails')
    shippers = relationship('Shippers')

    def __init__(self, orderid, customerid, orderdate, shipperid):
        self.OrderID = orderid
        self.CustomerID = customerid
        self.OrderDate = orderdate
        self.ShipperID = shipperid

    def __repr__(self):
        return f"{self.OrderID} {self.CustomerID} {self.OrderDate} {self.ShipperID} "


class Products(Base):
    __tablename__ = "Products"

    ProductID = Column("ProductID", Integer, primary_key=True, nullable=False)
    ProductName = Column("ProductName", String, nullable=False)
    Unit = Column("Unit", String, nullable=False)
    Price = Column("Price", Numeric, nullable=False)

    order_details = relationship('OrderDetails')
    orders = relationship('Orders')

    def __init__(self, productid, productname, unit, price):
        self.ProductID = productid
        self.ProductName = productname
        self.Unit = unit
        self.Price = price

    def __repr__(self):
        return f"{self.ProductID} {self.ProductName} {self.Unit} {self.Price} "


class Shippers(Base):
    __tablename__ = "Shippers"

    ShipperID = Column("ShipperID", Integer, primary_key=True, nullable=False)
    ShipperName = Column("ShipperName", String, nullable=False)
    Phone = Column("Phone", String, nullable=False)

    def __init__(self, shipperid, shippername, phone):
        self.ShipperID = shipperid
        self.ShipperName = shippername
        self.Phone = phone

    def __repr__(self):
        return f"{self.ShipperID} {self.ShipperName} {self.Phone}"


def show_all():
    Session = sessionmaker(bind=engine)
    session = Session()

    print(session.query(Customers).all())
    print(session.query(Orders).all())
    print(session.query(OrderDetails).all())
    print(session.query(Shippers).all())
    print(session.query(Products).all())


def show(table):
    Session = sessionmaker(bind=engine)
    session = Session()

    print(session.query(table).all())


def insert_customers():
    Session = sessionmaker(bind=engine)
    session = Session()
    print('CustomerID =', end=' ')
    while 1:
        id = input()
        id = int(id)
        if (id != (session.query(Customers).count() + 1)):
            print('Incorrect number entered, please enter again =>', end=' ')
        else:
            break
    print('CustomerName =', end=' ')
    name = input()
    print('ContactName =', end=' ')
    cname = input()
    print('Address =', end=' ')
    address = input()
    print('City =', end=' ')
    city = input()
    print('PostalCode =', end=' ')
    code = input()
    print('Country =', end=' ')
    country = input()

    session.add(Customers(id, name, cname, address, city, code, country))
    session.commit()


def insert_order_details():
    Session = sessionmaker(bind=engine)
    session = Session()

    print('OrderDetailID =', end=' ')
    while 1:
        id = input()
        id = int(id)
        if (id != (session.query(OrderDetails).count() + 1)):
            print('Incorrect number entered, please enter again =>', end=' ')
        else:
            break
    print('OrderID =', end=' ')
    while 1:
        o_id = input()
        o_id = int(o_id)
        if (o_id > session.query(Orders).count()):
            print('Incorrect number entered, please enter again =>', end=' ')
        else:
            break
    print('ProductID =', end=' ')
    while 1:
        p_id = input()
        p_id = int(p_id)
        if (p_id > session.query(Products).count()):
            print('Incorrect number entered, please enter again =>', end=' ')
        else:
            break
    print('Quantity =', end=' ')
    quantity = input()

    session.add(OrderDetails(id, o_id, p_id, quantity))
    session.commit()


def insert_orders():
    Session = sessionmaker(bind=engine)
    session = Session()

    print('OrderID =', end=' ')
    while 1:
        id = input()
        id = int(id)
        if (id != (session.query(Orders).count() + 1)):
            print('Incorrect number entered, please enter again =>', end=' ')
        else:
            break
    print('CustomerID =', end=' ')
    while 1:
        c_id = input()
        c_id = int(c_id)
        if (c_id > session.query(Customers).count()):
            print('Incorrect number entered, please enter again =>', end=' ')
        else:
            break
    print('OrderDate =', end=' ')
    date = input()
    print('ShipperID =', end=' ')
    while 1:
        s_id = input()
        s_id = int(s_id)
        if (s_id > session.query(Shippers).count()):
            print('Incorrect number entered, please enter again =>', end=' ')
        else:
            break

    session.add(Orders(id, c_id, date, s_id))
    session.commit()


def insert_products():
    Session = sessionmaker(bind=engine)
    session = Session()

    print('ProductID =', end=' ')
    while 1:
        id = input()
        id = int(id)
        if (id != (session.query(Products).count() + 1)):
            print('Incorrect number entered, please enter again =>', end=' ')
        else:
            break
    print('ProductName =', end=' ')
    name = input()
    print('Unit =', end=' ')
    unit = input()
    print('Price =', end=' ')
    price = input()

    session.add(Products(id, name, unit, price))
    session.commit()


def insert_shippers():
    Session = sessionmaker(bind=engine)
    session = Session()

    print('Shippers =', end=' ')
    while 1:
        id = input()
        id = int(id)
        if (id != (session.query(Shippers).count() + 1)):
            print('Incorrect number entered, please enter again =>', end=' ')
        else:
            break
    print('ShipperName =', end=' ')
    name = input()
    print('Phone =', end=' ')
    phone = input()

    session.add(Shippers(id, name, phone))
    session.commit()


def delete():
    Session = sessionmaker(bind=engine)
    session = Session()

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
        print("Enter the number CustomerID, which you want to delete =>", end=' ')
        while 1:
            id = input()
            id = int(id)
            if (id > session.query(Customers).count()):
                print('Incorrect number entered, please enter again =>', end=' ')
            else:
                break
        session.delete(session.query(Customers).filter(Customers.CustomerID == id).one())
    elif number == 2:
        print("Enter the number OrderDetailsID, which you want to delete =>", end=' ')
        while 1:
            id = input()
            id = int(id)
            if (id > session.query(Customers).count()):
                print('Incorrect number entered, please enter again =>', end=' ')
            else:
                break
        session.delete(session.query(OrderDetails).filter(OrderDetails.OrderDetailID == id).one())
    elif number == 3:
        print("Enter the number OrderID, which you want to delete =>", end=' ')
        while 1:
            id = input()
            id = int(id)
            if (id > session.query(Customers).count()):
                print('Incorrect number entered, please enter again =>', end=' ')
            else:
                break
        session.delete(session.query(Orders).filter(Orders.OrderID == id).one())
    elif number == 4:
        print("Enter the number ProductID, which you want to delete =>", end=' ')
        while 1:
            id = input()
            id = int(id)
            if (id > session.query(Customers).count()):
                print('Incorrect number entered, please enter again =>', end=' ')
            else:
                break
        session.delete(session.query(Products).filter(Products.ProductID == id).one())
    elif number == 5:
        print("Enter the number ShipperID, which you want to delete =>", end=' ')
        while 1:
            id = input()
            id = int(id)
            if (id > session.query(Customers).count()):
                print('Incorrect number entered, please enter again =>', end=' ')
            else:
                break
        session.delete(session.query(Shippers).filter(Shippers.ShipperID == id).one())
    session.commit()


def update():
    Session = sessionmaker(bind=engine)
    session = Session()

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
        print("Enter the number CustomerID, which you want to change =>", end=' ')
        while 1:
            id = input()
            id = int(id)
            if (id > session.query(Customers).count()):
                print('Incorrect number entered, please enter again =>', end=' ')
            else:
                break
        lines = ['CustomerName', 'ContactName', 'Address', 'City', 'PostalCode', 'Country']
        position = (width - max(map(len, lines))) // 2
        print(" ")
        for line in range(6):
            print(' ' * position + f'{line + 1}. ' + lines[line])
        print("Make your choice =>", end=' ')
        while 1:
            number = input()
            number = int(number)
            if 0 > number > 6:
                print('Incorrect number entered, please enter again =>', end=' ')
            else:
                break
        if number == 1:
            print("New value of CustomerName =>", end=' ')
            name = input()
            i = session.query(Customers).get(id)
            i.CustomerName = name
        elif number == 2:
            print("New value of ContactName =>", end=' ')
            name = input()
            i = session.query(Customers).get(id)
            i.ContactName = name
        elif number == 3:
            print("New value of Address =>", end=' ')
            address = input()
            i = session.query(Customers).get(id)
            i.Address = address
        elif number == 4:
            print("New value of City =>", end=' ')
            city = input()
            i = session.query(Customers).get(id)
            i.City = city
        elif number == 5:
            print("New value of PostalCode =>", end=' ')
            code = input()
            i = session.query(Customers).get(id)
            i.PostalCode = code
        elif number == 6:
            print("New value of Country =>", end=' ')
            country = input()
            i = session.query(Customers).get(id)
            i.Country = country
        session.add(i)
        session.commit()
    elif number == 2:
        print("Enter the number OrderDetailID, which you want to change =>", end=' ')
        while 1:
            id = input()
            id = int(id)
            if (id > session.query(OrderDetails).count()):
                print('Incorrect number entered, please enter again =>', end=' ')
            else:
                break
        lines = ['OrderID', 'ProductID', 'Quantity']
        position = (width - max(map(len, lines))) // 2
        print(" ")
        for line in range(3):
            print(' ' * position + f'{line + 1}. ' + lines[line])
        print("Make your choice =>", end=' ')
        while 1:
            number = input()
            number = int(number)
            if 0 > number > 3:
                print('Incorrect number entered, please enter again =>', end=' ')
            else:
                break
        if number == 1:
            print("New value of OrderID =>", end=' ')
            while 1:
                o_id = input()
                o_id = int(o_id)
                if (o_id > session.query(Orders).count()):
                    print('Incorrect number entered, please enter again =>', end=' ')
                else:
                    break
            i = session.query(OrderDetails).get(id)
            i.OrderID = o_id
        elif number == 2:
            print("New value of ProductID =>", end=' ')
            while 1:
                p_id = input()
                p_id = int(p_id)
                if (id > session.query(Products).count()):
                    print('Incorrect number entered, please enter again =>', end=' ')
                else:
                    break
            i = session.query(OrderDetails).get(id)
            i.ProductID = p_id
        elif number == 3:
            print("New value of Quantity =>", end=' ')
            quantity = input()
            i = session.query(OrderDetails).get(id)
            i.Quantity = quantity
        session.add(i)
        session.commit()
    elif number == 3:
        print("Enter the number OrderID, which you want to change =>", end=' ')
        while 1:
            id = input()
            id = int(id)
            if (id > session.query(OrderDetails).count()):
                print('Incorrect number entered, please enter again =>', end=' ')
            else:
                break
        lines = ['CustomerID', 'OrderDate', 'ShipperID']
        position = (width - max(map(len, lines))) // 2
        print(" ")
        for line in range(3):
            print(' ' * position + f'{line + 1}. ' + lines[line])
        print("Make your choice =>", end=' ')
        while 1:
            number = input()
            number = int(number)
            if 0 > number > 3:
                print('Incorrect number entered, please enter again =>', end=' ')
            else:
                break
        if number == 1:
            print("New value of CustomerID =>", end=' ')
            while 1:
                c_id = input()
                c_id = int(c_id)
                if (c_id > session.query(Customers).count()):
                    print('Incorrect number entered, please enter again =>', end=' ')
                else:
                    break
            i = session.query(Orders).get(id)
            i.CustomerID = c_id
        elif number == 2:
            print("New value of OrderDate =>", end=' ')
            date = input()
            i = session.query(Orders).get(id)
            i.OrderDate = date
        elif number == 3:
            print("New value of ShipperID =>", end=' ')
            while 1:
                s_id = input()
                s_id = int(s_id)
                if (s_id > session.query(Products).count()):
                    print('Incorrect number entered, please enter again =>', end=' ')
                else:
                    break
            i = session.query(Orders).get(id)
            i.ShipperID = s_id
        session.add(i)
        session.commit()
    elif number == 4:
        print("Enter the number ProductID, which you want to change =>", end=' ')
        while 1:
            id = input()
            id = int(id)
            if (id > session.query(Products).count()):
                print('Incorrect number entered, please enter again =>', end=' ')
            else:
                break
        lines = ['ProductName', 'Unit', 'Price']
        position = (width - max(map(len, lines))) // 2
        print(" ")
        for line in range(3):
            print(' ' * position + f'{line + 1}. ' + lines[line])
        print("Make your choice =>", end=' ')
        while 1:
            number = input()
            number = int(number)
            if 0 > number > 3:
                print('Incorrect number entered, please enter again =>', end=' ')
            else:
                break
        if number == 1:
            print("New value of ProductName =>", end=' ')
            name = input()
            i = session.query(Products).get(id)
            i.ProductName = name
        elif number == 2:
            print("New value of Unit =>", end=' ')
            unit = input()
            i = session.query(Products).get(id)
            i.Unit = unit
        elif number == 3:
            print("New value of Price =>", end=' ')
            price = input()
            i = session.query(Products).get(id)
            i.Price = price
        session.add(i)
        session.commit()
    elif number == 5:
        print("Enter the number OrderDetailID, which you want to change =>", end=' ')
        while 1:
            id = input()
            id = int(id)
            if (id > session.query(Shippers).count()):
                print('Incorrect number entered, please enter again =>', end=' ')
            else:
                break
        lines = ['ShipperName', 'Phone']
        position = (width - max(map(len, lines))) // 2
        print(" ")
        for line in range(2):
            print(' ' * position + f'{line + 1}. ' + lines[line])
        print("Make your choice =>", end=' ')
        while 1:
            number = input()
            number = int(number)
            if 0 > number > 2:
                print('Incorrect number entered, please enter again =>', end=' ')
            else:
                break
        if number == 1:
            print("New value of ShipperName =>", end=' ')
            name = input()
            i = session.query(Shippers).get(id)
            i.ShipperName = name
        elif number == 2:
            print("New value of Phone =>", end=' ')
            phone = input()
            i = session.query(Shippers).get(id)
            i.Phone = phone
        session.add(i)
        session.commit()


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
