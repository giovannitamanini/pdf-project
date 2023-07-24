import matplotlib.pyplot as plt
import mysql.connector

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

#Output graphs PATH
output_directory = "C:/Users/gdatn/Documentos/python/estudos/Atividades/pdfProject/graphs"

con = mysql.connector.connect(host = HOST, user = USER, passwd = PASSWD)

control = True

while control :

    #If connection is on, execute following
    if con.is_connected() :

        #Printing info about MySQL Server
        db_info = con.get_server_info()
        print("\nConnected in MySQL v", db_info,"\n")
        
        #Establishing cursor
        cursor = con.cursor()

        query = "USE pdf_project"
        cursor.execute(query)

        query = "SELECT id, name, number_top_words FROM pdf_information"
        cursor.execute(query)
        info = cursor.fetchall()

        print("Choose one PDF below to show the graph of the top words\n")

        for row in info :
            print(str(row[0]) + " - " + str(row[1]))
        
        pdf_id = int(input("\nEnter the related PDF number shown above:"))

        print("\nThis pdf already contains a default number of top words registered.")
        answer = input("\nDo you want to update the number of top words? Enter [Y] for yes, or [N] for no:")

        if answer == 'Y' :
            number = int(input("Enter a number for the update:"))
            query = "UPDATE pdf_information SET number_top_words = %d WHERE id = %d" %(number, pdf_id)
            cursor.execute(query)

        query = "SELECT number_top_words FROM pdf_information WHERE id = %d" %pdf_id
        cursor.execute(query)
        lines = cursor.fetchone()
        number = lines[0]
        query = "SELECT word, count FROM word_count WHERE id_pdf_information = %d ORDER BY count DESC LIMIT %d" %(pdf_id, number)
        cursor.execute(query)
        lines = cursor.fetchall()

        #Plots
        words = []
        counts = []
        labx = []

        number = 1 #Position of top words

        for i in lines:
            words.append(i[0])
            counts.append(i[1])
            labx.append("Top "+str(number))
            number += 1


        query = "SELECT name FROM pdf_information WHERE id = %d" %pdf_id
        cursor.execute(query)
        info = cursor.fetchone()
        name = info[0]

        plt.figure(figsize=(15, 6))
        # plt.bar to plot a bar graph with given values
        plt.bar(words, counts)
        # Setting xlabel of graph
        #plt.xlabel("Top Words")
        # Setting ylabel of graph
        plt.ylabel("Count of words")
        # Setting title of graph
        plt.title("Top words")
        graph_archive = name + "_" + "graph.png"
        output_archive = output_directory + "/" + graph_archive
        plt.savefig(output_archive, dpi = 300)
        print("Saving graph")
        plt.close()

    answer = input("\nDo you want to do some more analysis? Enter [Y] if yes or [N] to exit the program: ")

    if answer != "Y" : 
        control = False

#Commiting changes
con.commit()

#If the connection is still opened, close the connection
if con.is_connected() :
    cursor.close()
    con.close()
    print("\nMySQL connection closed.")