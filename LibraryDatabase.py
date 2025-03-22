#import sqlite3
#Will be replacing the list with a database in the next version

class LogicalBook:
    """Books won't have their each unique copy. Instead there is one larger logical book
    and if there are more than one copy of said book the copies would be two. Serial Number
    is the unique identification for each logical book."""
    def __init__(self, title, author, copies, serialNum):
        self.title = title
        self.author = author
        self.copies = copies
        self.serialNum = serialNum
    
    def changeTitle(self, newTitle):
        self.title = newTitle

    def changeAuthor(self, newAuthor):
        self.author = newAuthor
    
    def changeNumOfCopies(self, newCopiesNum):
        self.copies = newCopiesNum

    def changeSerialNum(self, newSerialNum):
        self.serialNum = newSerialNum

class Catalog:
    """Catalog holds all of the functions for editing a catalog."""
    def __init__(self, InitalBook):
        self.catalog = [InitalBook]


    def addBook(self, newBook):
        """Add a book to the catalog. If there already exists a copy of the book in the catalog 
        it will add the amount of copies in the object instead."""

        doesBookExist = self.doesBookExist(newBook.serialNum)
        if(doesBookExist == True):
            self.findBookBySerialNum(newBook.serialNum).changeNumOfCopies(self.findBookBySerialNum(newBook.serialNum).copies + newBook.copies)
        else:
            self.catalog.append(newBook)

        
    
    def removeBook(self, bookToRemove):
        """Removes books based on how many copies the object has."""
        doesBookExist = self.findBookBySerialNum(bookToRemove.serialNum)
        if(doesBookExist.copies - bookToRemove.copies > 1):
            doesBookExist.changeNumOfCopies(doesBookExist.copies - bookToRemove.copies)
        else:
            self.catalog.remove(bookToRemove)
    
    def editBook (self,newTitle, newAuthor, SerialNum):
       """Edits the Title and Author of a book"""
       if(self.doesBookExist(SerialNum) == True):
            BookToEdit = self.findBookBySerialNum(SerialNum)

            BookToEdit.changeTitle(newTitle)
            BookToEdit.changeAuthor(newAuthor)
           
      
       
       

    def printCatalog(self):
        """Self Explanatory Print Function."""
        print("Title        Author      Serial Number")
        for Book in self.catalog:
            print(f"{Book.title}     {Book.author}    {Book.copies}     {Book.serialNum}")
    
    def findBookBySerialNum(self, serialNumOfBook):
        """Search for a book in the catalog by serial number. Returns the one unique book."""
        for Book in self.catalog:
            if(serialNumOfBook == Book.serialNum):
                #print("Book Found")
                return Book
            
    def doesBookExist(self, serialNumOfBook):
        """Search for a book in the catalog by serial number. Returns a boolean"""
        for Book in self.catalog:
            if(serialNumOfBook == Book.serialNum):
                #print("Book Found")
                return True
            
        return False
            
    def findBookByAuthor(self, authorTarget):
        """Search for a book in the catalog by author. Can return multiple."""
        matchedBooks = list()
        for Book in self.catalog:
            if(authorTarget == Book.author):
                matchedBooks.append(Book)

        return matchedBooks 

    def findBookByTitle(self, titleTarget):
        """Search for a book in the catalog by title. Can return multiple."""
        matchedBooks = list()
        for Book in self.catalog:
            if(titleTarget == Book.title):
                matchedBooks.append(Book)  

        return matchedBooks 


#def connectToLibraryDatabase():
