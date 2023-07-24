# Program with graphic interface for registration (CRUD) in a table
# Packages
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
import mysql.connector

# Definition of the program's global variables:
global table
global last 
global actual 
global pdf_name

# The program already starts showing the first record of the table, if it exists
actual = 0 

# Program functions
def first_function():
	global table
	global last
	global actual
	global pdf_name
	
	actual = 0
	
	if last == -1:
		status_msg = "There are no registers in the table. Use the 'Add' option to add new registers"
		status = ttk.Label(screen, text=status_msg, width=65, border=1, relief=SUNKEN, anchor=W).place(x=5, y=200)
	else:
		item = table[actual]
		entry_pdf.delete(0,"end")
		entry_pdf.insert(0,item[1])
		entry_word.delete(0,"end")
		entry_word.insert(0,item[2])
		status_msg = "First register of the table"
		status = ttk.Label(screen, text=status_msg, width=65, border=1, relief=SUNKEN, anchor=W).place(x=5, y=200)
	
def previous_function():
	global table
	global last
	global actual

	actual -= 1

	if last == -1:
		status_msg = "There are no registers in the table. Use the 'Add' option to add new registers"
		status = ttk.Label(screen, text=status_msg, width=65, border=1, relief=SUNKEN, anchor=W).place(x=5, y=200)
	else:
		if actual < 0:
			actual = 0
			status_msg = "You are already on the first register of the table"
		else:
			status_msg = "Previous register of the table"
		item = table[actual]
		print(item)
		entry_pdf.delete(0,"end")
		entry_pdf.insert(0,item[1])
		entry_word.delete(0,"end")
		entry_word.insert(0,item[2])
		status = ttk.Label(screen, text=status_msg, width=65, border=1, relief=SUNKEN, anchor=W).place(x=5, y=200)
		
def next_function():
	global table
	global last
	global actual
	
	actual += 1
		
	if last == -1:
		status_msg = "There are no registers in the table. Use the 'Add' option to add new registers"
		status = ttk.Label(screen, text=status_msg, width=65, border=1, relief=SUNKEN, anchor=W).place(x=5, y=200)
	else:
		if actual > last:
			actual = last
			status_msg = "You are already on the last register of the table"
		else: 
			status_msg = "Next register of the table"
		item = table[actual]
		print(item)
		entry_pdf.delete(0,"end")
		entry_pdf.insert(0,item[1])
		entry_word.delete(0,"end")
		entry_word.insert(0,item[2])
		status = ttk.Label(screen, text=status_msg, width=65, border=1, relief=SUNKEN, anchor=W).place(x=5, y=200)
		
def last_function():
	global table
	global last
	global actual
	global pdf_name
	
	actual = last
	if last == -1:
		status_msg = "There are no registers in the table. Use the 'Add' option to add new registers"
		status = ttk.Label(screen, text=status_msg, width=65, border=1, relief=SUNKEN, anchor=W).place(x=5, y=200)
	else:
		item = table[actual]
		entry_pdf.delete(0,"end")
		entry_pdf.insert(0,item[1])
		entry_word.delete(0,"end")
		entry_word.insert(0,item[2])
		status_msg = "Last register of the table"
		status = ttk.Label(screen, text=status_msg, width=65, border=1, relief=SUNKEN, anchor=W).place(x=5, y=200)
	
def add_function():
	status_msg = "You have selected the 'Add' option"
	entry_id_pdf.delete(0,"end")
	pdf_name_add.delete(0,"end")
	entry_word_add.delete(0,"end")
	frameAdd.place(x=5,y=50, width=360, height=140)
	status_msg = "Add function selected! Enter the data and press the OK button"		
	status = ttk.Label(screen, text=status_msg, width=65, border=1, relief=SUNKEN, anchor=W).place(x=5, y=200)

def commit_add():
	global table
	global last 
	global actual
	global pdf_name	
	
	v_id_pdf = entry_id_pdf.get()
	word = entry_word_add.get()
	print(word)
	if v_id_pdf == "" or word == "":
		status_msg = "Enter a PDF and a Word before pressing the OK button!"
		status = ttk.Label(screen, text=status_msg, width=65, border=1, relief=SUNKEN, anchor=W).place(x=5, y=200)
	else:
		id_pdf = int(v_id_pdf)
		query = "SELECT * FROM special_word Where id_pdf_information = %d and word = '%s' " %(id_pdf, word)
		print(query)
		cursor.execute(query)
		result = cursor.fetchall()
		if len(result) == 0:
			query = "INSERT INTO special_word (id_pdf_information, word) VALUES (%d,'%s')" %(id_pdf, word)
			cursor.execute(query )
			#Commiting changes
			con.commit()
			status_msg = "Special word successfully added!"
			status = ttk.Label(screen, text=status_msg, width=65, border=1, relief=SUNKEN, anchor=W).place(x=5, y=200)
		
			# Commands to reposition the register navigation pointer
			query = "SELECT id, name, word FROM pdf_information, special_word Where id = id_pdf_information ORDER BY id, word;"
			cursor.execute(query)
			table = cursor.fetchall()
			print(table)
			last = len(table) - 1
			item_add = (id_pdf, pdf_name, word)
			actual = table.index(item_add)
			print(actual)
			item = table[actual]
			entry_pdf.delete(0,"end")
			entry_pdf.insert(0,item[1])
			entry_word.delete(0,"end")
			entry_word.insert(0,item[2])
			
		else:
			status_msg = "This word has already been reported for this PDF!"
			status = ttk.Label(screen, text=status_msg, width=65, border=1, relief=SUNKEN, anchor=W).place(x=5, y=200)

