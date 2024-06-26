  <div align="center">
  
  --- 
  
  <h1>Agil Note Project - PBI22</h1>



  <p>
    Agile development project build on:

    https://learn.microsoft.com/en-us/azure/developer/python/python-web-app-github-actions-app-service?tabs=azure-cli

    Afterwards modified by PBI22.
  </p>

[![BuildTest](https://github.com/PBI22/Agil-Flask-Note-Projekt/actions/workflows/build-and-test.yml/badge.svg)](https://github.com/PBI22/Agil-Flask-Note-Projekt/actions/workflows/build-and-test.yml)

  [![SonarCloud](https://sonarcloud.io/images/project_badges/sonarcloud-white.svg)](https://sonarcloud.io/summary/new_code?id=PBI22_Agil-Flask-Note-Projekt)

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=PBI22_Agil-Flask-Note-Projekt&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=PBI22_Agil-Flask-Note-Projekt) [![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=PBI22_Agil-Flask-Note-Projekt&metric=ncloc)](https://sonarcloud.io/summary/new_code?id=PBI22_Agil-Flask-Note-Projekt) [![Coverage](https://sonarcloud.io/api/project_badges/measure?project=PBI22_Agil-Flask-Note-Projekt&metric=coverage)](https://sonarcloud.io/summary/new_code?id=PBI22_Agil-Flask-Note-Projekt)  [![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/pylint-dev/pylint) 

[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=PBI22_Agil-Flask-Note-Projekt&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=PBI22_Agil-Flask-Note-Projekt)
 [![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=PBI22_Agil-Flask-Note-Projekt&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=PBI22_Agil-Flask-Note-Projekt) [![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=PBI22_Agil-Flask-Note-Projekt&metric=reliability_rating)](https://sonarcloud.io/summary/new_code?id=PBI22_Agil-Flask-Note-Projekt) [![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=PBI22_Agil-Flask-Note-Projekt&metric=vulnerabilities)](https://sonarcloud.io/summary/new_code?id=PBI22_Agil-Flask-Note-Projekt) 

[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=PBI22_Agil-Flask-Note-Projekt&metric=bugs)](https://sonarcloud.io/summary/new_code?id=PBI22_Agil-Flask-Note-Projekt) [![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=PBI22_Agil-Flask-Note-Projekt&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=PBI22_Agil-Flask-Note-Projekt)  [![Duplicated Lines (%)](https://sonarcloud.io/api/project_badges/measure?project=PBI22_Agil-Flask-Note-Projekt&metric=duplicated_lines_density)](https://sonarcloud.io/summary/new_code?id=PBI22_Agil-Flask-Note-Projekt) [![Technical Debt](https://sonarcloud.io/api/project_badges/measure?project=PBI22_Agil-Flask-Note-Projekt&metric=sqale_index)](https://sonarcloud.io/summary/new_code?id=PBI22_Agil-Flask-Note-Projekt)

---

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

```sh
git clone https://github.com/PBI22/Agil-Flask-Note-Projekt.git
```

Create and activate virtual environment
```sh
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

To run the application
```sh
cd hello_app
flask --app webapp run
```
You should now be able to access the application homepage in your browser at http://localhost:5000
 

</div>
