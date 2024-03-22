  <div align="center">
  
  --- 
  
  <h1>Agil Note Project - PBI22</h1>
  
  <p>
    Agile development project build on https://learn.microsoft.com/en-us/azure/developer/python/python-web-app-github-actions-app-service?tabs=azure-cli
    <br><br>
    Afterwards modified by PBI22.
  </p>

  <h4>
    <a href="#om-projektet">Introduction</a>
  <span> · </span>
    <a href="#resultat">The Product</a>
  <span> · </span>
      <a href="#installation">Installation</a>
  </h4>

  </div>

<!-- OM PROJEKTET -->
## 🗒️ Introduction of the Project
<div id="om-projektet">
The idea behind the project was to take an existing webapp and modify it to class requirements.
<br><br>
At the same time teaching the group how to work as a software development team using an Agile Development Process.
<br><br>

</div>
---

<!-- OM PRODUKTET -->
## 🎯 The Product
<div id="resultat">
The NoteApp is meant to be used as a shared space for PBI22, to be used as a place to exchange informations relating to classes.
<br><br>
It is build using the Flask framework (https://palletsprojects.com/p/flask/) with Python and Jinja2 and using SQLalchemy for manipulating a SQLite database.
<br><br>
Useraccounts are stored locally in the database and a basic version of OAuth is also implemented using GitHub OAuth.
<br><br>
---



<!-- Getting Started -->
## 	:toolbox: Installation

<div id="installation">

Cloning the project to your workstation:

```
  git clone https://github.com/PBI22/Agil-Flask-Note-Projekt.git
```


To run the application
```Open your favourite ZSH terminal app
 cd hello_app
 pip install -r requirements.txt
 flask --app webapp run
```
You should now be able to access the application homepage in your browser at http://localhost:5000
 

</div>
