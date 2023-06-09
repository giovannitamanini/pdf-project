#Importing modules
import mysql.connector
import PyPDF2
import time
from multiprocessing.pool import ThreadPool
#from multiprocessing import Pool

# Procedure to counting words in PDF

# =========================================
HOST = "localhost"
USER = "root"
PASSWD = "12345"
# =========================================

class WordCount():
	cursor = None
	
	def __init__( self, pdf_id):
		
		con = mysql.connector.connect(host = HOST, user = USER, passwd = PASSWD)
		
		print("\nProcessing PDF %d count" %pdf_id)

		#Printing info about MySQL Server
		db_info = con.get_server_info()
		#print("\nconnected in MySQL v", db_info,"\n")

		#Establishing cursor
		self.cursor = con.cursor()

		query = "USE pdf_project"
		self.cursor.execute(query)
		
		#self.cursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED")
		
		with con:		
			query = "SELECT word FROM word_count WHERE id_pdf_information = '%d'" %pdf_id
			self.cursor.execute(query)
			words = self.cursor.fetchall()

			if len(words) == 0 :
				
				query = "SELECT path FROM pdf_information WHERE id = '%d'" %pdf_id
				self.cursor.execute(query)
				pdf_path = self.cursor.fetchone()
				pdf_path = str(" ".join(pdf_path)) #List to String

				#Opening pdf file
				pdf = open(pdf_path, 'rb')
				pdf_object = PyPDF2.PdfReader(pdf)
				pages = len(pdf_object.pages)
				
				#For each page, the text is read, and the words are stored in a list
				#In the range function the first argument starts at 0 if we want to read from the first page
				for page in range(1, pages) :
					
					#The first page is equal to page+1
					#print("Page:", page + 1)
					page_num = page + 1
					pageObj = pdf_object.pages[page]
					
					#The page conntent is stored in a string
					page_conntent = pageObj.extract_text()
					
					#Replace special characters with white ' ' in string
					page_conntent = page_conntent.replace('/',' ').replace('-',' ').replace('.',' ').replace(',',' ').replace(':',' ').replace(';',' ').replace('!',' ').replace('?',' ').replace('"',' ').replace("'",' ').replace('(',' ').replace(')',' ').replace('_',' ').replace('―',' ').replace('–', ' ').replace('>',' ').replace('»', ' ').replace('•', ' ').replace('”', ' ')	
					
					#A replace of digits with white ' ' in the string
					page_conntent = page_conntent.replace('0',' ').replace('1',' ').replace('2',' ').replace('3',' ').replace('4',' ').replace('5',' ').replace('6',' ').replace('7',' ').replace('8',' ').replace('9',' ')
					
					#With split() we separate the words by storing them in a list
					word_list = page_conntent.split()
					
					#Reading each of the words on the list
					for word in word_list :
						
						#Leaving only the first letter capitalized in the word
						word = word.capitalize()

						#If the word has only one character replace it with "nothing"
						if len(word) == 1:
							word = "" 
						
						#If the word is different from "nothing", execute block
						if word != "" :

							#print(word)

							#Testing if the parsed word is in the exceptions word table
							query = "SELECT word FROM word_exception WHERE word = '%s' " %word
							self.cursor.execute(query)
							words = self.cursor.fetchall()

							#If the parsed word is not in the exceptions table, execute the following block
							if len(words) == 0 :

								query = "SELECT word FROM word_count WHERE id_pdf_information = '%d' AND word = '%s'" %(pdf_id, word)
								self.cursor.execute(query)
								words = self.cursor.fetchall()

								if len(words) == 0 :
									if "Jesus" in word :
										if len(word) == 5 :
											print(word + " - Comprimento = " + str(len(word)))
											query = "INSERT INTO word_count (id_pdf_information, word, count) VALUES ('%d', '%s', 1) " %(pdf_id, word)
											self.cursor.execute(query)
										else :
											print("A página da palavra corrompida é : " + str(page_num) + " e o PDF tem o ID: " + str(pdf_id))
											continue
									else :
										query = "INSERT INTO word_count (id_pdf_information, word, count) VALUES ('%d', '%s', 1) " %(pdf_id, word)
										#print(query)
										self.cursor.execute(query)
			
								else:
									query = "UPDATE word_count SET count = count + 1 WHERE id_pdf_information = '%d' AND word = '%s'" %(pdf_id, word)
									#print(query)
									self.cursor.execute(query)

								query = "INSERT INTO word_page_number (id_pdf_information, word, page_number) VALUES ('%d', '%s', '%d')" %(pdf_id, word, page_num)
								#print(query)
								self.cursor.execute(query)

			else :
				print("\nThis PDF has already been analyzed!")

			#Commiting changes
			con.commit()

		if con.is_connected() :
			self.cursor.close()
			con.close()