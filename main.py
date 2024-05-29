import random
import csv
from datetime import datetime, date, timedelta
import datetime
import tkinter as tk
import sys
import os
import getpass
import matplotlib.pyplot as plt
from time import sleep
import pytz

# Class to represent a Book with attributes and methods to generate serials and write to file
# class Book:
#     def __init__(self, pub_year, name, author, category, quantity):
#         self.pub_year = pub_year
#         self.author = author
#         self.category = category
#         self.name = name
#         self.quantity = quantity

#     # Method to generate serial numbers for books
#     def gen_serial(self):
#         self.page_count = random.randrange(100, 501)  # Random page count between 100 and 500
#         updated_serials = []
#         for i in range(int(self.quantity)):
#             prefix = str(self.pub_year)[2:4]  # Prefix based on the year
#             rand_num = random.randint(1, 9999)  # Random number for serial
#             new_serial = f"{prefix}{(self.category.upper())[:2]}{rand_num:04}"
#             updated_serials.append(new_serial)

#         self.book_serial = updated_serials
#         # Book details including serial numbers
#         self.book = {
#             "Serial No": self.book_serial,
#             "Publishing year": self.pub_year,
#             "title": self.name,
#             "author": self.author,
#             "category": self.category,
#             "quantity": self.quantity,
#             "Page count": self.page_count
#         }
#         self.fieldnames = list(self.book.keys())
#         return self.book_serial

#     # Method to write book details into a CSV file
#     def bookintofile(self):
#         self.page_count = random.randrange(100, 501)
#         updated_serials = []
#         for i in range(int(self.quantity)):
#             prefix = str(self.pub_year)[2:4]
#             rand_num = random.randint(1, 9999)
#             new_serial = f"{prefix}{(self.category.upper())[:2]}{rand_num:04}"
#             updated_serials.append(new_serial)

#         self.book_serial = updated_serials
#         self.book = {
#             "Serial No": self.book_serial,
#             "Publishing year": self.pub_year,
#             "title": self.name,
#             "author": self.author,
#             "category": self.category,
#             "quantity": self.quantity,
#             "Page count": self.page_count
#         }
#         self.fieldnames = list(self.book.keys())
#         with open("main.csv", 'a') as file:
#             writer = csv.DictWriter(file, fieldnames=self.fieldnames)
#             writer.writerow(self.book)


# Function to add books, handles both new and existing books
def addbooks(filedata):
    # Prompt the user to provide the details of the book order
    print("Please provide the details of the book order.")
    title = input("Title: ")
    flag = False

    # Check if the book already exists in the provided data
    for iter in range(len(filedata)):
        if title in filedata[iter].values():
            flag = True
            proindex = iter
            probook = filedata[iter]
            break
    
    if flag:
        # If the book exists, display its details
        print("There already exists a book with the same title:")
        print("Title: {}".format(probook["title"]))
        print("Author: {}".format(probook["author"]))
        print("Category: {}".format(probook["category"]))
        print("Quantity : {}".format(probook["quantity"]))
        choice = int(input("Press 1 if that's the book you want to add, any key otherwise: "))
        
        if choice == 1:
            # Update the quantity of the existing book
            orderqt = int(input("Enter the quantity of the order"))
            probook["quantity"] = str(int(probook["quantity"]) + orderqt)
            serialnos = retrieve_serial(probook["Serial No"])
            updated_serials = []
            #Code to generate unique serial number for each book
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
            # Add details for a new book
            ordertitle = title
            orderauthor = input("Enter the author of the book:")
            ordercategory = input("Enter the category of the book:")
            orderyop = input("Enter the year of publishing of the book:")
            orderqt = input("Enter the order quantity of this book:")
            orderpgcount = input("Enter the page count of the book:")
            bookdeets = {"title": ordertitle, "author": orderauthor, "category": ordercategory, "Publishing year": orderyop, "quantity": orderqt, "Page count": orderpgcount}
            filedata.append(bookdeets)
    else:
        # If the book does not exist, prompt to add it
        choice = int(input("It seems like there is no book with that name. Press 1 to add it or any other key to cancel the order: "))
        
        if choice == 1:
            # Add details for the new book
            ordertitle = title
            orderauthor = input("Enter the author of the book: ")
            ordercategory = input("Enter the category of the book: ")
            orderyop = input("Enter the year of publishing of the book: ")
            orderqt = input("Enter the order quantity of this book:")
            orderpgcount = input("Enter the page count of the book:")
            bookdeets = {"title": ordertitle, "author": orderauthor, "category": ordercategory, "Publishing year": orderyop, "quantity": orderqt, "Page count": orderpgcount}
            updated_serials = []
            for i in range(int(bookdeets["quantity"])):
                prefix = str(bookdeets["Publishing year"])[2:4]
                rand_num = random.randint(1, 9999)
                new_serial = f"{prefix}{(bookdeets['category'].upper())[:2]}{rand_num:04}"
                updated_serials.append(new_serial)
            bookdeets["Serial No"] = updated_serials
            filedata.append(bookdeets)
    
    # Return the updated file data
    return filedata



