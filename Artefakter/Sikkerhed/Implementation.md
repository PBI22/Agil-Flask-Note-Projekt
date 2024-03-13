# Implementation af sikkerhed mod XSS og SQL Injection

Beskyttelse mod XSS i Flask(python), HTML og SQLite
Der kan bruges libraries såsom Bleach eller Flask-Bleach til at sanitize bruger genererede indhold og fjerne skadeligt HTML og JavaScript kode.
Der kan bruges Jinja2 fra flask som en templating engine, hvilket laver HTML escaped tegn, hvilket reducere chancen for XSS angreb
Man kan bruge Content Security Policy(CSP) til at reducere hvor indhold kan blive indlæst og kørt. Man kan bruge Flask-CSP extension til at opsætte dette.

Beskyttelse mod SQL Injection i Flask(Python) og SQLite med SQLAlchemy

Der vil bruges parameterized queries til at skabe et niveau af beskyttelse mod SQL Injections fordi det vil fjerne muligheden for at tilføje et nyt variabel til en query. Ved brug af dette sikrer man, at input behandles som data frem for eksekverbar kode.
Eksempelvis så vil man se at hvis man indsætter books’Or+1=1--, så vil det sende det ind som en parameter, hvilket så kan sanitizes med SQLAlchemy og hermed indsendes uden potentielle trusler for databasens indhold. 

# SQLAlchemy
SQLalchemy bruger ORM, hvilket automatisk fikser problemet med queries, som reducerer risiko for SQL injection
SQLAlchemy gør så man kan lave classes i python som tilsvare forskellige tabeller i en database. Ved implementering af ORM, så bliver det muligt at interagere med databasens struktur inde i python, hvilket vil simplificere og skabe mere forståelse for hvordan dataen bliver sendt ind i databasen fra python. Dette kan sammen med den indbyggede funktion gøre udviklingen af sikkerhed nemmere.
Samlet set med SQLAlchemy så er der nogle keywords at kende
Parameterized queries(prepared statement)
ORM
Input validation og sanitization

# **Parametarized queries** 
En parametiseret forespørgsel **adskiller** SQL-kode, fra den data, som indsættes i forespørgslen. Det betyder, at brugerens input behandles som værdier og ikke en del af en SQL forespørgsel, hvilket forhindre brugeren i at lave en SQL-injection. 

Eksempel på parametiseret forespørgsel
```sql
sql_query = "SELECT * FROM users WHERE username = %s AND password = %s"
```

Eksempel på en **IKKE** parametiseret forespørgsel

```sql
sql_query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
```

# Direkte implementation (ChatGPT guide/punkter)
```python
from flask import Flask, request, jsonify
import re

app = Flask(__name__)

def validate_input(user_input):
	# Validering for Cross-Site Scripting (XSS)
	# Fjern HTML-tags fra input for at forhindre XSS-angreb
	user_input = re.sub('<[^<]+?>', '', user_input)

	# Validering for SQL Injection
	# Undgå SQL-injektion ved at bruge parameteriserede forespørgsler eller escape tegn
	# Dette er et simpelt eksempel; i en rigtig applikation bør du bruge parametrerede forespørgsler eller ORM
	# I dette eksempel tillader vi kun almindelige bogstaver, tal og mellemrum i inputtet
	if not re.match("^[a-zA-Z0-9 ]+$", user_input):
    	return False
	return True

@app.route('/input', methods=['POST'])
def handle_input():
	user_input = request.form.get('user_input')

	# Validér inputtet
	if user_input is None or not validate_input(user_input):
    	return jsonify({'error': 'Ugyldigt input'}), 400

	# Hvis inputtet er gyldigt, fortsæt med at behandle det
	# Her kan du tilføje din logik til at håndtere det gyldige input
	return jsonify({'message': 'Input modtaget og valideret korrekt'})

if __name__ == '__main__':
	app.run(debug=True)
```
Eksempel fra PortSwigger 
Eksemplet handler om beskyttelse mod brugerinput med først at unicode escape og derefter HTML-encode det. Eksemplet tager stilling mod JavaScript og hermed Client side XSS angreb.

Javascript har ikke sin egen API til at encode HTML og hermed vil man selv nødt til at udvikle en løsning. Hermed vil følgende kode erstatte et string om til HTML entities som hermed vil reducere muligheden for at lave XSS angreb.
```js
function htmlEncode(str){
	return String(str).replace(/[^\w. ]/gi, function(c){
    	return '&#'+c.charCodeAt(0)+';';
	});
}
```

Herefter vil man køre dette script ved steder hvor brugeren kan indsætte data vha. Inputfelter.
<script>document.body.innerHTML = htmlEncode(untrustedValue)</script>

Hvis inputtet er i en JavaScript string, så vil man skulle bruge en encoder som laver Unicode escaping. Her er sample Unicode-encoder.
```js
function jsEscape(str){
	return String(str).replace(/[^\w. ]/gi, function(c){
    	return '\\u'+('0000'+c.charCodeAt(0).toString(16)).slice(-4);
	});
}
```

Hermed vil man bruge dette script til at sanitize inputtet med hjælp af sampled fra før.
<script>document.write('<script>x="'+jsEscape(untrustedValue)+'";<\/script>')</script>

Her kan man se hvordan man som hacker kan udnytte svagheder i kommunikation mellem SQL og andre programmeringssprog(her python). Man vil altså hermed bypass nødvendigheden for et password, hvilket hæmmer sikkerheden på siden. Eksemplet er fra SecureFlag.
```python
@app.route("/login")
def login():

username = request.values.get('username')
password = request.values.get('password')

# Prepare database connection
db = pymysql.connect("localhost")
cursor = db.cursor()

# Execute the vulnerable SQL query concatenating user-provided input.
cursor.execute("SELECT * FROM users WHERE username = '%s' AND password = '%s'" % (username, password))

# If the query returns any matching record, consider the current user logged in.
record = cursor.fetchone()

if record:
session['logged_user'] = username

# disconnect from server
db.close()

Parameterized query med SQLAlchemy
stmt = sqlalchemy.sql.text("SELECT * FROM users WHERE username = :username and password = :password")
conn.execute(stmt, {"username": username, "password": password })
```

### Kilder
https://portswigger.net/web-security/cross-site-scripting/preventing

https://knowledge-base.secureflag.com/vulnerabilities/sql_injection/sql_injection_python.html