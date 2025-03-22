#import sqlite3

class Book:
    def __init__(self, title, author, serialNum):
        self.title = title
        self.author = author
        self.serialNum = serialNum
    
    def changeTitle(self, newTitle):
        self.title = newTitle

    def changeAuthor(self, newAuthor):
        self.author = newAuthor
    
    def changeTitle(self, newSerialNum):
        self.serialNum = newSerialNum

class Database:
    def __init__(self, InitalBook):
        self.catalog = [InitalBook]

    def addBook(self, newBook):
        self.catalog.append(newBook)
    
    def printCatalog(self):
        print("Title        Author      Serial Number")
        for Catalog in self.catalog:
            print(f"{Catalog.title}     {Catalog.author}    {Catalog.serialNum}")



#def connectToLibraryDatabase():
