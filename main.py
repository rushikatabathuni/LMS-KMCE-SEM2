import random
import csv
from datetime import datetime,date,timedelta
import datetime
import tkinter as tk
import sys
import os
import getpass
import matplotlib.pyplot as plt
from time import sleep
import pytz
import webbrowser
from prettytable import PrettyTable
from colorama import Fore, Style
import smtplib
from email.message import EmailMessage
import sqlite3

def duedatealert(subject,body,to):
    msg = EmailMessage()
    msg.set_content(body)
    msg["subject"] = subject
    msg["to"] = to
    system_mail = "lsystem390@gmail.com"
    sys_pas = "owtujwataafeozec"
    msg["from"] = system_mail

    server = smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login(system_mail,sys_pas)
    server.send_message(msg)
    server.quit()


def filterduedate(filedata):
    duecross = []
    duenear3 = []
    duenear1 = []
    for var in filedata:
        if int(var["Days left"]) < 0:
            duecross.append(var)
        elif int(var["Days left"]) == 3:
            duenear3.append(var)
        elif int(var["Days left"]) == 1:
            duenear1.append(var)

    for iter in duecross:
        body = f"""The due date for {iter['title']} has expired by {abs(int(iter['Days left']))} days and your due is {abs(int(iter['Days left']))*10} rupees"""
        subject = "Regarding the book you borrowed."
        duedatealert(subject,body,iter["Contact info"])

    for iter in duenear3:
        body = f"""The due date for {iter['title']} is yet to expire in {abs(int(iter['Days left']))} days"""
        subject = "Regarding the book you borrowed"
        duedatealert(subject,body,iter["Contact info"])

    for iter in duenear1:
        body = f"""The due date for {iter['title']} is yet to expire in {abs(int(iter['Days left']))} days"""
        subject = "Regarding the book you borrowed"
        duedatealert(subject,body,iter["Contact info"])
def colorize_text(text, color=Fore.WHITE):
    return f"{color}{text}{Style.RESET_ALL}"

def search_on_google(query):
    search_url = f"https://www.google.com/search?q={query}"
    webbrowser.open_new_tab(search_url)
def amazon_search(query):
    search_url = f"https://www.amazon.in/s?k={query}"
    webbrowser.open_new_tab(search_url)



class Book:
    def __init__(self,pub_year,name,author,category,quantity):
        self.pub_year =pub_year
        self.author = author
        self.category = category
        self.name  = name
        self.quantity = quantity

    def gen_serial(self):
        self.page_count = random.randrange(100,501)
        updated_serials = []
        for i in range(int(self.quantity)):
            prefix = str(self.pub_year)[2:4]
            rand_num = random.randint(1, 9999)
            new_serial = f"{prefix}{(self.category.upper())[:2]}{rand_num:04}"
            updated_serials.append(new_serial)

        self.book_serial = updated_serials
        self.book= {"Serial No":self.book_serial,"Publishing year":self.pub_year,"title":self.name,"author":self.author,"category":self.category,"quantity":self.quantity,"Page count":self.page_count}
        self.fieldnames = list(self.book.keys())
        return self.book_serial

    def bookintofile(self):
        self.page_count = random.randrange(100,501)
        updated_serials = []
        for i in range(int(self.quantity)):
            prefix = str(self.pub_year)[2:4]
            rand_num = random.randint(1, 9999)
            new_serial = f"{prefix}{(self.category.upper())[:2]}{rand_num:04}"
            updated_serials.append(new_serial)

        self.book_serial = updated_serials
        self.book= {"Serial No":self.book_serial,"Publishing year":self.pub_year,"title":self.name,"author":self.author,"category":self.category,"quantity":self.quantity,"Page count":self.page_count}
        self.fieldnames = list(self.book.keys())
        with open("main.csv", 'a') as file:
            writer = csv.DictWriter(file, fieldnames=self.fieldnames)
            writer.writerow(self.book)


def addbooks(filedata):
    addbook = {}
    print("Please provide the details of the book order.")
    title = input("Title: ")
    flag = False
    for iter in range(len(filedata)):
        if title in filedata[iter].values():
            flag = True
            proindex = iter
            probook = filedata[iter]
            break
    if flag:
        print("There already exists a book with the same title:")
        print("Title: {}".format(probook["title"]))
        print("Author: {}".format(probook["author"]))
        print("Category: {}".format(probook["category"]))
        print("Quantity : {}".format(probook["quantity"]))
        addbook = probook
        choice = int(input("Press 1 if thats the book you want to add, any key otherwise: "))
        if choice == 1:
            orderqt = int(input("Enter the quantity of the order"))
            probook["quantity"] = str(int(probook["quantity"]) + orderqt)
            serialnos = retrieve_serial(probook["Serial No"])
            updated_serials = []
            for i in range(orderqt):
                prefix = str(probook["Publishing year"])[2:4]
                rand_num = random.randint(1, 9999)
                new_serial = f"{prefix}{(probook['category'].upper())[:2]}{rand_num:04}"
                updated_serials.append(new_serial)
            serialnos.extend(updated_serials)
            probook["Serial No"] = serialnos
            filedata[proindex] = probook
            update = True
        else:
            ordertitle = title
            orderauthor = input("Enter the author of the book:")
            ordercategory = input("Enter the category of the book:")
            orderyop = input("Enter the year of publishing of the book:")
            orderqt = input("Enter the order quantity of this book:")
            orderpgcount = input("Enter the page count of the book:")
            bookdeets = {"title":ordertitle,"author":orderauthor,"category":ordercategory,"Publishing year":orderyop,"quantity":orderqt,"Page count":orderpgcount}
            addbook = bookdeets
            filedata.append(bookdeets)
    else:
        choice = int(input("It seems like there is no book with that name press 1 to add it or any other key to cancel the order: "))
        if choice == 1:
            ordertitle = title
            orderauthor = input("Enter the author of the book: ")
            ordercategory = input("Enter the category of the book: ")
            orderyop = input("Enter the year of publishing of the book: ")
            orderqt = input("Enter the order quantity of this book:")
            orderpgcount = input("Enter the page count of the book:")
            bookdeets = {"title":ordertitle,"author":orderauthor,"category":ordercategory,"Publishing year":orderyop,"quantity":orderqt,"Page count":orderpgcount}
            addbook = bookdeets
            updated_serials = []
            for i in range(int(bookdeets["quantity"])):
                prefix = str(bookdeets["Publishing year"])[2:4]
                rand_num = random.randint(1, 9999)
                new_serial = f"{prefix}{(bookdeets['category'].upper())[:2]}{rand_num:04}"
                updated_serials.append(new_serial)
            bookdeets["Serial No"] = updated_serials
            filedata.append(bookdeets)
            print(colorize_text("Book order of ",Fore.CYAN),end=" ")
            print(colorize_text(f"{ordertitle}",Fore.YELLOW),end=" ")
            print(colorize_text("Completed Successfully!",Fore.CYAN))
        else:print(colorize_text("Book order cancelled!",Fore.CYAN))
    return filedata,addbook


