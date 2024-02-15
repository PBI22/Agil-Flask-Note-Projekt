from datetime import datetime
from flask import Flask, render_template, json
from . import app

# Opening JSON file
f = open('note.json')
 
# returns JSON object as 
# a dictionary
notes = json.load(f)
 
# Iterating through the json
# list
for i in notes:
    print(i)

@app.route("/")
def home():
    return render_template("home.html", len = len(notes), notes = notes)

@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/create/")
def create():
    return render_template("createnote.html")

@app.route("/contact/")
def contact():
    return render_template("contact.html")

@app.route("/hello/")
@app.route("/hello/<name>")
def hello_there(name = None):
    return render_template(
        "hello_there.html",
        name=name,
        date=datetime.now()
    )

@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")
