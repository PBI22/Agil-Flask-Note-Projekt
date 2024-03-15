# Users and roles 

## Vores vision indtilvidere
	i. Antal tabeller = 3
		- en til brugere
		- en til roler
		- en til noter
	ii. Typer af roler
		- student 
		- teacher
	iii. Rettigheder som student:
		- create
		- read egen note
		- delete egen note
		- update egen note 
	iv: Rettigheder som teacher:
		- create
		- read alle noter
		- delete enhver note
		- update enhver note

## Praksis
1. Levels: 
	- data: data man kan få adang til 
		i. kræver tæt sammearbejde med data modellering delen af projektet. 
	- pages: funktionalitet/ sider man kan få adgang til. 
2. SetUp: 
	- note table
	- user table
	- role table 
	- association mellem user og role tabeller
	- association mellem user og note
3. Forudsætninger: 
	i. Bibliteker
		a. slqAlchemy: database funktionalitet
		b. flask security: 
			- bruger info: Usermixin 
			- roleMixin: role info
			- match med user_id og role_id som fk. 
		c. flask: 
			- bruge session til at holde user og role 
	ii. Adgang bestemt af dine roller. 
		- De næste 3 linjer viser hvem der adgang til bestemte sidere og deres funktionalitet. 
		
		<a href="/users">see alle brugere</a> (Access: Admin)<br><br>
		<a href="/notes">see all notes</a> (Access: Admin, Teacher)<br><br>
		<a href="/edit notes">redigere notes</a> (Access: Admin, Teacher, Student)<br><br>
		
	iii. Bruge af roller til at verificere
		
		{% if current_user.is_authenticated %}
			<b>Current user</b>: {{current_user.email}}
			<!-- Current users roles --> 
			| <b>Role</b>: {% for role in current_user.roles%}
                    {{role.name}}
           {% endfor %} <br><br>
	
			<a href="/logout">Logout</a>
		
		{% else %}
			<a href="/signup">Sign up</a> | <a href="/signin">Sign in</a>
		{% endif %}
			<br><br>

## UserRole ER diagram 
![userRole Img](img/UserRole.PNG)