def print_books_details():
    books = []
    
    # Open the CSV file and read the book data into a list of dictionaries
    with open("main.csv") as file:
        reader = csv.DictReader(file)
        for var in reader:
            books.append(var)

    # Print the header for the book details table
    print("{:<12} | {:<13} | {:<40} | {:<25} | {:<20} | {:<8} | {:<6}".format(
        "Serial No", "Publishing year", "Title", "Author", "Category", "Quantity", "Pagecount"))
    print("-" * 118)

    # Print each book's details in a formatted manner
    for book_info in books:
        serial_no = book_info["Serial No"][2:6]  # Extract a portion of the serial number for display
        print("{:<12} | {:<13} | {:<40} | {:<25} | {:<20} | {:<8} | {:<6}".format(
            serial_no, book_info["Publishing year"], book_info["title"], book_info["author"],
            book_info["category"], book_info["quantity"], book_info["Page count"]))


def print_books_by_category():
    books = []
    
    # Open the CSV file and read the book data into a list of dictionaries
    with open("main.csv") as file:
        reader = csv.DictReader(file)
        for var in reader:
            books.append(var)

    # Extract unique categories from the books
    categories = set(book["category"] for book in books)

    # Iterate through each category to print books under that category
    for category in categories:
        # Print the category header
        print("                 ╔════════════════════════════════════════════════╗")
        print(f"                              Category: {category}                ")
        print("                 ╚════════════════════════════════════════════════╝")

        # Filter and sort books within the current category by publishing year in descending order
        category_books = [book for book in books if book["category"] == category]
        sorted_books = sorted(category_books, key=lambda x: x['Publishing year'], reverse=True)

        # Print the header for the book details table
        print("{:<12} | {:<13} | {:<40} | {:<25} | {:<20} | {:<8} | {:<6}".format(
            "Serial No", "Publishing year", "Title", "Author", "Category", "Quantity", "Pagecount"))
        print("-" * 118)

        # Print each book's details in a formatted manner within the current category
        for book_info in sorted_books:
            serial_no = book_info["Serial No"][2:6]  # Extract a portion of the serial number for display
            print("{:<12} | {:<13} | {:<40} | {:<25} | {:<20} | {:<8} | {:<6}".format(
                serial_no, book_info["Publishing year"], book_info["title"], book_info["author"],
                book_info["category"], book_info["quantity"], book_info["Page count"]))
        
        # Print category footer
        print("════════════════════════════════════════════════════════════════════════════════════════════════")
        print("════════════════════════════════════════════════════════════════════════════════════════════════")


def print_books_by_pubyear():
    books = []
    
    # Open the CSV file and read the book data into a list of dictionaries
    with open("main.csv") as file:
        reader = csv.DictReader(file)
        for var in reader:
            books.append(var)

    # Sort the books by publishing year in descending order
    sorted_books = sorted(books, key=lambda x: int(x["Publishing year"].strip()) if x["Publishing year"] else 2000, reverse=True)
    
    # Print the header for the book details table
    print("{:<12} | {:<13} | {:<40} | {:<25} | {:<20} | {:<8} | {:<6}".format(
        "Serial No", "Publishing year", "Title", "Author", "Category", "Quantity", "Pagecount"))
    print("-" * 118)

    # Print each book's details in a formatted manner
    for book_info in sorted_books:
        serial_no = book_info["Serial No"][2:6]  # Extract a portion of the serial number for display
        print("{:<12} | {:<13} | {:<40} | {:<25} | {:<20} | {:<8} | {:<6}".format(
            serial_no, book_info["Publishing year"], book_info["title"], book_info["author"],
            book_info["category"], book_info["quantity"], book_info["Page count"]))


def print_books_by_Quantity():
    # Initialize an empty list to store book data
    books = []
    
    # Open the CSV file and read the book data into a list of dictionaries
    with open("main.csv") as file:
        reader = csv.DictReader(file)
        for var in reader:
            books.append(var)
    
    # Sort the books by quantity in descending order
    sorted_books = sorted(books, key=lambda x: int(x['quantity']) if x['quantity'] else 0, reverse=True)
    
    # Print the header for the book details table
    print("{:<12} | {:<13} | {:<40} | {:<25} | {:<20} | {:<8} | {:<6}".format(
        "Serial No", "Publishing year", "Title", "Author", "Category", "Quantity", "Pagecount"))
    print("-" * 118)

    # Print each book's details in a formatted manner
    for book_info in sorted_books:
        serial_no = book_info["Serial No"][2:6]  # Extract a portion of the serial number for display
        print("{:<12} | {:<13} | {:<40} | {:<25} | {:<20} | {:<8} | {:<6}".format(
            serial_no, book_info["Publishing year"], book_info["title"], book_info["author"],
            book_info["category"], book_info["quantity"], book_info["Page count"]))



def retrieve_serial(str):
    # Convert the input string to a list of characters
    str = list(str)
    
    # Remove the first and last characters (opening and closing square brackets)
    str.pop(0)
    str.pop(-1)
    
    # Join the characters back into a single string
    word = "".join(str)
    
    # Initialize an empty string to store the processed serial numbers
    new = ""
    
    # Iterate through each character in the string
    for var in word:
        # Exclude the single quotes from the string
        if var != "'":
            # Append non-single-quote characters to the new string
            new += var.strip()
    
    # Split the processed string by commas to get individual serial numbers
    return new.split(",")