def print_books_details():
    books = []
    with open("main.csv") as file:
        reader = csv.DictReader(file)
        for var in reader:
            books.append(var)

    table = PrettyTable(["Serial No", "Publishing year", "Title", "Author", "Category", "Quantity", "Pagecount"])
    table.align = "l"  # Set alignment to left

    for book_info in books:
        serial_no = book_info["Serial No"][2:6]
        table.add_row([serial_no, book_info["Publishing year"], book_info["title"], book_info["author"],
                       book_info["category"], book_info["quantity"], book_info["Page count"]])

    print(table)


def print_books_by_category():
    books = []
    with open("main.csv") as file:
        reader = csv.DictReader(file)
        for var in reader:
            books.append(var)
    categories = set(book["category"] for book in books)
    for category in categories:
        print("                 ╔════════════════════════════════════════════════╗")
        print(f"                              Category: {category}                ")
        print("                 ╚════════════════════════════════════════════════╝")
        category_books = [book for book in books if book["category"] == category]
        table = PrettyTable(["Serial No", "Publishing year", "Title", "Author", "Category", "Quantity", "Pagecount"])
        table.align = "l"  # Set alignment to left

        for book_info in category_books:
            serial_no = book_info["Serial No"][2:6]
            table.add_row([serial_no, book_info["Publishing year"], book_info["title"], book_info["author"],
                        book_info["category"], book_info["quantity"], book_info["Page count"]])

        print(table)
        print("════════════════════════════════════════════════════════════════════════════════════════════════")
        print("════════════════════════════════════════════════════════════════════════════════════════════════")


def print_books_by_pubyear():
    books = []
    with open("main.csv") as file:
        reader = csv.DictReader(file)
        for var in reader:
            books.append(var)

    sorted_books = sorted(books, key=lambda x: int(x["Publishing year"].strip()) if x["Publishing year"] else 2000, reverse=True)

    table = PrettyTable(["Serial No", "Publishing year", "Title", "Author", "Category", "Quantity", "Pagecount"])
    table.align = "l"  # Set alignment to left

    for book_info in sorted_books:
        serial_no = book_info["Serial No"][2:6]
        table.add_row([serial_no, book_info["Publishing year"], book_info["title"], book_info["author"],
                       book_info["category"], book_info["quantity"], book_info["Page count"]])

    print(table)

    

def print_books_by_Quantity():
    books = []
    with open("main.csv") as file:
        reader = csv.DictReader(file)
        for var in reader:
            books.append(var)

    sorted_books = sorted(books, key=lambda x: int(x['quantity']) if x['quantity'] else 0, reverse=True)

    table = PrettyTable(["Serial No", "Publishing year", "Title", "Author", "Category", "Quantity", "Pagecount"])
    table.align = "l"  # Set alignment to left

    for book_info in sorted_books:
        serial_no = book_info["Serial No"][2:6]
        table.add_row([serial_no, book_info["Publishing year"], book_info["title"], book_info["author"],
                       book_info["category"], book_info["quantity"], book_info["Page count"]])

    print(table)


def retrieve_serial(str):
    str = list(str)
    str.pop(0)
    str.pop(-1)
    word = "".join(str)
    new = ""
    for var in word:
        if var != "'":
            new += var.strip()
    return new.split(",")


def removebook(filedata):
    titles = []
    serials = []
    rembook = ""
    found = True
    for var in filedata:
        titles.append(var["title"])
        serials.append(var["Serial No"])
    revchoice = input("Enter S if you want to remove by Serial Number or N otherwise: ")
    if revchoice == "N":
        rembook= input("Enter the book that you wish to remove: ")
        flag = False
        for iter in filedata:
            if rembook == iter["title"]:
                flag = True
                rembook = iter["title"]
                print("Book found:")
                print("Title: {}".format(iter["title"]))
                print("Author: {}".format(iter["author"]))
                print("Category: {}".format(iter["category"]))
                print("Quantity : {}".format(iter["quantity"]))
                remquan = int(input("Enter the quantity of the same book that you wish to remove (In stock: {} ): ".format(iter["quantity"])))
                if int(iter["quantity"]) > remquan:
                    iter["quantity"] = str(int(iter["quantity"])-remquan)
                    serialnos = retrieve_serial(iter["Serial No"])
                    for _ in range(remquan):
                        serialnos.pop()
                    iter["Serial No"] = serialnos
                    print(colorize_text("Removal of ",Fore.CYAN),colorize_text(f"{remquan}",Fore.RED),colorize_text(f"{rembook}",Fore.YELLOW),colorize_text("Books Successful!",Fore.CYAN))
                elif int(iter["quantity"]) == remquan:
                    filedata.remove(iter)
                    print(colorize_text("Removal of all",Fore.CYAN),colorize_text(f"{rembook}",Fore.YELLOW),colorize_text("Books Successful!",Fore.CYAN))
                else:
                    print("Enter a valid quantity to remove")
    elif revchoice == "S":
        num = int(input("Enter the number of books that you wish to remove:"))

        for x in filedata:
            x["Serial No"] = retrieve_serial(x["Serial No"])
        for _ in range(num):
            revserial = input("Enter the Serial No of the book that you want to remove: ")
            for dict in filedata:
                fileserial = dict["Serial No"]
                if revserial in fileserial:
                    fileserial.remove(revserial)
                    dict["quantity"] = str(int(dict["quantity"])-1)
                    dict["Serial No"] = fileserial
                    rembook = dict["Name"]
                    print("Book(s) removed Successfully")
                    break
    else:print("You didn't enter either of options, exiting process!")
    return filedata,rembook

