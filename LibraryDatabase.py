import sqlite3

class LogicalBook:
    """Books won't have each unique copy recorded separately. Instead, there is one logical book entry, 
    and the number of copies represents how many copies exist. The serial number uniquely identifies each book entry."""
    
    def __init__(self, title, author, copies, serialNum):
        self.title = title
        self.author = author
        self.copies = copies
        self.serialNum = serialNum

class Catalog:
    """Catalog handles all book-related operations within the database."""
    
    def __init__(self, db_name="Library.db"):
        self.db_name = db_name
        self.initialize_database()

    def initialize_database(self):
        """Ensures the books table exists in the database."""
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            copies INTEGER NOT NULL,
            serialNum INTEGER UNIQUE NOT NULL
        )
        """)
        connection.commit()
        connection.close()

    def addBook(self, newBook):
        """Adds a book to the catalog or updates the copy count if it already exists."""
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()

        cursor.execute("SELECT copies FROM books WHERE serialNum = ?", (newBook.serialNum,))
        result = cursor.fetchone()

        if result:
            updated_copies = result[0] + newBook.copies
            cursor.execute("UPDATE books SET copies = ? WHERE serialNum = ?", (updated_copies, newBook.serialNum))
        else:
            cursor.execute("INSERT INTO books (title, author, copies, serialNum) VALUES (?, ?, ?, ?)",
                           (newBook.title, newBook.author, newBook.copies, newBook.serialNum))

        connection.commit()
        connection.close()

    def removeBook(self, serialNum, copiesToRemove):
        """Removes a book or reduces the copy count in the database."""
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()

        cursor.execute("SELECT copies FROM books WHERE serialNum = ?", (serialNum,))
        result = cursor.fetchone()

        if result:
            current_copies = result[0]
            if current_copies > copiesToRemove:
                cursor.execute("UPDATE books SET copies = ? WHERE serialNum = ?", (current_copies - copiesToRemove, serialNum))
            else:
                cursor.execute("DELETE FROM books WHERE serialNum = ?", (serialNum,))
        
        connection.commit()
        connection.close()

    def editBook(self, newTitle, newAuthor, serialNum):
        """Edits the title and author of a book identified by serial number."""
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute("UPDATE books SET title = ?, author = ? WHERE serialNum = ?", (newTitle, newAuthor, serialNum))
        connection.commit()
        connection.close()

    def printCatalog(self):
        """Prints the catalog from the database."""
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute("SELECT title, author, copies, serialNum FROM books")
        books = cursor.fetchall()
        connection.close()

        print("Title        Author      Copies   Serial Number")
        for book in books:
            print(f"{book[0]}     {book[1]}    {book[2]}     {book[3]}")

    def findBookBySerialNum(self, serialNumOfBook):
        """Finds and returns a book entry by serial number."""
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute("SELECT title, author, copies, serialNum FROM books WHERE serialNum = ?", (serialNumOfBook,))
        book = cursor.fetchone()
        connection.close()
        return book if book else None

    def doesBookExist(self, serialNumOfBook):
        """Checks if a book exists in the catalog by serial number."""
        return self.findBookBySerialNum(serialNumOfBook) is not None

    def findBookByAuthor(self, authorTarget):
        """Finds books by a specific author."""
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute("SELECT title, author, copies, serialNum FROM books WHERE author = ?", (authorTarget,))
        books = cursor.fetchall()
        connection.close()
        return books

    def findBookByTitle(self, titleTarget):
        """Finds books by a specific title."""
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute("SELECT title, author, copies, serialNum FROM books WHERE title = ?", (titleTarget,))
        books = cursor.fetchall()
        connection.close()
        return books
