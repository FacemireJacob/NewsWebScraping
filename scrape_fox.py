#This Script web scrapes articles from the Washington Post
# Article URL Are imported from a folder and organized into categories based on their name

#This script may be blocked by the site if used too much

#By Jacob Facemire


# imports for scraping
import requests;
from bs4 import BeautifulSoup;

#DB imports
import mysql.connector
import csv

## This Method scrapes the body of Articles from the Washington Post
def scrape_article(url):

    #Add to Body Array
    #Make connection
   
    r1 = requests.get(url)
    page = r1.content

    print("Connection Made...")

    #Make soup
    soup = BeautifulSoup(page, 'html.parser')

    print("Soup object is Made...")

    # #Select HTML tag to search for within class
    text = soup.find_all(class_='article-body')
    headline = soup.find('h1')

    articleBody = "" 

    #Build String of Article Body
    for i in range(0, len(text)):
         articleBody = articleBody + " " + text[i].get_text()

      #Clean String
    clean = str.maketrans({"'": r"\'"})
    articleBody = articleBody.translate(clean)

    if(len(articleBody) > 0):
        textAr.append([url, headline.get_text().translate(clean), articleBody])
        print("Text Scraped Succesfully")
    else:
        print("Scraping Failed for Article: " + headline.get_text().translate(clean))


## This method takes inputted Variables and searches for text files to import urls from
def import_url(table):

    # ### Connect To DB
    source = 'sources\FOX\\' + table + '.csv'
        # Initialize Vars
    global textAr; textAr = []

    try:
        conn = mysql.connector.connect(host='localhost', database = 'news', user = 'root', password = 'mysql')

        if conn.is_connected():
            db_info = conn.get_server_info()
            print("Connection made to DB, MySQL version:", db_info)
            cursor = conn.cursor()
            #Make new Table If needed using stock table as guide
            cursor.execute("CREATE TABLE IF NOT EXISTS " + table + " LIKE stock_table")
            cursor.execute("SELECT database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)

            ##Import
            with open(source) as file:
                urlArr = file.read().split(',')

                for i in range(0, len(urlArr)):
                    print(urlArr[i])

            ## Get Article Body
            for i in range(0, len(urlArr)):
                scrape_article(urlArr[i])

            #Add to DB
            for i in range (0, len(textAr)):
                #Build Query
                sqlQuery = "INSERT into " + table + " (Headline, Source, Link, Body) VALUES ('" + textAr[i][1]+"', 'FOX', '" + textAr[i][0] + "', '" + textAr[i][2] + "')"
                try:
                    cursor.execute(sqlQuery)
                    print("Record Inserted")
                except(mysql.connector.Error) as e:
                    print("Insert Failed, most likely duplicate row")
            
            #Commit
            conn.commit()

    except OSError as e:
        print("Error while Connecting: ", e)
## Main Method

print("To Import URL list, store URLs as a CSV file. Please name the file the same name as the DB table it is to be inserted to. The file should be stored in the directory: (this)\\sources\\WaPo. Please enter the name of the file to import:")
print("You can enter as many file names as you want, when you are done type '0'")
x = []
y = ""
while y != "0":
    y = input('file name (leave off .csv): ')
    if y != "0":
        x.append(y)

for i in range(0, len(x)):
    print("Attempting to Import CSV: " + x[i])
    import_url(x[i])