def update_book(filedata):
    action = ""
    flag=1
    while flag:
        book = input("Enter the name of the book that you want updated:")
        for var in filedata:
            if var["title"] == book:
                print("Found the book, Here are its details")
                print("Serial Numbers: {}".format(var["Serial No"]))
                print("Publishing Year: {}".format(var["Publishing year"]))
                print("Title: {}".format(var["title"]))
                print("Author: {}".format(var["author"]))
                print("Category: {}".format(var["category"]))
                print("Quantity : {}".format(var["quantity"]))
                choice = input("Enter E to proceed or any other key to exit.")
                if choice == "E":
                    print("Here are a list of attributes that you have for a book")
                    numbering = 1
                    for key in var.keys():
                        print(f"{numbering}. {key}")
                        numbering += 1
                    key = input("Enter the attribute of the book that you wish to be updated:")
                    print("Here is the current value of the key: {}".format(var[key]))
                    diffkey = input("Enter the value that you need it to change to ")
                    action = f"Updated {key} : {var[key]} to {diffkey}"
                    var[key] = diffkey
                    print("The value has been successfully changed to {}".format(diffkey))
                    updated_serials = []
                    for i in range(int(var["quantity"])):
                        prefix = str(var["Publishing year"])[2:4]
                        rand_num = random.randint(1, 9999)
                        new_serial = f"{prefix}{(var['category'].upper())[:2]}{rand_num:04}"
                        updated_serials.append(new_serial)
                    var["Serial No"] = updated_serials
                    flag=0
                    sleep(3)
                    print(colorize_text("Details of ",Fore.CYAN),colorize_text(f"{book}",Fore.YELLOW),colorize_text("updated successfully!",Fore.CYAN))
                    break
                else:
                    flag=0
                    print("You have exited the updation")
                    break
            else:flag=True
    return filedata,action


def userdataintofile(userdata):
    with open("userdata.csv","w") as file:
        writer = csv.DictWriter(file,["Name","Borrowed amount","Returned amount","fines registered","Level"])
        writer.writeheader()
        for var in userdata:
            writer.writerow(var)

def userdataupdatefines():
    userdata = []
    with open("userdata.csv") as file:
        reader = csv.DictReader(file)
        for val in reader:
            userdata.append(val)

    studentdata =[]
    with open("studentsdata.csv") as file:
        reader = csv.DictReader(file)
        for val in reader:
            studentdata.append(val)

    for iter in studentdata:
        if int(iter["Days left"] )< 0:
            for user in userdata:
                if user["Name"] == iter["Name"]:
                    user["fines registered"] = int(user["fines registered"]) + 1
                    user["Level"] = int(user["Level"]) - 2
    userdataintofile(userdata)

def borrow_mech(filedata,altfiledata):
    userdata = []
    with open("userdata.csv") as file:
        reader = csv.DictReader(file)
        for var in reader:
            userdata.append(var)


    number = int(input("Enter the number of books that you want to borrow: "))
    stud_name = input("Enter the name of the person borrowing the book: ")
    stud_contactinfo = input("Enter the Email Id of the person borrowing the book: ")
    flag = False
    for iter in userdata:
        if iter["Name"] == stud_name:
            flag = True
    if not flag:
        print("It seems that you're a new user, a one time password will be sent to th email for verification")
        otp = random.randrange(100000,1000000)
        duedatealert("One time Password for library registration",f"Here is your one time password for library registration {otp}",stud_contactinfo)
        pass_entry = int(input("Enter the one time password: "))
        if pass_entry == otp:
            print("You have been added")
            with open("userdata.csv","a") as file:
                writer = csv.DictWriter(file,["Name","Borrowed amount","Returned amount","Fines registered","Level"])
                writer.writerow({"Name":stud_name,"Borrowed amount":0,"Returned amount":0,"Fines registered":0,"Level":0})
        else:
            print("Incorrect password, You have exited the borrowing process")
            return filedata,altfiledata,{'title':"Nothing because it failed"},f"{stud_name}"


    flag = False
    for iter in userdata:
        if iter['Name'] == stud_name:
            flag = True
            borcount = 0
            for var in altfiledata:
                if var["Name"] == stud_name:
                    borcount += 1
            if int(iter["Level"]) < 3 and int(iter["Level"]) >= 0:
                if borcount < 1:
                    iter["Borrowed amount"] = int(iter["Borrowed amount"]) + 1
                else:
                    print(f"Borrow failed, as you have reached your limit for {iter['Level']} which is {(int(iter['Level'])//3)+1}")
                    return filedata,altfiledata,{'title':"Nothing, because it failed"},f"{iter['Name']}"
            elif int(iter["Level"]) // 3 >= borcount:
                print(f"Borrow failed, as you have reached your limit for {iter['Level']} which is {int(iter['Level'])//3}")
                return filedata,altfiledata,{'title':"Nothing, because it failed"},f"{iter['Name']}"
            else:
                iter["Borrowed amount"] = int(iter["Borrowed amount"]) + 1

    borrowed_book = {}
    for _ in range(number):
            serial_no = input('Enter serial No:')
            flag = False
            for dict in filedata:
                serialist = retrieve_serial(str(dict["Serial No"]))
                for serial in serialist:
                    if serial == serial_no:
                        print("Found the book, Here are its details")
                        print("Serial Numbers: {}".format(dict["Serial No"]))
                        print("Publishing Year: {}".format(dict["Publishing year"]))
                        print("Title: {}".format(dict["title"]))
                        print("Author: {}".format(dict["author"]))
                        print("Category: {}".format(dict["category"]))
                        print("Quantity : {}".format(dict["quantity"]))
                        borrowed_book = dict
                        person = stud_name
                        choice = input("Enter E to proceed or any other key to exit")
                        if choice == "E":
                            flag = True
                            addserial = serial
                            adddict = dict
                            serialist.remove(serial)
                            dict["Serial No"] = serialist
                            dict["quantity"] = str(int(dict["quantity"]) - 1)
                            break
                        else:
                            print("You have exited the borrowing process")
                if flag:

                    presentdate = date.today()
                    duedate = date.today()+(datetime.timedelta(days=15))
                    daysleft = (duedate-(date.today())).days
                    duedatealert("You Borrowed a book",f"You borrowed {adddict['title']} on {date.today()}, the due date issued is {duedate}, if you fail to return the book before the specified due date; The fine will increase by 10 rupees with each passing day",stud_contactinfo)
                    altfiledata.append({"Serial No":addserial,"title":adddict["title"],"Publishing year":adddict["Publishing year"],"author":adddict["author"],"category":adddict["category"],"Name":stud_name,"Contact info":stud_contactinfo,"Issued date":presentdate,"Due date":duedate,"Days left":daysleft})
                    break
    return filedata,altfiledata,borrowed_book,person



