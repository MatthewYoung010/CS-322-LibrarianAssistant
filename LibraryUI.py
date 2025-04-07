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

notebook = ttk.Notebook(window)
notebook.pack(expand=True, fill='both')

book_tab = ttk.Frame(notebook)
member_tab = ttk.Frame(notebook)
notebook.add(book_tab, text="📚 Books")

notebook.add(member_tab, text="👤 Members")

add_img = ImageTk.PhotoImage(Image.open("icons/bookAdd.png").resize((40, 40)))
mem_add_img = ImageTk.PhotoImage(Image.open("icons/memAdd.png").resize((40, 40)))
remove_img = ImageTk.PhotoImage(Image.open("icons/bookRemove.png").resize((40, 40)))
mem_remove_img = ImageTk.PhotoImage(Image.open("icons/memRemove.png").resize((40, 40)))
edit_img = ImageTk.PhotoImage(Image.open("icons/bookEdit.png").resize((40, 40)))
mem_edit_img = ImageTk.PhotoImage(Image.open("icons/memEdit.png").resize((40, 40)))
library_catalog = Catalog()

book_controls = tk.Frame(book_tab)
book_controls.pack(fill='x', pady=10)

book_list = tk.Text(book_tab, height=20, bg="lightgreen", fg="#103b10", font=("Courier", 20))
book_list.pack(padx=10, pady=10, fill='both', expand=True)

def display_books():
    book_list.delete("1.0", tk.END)
    books = library_catalog.getCatalog()
    book_list.insert(tk.END, f"{'Serial #':<15}{'Title':<25}{'Author':<25}{'Copies':<10}\n")
    book_list.insert(tk.END, "-" * 78 + "\n")
    for serial, title, author, copies in books:
        book_list.insert(tk.END, f"{serial:<15}{title:<25}{author:<25}{copies:<10}\n")

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
            entries["Copies"].get(),
            entries["Serial No"].get()
        )
        library_catalog.addBook(book)
        messagebox.showinfo("Added", "Book added!")
        win.destroy()

    tk.Button(win, text="Add Book", command=submit).pack(pady=10)

def remove_book():
    win = tk.Toplevel()
    win.title("Remove Book")
    win.geometry("300x200")

    tk.Label(win, text="Serial No to remove:").pack(pady=10)
    serial_entry = tk.Entry(win)
    serial_entry.pack()

    def submit():
        success = library_catalog.removeBook(serial_entry.get())
        messagebox.showinfo("Result", "Removed" if success else "Not found")
        win.destroy()

    tk.Button(win, text="Remove", command=submit).pack(pady=10)

# Book tab buttons
tk.Button(book_controls, image=add_img, command=add_book).pack(side='left', padx=10)
tk.Button(book_controls, image=remove_img, command=remove_book).pack(side='left', padx=10)
tk.Button(book_controls, image=edit_img, command=lambda: messagebox.showinfo("Unused Feature", "Feature coming soon!")).pack(side='left', padx=10)
book_reload_img = ImageTk.PhotoImage(Image.open("icons/bookRefresh.png").resize((40, 40)))
tk.Button(book_controls, image=book_reload_img, command=display_books).pack(side='left', padx=10)
book_search_img = ImageTk.PhotoImage(Image.open("icons/bookSearch.png").resize((40, 40)))

def show_book_search():
    if hasattr(window, 'book_search_bar'):
        return  # Already shown

    window.book_search_bar = tk.Frame(book_controls)
    window.book_search_bar.pack(side='left', padx=10)

    filter_combo = ttk.Combobox(window.book_search_bar, values=["Title", "Author", "Serial #", "Copies"], width=7, state="readonly")
    filter_combo.set("Filter")
    filter_combo.pack(side='left', padx=5)
    tk.Entry(window.book_search_bar, width=80).pack(side='left')
    filter_combo.set("Filter")
    filter_combo.pack(side='left', padx=5)

tk.Button(book_controls, image=book_search_img, command=show_book_search).pack(side='left', padx=10)

# --- Member Catalog Tab ---
user_db = UserDatabase()
member_controls = tk.Frame(member_tab)
member_controls.pack(fill='x', pady=10)

member_area = tk.Text(member_tab, height=20, bg="lightblue", fg="#0b2a3b", font=("Courier", 20))
member_area.pack(padx=10, pady=10, fill='both', expand=True)

def display_members():
    member_area.delete("1.0", tk.END)
    members = user_db.get_user_database()
    member_area.insert(tk.END, f"{'ID':<8}{'Name':<30}{'Email':<40}\n")
    member_area.insert(tk.END, "-" * 78 + "\n")
    for FirstName, LastName, EMail, ID, Password in members:
        full_name = f"{FirstName} {LastName}"
        member_area.insert(tk.END, f"{str(ID):<8}{full_name:<30}{EMail:<40}\n")

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

# Member tab buttons
tk.Button(member_controls, image=mem_add_img, command=add_user).pack(side='left', padx=10)
tk.Button(member_controls, image=mem_remove_img, command=remove_user).pack(side='left', padx=10)
tk.Button(member_controls, image=mem_edit_img, command=lambda: messagebox.showinfo("Unused Feature", "Feature coming soon!")).pack(side='left', padx=10)
mem_reload_img = ImageTk.PhotoImage(Image.open("icons/memReload.png").resize((40, 40)))
tk.Button(member_controls, image=mem_reload_img, command=display_members).pack(side='left', padx=10)
mem_search_img = ImageTk.PhotoImage(Image.open("icons/memSearch.png").resize((40, 40)))
def show_member_search():
    if hasattr(window, 'member_search_bar'):
        return  # Already shown

    window.member_search_bar = tk.Frame(member_controls)
    window.member_search_bar.pack(side='left', padx=10)

    filter_combo = ttk.Combobox(window.member_search_bar, values=["Last Name", "Email", "ID"], width=7, state="readonly")
    filter_combo.set("Filter")
    filter_combo.pack(side='left', padx=5)
    tk.Entry(window.member_search_bar, width=80).pack(side='left')
    filter_combo.set("Filter")
    filter_combo.pack(side='left', padx=5)

tk.Button(member_controls, image=mem_search_img, command=show_member_search).pack(side='left', padx=10)

# Bind tab switch event to auto-refresh

def on_tab_change(event):
    tab = event.widget.select()
    tab_text = event.widget.tab(tab, "text")
    if "Book" in tab_text:
        display_books()
    elif "Member" in tab_text:
        display_members()

notebook.bind("<<NotebookTabChanged>>", on_tab_change)

# Run the app
window.mainloop()
