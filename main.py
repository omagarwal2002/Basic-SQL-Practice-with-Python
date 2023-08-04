import tkinter as tk
from tkinter import messagebox
import mysql.connector
import hashlib
import random


conn = mysql.connector.connect(
    host='localhost',
    username='root',
    password='1234',
    database='celebaltech'
)
cursor = conn.cursor()

# Create tables if they don't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS teachers (
        username VARCHAR(50) PRIMARY KEY,
        password VARCHAR(64)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        roll_no VARCHAR(50) PRIMARY KEY,
        name VARCHAR(100),
        phone_no VARCHAR(20),
        address VARCHAR(200)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS parents (
        father_name VARCHAR(100),
        phone_no VARCHAR(20),
        occupation VARCHAR(100),
        child_roll_no VARCHAR(50),
        FOREIGN KEY (child_roll_no) REFERENCES students(roll_no)
    )
''')
def show_teacher_options():
    app_window.deiconify()
    login_window.withdraw()

    label_options = tk.Label(app_window, text="Teacher Options")
    label_options.pack()

    btn_register_student = tk.Button(app_window, text="Register Student", command=show_registration_window)
    btn_register_student.pack()

    btn_edit_student = tk.Button(app_window, text="Edit Student", command=show_edit_window)
    btn_edit_student.pack()

    btn_see_all_students = tk.Button(app_window, text="See All Students", command=show_all_students)
    btn_see_all_students.pack()


def show_registration_window():
    app_window.withdraw()
    register_window.deiconify()

def show_edit_window():
    def delete_student():
        # Get the roll_no from the entry widget
        roll_no = entry_roll_no_edit.get()

        # Delete the student and parent data from the tables
        cursor.execute("DELETE FROM parents WHERE child_roll_no=%s", (roll_no,))
        cursor.execute("DELETE FROM students WHERE roll_no=%s", (roll_no,))
        

        conn.commit()
        messagebox.showinfo("Success", "Student data deleted successfully!")

        # Close the edit window and show the registration window again
        edit_window.withdraw()
        register_window.deiconify()

    # Create the edit window
    edit_window = tk.Toplevel()
    edit_window.title("Edit Student Data")
    edit_window.geometry("300x100")

    label_roll_no_edit = tk.Label(edit_window, text="Enter Roll No:")
    label_roll_no_edit.pack()
    entry_roll_no_edit = tk.Entry(edit_window)
    entry_roll_no_edit.pack()

    btn_delete_student = tk.Button(edit_window, text="Delete Student", command=delete_student)
    btn_delete_student.pack()

def show_all_students():
    # Get all students from the database
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    # Create a new window to display all students
    all_students_window = tk.Toplevel()
    all_students_window.title("All Students")
    all_students_window.geometry("400x300")

    # Create a listbox to display the student information
    listbox_students = tk.Listbox(all_students_window, width=40)
    listbox_students.pack(padx=10, pady=10)

    # Insert each student's information into the listbox
    for student in students:
        student_info = f"Roll No: {student[0]}, Name: {student[1]}, Phone No: {student[2]}, Address: {student[3]}"
        listbox_students.insert(tk.END, student_info)

    # Add a scrollbar to the listbox in case there are too many students
    scrollbar = tk.Scrollbar(all_students_window)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    listbox_students.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox_students.yview)
# Function to handle user registration
def generate_roll_number():
    while True:
        # Generate a random integer between 100000 and 999999 (6-digit roll number)
        roll_no = str(random.randint(1, 1000))
        
        # Check if the generated roll number already exists in the database
        cursor.execute("SELECT * FROM students WHERE roll_no=%s", (roll_no,))
        if not cursor.fetchone():
            return roll_no

def register_student():
    name = entry_name.get()
    roll_no = generate_roll_number()
    phone_no = entry_phone_no.get()
    address = entry_address.get()
    father_name = entry_father_name.get()
    father_phone_no = entry_father_phone.get()
    occupation = entry_occupation.get()

    # Check if the roll_no already exists in the database
    cursor.execute("SELECT * FROM students WHERE roll_no=%s", (roll_no,))
    if cursor.fetchone():
        messagebox.showerror("Error", "Student with the given roll number already exists!")
        return

    # Insert data into students table
    cursor.execute("INSERT INTO students VALUES (%s, %s, %s, %s)", (roll_no, name, phone_no, address))

    # Insert data into parents table
    cursor.execute("INSERT INTO parents VALUES (%s, %s, %s, %s)", (father_name, father_phone_no, occupation, roll_no))

    conn.commit()
    messagebox.showinfo("Success", "Student registered successfully!")
    register_window.withdraw()

# Function to handle login
def login():
    # Check if the teacher's credentials are valid from the database
    username = entry_username.get()
    password = entry_password.get()

    # Hash the password for security
    #hashed_password = hashlib.sha256(password.encode()).hexdigest()
    hashed_password = password

    cursor.execute("SELECT * FROM teachers WHERE username=%s AND password=%s", (username, hashed_password))
    if cursor.fetchone():
        # Enable the main application window after successful login
        show_teacher_options()
        app_window.deiconify()
        login_window.withdraw()
    else:
        messagebox.showerror("Error", "Invalid credentials!")


register_window = tk.Toplevel()
register_window.title("Register Student")
register_window.geometry("400x400")
register_window.withdraw()


label_name = tk.Label(register_window, text="Name")
label_name.pack()
entry_name = tk.Entry(register_window)
entry_name.pack()

label_phone_no = tk.Label(register_window, text="Phone No")
label_phone_no.pack()
entry_phone_no = tk.Entry(register_window)
entry_phone_no.pack()

label_address = tk.Label(register_window, text="Address")
label_address.pack()
entry_address = tk.Entry(register_window)
entry_address.pack()

label_father_name = tk.Label(register_window, text="Father's Name")
label_father_name.pack()
entry_father_name = tk.Entry(register_window)
entry_father_name.pack()

label_father_phone = tk.Label(register_window, text="Father's Phone No")
label_father_phone.pack()
entry_father_phone = tk.Entry(register_window)
entry_father_phone.pack()

label_occupation = tk.Label(register_window, text="Father's Occupation")
label_occupation.pack()
entry_occupation = tk.Entry(register_window)
entry_occupation.pack()

btn_register = tk.Button(register_window, text="Register", command=register_student)
btn_register.pack()

# Create the main application window (app_window)
app_window = tk.Tk()
app_window.title("Teacher Application")
app_window.geometry("600x400")
app_window.withdraw()

# Create the login window (login_window) with login, signup, and forgot password options
login_window = tk.Toplevel()
login_window.title("Login")
login_window.geometry("300x150")

label_username = tk.Label(login_window, text="Username")
label_username.pack()
entry_username = tk.Entry(login_window)
entry_username.pack()

label_password = tk.Label(login_window, text="Password")
label_password.pack()
entry_password = tk.Entry(login_window, show="*")
entry_password.pack()

btn_login = tk.Button(login_window, text="Login", command=login)
btn_login.pack()

login_window.mainloop()

app_window.mainloop()
