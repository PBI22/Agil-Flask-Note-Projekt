# Test program for sqlite
import sqlite3
from sqlalchemy import create_engine


# Laver forbindelse til database
# Husk PATH
connection = sqlite3.connect('artefakter/db/sqlitetest.sqlite')


# .execute() -- Bruges til almindelige sql statements
curser = connection.execute("select * from role")

# curser har en returneret liste fra select statement. Det er nu en "Cursor"
for row in curser:
    print("ID = ", row[0])
    print("name = ", row[1])

# Lukker forbindelsen
connection.close()


# Test program for sqlite
import sqlite3
import os

connection = '/Artefakter/DB/sqlitetest.sqlite'

def get_database_path():
    # Få den aktuelle filplacering for denne Python-fil
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Konstruér den fulde sti til databasen
    database_path = os.path.join(current_dir, '..', 'artefakter', 'db', 'sqlitetest.sqlite')

    return database_path

def insert_image(image_path, image_number):
    # Åbn forbindelse til databasen
    conn = sqlite3.connect(get_database_path())
    cursor = conn.cursor()

    # Åbn billedfilen og læs binær data
    with open(image_path, 'rb') as image_file:
        image_data = image_file.read()
    cursor.execute("CREATE TABLE IF NOT EXISTS image(id int primary key, image blob);")
    conn.commit()
    
    # Indsæt data i databasen
    cursor.execute("INSERT INTO Images (id, image) VALUES (?, ?)", (image_number, image_data))

    # Gem ændringer og luk forbindelsen
    conn.commit()
    conn.close()


