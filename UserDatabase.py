import sqlite3

class User:
    """Each User will have its own unique ID number with 4 other parameters.'
    First Name, Last Name, E-mail, and Password. In the other 2 tables will probably
    be something like book, checkout date, etc and connected to the user's ID"""

    def __init__(self,firstName, lastName, EMail, IDNum, Password):
        self.firstName = firstName
        self.lastName = lastName
        self.EMail = EMail
        self.IDNum = IDNum
        self.Password = Password

        #Might add edit functions or not. Probably not since the editing will just be done in the table

    
class UserDatabase:

    def __init__(self, dbName='UserDatabase.db'):
        self.dbName = dbName
        self.initializeUserDatabase()

    def initializeUserDatabase(self):
        connection = sqlite3.connect(self.dbName)
        cursor = connection.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS UserDatabase (
            FirstName TEXT NOT NULL,
            LastName TEXT NOT NULL,
            EMail TEXT NOT NULL,
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Password INTEGER NOT NULL
        )
        """)
        connection.commit()
        connection.close()
    
    def CreateAccount (self, FirstName, LastName, EMail, Password):
        """Create an account that gets added to the user data base."""

    def Login (self, IDAttempt, passwordAttempt):
        """Login function for user to access their account. Will probably return a bool.
        Might have it change the state of the current user somehow to show their logged in with their credentials"""

    def editAccount(self, newFirstName, newLastName, newEMail, newPassword):
        """Edit the four editable parameters. The user must be logged in before they can edit.
         havenn't figured out how I want to implement that yet. """
    
