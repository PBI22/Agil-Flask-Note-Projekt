# flask basics 
## what is flask
et framework for web applicationer
## jinja
template der kombinere dom og data kilder for at skabe dynamiske sider
### route()
er en decorator der fortæller appen hvilken url at bruge. 
    - @app.route(rule, options)
    - rule: url
    - parametere der bliver givet til rule.
    f.eks. @app.route('/hello')
        def hello_world():
            retuen 'hello world!'
    - med data 
        @app.route('/hello/)
### hoved elementer i flask web apps
    - static: data, css 
    - templates: html
    - app: instantiation
    - views: logik og referencer til url
    - webapp: kombinere app og views 
### run local
    - install flask 
    - use: flask --app app_name run
    - terminate: ctrl + æ
### azure
    - cloud in general
    - shared responsibility model
    - cloud models: public, private and hybrid
    - use cases for each model
    - consumption based mdel 
    - pricing models
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
		
		
		<a href="/users">see alle brugere</a> (Access: Admin)<br><br>
		<a href="/notes">see all notes</a> (Access: Admin, Teacher)<br><br>
		<a href="/edit notes">redigere notes</a> (Access: Admin, Teacher, Staff)<br><br>
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




