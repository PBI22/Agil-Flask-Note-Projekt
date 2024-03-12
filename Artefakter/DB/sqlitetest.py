# Test program for sqlite
import sqlite3

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