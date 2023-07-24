#Importing modules
import mysql.connector
import PyPDF2
from pathlib import Path
import glob

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

#If connection is on, execute following
if con.is_connected() :

    #Printing info about MySQL Server
    db_info = con.get_server_info()
    print("\nConnected in MySQL v", db_info,"\n")
    
    #Establishing cursor
    cursor = con.cursor()

    #Making changes
    input_path = 'C://Users//gdatn//Documentos//python//estudos//Atividades//pdfProject//pdfs'
    answer = input("Do you want to inform the PATH of the PDF files? Or should I keep the default?\nEnter [Y] to inform, or [N] to default:")
    if answer == 'Y' :
        input_path = input("\nEnter the PATH of the PDF files:")
    pdfs_folder = Path(input_path)
    pdfs_paths = glob.glob('%s\\*.pdf' %pdfs_folder)

    for pdf_path in pdfs_paths :

        pdf_name = pdf_path.split( "." )[-2].split("\\")[-1]
        pdf_path = pdf_path.replace("\\","/")

        #Reading number of pages information from pdf
        pdf = open(pdf_path, 'rb')
        pdf_obj = PyPDF2.PdfReader(pdf)
        pdf_pages = len(pdf_obj.pages)

        query = "USE pdf_project"
        cursor.execute(query)

        query = "SELECT * FROM pdf_information WHERE path = '%s'" %pdf_path
        cursor.execute(query)
        lines = cursor.fetchall()

        if len(lines) == 0:

            query = "INSERT INTO pdf_information (path, name, pages) VALUES ('%s', '%s', '%d')" %(pdf_path, pdf_name, pdf_pages)
            cursor.execute(query)
        
        else:
            continue

    control = True

    while control:

        answer = input("Do you want to add or update the author of some PDF? Type [Y] to add/update or [N] if you want to exit:")
        
        if answer == 'Y' :

            query = "SELECT id, name FROM pdf_information"
            cursor.execute(query)
            info = cursor.fetchall()

            print("Choose one PDF below to add the author:\n")

            for row in info :
                print(str(row[0]) + " - " + str(row[1]))

            pdf_id = int(input("\nEnter the related number shown above: "))
            author = input("\nEnter the author name:")
            query = "UPDATE pdf_information SET author = '%s' WHERE id = %d" %(author, pdf_id)
            cursor.execute(query)
        
        elif answer != 'Y':
            control = False

#Commiting changes
con.commit()

#If the connection is still opened, close the connection
if con.is_connected() :
    cursor.close()
    con.close()
    print("\nMySQL connection closed.")