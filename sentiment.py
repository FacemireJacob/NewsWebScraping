### Please ensure Python Library "spacy" and the file 'en_core_web_sm' are downloaded in the encironment
###
### they can be done with:
###
### python -m pip install spaCy
### python -m spacy download en_core_web_sm
### $ pip install mysql-connector-python
### $ pip install spacytextblob


from encodings import utf_8
import spacy
from spacytextblob.spacytextblob import SpacyTextBlob
import mysql.connector

def analyze(table):

### Make conneciton to DB
    try:
        conn = mysql.connector.connect(host='localhost', database = 'news', user = 'root', password = 'mysql')

        if conn.is_connected():
            db_info = conn.get_server_info()
            print("Connection made to DB, MySQL version:", db_info)
            cursor = conn.cursor()
            cursor.execute("SELECT database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)
            sqlQuery = "SELECT Body FROM " + table
            cursor.execute(sqlQuery)
            record = cursor.fetchall()

    except OSError as e:
        print("Error while Connecting: ", e)


    ###Initiate nlp PAckage
    nlp = spacy.load('en_core_web_sm')
    nlp.add_pipe('spacytextblob')

    ##Loop through every rowTitl
    for i in range(0, len(record)):
        print("Analyzing record ", str(i+1))
        ##Select body of text to analyze
        doc = nlp(record[i][0])

        #print polarity values
        print("Polarity of text is: ", doc._.blob.polarity)
        #Construct Update query to add polarity values to records using i + 1 for the index
        query = "UPDATE " + table + " SET Body_Polarity = " + str(doc._.blob.polarity) + " WHERE article_num = " + str(i+1)
        print(query)
        
        #Run query
        cursor.execute(query)

    #Commit Changes
    conn.commit()
    conn.close() #End of Method

## Main Method
## Main Method

print("Please list the names of all of the tables you would like to process")
x = []
y = ""
while y != "0":
    y = input('Table name: ')
    if y != "0":
        x.append(y)

for i in range(0, len(x)):
    print("Analyzing Table: " + x[i])
    analyze(x[i])