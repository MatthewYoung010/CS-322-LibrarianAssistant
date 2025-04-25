import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from LibraryDatabaseMY import LogicalBook, Catalog
from UserDatabase import UserDatabase
import sqlite3

window = tk.Tk()
window.iconbitmap("icon.ico")
window.geometry("1280x720")
window.title("Librarian Assistant")

style = ttk.Style()
style.configure('TNotebook.Tab', font=('Arial', 16, 'bold'))
style.map('Treeview', background=[('selected', '#3a3a3a')])

notebook = ttk.Notebook(window)
notebook.pack(expand=True, fill='both')

book_tab = ttk.Frame(notebook)
member_tab = ttk.Frame(notebook)
notebook.add(book_tab, text="Books")
notebook.add(member_tab, text="Members")

# Restore all previously working icons
add_img = ImageTk.PhotoImage(Image.open("icons/bookAdd.png").resize((40, 40)))
remove_img = ImageTk.PhotoImage(Image.open("icons/bookRemove.png").resize((40, 40)))
edit_img = ImageTk.PhotoImage(Image.open("icons/bookEdit.png").resize((40, 40)))
book_reload_img = ImageTk.PhotoImage(Image.open("icons/bookRefresh.png").resize((40, 40)))
mem_reload_img = ImageTk.PhotoImage(Image.open("icons/memReload.png").resize((40, 40)))
mem_add_img = ImageTk.PhotoImage(Image.open("icons/memAdd.png").resize((40, 40)))
mem_remove_img = ImageTk.PhotoImage(Image.open("icons/memRemove.png").resize((40, 40)))
mem_edit_img = ImageTk.PhotoImage(Image.open("icons/memEdit.png").resize((40, 40)))

library_catalog = Catalog()
user_db = UserDatabase()

book_controls = tk.Frame(book_tab)
book_controls.pack(fill='x', pady=10)

search_vars = {"Serial #": "", "Title": "", "Author": "", "Copies": ""}
book_tree = ttk.Treeview(book_tab, columns=list(search_vars), show='headings', selectmode='browse')
for col in search_vars:
    book_tree.heading(col, text=col)
    book_tree.column(col, anchor='w', width=150)
book_tree.pack(fill='both', expand=True, padx=10, pady=10)

filter_combo = ttk.Combobox(book_controls, values=list(search_vars.keys()), width=10, state="readonly")
filter_combo.set("Filter")
filter_combo.pack(side='left', padx=5)

filter_entry = tk.Entry(book_controls, width=50)
filter_entry.pack(side='left', padx=5)

def display_books(filtered=None):
    for row in book_tree.get_children():
        book_tree.delete(row)
    books = filtered if filtered else library_catalog.getCatalog()
    for serial, title, author, copies in books:
        book_tree.insert('', 'end', values=(serial, title, author, copies))

def apply_filter():
    field = filter_combo.get()
    query = filter_entry.get().lower()
    if field not in search_vars:
        return
    all_books = library_catalog.getCatalog()
    filtered = [book for book in all_books if query in str(book[list(search_vars).index(field)]).lower()]
    display_books(filtered)

def add_book():
    win = tk.Toplevel()
    win.title("Add Book")
    win.geometry("400x400")
    fields = ["Serial No", "Title", "Author", "Copies"]
    entries = {}
    for field in fields:
        tk.Label(win, text=field).pack(pady=5)
        ent = tk.Entry(win)
        ent.pack()
        entries[field] = ent
    def submit():
        book = LogicalBook(
            entries["Title"].get(),
            entries["Author"].get(),
            int(entries["Copies"].get()),
            int(entries["Serial No"].get())
        )
        library_catalog.addBook(book)
        messagebox.showinfo("Added", "Book added!")
        win.destroy()
        display_books()
    tk.Button(win, text="Add Book", command=submit).pack(pady=10)

def remove_book():
    win = tk.Toplevel()
    win.title("Remove Book")
    win.geometry("300x200")
    tk.Label(win, text="Serial No to remove:").pack(pady=10)
    serial_entry = tk.Entry(win)
    serial_entry.pack()
    def submit():
        success = library_catalog.removeBook(int(serial_entry.get()))
        messagebox.showinfo("Result", "Removed" if success else "Not found")
        win.destroy()
        display_books()
    tk.Button(win, text="Remove", command=submit).pack(pady=10)

def checkout_selected_book():
    selected = book_tree.focus()
    if not selected:
        messagebox.showerror("Error", "Please select a book to check out.")
        return
    book = book_tree.item(selected)['values']
    serial_number = book[0]
    users = user_db.get_user_database()
    if not users:
        messagebox.showerror("Error", "No users found to check out this book.")
        return
    checkout_win = tk.Toplevel()
    checkout_win.title("Check Out Book")
    checkout_win.geometry("400x300")
    tk.Label(checkout_win, text="Select User:").pack(pady=10)
    user_choices = [f"{user[0]} {user[1]} (ID: {user[3]})" for user in users]
    user_ids = [user[3] for user in users]
    user_combo = ttk.Combobox(checkout_win, values=user_choices, state="readonly", width=40)
    user_combo.pack(pady=10)
    def confirm_checkout():
        index = user_combo.current()
        if index == -1:
            messagebox.showerror("Error", "Select a user")
            return
        user_id = user_ids[index]
        try:
            serial_int = int(serial_number)
        except ValueError:
            messagebox.showerror("Error", "Invalid serial number format for this book.")
            return
        library_catalog.checkOutBook(user_id, serial_int)
        checkout_win.destroy()
        display_books()
        display_members()
    tk.Button(checkout_win, text="Confirm Checkout", command=confirm_checkout).pack(pady=20)