def check_informed_data(*args):
	v_id_pdf = str(entry_id_pdf.get())
	word = str(entry_word_add.get())
	word = word.capitalize()
	entry_word_add.delete(0, "end")
	entry_word_add.insert(0, word)
	if v_id_pdf != "" and v_id_pdf.isnumeric:
		id_pdf = int(v_id_pdf)
		if not exist_counted_pdf(id_pdf):
			entry_id_pdf.delete(0, "end")
			pdf_name_add.delete(0, "end")
			status_msg = "Enter a PDF ID already registered and that already has the words counted!"
			status = ttk.Label(screen, text=status_msg, width=65, border=1, relief=SUNKEN, anchor=W).place(x=5, y=200)
		else:
			if word != "":
				if not word_in_pdf(id_pdf, word):
					entry_word_add.delete(0, "end")
					status_msg = "The word '%s' is missing from the list of word counts in this PDF!" %word
					status = ttk.Label(screen, text=status_msg, width=65, border=1, relief=SUNKEN, anchor=W).place(x=5, y=200)
				else:
					status_msg = "Press OK button to complete the Add"		
					status = ttk.Label(screen, text=status_msg, width=65, border=1, relief=SUNKEN, anchor=W).place(x=5, y=200)
	
def exist_counted_pdf(id_pdf):
	global pdf_name
	query = "SELECT name FROM pdf_information, word_count WHERE id = id_pdf_information AND id = %d" %id_pdf
	cursor.execute(query)
	result = cursor.fetchall()
	if len(result) == 0:
		return False
	else:
		pdf_name = result[0][0]
		pdf_name_add.delete(0, "end")
		pdf_name_add.insert(0, pdf_name)
		return True

def word_in_pdf(id_pdf, palavra):
	query = "SELECT * FROM word_count Where id_pdf_information = %d and word = '%s' " %(id_pdf, palavra)
	#print(query)
	cursor.execute(query)
	result = cursor.fetchall()
	if len(result) == 0:
		return False
	else:
		return True

def upd_function():
	status_msg = "Update functionality is disabled!"
	status = ttk.Label(screen, text=status_msg, width=65, border=1, relief=SUNKEN, anchor=W).place(x=5, y=200)

def del_function():
	global table
	global last 
	global actual
	global pdf_name

	v_name_pdf = entry_pdf.get()
	word = entry_word.get()

	if last != -1:
		#Use list table to take key id = table[0]
		query = "SELECT DISTINCT id FROM pdf_information WHERE name = '%s' ;" %v_name_pdf
		cursor.execute(query)
		result = cursor.fetchall()
		v_id_pdf = result[0]
		id_pdf = int(v_id_pdf[0])

		print(word)
	
		if messagebox.askyesno("Do you really want to delete?"):
			query = "DELETE FROM special_word WHERE id_pdf_information = %d AND word = '%s' ;" %(id_pdf, word)
			print(query)
			cursor.execute(query)
			#Commiting changes
			con.commit()
			entry_pdf.delete(0,"end")
			entry_word.delete(0,"end")
			status_msg = "Important word successfully deleted!"
			status = ttk.Label(screen, text=status_msg, width=65, border=1, relief=SUNKEN, anchor=W).place(x=5, y=200)
		
			# Commands to reposition the register navigation pointer
			query = "SELECT id, name, word FROM pdf_information, special_word Where id = id_pdf_information ORDER BY id, word;"
			cursor.execute(query)
			table = cursor.fetchall()
			print(table)
			last = len(table) - 1

			if last != -1:
				print(actual)
				item = table[actual]
				entry_pdf.delete(0,"end")
				entry_pdf.insert(0,item[1])
				entry_word.delete(0,"end")
				entry_word.insert(0,item[2])
			else:
				status_msg = "All registers have already been deleted"
				status = ttk.Label(screen, text=status_msg, width=65, border=1, relief=SUNKEN, anchor=W).place(x=5, y=200)
	
	else:
		status_msg = "There is no register to be deleted!"
		status = ttk.Label(screen, text=status_msg, width=65, border=1, relief=SUNKEN, anchor=W).place(x=5, y=200)

