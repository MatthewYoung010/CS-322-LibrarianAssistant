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


class UserDatabase:

    def __init__(self, dbName='UserDatabase.db'):
        self.dbName = dbName
        print(self.dbName)
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
            Password TEXT NOT NULL
        )
        """)
        connection.commit()
        connection.close()

    def createAccount(self, firstName, lastName, EMail, password):
        """Creates a new user account in the database."""
        connection = sqlite3.connect(self.dbName)
        cursor = connection.cursor()

        cursor.execute("INSERT INTO UserDatabase (FirstName, LastName, EMail, Password) VALUES (?, ?, ?, ?)",
                       (firstName, lastName, EMail, password))

        connection.commit()
        connection.close()
        print("Account successfully created.")

    def login(self, IDAttempt, passwordAttempt):
        """Attempts to log in with the provided user ID and password."""
        connection = sqlite3.connect(self.dbName)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM UserDatabase WHERE ID = ? AND Password = ?", (IDAttempt, passwordAttempt))
        user = cursor.fetchone()
        connection.close()

        if user:
            print("Login successful!")
            return True
        else:
            print("Invalid ID or password.")
            return False

    def editAccount(self, userID, newFirstName, newLastName, newEMail, newPassword):
        """Allows a user to edit their account details."""
        connection = sqlite3.connect(self.dbName)
        cursor = connection.cursor()

        cursor.execute("UPDATE UserDatabase SET FirstName = ?, LastName = ?, EMail = ?, Password = ? WHERE ID = ?",
                       (newFirstName, newLastName, newEMail, newPassword, userID))

        connection.commit()
        connection.close()
        print("Account details updated successfully.")

    def user_exists(self, user_id):
        """Checks if a user with the given user_id exists in the database."""
        connection = sqlite3.connect(self.dbName)
        cursor = connection.cursor()
        cursor.execute("SELECT ID FROM UserDatabase WHERE ID = ?", (user_id,))
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        return result is not None
    
    def get_user_database(self):
        """Gets the entire database"""
        connection = sqlite3.connect(self.dbName)
        cursor = connection.cursor()
        userDatabase = cursor.execute("SELECT * FROM UserDatabase").fetchall()
        cursor.close()
        connection.close()
        return userDatabase
    
    def get_user_information(self, userID):
        """Using User ID gets the members information"""
        connection = sqlite3.connect(self.dbName)
        cursor = connection.cursor()
        userInfo = cursor.execute("SELECT * FROM UserDatabase WHERE ID = ?", (userID)).fetchall()
        cursor.close()
        connection.close()

    #New search function using the LIKE Sqlite keyword
    def search_user(self, first_name_search, last_name_search, email_search, id_search):
        connection = sqlite3.connect("UserDatabase.db")
        cursor = connection.cursor()
        search_result = cursor.execute("""
                                        SELECT * FROM UserDatabase WHERE
                                        FirstName LIKE '%' || ? || '%' AND
                                        LastName LIKE '%' || ? || '%' AND
                                        EMail LIKE '%' || ? || '%' AND
                                        ID LIKE '%' || ? || '%'
                                         """, (first_name_search,last_name_search,email_search,id_search)).fetchall()
        cursor.close()
        connection.close()
        return search_result

