import mysql.connector as mc
import tabulate
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

print('''         _  _  ____  __     ___  __   _  _  ____    ____  __      __   ____  __  _  _  __    ___     ___   __   ____  ____       
        / )( \(  __)(  )   / __)/  \ ( \/ )(  __)  (_  _)/  \    / _\ (    \(  )( \/ )/  \  / __)   / __) / _\ (  __)(  __)      
        \ /\ / ) _) / (_/\( (__(  O )/ \/ \ ) _)     )( (  O )  /    \ ) D ( )(  )  /(  O )( (_ \  ( (__ /    \ ) _)  ) _)       
        (_/\_)(____)\____/ \___)\__/ \_)(_/(____)   (__) \__/   \_/\_/(____/(__)(__/  \__/  \___/   \___)\_/\_/(__)  (____)
''')

def greet_customer():
    hour = int(datetime.now().hour)
    if 0 <= hour < 12:
        print("Good Morning!")
    elif 12 <= hour < 18:
        print("Good Afternoon!")
    else:
        print("Good Evening!")


greet_customer()


def admin_additem():
    if not con.is_connected():
        print("Database not connected!")
    else:
        cur = con.cursor()
        cat = input("Enter category: ")
        item_name = input("Enter item name: ")
        price = input("Enter price: ")
        tup = (cat, item_name, price)
        cur.execute("insert into menu values(%s,%s,%s);", tup)
        con.commit()
        print(cur.rowcount, "Record inserted")


def admin_updatemenu():
    if not con.is_connected():
        print("Database not connected!")
    else:
        item_name = input("Enter the item name to update: ")
        new_price = input("Enter new price: ")
        new_category = input("Enter new category (or press Enter to keep current): ")
        try:
            if new_category:
                cur.execute("update menu set price = %s, category = %s where item = %s",
                            (new_price, new_category, item_name))
            else:
                cur.execute("update menu set price = %s where item = %s", (new_price, item_name))

            con.commit()
            print(cur.rowcount, "Record(s) updated")
        except mc.Error as e:
            print("Error updating record:", e)


def admin_deleteitem():
    if not con.is_connected():
        print("Database not connected!")
        return
    else:
        item_name = input("Enter the item name to delete: ")
        cur.execute("SELECT COUNT(*) FROM ORDEREDITEMS WHERE ITEM = %s", (item_name,))
        count = cur.fetchone()[0]
        if count > 0:
            cur.execute("DELETE FROM ORDEREDITEMS WHERE ITEM = %s", (item_name,))
            print(f"{cur.rowcount} record(s) deleted from ORDEREDITEMS.")
        cur.execute("DELETE FROM MENU WHERE ITEM = %s", (item_name,))
        con.commit()
        if cur.rowcount > 0:
            print(f"{cur.rowcount} record(s) deleted from MENU.")
        else:
            print("No item found in MENU with that name.")


def monthwise_ordersummary():
    if not con.is_connected():
        print("Database not connected!")
        return
    year = int(input("Enter year: "))
    query = """select month(orderdate) as month, count(*) as ordercount 
               from cust_order where year(orderdate) = %s group by month(orderdate);"""
    cur = con.cursor()
    cur.execute(query, (year,))
    data = cur.fetchall()
    if cur.rowcount != 0:
        months = []
        cnt = []
        colors = ['blue', 'orange', 'green', 'red', 'purple', 'brown',
                  'pink', 'gray', 'olive', 'cyan', 'magenta', 'lime']
        for row in data:
            month_num = row[0]
            cnt.append(row[1])
            month_name = datetime(2020, month_num, 1).strftime('%b')
            months.append(month_name)
        y_pos = np.arange(len(months))
        plt.bar(y_pos, cnt, align='center', color=colors[:len(months)])
        plt.xticks(y_pos, months)
        plt.ylabel('No. of Orders')
        plt.xlabel('Month')
        title = 'Monthwise Order Booking Statistics for year ' + str(year)
        plt.title(title)
        plt.show()
    else:
        print("No orders found for the specified year.")
    cur.close()


