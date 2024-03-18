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





# Vores landing Page - Der viser listen over noter
@app.route("/")
def home():
    return render_template("home.html", notes = updateList(), datetime = datetime.now())

# Create note
#Login required (what if you're already logged in)
@app.route("/create/", methods=["GET","POST"])
def create_note():

    if request.method == "GET":
        return render_template("createnote.html")

    # Hvis ikke GET, så er det POST, og så kører vi denne logik
    else:
        create_note_post(request)

    return redirect(url_for('home'))

#Login required (what if you're already logged in =session)
@app.route("/edit/<id>", methods=["GET","POST"])
def edit(id = None):

    note = find_note(id)

    if note is None:
        flash('Note not found', 'error')
        return redirect(url_for('home'))
    
    if request.method == "GET":
        return render_template("editnote.html", note=note)
    
    elif request.method == "POST":
        edit_note_post(request, id)

    else:
        flash("Invalid request method")
        
    return redirect(url_for('home'))

@app.route("/view/<id>")
def view(id = None):
    
    note = find_note(id)

    #Tjekker hvis det er et markdown note (som markeres med !MD i starten af teksten)
    if note.text.startswith("!MD"):
        note_markdown = markdown2.markdown(note.text.replace("!MD", ""), extras=["tables","fenced-code-blocks","code-friendly","mermaid","task_list","admonitions"])
        return render_template("mdnote.html", note=note, note_markdown=note_markdown)
    else:
        return render_template("mdnote.html", note=note, note_markdown=note.text)


@app.route("/delete/<id>")
def delete_note(id = None):
    
    if id is None:
        flash('Id is invalid', 'error')
        return redirect(url_for('home'))
    else:
        note = find_note(id)
        if note is None:
            flash('Note not found', 'error')
            return redirect(url_for('home'))
        else:
            
            dbsession.delete(note)
            dbsession.commit()
            flash('Note deleted successfully!', 'success')


    return redirect(url_for('home'))

@app.route("/search")
def search_results():
    query = request.args.get('query')

    if not query or query == "":
        return redirect(url_for('home'))

    # Søg efter noter, der matcher søgeordet
    search_results = searchbar(query)
    return render_template('search_results.html', results=search_results, query=query)

@app.route("/signup/", methods=["GET","POST"])
def create_account():
    if request.method == "POST":
        # Create account post logik
  
        if not request.form['username']:
            flash('Username is required', 'error')
            return redirect(url_for('create_account'))
        if not request.form['password']:
            flash('Password is required', 'error')
            return redirect(url_for('create_account'))
        if not request.form['email']:
            flash('Email is required', 'error')
            return redirect(url_for('create_account'))
        
        # Check if username already exists
        if dbsession.query(Account).filter_by(username=request.form['username']).first() is not None:
            flash('Username already exists', 'error')
            return redirect(url_for('create_account'))
        
        try:
            dbsession.add(Account(username = request.form['username'], password = request.form['password'], email = request.form['email']))
            dbsession.commit()
            flash('Account created successfully!', 'success')
            
        except:
            flash('Error creating account', 'error')
            return redirect(url_for('create_account'))
        return redirect(url_for('home'))
        
    else:
        return render_template("signup.html")

#login route
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":

        username = request.form.get('username')
        password = request.form.get('password')

        # Query the database for the account with provided username and password
        account = dbsession.query(Account).filter_by(username=username, password=password).first()

         
        if account:   

            session['user'] = account.username

            flash(f'Login successful for {account.username}', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password', 'error')
            return redirect(url_for('login'))

    # If request method is GET, render the login template
    return render_template('login.html')
@app.route('/logout')
def logout():
    user_logout = session['user']
    session.pop('user', None) 
    flash(f'You have been logged out, {user_logout}', 'success')
    return redirect(url_for('home'))
