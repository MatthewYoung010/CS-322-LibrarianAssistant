import sqlite3
#Will be replacing the list with a database in the next version

class LogicalBook:
    """Books won't have their each unique copy. Instead there is one larger logical book
    and if there are more than one copy of said book the copies would be two. Serial Number
    is the unique identification for each logical book."""
    def __init__(self, title, author, copies, serialNumber):
        self.title = title
        self.author = author
        self.copies = copies
        self.serialNumber = serialNumber
    
    def changeTitle(self, newTitle):
        self.title = newTitle

    def changeAuthor(self, newAuthor):
        self.author = newAuthor
    
    def changeNumOfCopies(self, newCopiesNum):
        self.copies = newCopiesNum

    def changeSerialNumber(self, newSerialNumber):
        self.serialNumber = newSerialNumber

class Catalog:
    """Catalog holds all of the functions for editing a catalog."""
    def __init__(self):
        connectionObj = sqlite3.connect('Library.db')

        cursorObj = connectionObj.cursor()
        #Deletes Table. (If parameters need to be updated delete the old table)
        cursorObj.execute("DROP TABLE IF EXISTS CATALOG")
        BookCatalog = """ CREATE TABLE IF NOT EXISTS Book_Catalog(
                            Serial_Number INT PRIMARY KEY,
                            Title VARCHAR(255) NOT NULL,
                            Author VARCHAR(255) NOT NULL,
                            Copies INT
                            ); """ 
        
        cursorObj.execute(BookCatalog)
        cursorObj.close() 
        connectionObj.close()


    def addBook(self, newBook):
        """Add a book to the catalog. If there already exists a copy of the book in the catalog 
        it will add the amount of copies in the object instead."""

        connection = sqlite3.connect("Library.db")
        cursor = connection.cursor()

        doesBookExist = self.doesBookExist(newBook.serialNumber)

        if(doesBookExist == True):
            cursor.execute("UPDATE Book_Catalog SET COPIES = ? WHERE Serial_Number = ?",
                           ((cursor.execute("SELECT Copies FROM Book_Catalog WHERE Serial_Number = ?",(newBook.serialNumber,)).fetchone()[0])+ newBook.copies,newBook.serialNumber))
        else:
            cursor.execute("""INSERT OR IGNORE INTO Book_Catalog (Serial_Number,Title,Author,Copies) 
                           VALUES (?,?,?,?)""", (newBook.serialNumber, newBook.title, newBook.author, newBook.copies))
        
        connection.commit()
        cursor.close()
        connection.close()

        
    def removeBook(self, serialNumber):
        """Removes one book copy from database. If there is 0 copies left the book is deleted."""
        connection = sqlite3.connect("Library.db")
        cursor = connection.cursor()

        cursor.execute("SELECT Copies FROM Book_Catalog WHERE Serial_Number = ?", (serialNumber,))
        result = cursor.fetchone()

        if result:
            current_copies = result[0]
            if current_copies > 1:
                cursor.execute("UPDATE Book_Catalog SET Copies = ? WHERE Serial_Number = ?", (current_copies - 1, serialNumber))
                connection.commit()
                connection.close()
                return True
            elif current_copies == 1:
                cursor.execute("DELETE FROM Book_Catalog WHERE Serial_Number = ?", (serialNumber,))
                connection.commit()
                connection.close()
                return True
            else:
                return False
        
    
    def editBook (self,newTitle, newAuthor, SerialNumber):
       """Edits the Title and Author of a book"""
       connection = sqlite3.connect("Library.db")
       cursor = connection.cursor()

       if(self.doesBookExist(SerialNumber) == True):
           cursor.execute("UPDATE Book_Catalog SET Title = ?, Author = ? WHERE Serial_Number = ?",(newTitle,newAuthor, SerialNumber))
       else:
           print("Serial Number not found")

       connection.commit()
       cursor.close()
       connection.close()

    def printCatalog(self):
        """Self Explanatory Print Function."""
        print("Title   Author   Serial Number  Copies")
        connection = sqlite3.connect("Library.db")
        cursor = connection.cursor()

        data=cursor.execute('''SELECT * FROM Book_Catalog''') 
        for row in data: 
            print(row)
        cursor.close()
        connection.close()
    
    def doesBookExist(self, serialNumberOfBook):
        """Search for a book in the catalog by serial number. Returns a boolean"""
        connection = sqlite3.connect("Library.db")
        cursor = connection.cursor()
        
        if (cursor.execute("SELECT EXISTS(SELECT 1 FROM Book_Catalog WHERE Serial_Number = ?)",(serialNumberOfBook,)).fetchone()[0] == 1):
            cursor.close()
            connection.close()
            return True
        else:
            cursor.close()
            connection.close()
            return False   

    def findBookBySerialNumber(self, serialNumberOfBook):
        """Search for a book in the catalog by serial number. Returns the one unique book."""

        connection = sqlite3.connect("Library.db")
        cursor = connection.cursor()

        if (self.doesBookExist(serialNumberOfBook) == True):
            bookReturn = cursor.execute("SELECT * FROM Book_Catalog WHERE Serial_Number = ?",(serialNumberOfBook,)).fetchall()
            cursor.close()
            connection.close()
            return bookReturn
        else:
           cursor.close()
           connection.close()
           return [LogicalBook("N/A","N/A",0,0000000)]
            
    def findBookByAuthor(self, authorTarget):
        """Search for a book in the catalog by author. Can return multiple."""
        connection = sqlite3.connect("Library.db")
        cursor = connection.cursor()
    
        if (cursor.execute("SELECT EXISTS(SELECT 1 FROM Book_Catalog WHERE Author = ?)",(authorTarget,)).fetchone()[0] == 1):
            booksReturn = cursor.execute("SELECT * FROM Book_Catalog WHERE Author = ?",(authorTarget,)).fetchall()
            cursor.close()
            connection.close()
            return booksReturn
        else:
            cursor.close()
            connection.close()
            return [LogicalBook("N/A","N/A",0,0000000)]

    def findBookByTitle(self, titleTarget):
        """Search for a book in the catalog by title. Can return multiple."""
        connection = sqlite3.connect("Library.db")
        cursor = connection.cursor()

        if (cursor.execute("SELECT EXISTS(SELECT 1 FROM Book_Catalog WHERE Title = ?)",(titleTarget,)).fetchone()[0] == 1):
            booksReturn = cursor.execute("SELECT * FROM Book_Catalog WHERE Title = ?",(titleTarget,)).fetchall()
            cursor.close()
            connection.close()
            return booksReturn
        else:
            cursor.close()
            connection.close()
            return [LogicalBook("N/A","N/A",0,0000000)]
        
    def getCatalog (self):
        """Get The Catalog"""
        connection = sqlite3.connect("Library.db")
        cursor = connection.cursor()
        bookCatalog = cursor.execute("SELECT * FROM Book_Catalog").fetchall()
        cursor.close()
        connection.close()
        return bookCatalog
