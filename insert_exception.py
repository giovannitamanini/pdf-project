#Importing modules
import mysql.connector

#Connecting to MySQL
HOST = input("Enter MySQL Host: ")
USER = input("Enter your MySQL User: ")
PASSWD = input("Enter the password: ")

con = mysql.connector.connect(host = HOST, user = USER, passwd = PASSWD)

#Printing info about MySQL Server
db_info = con.get_server_info()
print("\nConnected in MySQL v", db_info,"\n")

#Establishing cursor
cursor = con.cursor()

query = "USE pdf_project"
cursor.execute(query)

control = True

while control :

    #If connection is on, execute following
    if con.is_connected() :

        #Asking for user enter the word exception
        exception = input("Enter the word exception for add: ")
        exception = exception.capitalize()
        
        query = "SELECT word FROM word_exception WHERE word = '%s'" %exception
        cursor.execute(query)
        words = cursor.fetchall()

        if len(words) == 0 :
            query = "INSERT INTO word_exception (word) VALUES ('%s')" %exception
            cursor.execute(query)
            print("Word added succesfully!\n")

        else :
            print("The word already is a exception!\n")
        
        answer = input("Do you want to add another word exception? Enter [Y] to add or [N] to exit the program: ")

        if answer != "Y" : 
            control = False

#Commiting changes
con.commit()

#If the connection is still opened, close the connection
if con.is_connected() :
    cursor.close()
    con.close()
    print("\nMySQL connection closed.")