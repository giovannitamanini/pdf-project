# Script to generate line graphs with counted words
# ===========================================================
# Imports 
import mysql.connector
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

# =====================================================
#Output graphs PATH
output_directory = "C:/Users/gdatn/Documentos/python/estudos/Atividades/pdfProject/graphs"

# =====================================================
# Functions
def search_pdf_data (pdf) :
    global words
    global counts
    global name
    global labx

    sql_string = "SELECT number_top_words, name FROM pdf_information WHERE id = %d" %pdf
    cursor.execute(sql_string)
    lines = cursor.fetchone()
    number = lines[0]
    name = lines[1]
    sql_string = "SELECT word, count FROM word_count WHERE id_pdf_information = %d ORDER BY count DESC LIMIT %d" %(pdf, number)
    cursor.execute(sql_string)
    lines = cursor.fetchall()

    words = []
    counts = []
    labx = []
    number = 1
    for line in lines :
        words.append(line[0])
        counts.append(line[1])
        labx.append("Top#"+str(number))
        number += 1

    return()
        
# =====================================================
# Procedures
# Program Start...
global con 

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

global words
global counts
global labx
labx = []

#If connection is on, execute following
if con.is_connected() :

    #Printing info about MySQL Server
    db_info = con.get_server_info()
    print("\nConnected in MySQL v", db_info,"\n")
    
    #Establishing cursor
    cursor = con.cursor()

    sql_string = "USE pdf_project"
    cursor.execute(sql_string)

    sql_string = "SELECT DISTINCT id_pdf_information FROM word_count ORDER BY id_pdf_information"
    cursor.execute( sql_string )
    lines = cursor.fetchall()

    if len(lines) == 0:
        print("There is no data for any pdf yet!")
        exit(0)    
    
    pdfs = []

    for line in lines:
        id_pdf = line[0]
        if id_pdf not in pdfs:
            pdfs.append(id_pdf)
      
    sum_count = [0,0,0,0,0,0,0,0,0,0]

    # Plots
    plt.figure(figsize=(10, 6))
    count_pdf = 0
    for pdf in pdfs:
        search_pdf_data(pdf)
        x = labx
        y = counts
        text_label = str(name[0:29])
        print("-" * 60)
        print("words = ", words)
        print("y = ", y)
        print("labx = ", labx)

        plt.plot(x, y, label = text_label)
        #plt.xlabel("Top Words")
        plt.ylabel("Count")
        plt.legend()
        plt.title("Word Count for PDFs")
        #plt.xticks(x, labx)
        plt.grid(axis = 'y')
        
        for i, count in enumerate(counts):
            sum_count[i] = sum_count[i] + count
            
        print("sum_count = ", sum_count)
        count_pdf += 1

    avg_count = [sumc / count_pdf for sumc in sum_count]
    
    print("avg_count = ", avg_count)
    
    text_label = "Avg of all PDFs"
    plt.plot(x, avg_count, label = text_label, linewidth=4.0, linestyle='-')
    plt.legend()
    
    graph_archive = "pdfs_average_graph.png"
    output_archive = output_directory + "/" + graph_archive
    plt.savefig(output_archive, dpi = 300)
    print("Saving graph")
    plt.close()