def return_mech(filedata,altfiledata):
    number = int(input("Enter how many books you want to return :"))
    re_book = {}
    person = ""
    userdata = []
    with open("userdata.csv") as file:
        reader = csv.DictReader(file)
        for var in reader:
            userdata.append(var)
    for _ in range(number):
        serial_no = input("Enter the serial no of the {} book: ".format(_+1))
        flag = False
        for dict in altfiledata:
            if dict["Serial No"] == serial_no:
                print("Found the book, Here are its details")
                print("Serial Number: {}".format(dict["Serial No"]))
                print("Publishing Year: {}".format(dict["Publishing year"]))
                print("Title: {}".format(dict["title"]))
                print("Author: {}".format(dict["author"]))
                print("Category: {}".format(dict["category"]))
                print("User : {}".format(dict["Name"]))
                print("Contact information: {} ".format(dict["Contact info"]))
                print("Issued Date: {} ".format(dict["Issued date"]))
                print("Due date: {}".format(dict["Due date"]))
                print("Days left: {}".format(dict["Days left"]))
                choice = input("Enter E to proceed or any other key to exit: ")
                if choice == "E":
                    flag = True
                    re_book = dict
                    person = dict["Name"]
                    specbook = serial_no[:4]
                    addserial = serial_no
                    for var in userdata:
                        if var["Name"] == dict["Name"]:
                            var["Returned amount"] = int(var["Returned amount"]) + 1
                            var['Level'] = int(var['Level']) + 1
                    altfiledata.remove(dict)
                    print(colorize_text(dict["title"],Fore.CYAN),colorize_text("returned successfully!",Fore.YELLOW))
                    break
                else:
                    print("You have exited the returning process")
        if flag:
            for dict in filedata:
                serials = retrieve_serial(str(dict["Serial No"]))
                if serials[0][:4] == specbook:
                    serials.append(serial_no)
                    dict["Serial No"] = serials
                    dict["quantity"] = int(dict["quantity"]) + 1
                    break
        userdataintofile(userdata)
    return filedata,altfiledata,re_book,person



def find_bookserialno(filedata):
    findserialbook = ""
    findserial = input("Enter a Serial No: ")
    bookserial = findserial[:4]
    flag = False
    for dict in filedata:
        serials = retrieve_serial(dict["Serial No"])
        if serials[0][:4] == bookserial:
            for iter in serials:
                if iter == findserial:
                    findserialbook = dict
                    print("Found the book, Here are its details")
                    print("Serial Numbers: {}".format(dict["Serial No"]))
                    print("Publishing Year: {}".format(dict["Publishing year"]))
                    print("Title: {}".format(dict["title"]))
                    print("Author: {}".format(dict["author"]))
                    print("Category: {}".format(dict["category"]))
                    print("Quantity : {}".format(dict["quantity"]))
                    print("══════════════════════════════════════════════════════════════════════")
                    if input("Do You want to view Book Details and similar books in your Browser?(y/n)")=="y":
                        if input("View in Google search or Amazon?(Enter g for google , any other key for Amazon)")=="g":
                            search_on_google(f"{dict['title']} by {dict['author']} {dict['Publishing year']}")
                        else:amazon_search(f"{dict['title']} by {dict['author']}")

                    flag = True
                    break
        if flag:
            break
    if not flag:
        print("There is no book by that Serial No")
    return findserialbook

def update_times():
    student_data = []
    with open("studentsdata.csv") as file:
        for row in file:
            student_data.append(row)
    for dict in student_data:
        timeleft = (dict["Due date"]-(datetime.date.today())).days
        dict["Days left"]=timeleft
    studentdata_intofile(student_data)



def plot_categorydistribution():
    filedata = []
    with open("main.csv") as file:

     reader = csv.DictReader(file)
     for var in reader:
        filedata.append(var)
    category_counts = {}

    for item in filedata:
        category = item["category"]
        if category in category_counts:
            category_counts[category] += 1
        else:
            category_counts[category] = 1

    categories = list(category_counts.keys())
    counts = list(category_counts.values())

    sorted_categories_counts = sorted(zip(categories, counts), key=lambda x: x[0])
    sorted_categories, sorted_counts = zip(*sorted_categories_counts)

    positions = range(len(sorted_categories))

    plt.figure(figsize=(12, 6))
    plt.bar(positions, sorted_counts, align='center')

    plt.xticks(positions, sorted_categories, rotation=45,ha="right")

    plt.xlabel('Categories')
    plt.ylabel('Counts')
    plt.title('Category Distribution')

    plt.tight_layout()
    plt.show()

def plot_category_wise_bar_chart():
    filedata = []
    with open("main.csv") as file:
        reader = csv.DictReader(file)
        for var in reader:
            filedata.append(var)

    category_counts = {}
    for item in filedata:
        category = item["category"]
        if category in category_counts:
            category_counts[category] += 1
        else:
            category_counts[category] = 1

    categories = list(category_counts.keys())
    counts = list(category_counts.values())

    plt.figure(figsize=(12, 8))
    plt.bar(categories, counts, color='skyblue')

    plt.xlabel('Category', labelpad=20)
    plt.ylabel('Number of Books', labelpad=20)
    plt.title('Books by Category', fontsize=14)

    plt.xticks(rotation=45, ha='right')

    for i, count in enumerate(counts):
        plt.text(i, count + 0.05, str(count), ha='center', va='bottom', fontsize=8)

    plt.tight_layout()
    plt.show()


def studentdata_intofile(filedata):
    with open("studentsdata.csv","w",newline="") as file:
        writer = csv.DictWriter(file,fieldnames = ["Serial No","title","Publishing year","author","category","Name","Contact info","Issued date","Due date","Days left"])
        writer.writeheader()
        for rows in filedata:
            writer.writerow(rows)

def coldict_fileinput(filedata):
    with open("main.csv","w") as file:
        writer = csv.DictWriter(file,["Serial No","Publishing year","title","author","category","quantity","Page count"])
        writer.writeheader()
        for var in filedata:
            writer.writerow(var)



def load_credentials():
    credentials = {}
    with open('credentials.txt', 'r') as file:
        for line in file:
            username, password = line.strip().split(':')
            credentials[username] = password
    return credentials

def check_credentials(entered_username, entered_password):
    credentials = load_credentials()
    if entered_username in credentials and entered_password == credentials[entered_username]:
        return True
    else:
        return False

def update_times():
    student_data = []
    with open("studentsdata.csv") as file:
        reader = csv.DictReader(file)
        for row in reader:
            student_data.append(row)
    for student in student_data:
        due=student["Due date"].replace("00:00:00","").strip()
        due_date_str = datetime.datetime.strptime(due,'%Y-%m-%d')
        today_ = datetime.datetime.today()
        timeleft = (due_date_str - today_).days
        student["Days left"] = str(timeleft)
    studentdata_intofile(student_data)



