#Importing modules
import mysql.connector
import PyPDF2

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

    if con.is_connected() :
        
        query = "SELECT id, name FROM pdf_information"
        cursor.execute(query)
        info = cursor.fetchall()

        print("Choose one PDF below to count the number of occurrences of the words\n")

        for row in info :
            print(str(row[0]) + " - " + str(row[1]))

        pdf_id = int(input("\nFor which pdf should the count be made? Enter the related number shown above: "))

        query = "SELECT word FROM word_count WHERE id_pdf_information = '%d'" %pdf_id
        cursor.execute(query)
        words = cursor.fetchall()

        if len(words) == 0 :
            
            query = "SELECT path FROM pdf_information WHERE id = '%d'" %pdf_id
            cursor.execute(query)
            pdf_path = cursor.fetchone()
            pdf_path = str(" ".join(pdf_path)) #List to String

            #Opening pdf file
            pdf = open(pdf_path, 'rb')
            pdf_object = PyPDF2.PdfReader(pdf)
            pages = len(pdf_object.pages)
            
            #For each page, the text is read, and the words are stored in a list
            #In the range function the first argument starts at 0 if we want to read from the first page
            for page in range(1, pages) :
                
                #The first page is equal to page+1
                print("Page:", page + 1)
                page_num = page + 1
                pageObj = pdf_object.pages[page]
                
                #The page content is stored in a string
                page_content = pageObj.extract_text()
                
                #Replace special characters with white ' ' in string
                page_content = page_content.replace('/',' ').replace('-',' ').replace('.',' ').replace(',',' ').replace(':',' ').replace(';',' ').replace('!',' ').replace('?',' ').replace('"',' ').replace("'",' ').replace('(',' ').replace(')',' ').replace('_',' ').replace('―',' ').replace('–', ' ').replace('>',' ').replace('»', ' ').replace('•', ' ')    
                
                #A replace of digits with white ' ' in the string
                page_content = page_content.replace('0',' ').replace('1',' ').replace('2',' ').replace('3',' ').replace('4',' ').replace('5',' ').replace('6',' ').replace('7',' ').replace('8',' ').replace('9',' ')
                
                #With split() we separate the words by storing them in a list
                word_list = page_content.split()
                
                #Reading each of the words on the list
                for word in word_list :
                    
                    #Leaving only the first letter capitalized in the word
                    word = word.capitalize()

                    #If the word has only one character replace it with "nothing"
                    if len(word) == 1:
                        word = "" 
                    
                    #If the word is different from "nothing", execute block
                    if word != "" :

                        print(word)

                        #Testing if the parsed word is in the exceptions word table
                        query = "SELECT word FROM word_exception WHERE word = '%s' " %word
                        cursor.execute(query)
                        words = cursor.fetchall()

                        #If the parsed word is not in the exceptions table, execute the following block
                        if len(words) == 0 :

                            query = "SELECT word FROM word_count WHERE id_pdf_information = '%d' AND word = '%s'" %(pdf_id, word)
                            cursor.execute(query)
                            words = cursor.fetchall()

                            if len(words) == 0 :
                                query = "INSERT INTO word_count (id_pdf_information, word, count) VALUES ('%d', '%s', 1) " %(pdf_id, word)
                                cursor.execute(query)
        
                            else:
                                query = "UPDATE word_count SET count = count + 1 WHERE id_pdf_information = '%d' AND word = '%s'" %(pdf_id, word)
                                cursor.execute(query)

                            query = "INSERT INTO word_page_number (id_pdf_information, word, page_number) VALUES ('%d', '%s', '%d')" %(pdf_id, word, page_num)
                            cursor.execute(query)

        else :
            print("\nThis PDF has already been analyzed!") 

        answer = input("\nDo you want to analyze another pdf? Enter [Y] if is true or [N] to exit:")

    if answer != 'Y' :
        control = False

#Commiting changes
con.commit()

#If the connection is still opened, close the connection
if con.is_connected() :
    cursor.close()
    con.close()
    print("\nMySQL connection closed.")