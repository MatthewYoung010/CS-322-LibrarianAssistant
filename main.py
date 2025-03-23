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

#Print Current State of Catalog
LibraryCatalog.printCatalog()

#Remove Art of War
LibraryCatalog.removeBook(ArtOfWar)

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