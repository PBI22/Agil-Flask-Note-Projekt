# Cross site scripting(XSS)

Web sikkerhed sårbarhed
Ondsindet kode sendt til uvidende brugere
Udnytter mangel på validation og encoding af input (sanitization)

Fungerer således:
Uden validering af input, så har en DOM ingen ide om at input er kode eller tekst. Hermed kan man eksempelvis skrive <script>alert(‘me are steal you data…’)</script> og få siden til at tro at det er et godkendt input. Siden vil hermed indsætte det som kode, hvilket eksempelvis vil betyde at på et forum, så vil alle der ser opslaget blive ramt. 

## Typer af XSS

### Reflected XSS (AKA Non-Persistent or Type I)
Data bliver ikke gemt fx i en database, men kan medføre skader på hjemmesiden ved fx. at implementere eksternt kode i en fejlbesked. Hermed kan angreb som eksempelvis stjæler session cookies, omlede brugeren til phishing side eller “defacing” af hjemmeside.

### Stored XSS (AKA Persistent or Type II)
Data her bliver gemt eksempelvis i en database, hvor serveren kan fremvise dem i et forum, kommentarfelt osv. Hackeren kan hermed stjæle brugerens data og oplysninger, som bliver sent på siden og hermed optage information som kan være sensitivt. 

### DOM Based XSS (AKA Type-0)
Også kaldt “Type-0 XSS” hvor der angribes ved at modificere DOM’en i brugerens browser. Selve siden i sig selv (HTTP responsen) ændres ikke, men selve brugerens side udføres anderledes grundet ondsindede modifikationer som er sket i DOM’en.

### Server XSS
Server XSS sker når upålidelige brugerdata inkluderes i en HTTP respons, som genereres af serveren. Selve kilden for denne data kan komme fra requesten eller en anden gemt lokation. Det kan både være reflected server XSS og stored server XSS. I denne situation ligger sårbarheden i server-side kode, og browseren kan derfor bare kører hvilket som helst script, som er indlejret i den kode.

### Client XSS
Client XSS sker når uønsket bruger forsynet data bliver brugt til at opdatere DOM’en med et usikkert JavaScript kald. Usikkerheden opstår når man kan indsende skadeligt JS kode som ses at være valid for klienten. 
Dataen kan være fra DOM eller sent fra serveren med AJAX eller et page load. Dataen kan komme fra enten et gemt sted på klienten eller på serveren. Der kan være problemer med både Reflected Client XSS og Stored Client XSS.


## Løsning til XSS

### Forsvar mod Server XSS
Server XSS sker når der inkluderes uønsket data i HTML.

### Løsning vil være at kigge på “Context-sensitive server side output encoding”.
Dette betyder at man vil kigge på indholdet af inputs ift. konteksten og redigere brugerinput herfra. Det vil eksempelvis være vigtigt at fjerne <script> tags fra brugerinput eftersom det vil betyde at brugeren ikke kan indsende ondsindet scripts på siden. 
Man kan i serverdelen konvertere potentielle farlige tegn såsom <, >, “ og ‘ til deres html-version, hvilket vil gøre at siden prøver at vise det samme som før, men uden risikoen for at kode bliver sendt ind på hjemmesiden.

### Forsvar mod client XSS
Client XSS sker, når usikker data bruges til at opdatere DOM’en med et usikkert JS call. Det bedste forsvar mod det er, at man skal bruge sikre Javascript API’er.

### SQL Injection
Et angreb med SQL injection er en indsættelse af en SQL query via inputtet fra brugeren til applikationen. SQL kommandoer indføres i et brugerinput, for at kunne ændre på selve udførelselsen af prædefineret SQL commands.
Indsættelse af SQL query via input fra bruger
Ændre udførelse af prædefineret SQL command

### En succesfuld SQL injection kan ting som:
Læse sensitiv brugerdata
Modificere database data
Udføre adminstrations operationer(lukke database management system)
Hermed skade forretningers økonomi og rygte

### Mulige svagheder mod SQL
Boolean conditions
Single quote ‘
Query baseret på data fra URL
OAST payloads designed til at udføre out-of-band netværksinteraktioner


### Eksempel på single quote “exploitation”
Single quote stopper string fra URL tidligt og tilføjer OR+1=1-- til query, hvilket eksempelvis kan bypass det restriktioner sat af udvikleren.
URL
https://example.com/products?category=books'+OR+1=1--
Query
SELECT * FROM products WHERE category = 'books' OR 1=1--'

Et værre eksempel kunne være at logge ind på en konto med brugernavnet og password, hvor man siger OR 1=1, hvilket vil bypass password restriktionen.