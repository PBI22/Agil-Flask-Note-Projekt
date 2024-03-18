import markdown2
import json
import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from . import app
from .models import Note, Account
from .utils import *
from json import JSONEncoder
import sqlite3
import requests

@app.route('/noteJSON')
def display_data():
    # Connect to the SQLite database
    conn = sqlite3.connect('database/db.sqlite')
    cursor = conn.cursor()

    # Execute a query to fetch data from the database
    cursor.execute('''SELECT * FROM note''')

    rows = cursor.fetchall()



    # Convert the data to a list of dictionaries
    data_list = []
    for row in rows:
        # Assuming each row is represented as a dictionary with column names as keys
        created_datetime_iso = datetime.strptime(row[3], '%Y-%m-%d %H:%M:%S.%f').isoformat()
        lastedited_datetime_iso = datetime.strptime(row[4], '%Y-%m-%d %H:%M:%S.%f').isoformat()
        data_dict = {
            'noteID': row[0],
            'title': row[1],
            'text': row[2],
            'created': created_datetime_iso,
            'lastedited': lastedited_datetime_iso,
            'imagelink': row[5],
            'author': row[6],
        }
        #print(type(data_dict['created']))
        data_list.append(data_dict)

    # Close the database connection
    conn.close()

    # Convert the list of dictionaries to JSON
    json_data = json.dumps(data_list, indent=4)

    # Return JSON data
    return jsonify(data_list)

if __name__ == '__main__':
    app.run(debug=True)