def finduserdetails(filedata):
    username = input("Enter the name of the user: ")
    spec_user = ""
    borrowlist = []
    flag = False
    for dict in filedata:
        if dict["Name"] == username:
            borrowlist.append(dict)
            spec_user = username
            flag = True
    if flag:
        for iter in range(len(borrowlist)):
            print("Book No: {} ".format(iter+1))
            print("Serial Number: {}".format(borrowlist[iter]["Serial No"]))
            print("Publishing Year: {}".format(borrowlist[iter]["Publishing year"]))
            print("Title: {}".format(borrowlist[iter]["title"]))
            print("Author: {}".format(borrowlist[iter]["author"]))
            print("Category: {}".format(borrowlist[iter]["category"]))
            print("Contact information: {} ".format(borrowlist[iter]["Contact info"]))
            print("Issued Date: {} ".format(borrowlist[iter]["Issued date"]))
            print("Due date: {}".format(borrowlist[iter]["Due date"]))
            print("Days left: {}".format(borrowlist[iter]["Days left"]))
            print("="*40)

    else:
        print("No user id was found")
    return spec_user

def display_borrow_data(filedata):
    borrowdata_table = PrettyTable(list(filedata[0].keys()))
    borrowdata_table.align = "l"
    for var in filedata:
        borrowdata_table.add_row(var.values())
    print(borrowdata_table)

def display_speclink():
    ratingdata = []
    with open("ratings.csv") as file:
        reader = csv.DictReader(file)
        for var in reader:
            ratingdata.append(var)
    flag = False
    specbook = input("Enter Book Name: ")
    for var in ratingdata:
        if var["Book Name"] == specbook:
            flag = True
            print(f"Link: {var['Link']}")

    if not flag:
        print("Book Not found.")


def update_studentdata():
    filedata = []
    action = ""
    with open("main.csv") as file:
        reader = csv.DictReader(file)
        for var in reader:
            filedata.append(var)

    studentdata = []
    with open("studentsdata.csv") as file:
        reader = csv.DictReader(file)
        for row in reader:
            studentdata.append(row)
    while True:
        print(colorize_text("╔═══════════════════════════════════════════════════════════════════════════════╗", Fore.YELLOW))
        print(colorize_text("║                         ", Fore.YELLOW), end="")
        print(colorize_text("Choose What you want to Edit:                         ", Fore.CYAN), end="")
        print(colorize_text("║", Fore.YELLOW))
        print(colorize_text("║                                                                               ║", Fore.YELLOW))
        print(colorize_text("║   ", Fore.YELLOW), colorize_text("1. Serial No                                                              ", Fore.CYAN), colorize_text("║", Fore.YELLOW))
        print(colorize_text("║   ", Fore.YELLOW), colorize_text("2. Student Name                                                           ", Fore.CYAN), colorize_text("║", Fore.YELLOW))
        print(colorize_text("║   ", Fore.YELLOW), colorize_text("3. Student Contact Info.                                                  ", Fore.CYAN), colorize_text("║", Fore.YELLOW))
        print(colorize_text("║   ", Fore.YELLOW), colorize_text("4. Extend Due date                                                        ", Fore.CYAN), colorize_text("║", Fore.YELLOW))
        print(colorize_text("║   ", Fore.YELLOW), colorize_text("5. None [Exit]                                                            ", Fore.CYAN), colorize_text("║", Fore.YELLOW))
        print(colorize_text("╚═══════════════════════════════════════════════════════════════════════════════╝", Fore.YELLOW))
        ch = int(input())
        if ch == 1:
            sr = input("Enter Serial Number to Edit: ")
            for item in studentdata:
                if item["Serial No"] == sr:
                    print("Serial Found!")
                    new_sr = input("Enter new Valid Serial no: ")
                    action = f"Changed borrowed serial no: {sr} to {new_sr}"
                    for data in filedata:
                        if data["Serial No"] == new_sr:
                            print("Book Found! ")
                            print("Updating data...")
                            item.update(data)

                            print("Updation Successful!")
                            break
                    else:
                        print("Serial Not Found In Library")
                    break
            else:
                print("Serial no not found in Borrowed Data. Re-enter")
        elif ch == 2:
            contact = input("Enter your contact Info. [Ph.no or Email]: ")
            new_name = input("Enter Correct Name: ")
            flag=1

            for data in studentdata:
                if data["Contact info"] == contact:
                    action = f"Changed Contact info: {contact} to {new_name}"
                    data["Name"] = new_name
                    flag=0
            
            if flag:
                print("Contact info not found!! Re-enter.")
            else:print("Updated Successfully")
        elif ch == 3:
            name = input("Enter your Name: ")
            for data in studentdata:
                if data["Name"] == name:
                    new_contact = input("Enter Correct Contact Info: ")
                    data["Contact info"] = new_contact
                    print("Data Updated Successfully!")
                    break
            else:
                print("Name not found!! Re-enter.")
        elif ch == 4:
            choice = int(input("Enter:\n1: Change through Name\n2: Change through Contact Info: "))
            if choice == 1:
                search = "Name"
            elif choice == 2:
                search = "Contact info"
            else:
                print("Invalid choice!")
                continue

            inp = input(f"Enter {search}: ")
            sr = input("Enter Serial No: ")
            for data in studentdata:
                if data[search] == inp and data['Serial No'] == sr:
                    original_due_date = datetime.strptime(data["Due date"], '%Y-%m-%d')
                    new_due_date = original_due_date + timedelta(days=15)
                    data["Due date"] = new_due_date.strftime('%Y-%m-%d')
                    print("15 Days Extended!!")
                    studentdata_intofile(studentdata)
                    update_times()
                    break
            else:
                print("Data not found or Serial no not matching.")
        elif ch == 5:
            print("Exiting...")
            break
        else:
            print("Invalid choice!")

def view_userdetails():
    userdata = []
    with open("userdata.csv") as file:
        reader = csv.DictReader(file)
        for var in reader:
            userdata.append(var)

    usertable = PrettyTable(["Name","Borrowed amount","Returned amount","fines registered","Level"])
    userdata = sorted(userdata,key= lambda x:x["Level"],reverse=True)
    for iter in userdata:
        usertable.add_row([iter['Name'],iter['Borrowed amount'],iter['Returned amount'],iter['fines registered'],iter['Level']])
    print(usertable)


