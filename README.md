# LIBRARY MANAGEMENT SYSTEM

## Project Description

The Library Management System is a comprehensive command-line application designed to streamline the operations of a library. It provides an intuitive interface for managing books,and tracking book borrowing and returning activities.

The system is built using Python and uses various libraries such as `csv` for data handling, `matplotlib` for data visualization, `pytz` for time zone handling, `datetime` module , `random` to  generate serial numbers , `sys`and `os` for clean output in the terminal  

The application's core functionality revolves around three main components:

1. **Book Management**: This module allows library administrators to add new book orders, update existing book details, remove books from the inventory, and search for specific books based serial numbers or names. It also generates unique serial numbers for each book, ensuring efficient tracking and organisation.

2. **User Management**: This module handles user accounts and book borrowing/returning activities. Users can borrow and return books, find their own details (borrowed books, due dates, etc.), and update their personal information (name, contact info, extend due dates).

3. **Data Visualization and Reporting**: The system provides powerful data visualization capabilities, enabling library administrators to gain insights into the book inventory. It can generate category-wise distribution charts (pie charts and bar charts), as well as book quantity distribution charts (horizontal bar charts).

The application also includes features such as user authentication with username and password, ensuring that only authorized personnel can access and manage the system. Additionally, it maintains a log of user actions (borrowing, returning, updating, etc.) with timestamps for auditing and record-keeping purposes.


## Table of Contents

* Features
* Installation
* Usage
* Contributing
* Credits
* License

## 1.Features
Detailed Menus are printed in every case.
### Login Page
![](./screenshots/login.png)
### Main Menu
![](./screenshots/mainmenu.png)
### Book Menu
![](./screenshots/bookmenu.png)
### User Menu
![](./screenshots/usermenu.png)
### Update Student Details
![](./screenshots/studentdetails.png)

Printing Details of books in specific orders
We can even update book details, student details.
The code contails logs, in which we can see which user made what changes.
We even used web scraping to extract the rating of books from `goodreads.com` and created a popularity quotient to arrange the books on these ratings.


## 2.Installation
### Clone the Repository

```bash
 git clone https://github.com/rushikatabathuni/LMS-KMCE-SEM2
```
## 3.Navigate to Directory
```bash
cd <your directory>
```
## 4.Install the Required Dependencies
```bash
pip install -r requirements.txt
```


## Usage

### 1. Run the `main.py` script.
### 2. Enter your username and password when prompted to log in.
### 3. Follow the on-screen instructions to navigate through the menu options and perform various actions.
## Authors
#### 1. [K.RUSHI](https://github.com/rushikatabathuni)  [23P81A0528]

#### 2. [VIREN LOKA](https://github.com/VirenLoka)[23P81A6663]