def removebook(filedata):
    # Initialize lists to store titles and serial numbers of books
    titles = []
    serials = []
    
    # Extract titles and serial numbers from each book in the filedata
    for var in filedata:
        titles.append(var["title"])
        serials.append(var["Serial No"])
    
    # Prompt the user for the removal method
    revchoice = input("Enter S if you want to remove by Serial Number or N otherwise: ")
    
    # If removal by book title
    if revchoice == "N":
        rembook = input("Enter the book that you wish to remove: ")
        flag = False
        
        # Search for the book in the filedata
        for iter in filedata:
            if rembook == iter["title"]:
                flag = True
                print("Book found:")
                print("Title: {}".format(iter["title"]))
                print("Author: {}".format(iter["author"]))
                print("Category: {}".format(iter["category"]))
                print("Quantity : {}".format(iter["quantity"]))
                
                # Prompt user for the quantity to remove
                remquan = int(input("Enter the quantity of the same book that you wish to remove (In stock: {} ): ".format(iter["quantity"])))
                
                # Update quantity and serial numbers accordingly
                if int(iter["quantity"]) > remquan:
                    iter["quantity"] = str(int(iter["quantity"]) - remquan)
                    serialnos = retrieve_serial(iter["Serial No"])
                    for _ in range(remquan):
                        serialnos.pop()
                    iter["Serial No"] = serialnos
                elif int(iter["quantity"]) == remquan:
                    filedata.remove(iter)
                else:
                    print("Enter a valid quantity to remove")
    
    # If removal by serial number
    elif revchoice == "S":
        num = int(input("Enter the number of books that you wish to remove:"))
        
        # Convert serial numbers in each book to lists
        for x in filedata:
            x["Serial No"] = retrieve_serial(x["Serial No"])
        
        # Remove specified number of books by serial number
        for _ in range(num):
            revserial = input("Enter the Serial No of the book that you want to remove: ")
            for dict in filedata:
                fileserial = dict["Serial No"]
                if revserial in fileserial:
                    fileserial.remove(revserial)
                    dict["quantity"] = str(int(dict["quantity"]) - 1)
                    dict["Serial No"] = fileserial
                    print("Book(s) removed Successfully")
                    break
    
    return filedata


def update_book(filedata):
    flag = 1
    while flag:
        # Prompt user to enter the name of the book to be updated
        book = input("Enter the name of the book that you want updated:")
        
        # Search for the book in the filedata
        for var in filedata:
            if var["title"] == book:
                print("Found the book, Here are its details")
                print("Serial Numbers: {}".format(var["Serial No"]))
                print("Publishing Year: {}".format(var["Publishing year"]))
                print("Title: {}".format(var["title"]))
                print("Author: {}".format(var["author"]))
                print("Category: {}".format(var["category"]))
                print("Quantity : {}".format(var["quantity"]))
                
                # Prompt user to proceed with the update
                choice = input("If you wish to proceed with the Updating press E, or press any other key otherwise: ")
                
                if choice == "E":
                    print("Here are a list of attributes that you have for a book")
                    
                    # Display available attributes for updating
                    numbering = 1
                    for key in var.keys():
                        print(f"{numbering}. {key}")
                        numbering += 1
                    
                    # Prompt user to select the attribute to be updated
                    key = input("Enter the attribute of the book that you wish to be updated:")
                    print("Here is the current value of the key: {}".format(var[key]))
                    
                    # Prompt user to enter the new value for the selected attribute
                    diffkey = input("Enter the value that you need it to change to ")
                    var[key] = diffkey
                    print("The value has been successfully changed to {}".format(diffkey))
                    
                    # Generate and update serial numbers based on the new quantity
                    updated_serials = []
                    for i in range(int(var["quantity"])):
                        prefix = str(var["Publishing year"])[2:4]
                        rand_num = random.randint(1, 9999)
                        new_serial = f"{prefix}{(var['category'].upper())[:2]}{rand_num:04}"
                        updated_serials.append(new_serial)
                    var["Serial No"] = updated_serials
                    flag = 0
                    sleep(3)
                    break
                else:
                    flag = 0
                    print("You have exited the updation")
                    break
            else:
                flag = True  # Set flag to True to continue the loop if the book is not found
    
    return filedata


