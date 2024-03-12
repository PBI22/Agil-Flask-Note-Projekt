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

# Direkte implementation (ChatGPT guide/punkter)
https://chat.openai.com/share/d07e32c1-77cd-4ab4-95a2-13900a93617c