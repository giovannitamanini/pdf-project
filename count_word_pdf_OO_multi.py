#Importing modules
import mysql.connector
import PyPDF2
import time
from multiprocessing.pool import ThreadPool # https://docs.python.org/3/library/multiprocessing.html
from multiprocessing import Pool
from entities.WordCount import WordCount

# Class to count PDF
# =========================================
HOST = "localhost"
USER = "root"
PASSWD = "12345"
# =========================================
class CountPDF():
	
	def __init__( self):
	
		#Connecting to MySQL
		#HOST = input("Enter MySQL Host: ")
		#USER = input("Enter your MySQL User: ")
		#PASSWD = input("Enter the password: ")

		con = mysql.connector.connect(host = HOST, user = USER, passwd = PASSWD)

		#Printing info about MySQL Server
		db_info = con.get_server_info()
		print("\nConnected in MySQL v", db_info,"\n")

		#Establishing cursor
		cursor = con.cursor()

		query = "USE pdf_project"
		cursor.execute(query)

		control = True

		if con.is_connected() :
			
			query = "SELECT id, name FROM pdf_information"
			cursor.execute(query)
			info = cursor.fetchall()

			answer = input("\nDo you want to count all the PDF's? Enter [Y] if yes or [N] to choose one: ")
			answer = answer.upper()
			
			if answer == "Y" :
				query = "DELETE FROM word_page_number" 
				cursor.execute(query)
				query = "DELETE FROM word_count"
				cursor.execute(query)
				#Commiting changes
				con.commit()
				
				t1 = time.time()
				pdf_id_array = []
				for row in info :
					self.pdf_id = int(row[0])
					name = row[1]
					pdf_id_array.append( [self.pdf_id] )			
					
				print("---->", pdf_id_array)
				
				pool = ThreadPool( 5 )
				pool.map( self.processPDF, pdf_id_array )
				pool.close()
				pool.join()
				
				'''
				
				with Pool(5) as p:
					p.map( self.processPDF, pdf_id_array )
				
				'''
				t2 = time.time()

				print("\n\nExecution time = %f seconds\n\n" %(t2 - t1))

			else :
				while control:
					print("Choose one PDF below to count the number of occurrences of the words\n")
					
					pdfs_id = []
					for row in info :
						print(str(row[0]) + " - " + str(row[1]))
						pdfs_id.append(str(row[0]))
					
					pdf_id_inf = ""
					while not pdf_id_inf in pdfs_id:
						pdf_id_inf = str(input("\nEnter one related number shown above: "))
						if pdf_id_inf == "":
							break # to allow exit the while looping when the user press enter
					
					if pdf_id_inf != "":					
						self.pdf_id = int(pdf_id_inf)
						wordcount = WordCount( self.pdf_id )
										
					answer = input("\nDo you want to analyze another pdf? Enter [Y] if is true or [N] to exit:")
					answer = answer.upper()
					
					if answer != 'Y' :
						control = False

		
		#If the connection is still opened, close the connection
		if con.is_connected() :
			cursor.close()
			con.close()
			print("\nMySQL connection closed.")
	
	
	def processPDF( self, argumentos ):

		wordcount = WordCount( argumentos[0] )
		
		
if __name__ == "__main__": 
	countpdf = CountPDF()
	
	