# Book tab buttons
tk.Button(book_controls, image=add_img, command=add_book).pack(side='left', padx=10)
tk.Button(book_controls, image=remove_img, command=remove_book).pack(side='left', padx=10)
tk.Button(book_controls, image=edit_img, command=lambda: messagebox.showinfo("Unused Feature", "Feature coming soon!")).pack(side='left', padx=10)
tk.Button(book_controls, image=book_reload_img, command=display_books).pack(side='left', padx=10)
tk.Button(book_controls, text="Check Out Book", bg="#28a745", fg="white", font=("Arial", 12, "bold"), command=checkout_selected_book).pack(side='left', padx=10)

# --- Member Tab ---
member_controls = tk.Frame(member_tab)
member_controls.pack(fill='x', pady=10)

member_tree = ttk.Treeview(member_tab, columns=("ID", "Name", "Email"), show='headings', selectmode='browse')
member_tree.heading("ID", text="ID")
member_tree.heading("Name", text="Name")
member_tree.heading("Email", text="Email")
member_tree.pack(fill='both', expand=True, padx=10, pady=10)

def display_members():
    for row in member_tree.get_children():
        member_tree.delete(row)
    members = user_db.get_user_database()
    for FirstName, LastName, EMail, ID, Password in members:
        full_name = f"{FirstName} {LastName}"
        member_tree.insert('', 'end', values=(ID, full_name, EMail))

def add_user():
    win = tk.Toplevel()
    win.title("Add User")
    win.geometry("400x300")
    fields = ["First Name", "Last Name", "Email", "Password"]
    entries = {}
    for field in fields:
        tk.Label(win, text=field).pack(pady=5)
        ent = tk.Entry(win, show="*" if field == "Password" else None)
        ent.pack()
        entries[field] = ent
    def submit():
        first = entries["First Name"].get()
        last = entries["Last Name"].get()
        email = entries["Email"].get()
        password = entries["Password"].get()
        if not first or not last or not email or not password:
            messagebox.showerror("Error", "All fields are required.")
            return
        user_db.createAccount(first, last, email, password)
        messagebox.showinfo("Added", "User added!")
        win.destroy()
        display_members()
    tk.Button(win, text="Add User", command=submit).pack(pady=10)

def remove_user():
    win = tk.Toplevel()
    win.title("Remove User")
    win.geometry("300x200")
    tk.Label(win, text="User ID to remove:").pack(pady=10)
    id_entry = tk.Entry(win)
    id_entry.pack()
    def submit():
        user_id = id_entry.get()
        if not user_id.isdigit():
            messagebox.showerror("Error", "Please enter a valid numeric ID.")
            return
        connection = sqlite3.connect(user_db.dbName)
        cursor = connection.cursor()
        cursor.execute("DELETE FROM UserDatabase WHERE ID = ?", (int(user_id),))
        connection.commit()
        deleted = cursor.rowcount
        connection.close()
        if deleted:
            messagebox.showinfo("Removed", f"User ID {user_id} removed.")
        else:
            messagebox.showinfo("Not Found", "No user with that ID.")
        win.destroy()
        display_members()
    tk.Button(win, text="Remove", command=submit).pack(pady=10)

def view_selected_member():
    selected = member_tree.focus()
    if not selected:
        messagebox.showerror("Error", "Please select a member to view.")
        return
    member = member_tree.item(selected)['values']
    user_id = member[0]
    name = member[1]
    email = member[2]
    view_win = tk.Toplevel()
    view_win.title("Member Details")
    view_win.geometry("500x400")
    tk.Label(view_win, text=f"Name: {name}", font=("Arial", 14)).pack(pady=10)
    tk.Label(view_win, text=f"Email: {email}", font=("Arial", 12)).pack(pady=5)
    tk.Label(view_win, text="Books Checked Out:").pack(pady=10)
    books = library_catalog.getUsersCheckedOutBooks(user_id)
    text = tk.Text(view_win, height=15, width=60)
    if books:
        for b in books:
            text.insert(tk.END, f"Serial: {b[2]} | Checked Out ID: {b[0]} | Date: {b[3]}\n")
    else:
        text.insert(tk.END, "No books checked out.")
    text.pack()

tk.Button(member_controls, image=mem_add_img, command=add_user).pack(side='left', padx=10)
tk.Button(member_controls, image=mem_remove_img, command=remove_user).pack(side='left', padx=10)
tk.Button(member_controls, image=mem_edit_img, command=lambda: messagebox.showinfo("Unused Feature", "Feature coming soon!")).pack(side='left', padx=10)
tk.Button(member_controls, image=mem_reload_img, command=display_members).pack(side='left', padx=10)
tk.Button(member_controls, text="View Member Details", bg="#007bff", fg="white", font=("Arial", 12, "bold"), command=view_selected_member).pack(side='left', padx=10)

def on_tab_change(event):
    tab = event.widget.select()
    tab_text = event.widget.tab(tab, "text")
    if "Book" in tab_text:
        display_books()
    elif "Member" in tab_text:
        display_members()

notebook.bind("<<NotebookTabChanged>>", on_tab_change)

display_books()
display_members()
window.mainloop()
