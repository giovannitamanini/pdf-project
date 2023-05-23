# PDF Project
This project was created for training the Python programming language in conjunction with the use of the MySQL database. Primarily consists of using a programs menu where the user can analyze PDF files, counting and classifying the words that are most used. A CSV file contains exception words (as well as articles) that will be disregarded in the procedures. A CRUD program for recording, reading, updating and removing records was developed to maintain a table (special word) that stores words that the user may consider important in future analyses. With new updates, the objective is to generate an index of the words that appear most in the specified PDFs and also of the special words.

## Considerations
Built and tested with Windows 10/11, Python 3.9.13('base':conda), MySQL v.8.0.31

You will need a folder called pdfs in the root folder containing the pdfs for analysis, and:

````
pip install PyPDF2
pip install mysql-connector-python
pip install matplotlib
````

## Documentation

First, run the program to create the database in MySQL, assuming that the user has already made the previous configurations in the database:

````
python create_db.py
````

Run the programs menu to choose a feature:

````
python programs_menu.py
````

First register the most important information of the pdf in the database, running option [1];

Add the words exceptions from the CSV file by running option [2]. Remembering that exception words will not be counted in the word analysis of the pdf (that's why they are exceptions);

If you want to add some more exception words to the database, run option [3];

Choose option [4] for the application to register the words in the pdf in the database and count how many times they appear;

If you want to show which words appear most in the pdf, run option [5];

Select option [6] to generates index for a chosen PDF;

If you want to generate a bar chart with the words that appear the most in a given PDF choose option [7];

You can add some word that you think is special in the analysis, using CRUD Special Word (option [8]);

To exit choose option [0];

## Authors
Giovanni de Aguirre Tamanini

Juarez Tamanini

## Version
PDF Project v0.2.0