def borrow_mech(filedata, altfiledata):
    # Prompt user for borrowing details
    number = int(input("Enter the number of books that you want to borrow: "))
    stud_name = input("Enter the name of the person borrowing the book: ")
    stud_contactinfo = input("Enter the contact info of the person Email Id / Phone No. :")
    
    # Iterate for each book to be borrowed
    for _ in range(number):
        serial_no = input('Enter serial No:')
        flag = False
        
        # Check if the entered serial number matches any book in the library
        for dict in filedata:
            serialist = retrieve_serial(str(dict["Serial No"]))
            
            # Check if the entered serial number matches any serial number of the book
            for serial in serialist:
                if serial == serial_no:
                    print("Found the book, Here are its details")
                    print("Serial Numbers: {}".format(dict["Serial No"]))
                    print("Publishing Year: {}".format(dict["Publishing year"]))
                    print("Title: {}".format(dict["title"]))
                    print("Author: {}".format(dict["author"]))
                    print("Category: {}".format(dict["category"]))
                    print("Quantity : {}".format(dict["quantity"]))
                    
                    # Prompt user to confirm borrowing
                    choice = input("Enter E if you wish to proceed with the borrowing of the book or any other key otherwise: ")
                    
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
                # Record borrowing details
                presentdate = datetime.date.today()
                duedate = datetime.date.today() + (datetime.timedelta(days=15))
                daysleft = (duedate - (datetime.date.today())).days
                
                # Append borrowing details to altfiledata
                altfiledata.append({
                    "Serial No": addserial,
                    "title": adddict["title"],
                    "Publishing year": adddict["Publishing year"],
                    "author": adddict["author"],
                    "category": adddict["category"],
                    "Name": stud_name,
                    "Contact info": stud_contactinfo,
                    "Issued date": presentdate,
                    "Due date": duedate,
                    "Days left": daysleft
                })
                break
    
    return filedata, altfiledata




def return_mech(filedata, altfiledata):
    # Prompt user for the number of books to return
    number = int(input("Enter how many books you want to return: "))
    
    # Iterate for each book to be returned
    for i in range(number):
        serial_no = input("Enter the serial no of the {} book: ".format(i+1))
        flag = False
        
        # Search for the book in the borrowed books data
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
                
                # Prompt user to confirm returning
                choice = input("Enter E to proceed with the returning of the book or any other key otherwise: ")
                
                if choice == "E":
                    flag = True
                    specbook = serial_no[:4]  # Extract the first 4 characters of the serial number
                    addserial = serial_no
                    altfiledata.remove(dict)  # Remove the book from the borrowed books data
                    break
                else:
                    print("You have exited the returning process")
        
        # If the book is found and the user confirms returning, update the library records
        if flag:
            for dict in filedata:
                serials = retrieve_serial(str(dict["Serial No"]))
                
                # Check if the book belongs to the same category in the library records
                if serials[0][:4] == specbook:
                    serials.append(serial_no)
                    dict["Serial No"] = serials
                    dict["quantity"] = int(dict["quantity"]) + 1  # Increase the quantity by 1
                    break
    
    return filedata, altfiledata



def find_bookserialno(filedata):
    # Prompt the user to enter a serial number
    findserial = input("Enter a Serial No: ")
    
    # Extract the first 4 characters of the serial number to identify the book
    bookserial = findserial[:4]
    
    # Initialize a flag to indicate if the book is found
    flag = False
    
    # Iterate through each book in the library data
    for dict in filedata:
        serials = retrieve_serial(dict["Serial No"])
        
        # Check if the book's serial number matches the input serial number
        if serials[0][:4] == bookserial:
            for iter in serials:
                if iter == findserial:
                    # If the book is found, print its details
                    print("Found the book, Here are its details")
                    print("Serial Numbers: {}".format(dict["Serial No"]))
                    print("Publishing Year: {}".format(dict["Publishing year"]))
                    print("Title: {}".format(dict["title"]))
                    print("Author: {}".format(dict["author"]))
                    print("Category: {}".format(dict["category"]))
                    print("Quantity : {}".format(dict["quantity"]))
                    flag = True
                    break
        if flag:
            break
    
    # If the book is not found, notify the user
    if not flag:
        print("There is no book with that Serial No")


def update_times():
    # Initialize an empty list to store student data
    student_data = []
    
    # Open the "studentsdata.csv" file and read its contents
    with open("studentsdata.csv") as file:
        # Iterate through each row in the file
        for row in file:
            # Append each row to the student_data list
            student_data.append(row)
    
    # Iterate through each dictionary in the student_data list
    for dict in student_data:
        # Calculate the number of days left until the due date
        timeleft = (dict["Due date"] - datetime.date.today()).days
        
        # Update the "Days left" value in the dictionary
        dict["Days left"] = timeleft
    
    # Call a function to write the updated student data back to the file
    studentdata_intofile(student_data)

