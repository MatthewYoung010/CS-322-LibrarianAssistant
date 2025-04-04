import tkinter as tk
from tkinter import *
from tkinter import messagebox
from LibraryDatabaseMY import LogicalBook, Catalog
from UserDatabase import User, UserDatabase 
from PIL import Image, ImageTk

window = tk.Tk()
window.geometry("1280x720")
window.title("Librarian Assistant")
window.config(bg="#1d291b")
#window.iconbitmap("icon.ico")

library_catalog = Catalog()

# Function to display the catalog
def display_catalog():
    book_list.delete("1.0", END)
    book_list.tag_configure("big", font=("Times New Roman", 18, "bold"))
    books = library_catalog.getCatalog()
    
    if not books:
        book_list.insert(END, "No books available.\n", "big")
    else:
        book_list.insert(END, "Serial #\t\tTitle\t\t\tAuthor\t\t\tCopies\n", "big")
        book_list.insert(END, "-" * 80 + "\n")
        for book in books:
            serial, title, author, copies = book
            book_list.insert(END, f"{serial}\t\t{title}\t\t\t{author}\t\t\t{copies}\n")

# Create UI elements for the "Display Book Catalog" button
display_button = tk.Button(window, text="Display Book Catalog", font=('Times New Roman',24, "bold"), bg="#c3ffbd", command=display_catalog)
display_button.pack(pady=20)

# Book list display area
book_list = Text(window, height=15, width=80, bg="lightgreen")
book_list.pack()

# Load images for the buttons
add_image = Image.open("add.png")
add_image = add_image.resize((75, 75))
add_image_tk = ImageTk.PhotoImage(add_image)

minus_image = Image.open("minus.png")
minus_image = minus_image.resize((75, 75))
minus_image_tk = ImageTk.PhotoImage(minus_image)

edit_image = Image.open("edit.png")
edit_image = edit_image.resize((75, 75))
edit_image_tk = ImageTk.PhotoImage(edit_image)

# Function to show icon button working
def on_button_click(button_name):
    print(f"{button_name} clicked")

# Create a frame for the buttons to be aligned horizontally
button_frame = Frame(window, bg="#1d291b")
button_frame.pack(pady=10)

# Create a frame for each button and its label, and align horizontally
def create_button_with_label(image, label_text, command):
    button_label_frame = Frame(button_frame, bg="")
    button_label_frame.pack(side="left", padx=20)
    
    button = Button(button_label_frame, image=image, command=command)
    button.pack(side="top")
    
    label = Label(button_label_frame, text=label_text, font=("Arial", 12, "bold"), bg="#1d291b", fg="white")
    label.pack(side="top")
    
    return button_label_frame

# Define functionality for the "Add Book" button
def add_book():
    add_win = tk.Toplevel()
    add_win.geometry("500x500")
    add_win.title("Add a Book")
    add_win.config(bg="#1d291b")

    tk.Label(add_win, text="Serial Number:").pack(pady=(100, 5))
    serialNo_entry = tk.Entry(add_win)
    serialNo_entry.pack()

    tk.Label(add_win, text="Title:").pack(pady=(10, 5))
    title_entry = tk.Entry(add_win)
    title_entry.pack()

    tk.Label(add_win, text="Author:").pack(pady=(10, 5))
    author_entry = tk.Entry(add_win)
    author_entry.pack()

    tk.Label(add_win, text="Copies:").pack(pady=(10, 5))
    copies_entry = tk.Entry(add_win)
    copies_entry.pack()

    def add():
        serialNo = serialNo_entry.get()
        title = title_entry.get()
        author = author_entry.get()
        copies = copies_entry.get()

        newBook = LogicalBook(title,author,copies,serialNo)
        library_catalog.addBook(newBook)

        # There will be a logic here that confirms the details are viable
        messagebox.showinfo("Book Added", "Your book has been added to the catalog!")

        add_win.destroy()

    add_button = tk.Button(add_win, text="Add", command=add)
    add_button.pack(pady=10)

def remove_book():
    rem_win = tk.Toplevel()
    rem_win.geometry("500x500")
    rem_win.title("Remove a Book")
    rem_win.config(bg="#1d291b")

    tk.Label(rem_win, text="Enter the serial number of a book to delete:").pack(pady=(200, 5))
    serialNo_entry = tk.Entry(rem_win)
    serialNo_entry.pack()

    def rem():
        serialNo = serialNo_entry.get()

        if(library_catalog.removeBook(serialNo)):
            messagebox.showinfo("Book Removed", "The book has successfully been removed from the library.")
        else:
            messagebox.showinfo("Unable to Remove", "The system encountered an error. Please try again.")
        
        rem_win.destroy()
    
    remove_button = tk.Button(rem_win, text="Remove", command=rem)
    remove_button.pack(pady=10)

def add_user():
    add2_win = tk.Toplevel()
    add2_win.geometry("500x500")
    add2_win.title("Add a User")
    add2_win.config(bg="#1d291b")

    tk.Label(add2_win, text="First Name:").pack(pady=(100, 5))
    firstName_entry = tk.Entry(add2_win)
    firstName_entry.pack()

    tk.Label(add2_win, text="Last Name:").pack(pady=(10, 5))
    lastName_entry = tk.Entry(add2_win)
    lastName_entry.pack()

    tk.Label(add2_win, text="Email:").pack(pady=(10, 5))
    email_entry = tk.Entry(add2_win)
    email_entry.pack()

    def add2():
        firstName = firstName_entry.get()
        lastName = lastName_entry.get()
        email = email_entry.get()

        # do stuff here

        # There will be a logic here that confirms the details are viable
        messagebox.showinfo("User Added", "A new user has been added to the catalog!")

        add2_win.destroy()

    add2_button = tk.Button(add2_win, text="Add User", command=add2()
    add2_button.pack(pady=10)

# Create the buttons and labels
create_button_with_label(add_image_tk, "Add User", lambda: add_user())
create_button_with_label(add_image_tk, "Add Book", lambda: add_book())
create_button_with_label(minus_image_tk, "Remove Book", lambda: remove_book())
create_button_with_label(edit_image_tk, "Edit Book", lambda: on_button_click("Edit"))
create_button_with_label(edit_image_tk, "Check In & Out", lambda: on_button_click("Checking"))

# Load the larger book icon
book_image = Image.open("book.png")
book_image = book_image.resize((200, 200))
book_image_tk = ImageTk.PhotoImage(book_image)

# Display the book icon below the buttons and center it
book_icon_label = Label(window, image=book_image_tk, bg="#1d291b")
book_icon_label.pack(pady=20)

# The loop displaying the window.
window.mainloop()