def catwise_ordersummary():
    if not con.is_connected():
        print("Database not connected!")
    else:
        query = """select category,sum(o.price*qty) 
                   from menu m, cust_order c, ordereditems o 
                   where c.orderid=o.orderid and m.item = o.item 
                   group by category"""
        cur.execute(query)
        records = cur.fetchall()
        if cur.rowcount != 0:
            cat = []
            totsales = []
            for row in records:
                cat.append(row[0])
                totsales.append(row[1])
            plt.pie(totsales, labels=cat, autopct='%.2f%%')
            title = "Categorywise Total Order Sales"
            plt.title(title)
            plt.legend()
            plt.show()


def maximum_businessday():
    query = """select orderdate, count(*) as ordercount 
               from cust_order where orderdate >= curdate() - interval 7 day 
               group by orderdate;"""
    cur.execute(query)
    data = cur.fetchall()
    if data:
        dates = [row[0] for row in data]
        counts = [row[1] for row in data]
        plt.figure(figsize=(10, 5))
        plt.bar(dates, counts, color='blue')
        plt.xlabel('Date')
        plt.ylabel('Number of Orders')
        plt.title('Number of Orders in the Last Week')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    else:
        print("No orders found in the last week.")


def init():
    try:
        if not con.is_connected():
            print("Database not connected!")
        else:
            cur = con.cursor()
            cur.execute("create database if not exists adiyogi;")
            cur.execute("use adiyogi;")
            cur.execute("""create table if not exists menu(
                            category varchar(15),
                            item varchar(35) primary key,
                            price integer)""")
            cur.execute("""create table if not exists cust_order(
                            orderid int auto_increment primary key,
                            orderdate date, 
                            custname varchar(25), 
                            totalamt int)""")
            cur.execute("""create table if not exists ordereditems(
                            orderid int, 
                            item varchar(35), 
                            price integer, 
                            qty int,
                            foreign key(orderid) references cust_order(orderid),
                            foreign key(item) references menu(item))""")
            for i in menu_1:
                cur.execute("insert into menu values(%s,%s,%s);", i)
            con.commit()
    except Exception as e:
        print("Error:", e)


def menu():
    cur.execute("select * from menu order by category;")
    data = cur.fetchall()
    table_heading = ["Cuisine", "Item", "Price"]
    print(tabulate.tabulate(data, tablefmt="grid", headers=table_heading))


def place_order():
    if not con.is_connected():
        print("Database not connected!")
    else:
        totalamt = 0
        while True:
            cur.execute("Select distinct category from menu")
            cats = cur.fetchall()
            table_heading = ["Category"]
            print(tabulate.tabulate(cats, tablefmt="grid", headers=table_heading, showindex="always"))
            ch1 = int(input("Enter Cuisine you want to eat:"))
            cat = cats[ch1][0]
            tup = (cat,)
            cur.execute("select * from menu where category=%s order by price;", tup)
            data = cur.fetchall()
            table_heading = ["Cuisine", "Item", "Price"]
            print(tabulate.tabulate(data, tablefmt="grid", headers=table_heading, showindex="always"))
            ch2 = int(input("Enter choice of item: "))
            item = data[ch2][1]
            price = data[ch2][2]
            print(item, price)

            qty = int(input("Enter Quantity: "))
            if totalamt == 0:
                custname = input("Enter your name: ")
                address = input("Enter delivery address: ")
                contact = input("Enter contact number: ")
                curdate = datetime.now()
                tup1 = (curdate, custname, totalamt)
                cur.execute("INSERT INTO CUST_ORDER(orderdate, custname, totalamt) VALUES(%s,%s,%s);", tup1)
                orderid = cur.lastrowid
                tup2 = (orderid, item, price, qty)
                cur.execute("insert into ordereditems values(%s,%s,%s,%s);", tup2)
            else:
                tup2 = (orderid, item, price, qty)
                cur.execute("insert into ordereditems values(%s,%s,%s,%s);", tup2)
            totalamt += qty * price
            ch = input("Add more items with the order (y/n):")
            if ch == 'n':
                tup3 = (totalamt, orderid)
                cur.execute("update cust_order set totalamt=%s where orderid=%s", tup3)
                con.commit()
                print("Order Placed!! OrderID:", orderid)
                print("Total Amount Payable: ", totalamt)
                print("Your order is being prepared!!!")
                break