def update_studentdata(filedata, studentdata):
    # Infinite loop to continuously prompt the user for input
    while True:
        # Display menu options
        print("╔═════════════════════════════════════════════════════════════════════════════════╗")
        print("║                         Choose What you want to Edit:                           ║")
        print("║                                                                                 ║")
        print("║   1. Serial No                                                                  ║")
        print("║   2. Student Name                                                               ║")
        print("║   3. Student Contact Info.                                                      ║")
        print("║   4. Extend Due date                                                            ║")
        print("║   5. None [Exit]                                                                ║")
        print("╚═════════════════════════════════════════════════════════════════════════════════╝")
        
        # Get user choice
        ch = int(input())
        
        # Check user choice
        if ch == 1:
            flag = 1
            # Loop to handle serial number editing
            while True:
                sr = input("Enter Serial Number to Edit:")
                for dict in studentdata:
                    if dict["Serial No"] == sr:
                        print("Serial Found!")
                        while True:
                            new_sr = input("Enter new Valid Serial no:")
                            for data in filedata:
                                for serial in data["Serial No"]:
                                    if serial == new_sr:
                                        print("Book Found! ")
                                        print("Updating data...")
                                        # Update student data with book information
                                        dict["Serial No"] = data["Serial No"]
                                        dict["Title"] = data["Title"]
                                        dict["Publishing year"] = data["Publishing year"]
                                        dict["author"] = data["author"]
                                        dict["category"] = data["category"]
                                        # Write updated student data to file
                                        studentdata_intofile(studentdata)
                                        print("Updation Successful!")
                                        flag = 0
                            if flag:
                                print("Serial Not Found In Library")
                    print("Serial no not found in Borrowed Data. Re enter")
        elif ch == 2:
            # Loop to handle student name editing
            while True:
                contact = input("Enter your contact Info. [Ph.no or Email]")
                for data in studentdata:
                    if data["Contact info"] == contact:
                        new_name = input("Enter Correct Name:")
                        # Update student name
                        data["Name"] = new_name
                        # Write updated student data to file
                        studentdata_intofile(studentdata)
                        break
                print("Contact info not found!! Re-enter.")
        elif ch == 3:
            # Loop to handle student contact info editing
            while True:
                name = input("Enter your Name:")
                for data in studentdata:
                    if data["Name"] == name:
                        new_contact = input("Enter Correct Contact Info:")
                        # Update student contact info
                        data["Contact"] = new_contact
                        # Write updated student data to file
                        studentdata_intofile(studentdata)
                        break
                print("Name not found!! Re-enter.")
        elif ch == 4:
            # Loop to handle extending due date
            while True:
                choice = int(input("Enter :\n 1:Change through Name\n2:Change through Contact Info"))
                if choice == 1:
                    search = "Name"
                elif choice == 2:
                    search = "Contact info"
                inp = input(f"Enter {search}:")
                for data in studentdata:
                    if data[search] == inp:
                        sr = input("Enter Serial No:")
                        if sr == data["Serial no"]:
                            data["Due date"] += 15
                            print("15 Days Extended!!")
                            # Write updated student data to file
                            studentdata_intofile(studentdata)
                            break
                        print("Serial not found")
                        break
                    print(f"{search} not found!")
                    break

def plot_categorydistribution():
    # Initialize an empty list to store data from the CSV file
    filedata = []
    # Open the CSV file
    with open("main.csv") as file:
        # Create a CSV reader object
        reader = csv.DictReader(file)
        # Iterate over each row in the CSV file
        for var in reader:
            # Append each row as a dictionary to the filedata list
            filedata.append(var)
    
    # Initialize an empty dictionary to store category counts
    category_counts = {}

    # Iterate over each item in the filedata list
    for item in filedata:
        # Get the category of the item
        category = item["category"]
        # If the category already exists in the category_counts dictionary, increment its count
        if category in category_counts:
            category_counts[category] += 1
        # If the category doesn't exist in the dictionary, initialize its count to 1
        else:
            category_counts[category] = 1

    # Extract categories and their respective counts
    categories = list(category_counts.keys())
    counts = list(category_counts.values())

    # Sort categories and counts based on category names
    sorted_categories_counts = sorted(zip(categories, counts), key=lambda x: x[0])
    sorted_categories, sorted_counts = zip(*sorted_categories_counts)

    # Generate positions for the bars
    positions = range(len(sorted_categories))

    # Plotting
    plt.figure(figsize=(12, 6))
    plt.bar(positions, sorted_counts, align='center')

    # Set x-axis labels to the sorted categories with 45-degree rotation for better readability
    plt.xticks(positions, sorted_categories, rotation=45, ha="right")

    # Set labels and title
    plt.xlabel('Categories')
    plt.ylabel('Counts')
    plt.title('Category Distribution')

    # Adjust layout and display the plot
    plt.tight_layout()
    plt.show()

def plot_category_wise_bar_chart():
    # Initialize an empty list to store data from the CSV file
    filedata = []
    # Open the CSV file
    with open("main.csv") as file:
        # Create a CSV reader object
        reader = csv.DictReader(file)
        # Iterate over each row in the CSV file
        for var in reader:
            # Append each row as a dictionary to the filedata list
            filedata.append(var)

    # Initialize an empty dictionary to store category counts
    category_counts = {}
    # Iterate over each item in the filedata list
    for item in filedata:
        # Get the category of the item
        category = item["category"]
        # If the category already exists in the category_counts dictionary, increment its count
        if category in category_counts:
            category_counts[category] += 1
        # If the category doesn't exist in the dictionary, initialize its count to 1
        else:
            category_counts[category] = 1

    # Extract categories and their respective counts
    categories = list(category_counts.keys())
    counts = list(category_counts.values())

    # Create a figure and axis with specified size
    plt.figure(figsize=(12, 8))
    
    # Create a bar chart with categories on x-axis and counts on y-axis
    plt.bar(categories, counts, color='skyblue')

    # Set labels and title
    plt.xlabel('Category', labelpad=20)
    plt.ylabel('Number of Books', labelpad=20)
    plt.title('Books by Category', fontsize=14)

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45, ha='right')

    # Add count labels on top of the bars
    for i, count in enumerate(counts):
        plt.text(i, count + 0.05, str(count), ha='center', va='bottom', fontsize=8)

    # Adjust layout and display the plot
    plt.tight_layout()
    plt.show()


