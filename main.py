from LibraryDatabase import *


Wikipeida = Book("Wikipeida", "John Doe", 90000001)
Mistborn = Book("Mistborn", "Brandon Sanderson", 90000002)
PythonForDumDums = Book("Python For Dum Dum's", "Some nerd", 90000003)

LibraryCatalog = Database(Wikipeida)
LibraryCatalog.addBook(Mistborn)
LibraryCatalog.addBook(PythonForDumDums)

LibraryCatalog.printCatalog()