def view_order():
    orderid = int(input("Enter OrderID:"))
    cur.execute("select * from cust_order where orderid=%s", (orderid,))
    order = cur.fetchone()
    if cur.rowcount != 0:
        invoice_width = 60
        print("|" + "=" * invoice_width + "|")
        print("|{:^60}|".format("ORDER INVOICE"))
        print("|" + "-" * 60 + "|")
        print("| {:<20} {:<38}|".format("Order ID:", orderid))
        print("| {:<20} {:<38}|".format("Order Date:", str(order[1])))
        print("| {:<20} {:<38}|".format("Customer Name:", order[2]))
        print("|" + "-" * 60 + "|")
        cur.execute("select item,price,qty,price*qty as amount from ordereditems where orderid=%s", (orderid,))
        orderdetail = cur.fetchall()
        table_heading = ["Item", "Price", "Quantity", "Amount"]
        print(tabulate.tabulate(orderdetail, tablefmt="grid", headers=table_heading))
        print("|" + "-" * 60 + "|")
        print("| {:<20} ${:<37.2f}|".format("Total Amount:", order[3]))
        print("|" + "=" * invoice_width + "|")


def cafe_details():
    print('Cafe name: AdiYogi Cafe')
    print("Contact details:- \n Phone Number : Yog's phone number \n Email ID : projcafe0@gmail.com")
    print("Cafe registration number : xxxxxGJ02024xxx")
    print("Address : Ahmedabad")


def user_type():
    cur.execute("Use ADIYOGI")
    usertype = input("Enter user type(Admin/User): ")
    if usertype.lower() == 'admin':
        pswd = input("Enter password: ")
        if pswd == '1234':
            while True:
                print('1.Initialize Database.')
                print('2.Add new items to menu.')
                print('3.Update menu item.')
                print('4.Delete menu item.')
                print('5.Show menu items.')
                print('6.Show Month-wise order summary.')
                print('7.Show Category-wise order summary.')
                print('8.Show maximum business day of the week.')
                print('9.To Exit.')
                ch = int(input("Enter your choice: "))
                if ch == 1:
                    init()
                    print('Database initialized.')
                elif ch == 2:
                    admin_additem()
                elif ch == 3:
                    admin_updatemenu()
                elif ch == 4:
                    admin_deleteitem()
                elif ch == 5:
                    menu()
                elif ch == 6:
                    monthwise_ordersummary()
                elif ch == 7:
                    catwise_ordersummary()
                elif ch == 8:
                    maximum_businessday()
                elif ch == 9:
                    break
                else:
                    print('Enter valid choice!')
        else:
            print("LOGIN PREVENTED!!!")
    elif usertype.lower() == 'user':
        cur.execute("Use ADIYOGI")
        while True:
            print("1. Display Menu")
            print("2. Place Order")
            print("3. View Order Details")
            print("4. Cafe Details")
            print("5. To Exit")
            ch = int(input("Enter your choice:"))
            if ch == 1:
                menu()
            elif ch == 2:
                place_order()
            elif ch == 3:
                view_order()
            elif ch == 4:
                cafe_details()
            elif ch == 5:
                break


menu_1 = (
    ('Sandwich', 'Grilled Sandwich', 99),
    ('Sandwich', 'Cheese Burst Sandwich', 79),
    ('Sandwich', 'Plain Sandwich', 69),
    ('Sandwich', 'Aloo Sandwich', 89),
    ('Sandwich', 'Butter Toast', 49),
    ('Burger', 'Aloo Tikki Burger', 119),
    ('Burger', 'Big Mexican Burger', 149),
    ('Burger', 'Mayoniese Burger', 139),
    ('Burger', 'Veg. Hot Burger', 249),
    ('Burger', 'Cheese Burst Burger', 159),
    ('Pizza', 'Mexican Pizza', 219),
    ('Pizza', 'Indian Style Pizza', 219),
    ('Pizza', 'Cheese Burst Pizza', 239),
    ('Pizza', 'ExtraVaganza Pizza', 269),
    ('Pizza', 'Hot and spicy Pizza', 259),
    ('Drinks', 'Lemonade', 20),
    ('Drinks', 'Fruit Punch', 79),
    ('Drinks', 'Hot Chocolate', 79),
    ('Drinks', 'Tea', 20),
    ('Drinks', 'Coffee', 30)
)

con = mc.connect(host="localhost", user="root", passwd="1234")
cur = con.cursor()
user_type()