def studentdata_intofile(filedata):
    # Write student data to a CSV file
    with open("studentsdata.csv", "w", newline="") as file:
        # Create a CSV writer object with specified fieldnames
        writer = csv.DictWriter(file, fieldnames=["Serial No", "title", "Publishing year", "author", "category", "Name", "Contact info", "Issued date", "Due date", "Days left"])
        # Write the header row
        writer.writeheader()
        # Iterate over each row in the filedata list
        for rows in filedata:
            # Write each row to the CSV file
            writer.writerow(rows)

def coldict_fileinput(filedata):
    # Write book data to a CSV file
    with open("main.csv", "w") as file:
        # Create a CSV writer object with specified fieldnames
        writer = csv.DictWriter(file, ["Serial No", "Publishing year", "title", "author", "category", "quantity", "Page count"])
        # Write the header row
        writer.writeheader()
        # Iterate over each dictionary in the filedata list
        for var in filedata:
            # Write each dictionary as a row to the CSV file
            writer.writerow(var)




def load_credentials():
    # Initialize an empty dictionary to store credentials
    credentials = {}
    # Open the file containing credentials for reading
    with open('credentials.txt', 'r') as file:
        # Iterate over each line in the file
        for line in file:
            # Split the line by ':' to separate username and password
            username, password = line.strip().split(':')
            # Add the username-password pair to the credentials dictionary
            credentials[username] = password
    # Return the dictionary containing credentials
    return credentials

def check_credentials(entered_username, entered_password):
    # Load credentials from the file
    credentials = load_credentials()
    # Check if entered username is in the credentials dictionary and the entered password matches
    if entered_username in credentials and entered_password == credentials[entered_username]:
        # Return True if credentials are valid
        return True
    else:
        # Return False if credentials are invalid
        return False


def update_times():
    # Initialize an empty list to store student data
    student_data = []
    # Open the file containing student data for reading
    with open("studentsdata.csv") as file:
        # Use DictReader to read the CSV file and parse it as dictionaries
        reader = csv.DictReader(file)
        # Iterate over each row in the CSV file
        for row in reader:
            # Append each row (student data) to the student_data list
            student_data.append(row)
    
    # Iterate over each student's data in the student_data list
    for student in student_data:
        # Extract the due date string from the student's data and remove the time part
        due = student["Due date"].replace("00:00:00", "").strip()
        # Convert the due date string to a datetime object
        due_date_str = datetime.datetime.strptime(due, '%Y-%m-%d')
        # Get the current date
        today_ = datetime.datetime.today()
        # Calculate the number of days left until the due date
        timeleft = (due_date_str - today_).days
        # Update the "Days left" field in the student's data with the calculated value
        student["Days left"] = str(timeleft)
    
    # Call the function to write the updated student data back to the file
    studentdata_intofile(student_data)



def finduserdetails(filedata):
    # Ask the user to enter the name of the user whose details they want to find
    username = input("Enter the name of the user: ")
    # Create an empty list to store the borrowed books of the user
    borrowlist = []
    # Flag to track if user details were found or not
    flag = False
    # Iterate over each record in the filedata
    for data in filedata:
        # Check if the user name matches the input username
        if data["Name"] == username:
            # If matched, append the user's record to the borrowlist
            borrowlist.append(data)
            # Set the flag to True indicating that user details were found
            flag = True
    # Check if user details were found
    if flag:
        # Iterate over each borrowed book record for the user
        for i, borrow_info in enumerate(borrowlist, 1):
            # Print the details of each borrowed book
            print("Book No: {} ".format(i))
            print("Serial Number: {}".format(borrow_info["Serial No"]))
            print("Publishing Year: {}".format(borrow_info["Publishing year"]))
            print("Title: {}".format(borrow_info["title"]))
            print("Author: {}".format(borrow_info["author"]))
            print("Category: {}".format(borrow_info["category"]))
            print("Contact information: {} ".format(borrow_info["Contact info"]))
            print("Issued Date: {} ".format(borrow_info["Issued date"]))
            print("Due date: {}".format(borrow_info["Due date"]))
            print("Days left: {}".format(borrow_info["Days left"]))
            print("=" * 40)
    else:
        # If user details were not found, print a message
        print("No user ID was found")


