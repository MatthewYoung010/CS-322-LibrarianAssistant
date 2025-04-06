from LibraryDatabaseMY import *

#This is all one giant test for the functions
#Create all of the books
Wikipeida = LogicalBook("Wikipeida", "John Doe",2, 90000001)
Mistborn = LogicalBook("Mistborn", "Brandon Sanderson",3, 90000002)
ExtraCopyOfMistborn = LogicalBook("Mistborn", "Brandon Sanderson",1, 90000002)
PythonForDumDums = LogicalBook("Python For Dum Dum's", "Some nerd",1, 90000003)
ArtOfWar = LogicalBook("Art Of War", "Sun Tzu",1, 90000004)
SecretBook = LogicalBook("Secret Book", "John Doe",1, 90000005)

#Add Books to Catalog
LibraryCatalog = Catalog()
LibraryCatalog.addBook(Mistborn)
LibraryCatalog.addBook(ExtraCopyOfMistborn)
LibraryCatalog.addBook(PythonForDumDums)
LibraryCatalog.addBook(Wikipeida)
LibraryCatalog.addBook(ArtOfWar)
LibraryCatalog.addBook(SecretBook)
LibraryCatalog.addBook(Mistborn)
LibraryCatalog.addBook(ExtraCopyOfMistborn)
LibraryCatalog.addBook(PythonForDumDums)
LibraryCatalog.addBook(Wikipeida)
LibraryCatalog.addBook(ArtOfWar)
LibraryCatalog.addBook(SecretBook)
LibraryCatalog.addBook(Mistborn)
LibraryCatalog.addBook(ExtraCopyOfMistborn)
LibraryCatalog.addBook(PythonForDumDums)
LibraryCatalog.addBook(Wikipeida)
LibraryCatalog.addBook(ArtOfWar)
LibraryCatalog.addBook(SecretBook)
LibraryCatalog.addBook(Mistborn)
LibraryCatalog.addBook(ExtraCopyOfMistborn)
LibraryCatalog.addBook(PythonForDumDums)
LibraryCatalog.addBook(Wikipeida)
LibraryCatalog.addBook(ArtOfWar)
LibraryCatalog.addBook(SecretBook)
LibraryCatalog.addBook(Mistborn)
LibraryCatalog.addBook(ExtraCopyOfMistborn)
LibraryCatalog.addBook(PythonForDumDums)
LibraryCatalog.addBook(Wikipeida)
LibraryCatalog.addBook(ArtOfWar)
LibraryCatalog.addBook(SecretBook)


#Print Current State of Catalog
LibraryCatalog.printCatalog()

#Remove Art of War
LibraryCatalog.removeBook(90000004)

#Edit a Book
print("This will edit the Python for Dumdum's book.")
print("What is the new title of the book?")
newTitle = input()
print("Who is the author of this book?")
newAuthor = input()
LibraryCatalog.editBook(newTitle,newAuthor,90000003)

#Print Catalog where Art of War is gone and the Python for Dum Dum's is modified
LibraryCatalog.printCatalog()

#Find a book by serial number
print("What is the serial number of the book you want to find?")
serialNumber = int(input())
foundBook = LibraryCatalog.findBookBySerialNumber(serialNumber)
print(foundBook)

#Find books by author
print("What is the name of the author you want to find?")
searchAuthor = input()
foundBooks = LibraryCatalog.findBookByAuthor(searchAuthor)
for Book in foundBooks:
    print(Book)

#Find books by title
print("What is the name of the title you want to find?")
searchTitle = input()
foundBooks = LibraryCatalog.findBookByTitle(searchTitle)
for Book in foundBooks:
    print(Book)

# Initialize User Database
UserDB = UserDatabase()

# Validate user ID
def is_valid_user(user_id):
    return UserDB.user_exists(user_id)

# Checkout book
print("\n--- Checking out a book ---")
user_id = int(input("Enter your User ID: "))

if not is_valid_user(user_id):
    print("Invalid User ID.")
else:
    serial_number = int(input("Enter the serial number of the book to checkout: "))
    LibraryCatalog.checkOutBook(user_id, serial_number)

# Return book
print("\n--- Returning a book ---")
user_id = int(input("Enter your User ID: "))

if not is_valid_user(user_id):
    print("Invalid User ID.")
else:
    serial_number = int(input("Enter the serial number of the book to return: "))
    LibraryCatalog.returnBook(user_id, serial_number)


# Send Notification
print("\n--- Sending a test notification ---")

test_user_id = 1  # This user must exist for notification to be sent
test_message = "Reminder: You have a book due tomorrow."

if is_valid_user(test_user_id):
    LibraryCatalog.sendNotification(test_user_id, test_message)
else:
    print("Invalid User ID: Notification not sent.")

# Check that the notification was logged in the database
import sqlite3
connection = sqlite3.connect("Library.db")
cursor = connection.cursor()
cursor.execute("SELECT * FROM Notifications WHERE user_id = ?", (test_user_id,))
notifications = cursor.fetchall()
print("\nNotifications for User ID", test_user_id)
for note in notifications:
    print(note)
connection.close()