def exit_function():
	status_msg = "You have selected the 'Exit' option"
	status = ttk.Label(screen, text=status_msg, width=65, border=1, relief=SUNKEN, anchor=W).place(x=5, y=200)
	if messagebox.askyesno("Do you want to leave the program?"):
		exit(0)	

def close_frame():
	frameAdd.place(x=0,y=0, width=0, height=0)
	#frameAdd.destroy
	status_msg = "Select a navigation option by clicking one of the buttons above..."
	status = ttk.Label(screen, text=status_msg, width=65, border=1, relief=SUNKEN, anchor=W).place(x=5, y=200)

#Connecting to MySQL
# =========================================
HOST = "localhost"
USER = "root"
PASSWD = "12345"
# =========================================
"""
HOST = input("Enter MySQL Host: ")
USER = input("Enter your MySQL User: ")
PASSWD = input("Enter the password: ")
"""

con = mysql.connector.connect(host = HOST, user = USER, passwd = PASSWD)

if con.is_connected() :
	#Printing info about MySQL Server
	db_info = con.get_server_info()
	print("\nConnected in MySQL v", db_info,"\n")
	#Establishing cursor
	cursor = con.cursor()
	query = "USE pdf_project"
	cursor.execute(query)
		
# Assembly of the graphical interface	
screen=Tk()
screen.title("Special Word Table Maintenance")
screen.geometry("410x230")
btn_first=Button(screen,text="<< ",command=first_function)
btn_first.place(x=10, y=10)
btn_previous=Button(screen,text=" < ",command=previous_function)
btn_previous.place(x=45, y=10)
btn_next=Button(screen,text=" > ",command=next_function)
btn_next.place(x=75, y=10)
btn_last=Button(screen,text=">> ",command=last_function)
btn_last.place(x=105, y=10)
btn_add=Button(screen,text="Add",command=add_function)
btn_add.place(x=140, y=10)
btn_upd=Button(screen,text="Upd",command=upd_function)
btn_upd.place(x=180, y=10)
btn_del=Button(screen,text="Del",command=del_function)
btn_del.place(x=220, y=10)
btn_del=Button(screen,text="Exit",command=exit_function)
btn_del.place(x=255, y=10)

Label(screen,text="               PDF:").place(x=2, y=80) 
entry_pdf = ttk.Entry(screen, width=30)
entry_pdf.place(x=117, y=80) 
Label(screen,text="Special Word:").place(x=2, y=110)
entry_word = ttk.Entry(screen, width=30)
entry_word.place(x=117, y=110)

# -- fields for the Add function screen
frameAdd = Frame(screen, borderwidth=1, relief='solid')
Label(frameAdd,text="               PDF:").place(x=2, y=10)
entry_id_pdf = ttk.Entry(frameAdd, width=4)
entry_id_pdf.place(x=115, y=10)
pdf_name_add = ttk.Entry(frameAdd, width=30)
pdf_name_add.place(x=150, y=10)
Label(frameAdd,text="Special Word:").place(x=2, y=45)
entry_word_add = ttk.Entry(frameAdd, width=30)
entry_word_add.place(x=115, y=45)
btn_ok=Button(frameAdd,text="OK",command=commit_add)
btn_ok.place(x=5, y=95)
btn_cancel=Button(frameAdd,text="Cancel",command=close_frame)
btn_cancel.place(x=40, y=95)

entry_id_pdf.bind('<Return>', check_informed_data)
entry_id_pdf.bind('<Tab>', check_informed_data)
entry_word_add.bind('<Return>', check_informed_data)
entry_word_add.bind('<Tab>', check_informed_data)
screen.bind('<Button-1>', check_informed_data)

# Start of the program
query = "SELECT id, name, word FROM pdf_information, special_word WHERE id = id_pdf_information ORDER BY id, word;"
cursor.execute(query)
table = cursor.fetchall()
if len(table) == 0:
	status_msg = "There are no registers in the table. Use the 'Add' option to add new registers"
	status = ttk.Label(screen, text=status_msg, width=65, border=1, relief=SUNKEN, anchor=W).place(x=5, y=200)
else:
	status_msg = "Select a navigation option by clicking one of the buttons above..."
	status = ttk.Label(screen, text=status_msg, width=65, border=1, relief=SUNKEN, anchor=W).place(x=5, y=200)
	
last = len(table) - 1

if last != -1:
	item = table[actual]
	entry_pdf.delete(0,"end")
	entry_pdf.insert(0,item[1])
	entry_word.delete(0,"end")
	entry_word.insert(0,item[2])
		
screen.mainloop()