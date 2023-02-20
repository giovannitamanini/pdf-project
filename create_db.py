#Importing modules
import mysql.connector

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
    
    #Excluding, creating and using the database
    query = "DROP DATABASE IF EXISTS pdf_project"
    cursor.execute(query)
    query = "CREATE DATABASE pdf_project"
    cursor.execute(query)
    query = "USE pdf_project"
    cursor.execute(query)
    
    #Excluding and creating tables
    query = "DROP TABLE IF EXISTS pdf_information"
    cursor.execute(query)
    query = "CREATE TABLE pdf_information (id INT NOT NULL AUTO_INCREMENT, path VARCHAR(250) NOT NULL, name VARCHAR(200) NOT NULL, author VARCHAR(45), pages SMALLINT NOT NULL, number_top_words SMALLINT DEFAULT 10, PRIMARY KEY (id))"
    cursor.execute(query)

    query = "DROP TABLE IF EXISTS word_count"
    cursor.execute(query)
    query = "CREATE TABLE word_count (word VARCHAR(30) NOT NULL, count SMALLINT NOT NULL, id_pdf_information INT NOT NULL, PRIMARY KEY (id_pdf_information, word), FOREIGN KEY (id_pdf_information) REFERENCES pdf_information(id))"
    cursor.execute(query)

    query = "DROP TABLE IF EXISTS word_page_number"
    cursor.execute(query)
    query = "CREATE TABLE word_page_number (id_pdf_information INT NOT NULL, word VARCHAR(30) NOT NULL, page_number SMALLINT NOT NULL, FOREIGN KEY (id_pdf_information, word) REFERENCES word_count(id_pdf_information, word))"
    cursor.execute(query)

    query = "DROP TABLE IF EXISTS special_word"
    cursor.execute(query)
    query = "CREATE TABLE special_word (word VARCHAR(30) NOT NULL, id_pdf_information INT NOT NULL, PRIMARY KEY (word, id_pdf_information), FOREIGN KEY (id_pdf_information) REFERENCES pdf_information(id))"
    cursor.execute(query)

    query = "DROP TABLE IF EXISTS word_exception"
    cursor.execute(query)
    query = "CREATE TABLE word_exception (word VARCHAR(30) NOT NULL, PRIMARY KEY (word))"
    cursor.execute(query)

    print("\nDatabase created successfully!\n")

    #Commiting changes
    con.commit()

#If the connection is still opened, close the connection
if con.is_connected() :
    cursor.close()
    con.close()
    print("\nMySQL connection closed.")