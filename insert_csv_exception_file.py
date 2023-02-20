#Importing modules
import mysql.connector
import csv

#Path csv_file
csv_file = ''
answer = input("Do you want to inform the PATH of the CSV file? Or should I keep the default?\nEnter [Y] to inform, or [N] to default:")
if answer == 'Y' :
    csv_file = input("\nEnter the PATH of the CSV file:")

#Connecting to MySQL
HOST = input("Enter MySQL Host: ")
USER = input("Enter your MySQL User: ")
PASSWD = input("Enter the password: ")

con = mysql.connector.connect(host = HOST, user = USER, passwd = PASSWD)

#If connection is on, execute following
if con.is_connected() :
    
    #Printing info about MySQL Server
    db_info = con.get_server_info()
    print("\nConnected in MySQL v", db_info,"\n")
    
    #Establishing cursor
    cursor = con.cursor()

    query = "USE pdf_project"
    cursor.execute(query)

    #Opening csv_file
    with open(csv_file) as file :

        exceptions = csv.reader(file)
        
        #Each line represents an exception word in the csv file
        for line in exceptions :
            
            #Lines started with the # character are ignored in reading
            if '#' not in line[0] :

                exception = line[0].capitalize()
                exception = exception.strip()
                query = "INSERT INTO word_exception (word) VALUES ('%s')" % exception
                cursor.execute(query)

#Commiting changes
con.commit()

#If the connection is still opened, close the connection
if con.is_connected() :
    cursor.close()
    con.close()
    print("\nMySQL connection closed.")   