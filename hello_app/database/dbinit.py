"""
This module provides functionality to reset the database to its initial state by executing a predefined SQL script.

Functions:
- reset_db: Resets the database by reading and executing the SQL commands from 'database/init_script.sql'.
"""

import sqlite3


# Åbn forbindelse til databasen
def reset_db():
    """
    Resets the database by executing the SQL script located in 'database/init_script.sql'.

    Parameters:
    None

    Returns:
    None

    Raises:
    None
    """
    conn = sqlite3.connect("database/db.sqlite")
    cursor = conn.cursor()

    # Læs SQL-script fra en fil
    with open("database/init_script.sql", "r", encoding="utf-8") as f:
        sql_script = f.read()

    # Kør SQL-scriptet
    cursor.executescript(sql_script)

    # Commit ændringer og luk forbindelsen
    conn.commit()
    conn.close()


reset_db()
