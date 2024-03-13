# Users and roles 
1. Levels: 
	- data: data man kan få adang til 
		i. kræver tæt sammearbejde med data modellering delen af projektet. 
			- bruger tabel
			- 
	- pages: funktionalitet/ sider man kan få adgang til. 
2. SetUp: 
	- user table
	- role table 
	- association mellem user og role tabeller
3. Forudsætninger: 
	i. Bibliteker
		a. slqAlchemy: database funktionalitet
		b. flask security: 
			- bruger info: Usermixin 
			- roleMixin: role info
			- match med user_id og role_id som fk. 
		c. flask obviously. 
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