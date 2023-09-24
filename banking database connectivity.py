from tabulate import tabulate
import mysql.connector
import random

con = mysql.connector.connect(host="localhost", user="root", password="Pass@1234", database="dbase1")

def insert(acc_num, name, Address, Phone, Govt_id, Amount):
    res = con.cursor()
    sql = "insert into bankingconnector (acc_num, name, Address, Phone, Govt_id, Amount) values (%s, %s, %s, %s, %s, %s)"
    user = (acc_num, name, Address, Phone, Govt_id, Amount)
    res.execute(sql, user)
    con.commit()
    print("Data Insert Success")

def update(name, Address, Phone, Govt_id, id):
    res = con.cursor()
    sql = "update bankingconnector set name = %s, Address = %s, Phone = %s, Govt_id = %s where id = %s"
    user = (name, Address, Phone, Govt_id, id)
    res.execute(sql, user)
    con.commit()
    print("Data Update Success")

def select():
    res = con.cursor()
    sql = "SELECT * from bankingconnector"
    res.execute(sql)
    result = res.fetchall()
    print(tabulate(result, headers=["Id", "acc_num", "name", "Address", "Phone", "Govt_id", "Amount"]))

def delete(id):
    res = con.cursor()
    sql = "delete from bankingconnector where id = %s"
    user = (id,)
    res.execute(sql, user)
    con.commit()
    print("Data Delete Success")

def amount_verify(acc_num):
    res = con.cursor()
    sql = "SELECT Amount from bankingconnector where acc_num = %s"
    res.execute(sql, (acc_num,))
    result = res.fetchone()
    if result:
        return result[0]
    else:
        return None

def total():
    while True:
        choice2 = int(input("1. New customer\n2. Existing customer\n3. Update\n4. Select the table\n5. Delete data\n6. Exit\nEnter choice: "))
        if choice2 == 1:
            acc_num = str(random.randint(10000, 99999))
            name = input("Enter your name: ")
            Address = input("Enter your Address: ")
            Phone = input("Enter your Phone: ")
            Govt_id = input("Enter your Govt id: ")
            Amount = int(input("Enter your Amount: "))
            print("Your account number is:", acc_num)
            print("Account created")
            print("********************************************************")
            insert(acc_num, name, Address, Phone, Govt_id, Amount)

        elif choice2 == 2:
            res = con.cursor()
            sql = "SELECT * from bankingconnector"
            res.execute(sql)
            result = res.fetchall()

            list1 = []
            list2 = []
            
            for i in result:
                list1.append(list(i))

            for j in list1:
                list2.append(j[1])

            acc_num = input("Enter your account number: ")
            while acc_num not in list2 or not acc_num.isdigit() or len(acc_num) != 5:
                print("Please check your account number")
                acc_num = input("Enter your account number:")

            if acc_num in list2:
                print("Account found")

            choice = int(input("1. Check balance\n2. Withdraw\n3. Deposit\nEnter choice: "))

            if choice == 1:
                balance = amount_verify(acc_num)
                if balance is not None:
                    print("Available balance:", balance)
                else:
                    print("Account not found")
                print("********************************************************")

            elif choice == 2:
                balance = amount_verify(acc_num)
                if balance is not None:
                    amt = int(input("Enter amount to withdraw: "))
                    if amt > balance:
                        print("Insufficient balance. Your available balance is:", balance)
                    else:
                        new_balance = balance - amt
                        # Update the account balance in the database
                        res = con.cursor()
                        sql = "UPDATE bankingconnector SET Amount = %s WHERE acc_num = %s"
                        res.execute(sql, (new_balance, acc_num))
                        con.commit()
                        print("Withdraw successful")
                        print("Available Balance:", new_balance)
                else:
                    print("Account not found")

            elif choice == 3:
                amt = int(input("Enter amount to deposit: "))
                balance = amount_verify(acc_num)
                if balance is not None:
                    new_balance = balance + amt
                    # Update the account balance in the database
                    res = con.cursor()
                    sql = "UPDATE bankingconnector SET Amount = %s WHERE acc_num = %s"
                    res.execute(sql, (new_balance, acc_num))
                    con.commit()
                    print("Deposit successful")
                    print("Available Balance:", new_balance)
                else:
                    print("Account not found")

        elif choice2 == 3:
            id = input("Enter which id you want to update: ")
            name = input("Enter your name: ")
            Address = input("Enter your Address: ")
            Phone = input("Enter your Phone: ")
            Govt_id = input("Enter your Govt id: ")
            update(name, Address, Phone, Govt_id, id)

        elif choice2 == 4:
            select()

        elif choice2 == 5:
            id = input("Enter which ID you want to Delete: ")
            delete(id)

        elif choice2 == 6:
            print("*****************************Thank you For Banking With us*****************************")
            break

total()