def update_studentdata():
    # Load data from main.csv
    filedata = []
    with open("main.csv") as file:
        reader = csv.DictReader(file)
        for var in reader:
            filedata.append(var)

    # Load student data from studentsdata.csv
    studentdata = []
    with open("studentsdata.csv") as file:
        reader = csv.DictReader(file)
        for row in reader:
            studentdata.append(row)

    while True:
        # Display menu for user choices
        print("╔═════════════════════════════════════════════════════════════════════════════════╗")
        print("║                         Choose What you want to Edit:                           ║")
        print("║                                                                                 ║")
        print("║   1. Serial No                                                                  ║")
        print("║   2. Student Name                                                               ║")
        print("║   3. Student Contact Info.                                                      ║")
        print("║   4. Extend Due date                                                            ║")
        print("║   5. None [Exit]                                                                ║")
        print("╚═════════════════════════════════════════════════════════════════════════════════╝")
        
        # Prompt user for choice
        ch = int(input())
        
        # Update Serial No
        if ch == 1:
            sr = input("Enter Serial Number to Edit: ")
            for item in studentdata:
                if item["Serial No"] == sr:
                    print("Serial Found!")
                    new_sr = input("Enter new Valid Serial no: ")
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
        
        # Update Student Name
        elif ch == 2:
            contact = input("Enter your contact Info. [Ph.no or Email]: ")
            new_name = input("Enter Correct Name: ")
            flag = 1
            for data in studentdata:
                if data["Contact info"] == contact:
                    data["Name"] = new_name
                    flag = 0
            
            if flag:
                print("Contact info not found!! Re-enter.")
            else:
                print("Updated Successfully")
        
        # Update Student Contact Info
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
        
        # Extend Due Date
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
                    # Parse date string including time information
                    original_due_date = datetime.strptime(data["Due date"], '%Y-%m-%d')
                    # Add 15 days to the date
                    new_due_date = original_due_date + timedelta(days=15)
                    # Convert the new due date back to the same format
                    data["Due date"] = new_due_date.strftime('%Y-%m-%d')
                    print("15 Days Extended!!")
                    studentdata_intofile(studentdata)
                    break
            else:
                print("Data not found or Serial no not matching.")
        
        # Exit the loop
        elif ch == 5:
            break
        
        else:
            print("Invalid choice!")


def plot_category_distribution():
    # Read data from main.csv
    filedata = []
    with open("main.csv") as file:
        reader = csv.DictReader(file)
        for var in reader:
            filedata.append(var)
    
    # Count occurrences of each category
    category_counts = {}
    for item in filedata:
        category = item["category"]
        if category in category_counts:
            category_counts[category] += 1
        else:
            category_counts[category] = 1

    categories = list(category_counts.keys())
    counts = list(category_counts.values())

    # Create pie chart
    plt.figure(figsize=(10, 8))
    wedges, texts, autotexts = plt.pie(counts, labels=categories, autopct='%1.1f%%', startangle=140, textprops=dict(fontsize=8))

    # Adjust font size of percentage labels
    for autotext in autotexts:
        autotext.set_fontsize(8)

    plt.title('Category Distribution')
    plt.tight_layout()

    plt.show()


