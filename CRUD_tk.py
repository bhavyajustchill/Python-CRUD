import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from tkinter import *

def get_single_record(event):
    reset_entries()
    try:
        row_id = treeview.selection()[0]
        select = treeview.set(row_id)
        entry1.insert(0,select['Employee ID'])
        entry2.insert(0,select['Employee Name'])
        entry3.insert(0,select['Mobile Number'])
        entry4.insert(0,select['Employee Salary'])
    except Exception as e:
        print(e)

def insert_data():
    id = entry1.get()
    empname = entry2.get()
    mobile = entry3.get()
    salary = entry4.get()
    
    try:
        mydb=mysql.connector.connect(host="localhost", user="root", password="", database="crud_tk_py")
        mycursor=mydb.cursor()
        sql = "INSERT INTO  registration (id,empname,mobile,salary) VALUES (%s, %s, %s, %s)"
        val = (id,empname,mobile,salary)
        mycursor.execute(sql, val)
        mydb.commit()
        lastid = mycursor.lastrowid
        messagebox.showinfo("Success!", "Record Inserted Successfully!")
        show()
        reset_entries()
    except Exception as e:
        print(e)
        mydb.rollback()
        mydb.close()

def update_data():
    id = entry1.get()
    empname = entry2.get()
    mobile = entry3.get()
    salary = entry4.get()
    try:
        mydb=mysql.connector.connect(host="localhost", user="root", password="", database="crud_tk_py")
        mycursor=mydb.cursor()
        sql = "Update  registration set empname= %s,mobile= %s,salary= %s where id= %s"
        val = (empname,mobile,salary,id)
        mycursor.execute(sql, val)
        mydb.commit()
        lastid = mycursor.lastrowid
        messagebox.showinfo("Success!", "Record Updated Successfully!")
        show()
        reset_entries()
    except Exception as e:
        print(e)
        mydb.rollback()
        mydb.close()

def delete_data():
    id = entry1.get()
    try:
        mydb=mysql.connector.connect(host="localhost", user="root", password="", database="crud_tk_py")
        mycursor=mydb.cursor()
        sql = "delete from registration where id = %s"
        val = (id,)
        mycursor.execute(sql, val)
        mydb.commit()
        lastid = mycursor.lastrowid
        messagebox.showinfo("Success!", "Record Deleted Successfully!")
        show()
        reset_entries()
    except Exception as e:
        print(e)
        mydb.rollback()
        mydb.close()

def reset_entries():
    entry1.delete(0, END)
    entry2.delete(0, END)
    entry3.delete(0, END)
    entry4.delete(0, END)
    entry1.focus_set()

def reset():
    reset_entries()
    treeview.selection_remove(*treeview.selection())

def show():
    try:
        mydb = mysql.connector.connect(host="localhost", user="root", password="", database="crud_tk_py")
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM registration")
        records = mycursor.fetchall()

        for item in treeview.get_children():
            treeview.delete(item)

        for i, (id,stname, course,fee) in enumerate(records, start=1):
            treeview.insert("", "end", values=(id, stname, course, fee))
            mydb.close()
    except Exception as e:
        print(e)

root = Tk()
root.title("Python - CRUD with Tkinter + MySQL")
root.geometry("925x525")
global entry1
global entry2
global entry3
global entry4

tk.Label(root, text="CRUD with Tkinter + MySQL", font=(None, 30)).place(x=360, y=40)
tk.Label(root, text="Employee ID").place(x=10, y=10)
tk.Label(root, text="Employee Name").place(x=10, y=40)
tk.Label(root, text="Mobile Number").place(x=10, y=70)
tk.Label(root, text="Employee Salary").place(x=10, y=100)

entry1 = Entry(root)
entry1.place(x=140, y=10)
entry2 = Entry(root)
entry2.place(x=140, y=40)
entry3 = Entry(root)
entry3.place(x=140, y=70)
entry4 = Entry(root)
entry4.place(x=140, y=100)

tk.Button(root, text="Insert", command = insert_data, height=2, width=10).place(x=160, y=140) #Insert Button Color - #84E8F8
tk.Button(root, text="Update", command = update_data, height=2, width=10).place(x=280, y=140) #Update Button Color - #84F894
tk.Button(root, text="Delete", command = delete_data, height=2, width=10).place(x=400, y=140) #Delete Button Color - #FF9999
tk.Button(root, text="Reset", command = reset, height=2, width=10).place(x=520, y=140) #Reset Button Color - #F4FE82

cols = ('Employee ID', 'Employee Name', 'Mobile Number','Employee Salary')
treeview = ttk.Treeview(root, columns=cols, show='headings')

for col in cols:
    treeview.heading(col, text=col)
    treeview.grid(row=1, column=0, columnspan=2)
    treeview.place(x=60, y=250)
    treeview.column(col, anchor="center")

show()
treeview.bind('<Double-Button-1>',get_single_record)
root.mainloop()
