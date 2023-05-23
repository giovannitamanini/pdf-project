#Programs menu for the PDF project
import os

def run_program(option):
    #Use the ls shell1 command
	#Erase the screen
	os.system("cls")
	
	print("Starting execution of selected program...")
	if option == 1:
		os.system("python insert_pdf_info.py")
	elif option == 2:
		os.system("python insert_csv_exception_file.py")
	elif option == 3:
		os.system("python insert_exception.py")
	elif option == 4:
		os.system("python count_word_pdf_OO_multi.py")
	elif option == 5:
		os.system("python top_words.py")
	elif option == 6:
		os.system("python generates_index.py")
	elif option == 7:
		os.system("python plot.py")
		os.system("python plot2.py")
	elif option == 8:
		os.system("python crud.py")
	print()
	answer = input("Press enter to return to the program menu...")
		
def main():
	while True:
		os.system("cls")
		print("-" * 70)
		print("PDF Project - Programs Menu")
		print("-" * 70)
		print()
		print("Options: ")
		print("[1] - Register PDF information")
		print("[2] - Add exceptions from a csv file")
		print("[3] - Register exception words for analyzes")
		print("[4] - Count the words of the given PDF")
		print("[5] - Show the top words of the chosen PDF")
		print("[6] - Generates index for the chosen PDF")
		print("[7] - Generates a bar chart with the words that appear the most in a given PDF")
		print("[8] - CRUD Special Word")
		print("[0] - Exit menu")
		print()
		print("-" * 70)
		print()
		
		answer = ""
		answer = input("Your option: ")
		
		if answer == None or answer == "" or answer.isalpha():
			option = 99
			break
			
		option = int(answer)
		if option == 0:
			break
		elif option > 0 and option < 9:
			run_program(option)
			break
		
	if option != 0:
		os.system("python programs_menu.py")
	
main()