def plot_book_quantities_bar():
    # Read data from main.csv
    filedata = []
    with open("main.csv") as file:
        reader = csv.DictReader(file)
        for var in reader:
            filedata.append(var)

    # Initialize lists to store titles and quantities
    titles = []
    quantities = []

    # Extract titles and quantities from the data
    for item in filedata:
        titles.append(item["title"])
        # If quantity is available, convert it to an integer; otherwise, set it to 0
        if item["quantity"]:
            quantities.append(int(item["quantity"]))
        else:
            quantities.append(0)

    # Create horizontal bar chart
    plt.figure(figsize=(12, 8))
    plt.barh(titles, quantities, color='skyblue', height=0.8)

    # Set labels and title
    plt.xlabel('Quantity', labelpad=20)
    plt.ylabel('Book Title', labelpad=20)
    plt.title('Book Quantities')

    # Adjust x-axis ticks
    max_quantity = max(quantities)
    plt.xticks(range(0, max_quantity + 1, max(1, max_quantity // 10)))
    plt.xlim(0, max_quantity + max_quantity // 10)

    # Adjust layout and font size
    plt.tight_layout()
    plt.yticks(fontsize=6, rotation=0, va='center')

    # Display the plot
    plt.show()

def filecleanup():
    # Initialize a list to store dictionaries
    dictolists = []

    # Read data from main.csv
    with open("main.csv") as file:
        reader = csv.DictReader(file)
        for var in reader:
            dictolists.append(var)

    # Iterate over dictionaries and remove entries with empty or "[]" Serial No
    cleaned_data = [d for d in dictolists if d["Serial No"] and d["Serial No"] != "[]"]

    # Write cleaned data back to main.csv
    coldict_fileinput(cleaned_data)

def log_entries(username, action):
    # Open log.csv file in append mode and write log entries
    with open("log.csv", "a") as file:
        writer = csv.DictWriter(file, ["Time", "Date", "Action", "Name"])
        # Get current time in Asia/Kolkata timezone
        ist = pytz.timezone('Asia/Kolkata')
        time = datetime.datetime.now(ist)
        # Write log entry with current time, date, action, and username
        writer.writerow({"Time": time.time(), "Date": datetime.date.today(), "Action": action, "Name": username})



def login():
    """
    Implements a login system with username and password verification.

    Provides a user-friendly interface with clear messages and security best practices.

    Returns:
        None (exits the program if login fails or enters the main menu on success)
    """

    log = False  # Flag to track successful login
    attempts = 0
    max_attempts = 3

    # Banner with library system branding (replace with actual branding elements)
    print("Welcome to the Terminal Login Page")
    print("╔═════════════════════════════════════════════════════════╗")
    print("║                  LIBRARY MANAGEMENT SYSTEM              ║")
    print("║                                                         ║")
    print("║                     Welcome User!                       ║")
    print("╚═════════════════════════════════════════════════════════╝")

    while attempts < max_attempts:
        entered_username = input("Enter Username: ")
        entered_password = getpass.getpass("Enter Password: ")  # Use getpass for password masking

        # Implement secure credential checking using a dedicated function (not shown)
        if check_credentials(entered_username, entered_password):
            print("╔═════════════════════════════════════════════════════════╗")
            print("║                   LOGIN SUCCESSFUL!                     ║")
            print("╚═════════════════════════════════════════════════════════╝")
            log = True
            break
        else:
            attempts += 1

            if attempts < max_attempts:
                print("╔═════════════════════════════════════════════════════════╗")
                print("║               INVALID USERNAME OR PASSWORD!             ║")
                print(f"║       TRY AGAIN ({attempts + 1}/{max_attempts})         ║")
                print("╚═════════════════════════════════════════════════════════╝")
            else:
                print("╔═════════════════════════════════════════════════════════╗")
                print("║             MAXIMUM LOGIN ATTEMPTS REACHED.             ║")
                print("║                 Exiting Program...                      ║")
                print("╚═════════════════════════════════════════════════════════╝")
                sys.exit()

    if log:
        main_menu(entered_username)  # Call the main menu function if login is successful


def main_menu(username):
    while True:
        os.system('cls')
        filecleanup()#calling function to clear any blanks in csv files
        print("╔═════════════════════════════════════════════════════════════════════════════════╗")
        print("║                        LIBRARY MANAGEMENT SYSTEM                                ║")
        print("║                                MAIN MENU                                        ║")
        print("║                            1.Book Management                                    ║")
        print("║                            2.User Management                                    ║")
        print("║                            3.Exit                                               ║")
        print("╚═════════════════════════════════════════════════════════════════════════════════╝")

        choice=int(input("Enter Your Choice:"))#asking user to input choice
        os.system('cls')
        #calling functions based on input
        if choice==1:
            book_menu(username)

        elif choice==2:
            user_menu(username)
            print()
        else:sys.exit()

def user_menu(username):
    os.system('cls')
    #reading main.csv and studentsdata.csv
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
        print("╔═════════════════════════════════════════════════════════════════════════════════╗")
        print("║                             User Management Menu                                ║")
        print("║                               Choose an option:                                 ║")
        print("║                                                                                 ║")
        print("║   1. Borrow book                                                                ║")
        print("║   2. Return a book                                                              ║")
        print("║   3. Find User details                                                          ║")
        print("║   4. Update student details                                                     ║")
        print("║   5.Exit to Main Menu                                                           ║")
        print("╚═════════════════════════════════════════════════════════════════════════════════╝")
        choice = int(input("Enter Choice Here: "))
        match choice:
            case 1:
                coldict, alcoldict = borrow_mech(coldict,alcoldict)
                coldict_fileinput(coldict)
                studentdata_intofile(alcoldict)
                log_entries(username,"Borrowing of a book")
            case 2:
                coldict, alcoldict = return_mech(coldict,alcoldict)
                coldict_fileinput(coldict)
                studentdata_intofile(alcoldict)
                log_entries(username,"Returning of a book")
            case 3:
                finduserdetails(alcoldict)
                log_entries(username,"Search user details")
                
            case 4:
                update_studentdata()
                log_entries(username,"Update user data")
            case 5:break

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
        print("╔═════════════════════════════════════════════════════════════════════════════════╗")
        print("║                             Book Management Menu                                ║")
        print("║                               Choose an option:                                 ║")
        print("║                                                                                 ║")
        print("║   1. Add a Book order                                                           ║")
        print("║   2. Update a book                                                              ║")
        print("║   3. Show all books                                                             ║")
        print("║   4. Find a book by Serial Number                                               ║")
        print("║   5. Show books Published-Year-wise                                             ║")
        print("║   6. Show books Category-Wise                                                   ║")
        print("║   7. Show books Quantity-Wise                                                   ║")
        print("║   8. Remove a book                                                              ║")
        print("║   9. Show quantity wise bar graph                                               ║")
        print("║   10.Show category wise pie chart                                               ║")
        print("║   11.Show category wise bar graph                                               ║")
        print("║   12.Exit to Main Menu                                                          ║")
        print("╚═════════════════════════════════════════════════════════════════════════════════╝")
        choice = int(input("Enter Here: "))
        os.system('cls')
        match choice:
            case 1:
                coldict = addbooks(coldict)
                coldict_fileinput(coldict)
                log_entries(username,"Received book order")
            case 2:
                coldict = update_book(coldict)
                coldict_fileinput(coldict)
                log_entries(username,"Update a book")
            case 3:
                print_books_details()
                log_entries(username,"Viewing book inventory")
            case 4:
                coldict = []
                with open("main.csv") as file:
                    reader = csv.DictReader(file)
                    for var in reader:
                        coldict.append(var)
                find_bookserialno(coldict)
                log_entries(username,"Viewing specific book")
            case 5:
                print_books_by_pubyear()
                log_entries(username,"Viewing book inventory")
            case 6:
                print_books_by_category()
                log_entries(username,"Viewing book inventory")
            case 7:
                print_books_by_Quantity()
                log_entries(username,"Viewing book inventory")
            case 8:
                coldict = removebook(coldict)
                coldict_fileinput(coldict)
                log_entries(username,"Removed a book")
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
                os.system('cls')
                break
    os.system('cls')

login()
