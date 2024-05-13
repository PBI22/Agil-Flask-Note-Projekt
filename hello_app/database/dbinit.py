import sqlite3
# Åbn forbindelse til databasen
def reset_db():
    conn = sqlite3.connect('database/db.sqlite')
    cursor = conn.cursor()

    # Læs SQL-script fra en fil
    with open('database/init_script.sql', 'r') as f:
        sql_script = f.read()

    # Kør SQL-scriptet
    cursor.executescript(sql_script)

    # Commit ændringer og luk forbindelsen
    conn.commit()
    conn.close()

reset_db()
