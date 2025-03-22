from LibraryDatabase import *


Wikipeida = LogicalBook("Wikipeida", "John Doe",2, 90000001)
Mistborn = LogicalBook("Mistborn", "Brandon Sanderson",3, 90000002)
PythonForDumDums = LogicalBook("Python For Dum Dum's", "Some nerd",1, 90000003)

LibraryCatalog = Catalog(Wikipeida)
LibraryCatalog.addBook(Mistborn)
LibraryCatalog.addBook(PythonForDumDums)

LibraryCatalog.printCatalog()

print("Enter the Serial Number of the book to edit:")
serialNum = int(input())

print("What is the new title?")
newTitle = input()

print("What is the new author?")
newAuthor = input()

LibraryCatalog.editBook(newTitle, newAuthor, serialNum)


LibraryCatalog.printCatalog()

AnotherCopyOfMistborn = LogicalBook("Mistborn", "Brandon Sanderson", 1, 90000002)
LibraryCatalog.addBook(AnotherCopyOfMistborn)
Heros = LogicalBook("Heros","Brandon Sanderson", 1, 90000004)
LibraryCatalog.addBook(Heros)

print("Title        Author      Number Of Copies        Serial Number")
for Book in LibraryCatalog.findBookByAuthor("Brandon Sanderson"):
     print(f"{Book.title}     {Book.author}    {Book.copies}        {Book.serialNum}")


print("Enter the Serial Number of the book to edit:")
serialNum = int(input())

print("What is the new title?")
newTitle = input()

print("What is the new author?")
newAuthor = input()

LibraryCatalog.editBook(newTitle, newAuthor, serialNum)
LibraryCatalog.printCatalog()