def plot_category_distribution():
    filedata = []
    with open("main.csv") as file:
     reader = csv.DictReader(file)
     for var in reader:
        filedata.append(var)
    category_counts = {}

    for item in filedata:
        category = item["category"]
        if category in category_counts:
            category_counts[category] += 1
        else:
            category_counts[category] = 1

    categories = list(category_counts.keys())
    counts = list(category_counts.values())

    plt.figure(figsize=(10, 8))
    wedges, texts, autotexts = plt.pie(counts, labels=categories, autopct='%1.1f%%', startangle=140, textprops=dict(fontsize=8))

    for autotext in autotexts:
        autotext.set_fontsize(8)

    plt.title('Category Distribution')
    plt.tight_layout()

    plt.show()

def plot_book_quantities_bar():
    filedata = []
    with open("main.csv") as file:
        reader = csv.DictReader(file)
        for var in reader:
            filedata.append(var)

    titles = []
    quantities = []

    for item in filedata:
        titles.append(item["title"])
        if item["quantity"]:
            quantities.append(int(item["quantity"]))
        else:
            quantities.append(0)

    plt.figure(figsize=(12, 8))
    plt.barh(titles, quantities, color='skyblue', height=0.8)

    plt.xlabel('Quantity', labelpad=20)
    plt.ylabel('Book Title', labelpad=20)
    plt.title('Book Quantities')


    max_quantity = max(quantities)
    plt.xticks(range(0, max_quantity + 1, max(1, max_quantity // 10)))
    plt.xlim(0, max_quantity + max_quantity // 10)

    plt.tight_layout()
    plt.yticks(fontsize=6, rotation=0, va='center')

    plt.show()

def filecleanup():
    dictolists = []
    with open("main.csv") as file:
        reader = csv.DictReader(file)
        for var in reader:
            dictolists.append(var)

    for dicts in dictolists:
        if (not dicts["Serial No"]) or dicts["Serial No"]=="[]":
            dictolists.remove(dicts)

    coldict_fileinput(dictolists)

def studfile_cleanup():
    dictolists = []
    with open("studentsdata.csv") as file:
        reader = csv.DictReader(file)
        for var in reader:
            dictolists.append(var)

    for dicts in dictolists:
        if (not dicts["Serial No"]) or dicts["Serial No"]=="[]":
            dictolists.remove(dicts)

    studentdata_intofile(dictolists)

def log_entries(username,action):
    main = sqlite3.connect("log.db")
    cur = main.cursor()
    ist = pytz.timezone('Asia/Kolkata')
    time = datetime.datetime.now(ist)
    entry = [str(time.time()),str(datetime.date.today()),action,username]
    cur.execute("INSERT INTO logatt VALUES (?,?,?,?)",entry)
    main.commit()
    main.close()
def display_logentries():
    net = sqlite3.connect("log.db")
    cur = net.cursor()
    cur.execute("SELECT * FROM logatt")
    logdata= cur.fetchall()
    logentry_table = PrettyTable(["Time","Date","Action","Name"])
    for ele in logdata:
        logentry_table.add_row([ele[0],ele[1],ele[2],ele[3]])
    print(logentry_table)
    net.commit()
    net.close()


def displayselective_logentries():
    net = sqlite3.connect("log.db")
    cur = net.cursor()
    cur.execute("SELECT * FROM logatt")
    logdata = cur.fetchall()
    admin = input("Enter the name of the librarian: ")
    logtable = PrettyTable(["Time","Date","Action"])
    for var in logdata:
        if var[3] == admin:
            logtable.add_row([var[0],var[1],var[2]])
    print(logtable)

def print_booksbasedpopularity():
    ratingdata = []
    with open("ratings.csv") as file:
        reader = csv.DictReader(file)
        for var in reader:
            ratingdata.append(var)

    ratingdata = sorted(ratingdata,key= lambda x:float(x["Popularity Quotient"].format(".2f")),reverse=True)
    poptable = PrettyTable(["Book Name","Author","Rating","Popularity Quotient","Link"])
    for var in ratingdata:
        poptable.add_row([var['Book Name'],var['Author'],var['Rating'],var['Popularity Quotient'],var['Link']])
    print(poptable)

def display_bookratingranking():
    ratingdata = []
    with open("ratings.csv") as file:
        reader = csv.DictReader(file)
        for var in reader:
            ratingdata.append(var)
    ratingdata = sorted(ratingdata,key = lambda x:float(x['Rating']),reverse = True)
    ratingtable= PrettyTable(["Book Name","Author","Rating","Popularity Quotient","Link"])
    for var in ratingdata:
        ratingtable.add_row([var['Book Name'],var['Author'],var['Rating'],var['Popularity Quotient'],var['Link']])
    print(ratingtable)

def duedate_reminder(filedata):
    for iter in range(len(filedata)):
        if int(filedata[iter]["Days left"]) <= 0:
            print("Book No: {} ".format(iter+1))
            print("Serial Number: {}".format(filedata[iter]["Serial No"]))
            print("Publishing Year: {}".format(filedata[iter]["Publishing year"]))
            print("Title: {}".format(filedata[iter]["title"]))
            print("Author: {}".format(filedata[iter]["author"]))
            print("Category: {}".format(filedata[iter]["category"]))
            print("Contact information: {} ".format(filedata[iter]["Contact info"]))
            print("Issued Date: {} ".format(filedata[iter]["Issued date"]))
            print("Due date: {}".format(filedata[iter]["Due date"]))
            print("Days left: {}".format(filedata[iter]["Days left"]))
            print("="*40)


def login():
    log=False
    attempts = 0
    max_attempts = 3

    print("Welcome to the Terminal Login Page")
    print(colorize_text("╔═══════════════════════════════════════════════════════════════════════════════╗", Fore.YELLOW))
    print(colorize_text("║                        ", Fore.YELLOW), colorize_text("LIBRARY MANAGEMENT SYSTEM                            ", Fore.CYAN), colorize_text("║", Fore.YELLOW))
    print(colorize_text("║                     ", Fore.YELLOW), colorize_text("Welcome to the Terminal Login Page                      ", Fore.CYAN), colorize_text("║", Fore.YELLOW))
    print(colorize_text("╚═══════════════════════════════════════════════════════════════════════════════╝", Fore.YELLOW))

    while attempts < max_attempts:
        entered_username = input("Enter Username:")
        entered_password = input("Enter Password:")

        if check_credentials(entered_username, entered_password):
            # os.system('cls')
            print(colorize_text("╔═══════════════════════════════════════════════════════════════════════════════╗", Fore.YELLOW))
            print(colorize_text("║                        ", Fore.YELLOW), colorize_text("LOGIN SUCCESSFUL!!                                   ", Fore.CYAN), colorize_text("║", Fore.YELLOW))
            print(colorize_text("╚═══════════════════════════════════════════════════════════════════════════════╝", Fore.YELLOW))
            log=True
            break
        else:
            attempts += 1
            if attempts < max_attempts:
                print(colorize_text("╔═══════════════════════════════════════════════════════════════════════════════╗", Fore.YELLOW))
                print(colorize_text("║                     ", Fore.YELLOW), colorize_text("INVALID USERNAME OR PASSWORD!!                          ", Fore.CYAN), colorize_text("║", Fore.YELLOW))
                print(colorize_text("║                     ", Fore.YELLOW), colorize_text(f"TRY AGAIN({attempts+1}/{max_attempts})                                          ", Fore.CYAN), colorize_text("║", Fore.YELLOW))
                print(colorize_text("╚═══════════════════════════════════════════════════════════════════════════════╝", Fore.YELLOW))  
            else:
                print(colorize_text("╔═══════════════════════════════════════════════════════════════════════════════╗", Fore.YELLOW))
                print(colorize_text("║              ", Fore.YELLOW), colorize_text("MAXIMUM LOGIN ATTEMPTS REACHED. EXITING PROGRAM.               ", Fore.CYAN), colorize_text("║", Fore.YELLOW))
                print(colorize_text("╚═══════════════════════════════════════════════════════════════════════════════╝", Fore.YELLOW))
                sys.exit()
    if log:main_menu(entered_username)

def main_menu(username):
    while True:
        # os.system('cls')
        filecleanup()
        studfile_cleanup()
        print(colorize_text("╔═══════════════════════════════════════════════════════════════════════════════╗", Fore.YELLOW))
        print(colorize_text("║                        ", Fore.YELLOW), colorize_text("LIBRARY MANAGEMENT SYSTEM                            ", Fore.CYAN), colorize_text("║", Fore.YELLOW))
        print(colorize_text("║                                ", Fore.YELLOW), colorize_text("MAIN MENU                                    ", Fore.CYAN), colorize_text("║", Fore.YELLOW))
        print(colorize_text("║                            ", Fore.YELLOW), colorize_text("1.Book Management                                ", Fore.CYAN), colorize_text("║", Fore.YELLOW))
        print(colorize_text("║                            ", Fore.YELLOW), colorize_text("2.User Management                                ", Fore.CYAN), colorize_text("║", Fore.YELLOW))
        print(colorize_text("║                            ", Fore.YELLOW), colorize_text("3.Exit                                           ", Fore.CYAN), colorize_text("║", Fore.YELLOW))
        print(colorize_text("╚═══════════════════════════════════════════════════════════════════════════════╝", Fore.YELLOW))

        choice=int(input("Enter Your Choice:"))
        # os.system('cls')
        if choice==1:
            book_menu(username)

        elif choice==2:
            user_menu(username)
            print()
        else:sys.exit()

def user_menu(username):

    # os.system('cls')
    coldict = []
    with open("main.csv") as file:
        reader = csv.DictReader(file)
        for var in reader:
            coldict.append(var)

    alcoldict = []
    with open("studentsdata.csv") as file:
        reader = csv.DictReader(file)
        for row in reader:
            alcoldict.append(row)
    while True:
        update_times()
        print(colorize_text("╔═══════════════════════════════════════════════════════════════════════════════╗", Fore.YELLOW))
        print(colorize_text("║                             ", Fore.YELLOW), colorize_text("User Management Menu                            ", Fore.CYAN), colorize_text("║", Fore.YELLOW))
        print(colorize_text("║                               ", Fore.YELLOW), colorize_text("Choose an option:                             ", Fore.CYAN), colorize_text("║", Fore.YELLOW))
        print(colorize_text("║                                                                               ║", Fore.YELLOW))
        print(colorize_text("║   ", Fore.YELLOW), colorize_text("1. Borrow book                                                            ", Fore.CYAN), colorize_text("║", Fore.YELLOW))
        print(colorize_text("║   ", Fore.YELLOW), colorize_text("2. Return a book                                                          ", Fore.CYAN), colorize_text("║", Fore.YELLOW))
        print(colorize_text("║   ", Fore.YELLOW), colorize_text("3. Find User details                                                      ", Fore.CYAN), colorize_text("║", Fore.YELLOW))
        print(colorize_text("║   ", Fore.YELLOW), colorize_text("4. Update student details                                                 ", Fore.CYAN), colorize_text("║", Fore.YELLOW))
        print(colorize_text("║   ", Fore.YELLOW), colorize_text("5. Due date reminders                                                     ", Fore.CYAN), colorize_text("║", Fore.YELLOW))
        print(colorize_text("║   ", Fore.YELLOW), colorize_text("6. Check Borrow data                                                     ", Fore.CYAN), colorize_text(" ║", Fore.YELLOW))
        print(colorize_text("║   ", Fore.YELLOW), colorize_text("7. Check User Ranking                                                     ", Fore.CYAN), colorize_text("║", Fore.YELLOW))
        print(colorize_text("║   ", Fore.YELLOW), colorize_text("8. Check book based on global popularity                                  ", Fore.CYAN), colorize_text("║", Fore.YELLOW))
        print(colorize_text("║   ", Fore.YELLOW), colorize_text("9. Get Specific book link                                                 ", Fore.CYAN), colorize_text("║", Fore.YELLOW))
        print(colorize_text("║   ", Fore.YELLOW), colorize_text("10. Check books based on global ratings                                  ", Fore.CYAN), colorize_text(" ║", Fore.YELLOW))
        print(colorize_text("║   ", Fore.YELLOW), colorize_text("11. Exit to Main menu                                                     ", Fore.CYAN), colorize_text("║", Fore.YELLOW))
        print(colorize_text("╚═══════════════════════════════════════════════════════════════════════════════╝", Fore.YELLOW))
        choice = int(input("Enter Choice Here: "))
        match choice:
            case 1:
                coldict, alcoldict, obj,b_person = borrow_mech(coldict,alcoldict)
                coldict_fileinput(coldict)
                studentdata_intofile(alcoldict)
                log_entries(username,f"{b_person} Borrowed {obj['title']}")
            case 2:
                coldict, alcoldict,reobj, r_person = return_mech(coldict,alcoldict)
                coldict_fileinput(coldict)
                studentdata_intofile(alcoldict)
                log_entries(username,f"{r_person} returned {reobj['title']}")
            case 3:
                spec_user = finduserdetails(alcoldict)
                log_entries(username,f"Searched {spec_user} details")
            case 4:
                updateuser = update_studentdata()
                log_entries(username,"Update user data")
            case 5:
                log_entries(username,"Checked due dates for specific user. ")
                duedate_reminder(alcoldict)
            case 6:
                display_borrow_data(alcoldict)
            case 7:
                view_userdetails()
            case 8:
                print_booksbasedpopularity()
            case 9:
                display_speclink()
            case 10:
                display_bookratingranking()
            case 11:
                break

def book_menu(username):
    coldict = []
    with open("main.csv") as file:
        reader = csv.DictReader(file)
        for var in reader:
            coldict.append(var)

    alcoldict = []
    with open("studentsdata.csv") as file:
        reader = csv.DictReader(file)
        for row in reader:
            alcoldict.append(row)
    update_times()
    while True:
        filecleanup()
        update_times()
        sleep(2)
        print(colorize_text("╔═══════════════════════════════════════════════════════════════════════════════╗", Fore.YELLOW))
        print(colorize_text("║                             ", Fore.YELLOW), colorize_text("Book Management Menu                            ", Fore.CYAN), colorize_text("║", Fore.YELLOW))
        print(colorize_text("║                               ", Fore.YELLOW), colorize_text("Choose an option:                             ", Fore.CYAN), colorize_text("║", Fore.YELLOW))
        print(colorize_text("║                                                                               ║", Fore.YELLOW))
        print(colorize_text("║   ", Fore.YELLOW), colorize_text("1. Add a Book order                                                       ", Fore.CYAN), colorize_text("║", Fore.YELLOW))
        print(colorize_text("║   ", Fore.YELLOW), colorize_text("2. Update a book                                                          ", Fore.CYAN), colorize_text("║", Fore.YELLOW))
        print(colorize_text("║   ", Fore.YELLOW), colorize_text("3. Show all books                                                         ", Fore.CYAN), colorize_text("║", Fore.YELLOW))
        print(colorize_text("║   ", Fore.YELLOW), colorize_text("4. Find a book by Serial Number                                           ", Fore.CYAN), colorize_text("║", Fore.YELLOW))
        print(colorize_text("║   ", Fore.YELLOW), colorize_text("5. Show books Published-Year-wise                                         ", Fore.CYAN), colorize_text("║", Fore.YELLOW))
        print(colorize_text("║   ", Fore.YELLOW), colorize_text("6. Show books Category-Wise                                               ", Fore.CYAN), colorize_text("║", Fore.YELLOW))
        print(colorize_text("║   ", Fore.YELLOW), colorize_text("7. Show books Quantity-Wise                                               ", Fore.CYAN), colorize_text("║", Fore.YELLOW))
        print(colorize_text("║   ", Fore.YELLOW), colorize_text("8. Remove a book                                                          ", Fore.CYAN), colorize_text("║", Fore.YELLOW))
        print(colorize_text("║   ", Fore.YELLOW), colorize_text("9. Show quantity wise bar graph                                           ", Fore.CYAN), colorize_text("║", Fore.YELLOW))
        print(colorize_text("║   ", Fore.YELLOW), colorize_text("10.Show category wise pie chart                                           ", Fore.CYAN), colorize_text("║", Fore.YELLOW))
        print(colorize_text("║   ", Fore.YELLOW), colorize_text("11.Show category wise bar graph                                           ", Fore.CYAN), colorize_text("║", Fore.YELLOW))
        print(colorize_text("║   ", Fore.YELLOW), colorize_text("12.Show Logs                                                              ", Fore.CYAN), colorize_text("║", Fore.YELLOW))
        print(colorize_text("║   ", Fore.YELLOW), colorize_text("13.Show specific logs                                                     ", Fore.CYAN), colorize_text("║", Fore.YELLOW))
        print(colorize_text("║   ", Fore.YELLOW), colorize_text("14.Exit to Main Menu                                                      ", Fore.CYAN), colorize_text("║", Fore.YELLOW))
        print(colorize_text("╚═══════════════════════════════════════════════════════════════════════════════╝", Fore.YELLOW))
        choice = int(input("Enter Here: "))
        # os.system('cls')
        match choice:
            case 1:
                coldict,addbook = addbooks(coldict)
                coldict_fileinput(coldict)
                log_entries(username,f"Received {addbook['title']} order")
            case 2:
                coldict,updateaction = update_book(coldict)
                coldict_fileinput(coldict)
                log_entries(username,f"{updateaction}")
            case 3:
                print_books_details()
                log_entries(username,"Viewing book inventory")
            case 4:
                coldict = []
                with open("main.csv") as file:
                    reader = csv.DictReader(file)
                    for var in reader:
                        coldict.append(var)
                findbook = find_bookserialno(coldict)
                log_entries(username,f"Viewing {findbook['title']}")
            case 5:
                print_books_by_pubyear()
                log_entries(username,"Viewing book inventory publishing year wise")
            case 6:
                print_books_by_category()
                log_entries(username,"Viewing book inventory category wise")
            case 7:
                print_books_by_Quantity()
                log_entries(username,"Viewing book inventory quantity wise")
            case 8:
                coldict,rembook = removebook(coldict)
                coldict_fileinput(coldict)
                log_entries(username,f"Removed {rembook}")
            case 9:
                plot_book_quantities_bar()
                log_entries(username,"Viewing book inventory graphs")
            case 10:
                plot_category_distribution()
                log_entries(username,"Viewing book inventory graphs")
            case 11:
                plot_categorydistribution()
                log_entries(username,"Viewing book inventory graphs")
            case 12:
                display_logentries()
            case 13:
                displayselective_logentries()
            case 14:
                # os.system('cls')
                break
    # os.system('cls')

def due_datetimer():
    with open("duedatetimer.txt") as file:
        date = file.readline()
    date = int(date[-2] + date[-1])
    curdate = datetime.date.today()
    if date != curdate.day:
        with open("duedatetimer.txt","w") as file:
            file.writelines(f"{datetime.date.today()}")
        alcoldict = []
        with open("studentsdata.csv") as file:
            reader = csv.DictReader(file)
            for row in reader:
                alcoldict.append(row)
        filterduedate(alcoldict)

def finetimer():
    with open("finetimer.txt") as file:
        date = file.readline()
        date = int(date[-2] +date[-1])
        curdate = datetime.date.today()
        if date != curdate.day:
            with open("finetimer.txt","w") as file:
                file.writelines(f"{datetime.date.today()}")
            userdataupdatefines()


finetimer()
due_datetimer()
login()






#
# RESET MAIN FILE
# coldict = []
# with open("backup.csv") as file:
#     reader = csv.DictReader(file)
#     for var in reader:
#         coldict.append(var)
#
# with open("main.csv","w") as file:
#     writer = csv.DictWriter(file,["Serial No","Publishing year","title","author","category","quantity","Page count"])
#     writer.writeheader()
#     for var in coldict:
#         writer.writerow(var)
























