## cURL
cURL kan bruges i cmd til at lave en request til en API som hermed vil lave en GET eller POST request.
De vil blive dokumenteret her for at kunne fremhæve test af API og at det virker.
cURL bruge som en løsning til test af implementation af API. Der kan være muligheder for at indføre en anden løsning som muligvis Swagger.

## Adgangskrav
Alle har adgang til /view og /view/<id>
Man skal bruge en JWT Token for at få adgang til resten af endpoints
Alle endpoints som har @jwt_required skal bruge en valid token
Man skal sende en query til /api/login med et username og password
Ved godkendt login, så får man en JWT Token som vare 2 timer

JWT Token skal hermed gives i queries for at godkende at det er en bruger der sender gennem API'en
Der kan testes om ens token virker i /api/unprotected og /api/protected

## cURL request til create
Requesten laver en ny note som giver en titel, text og image link.
created og lastedited bruger lokalt datetime.now() og er dermed ikke eftersøgt
Ved at bruge JWT Token, så ved den hvilken author der er tilknyttet kontoen. Dette betyder at author automatisk vil blive tilføjet ved create
```
curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer <JWT Token>" -d "{\"title\":\"Title posted through API\",\"text\":\"Text posted through API\",\"imagelink\":\"Image posted through API\" }" http://localhost:5000/api/create
```
{
  "Author": 3,
  "Imagelink": "Image posted through API",
  "Text": "Text posted through API",
  "Titel": "Title posted through API",
  "message": "Note created successfully",
  "noteID": 6
}
```

## cURL request til edit
Requesten tager noten med id givet i URL parameter. Hermed vil man kunne indsætte title, text og imagelink. Hvis noget ikke bliver indsat, så ændre den det ikke. Så hvis text er tom, men title og imagelink har noget skrevet, så vil title og imagelink ændres og text forblive det samme. Lastedited vil også automatisk blive ændret til det nye tidspunkt. Eksempel på en edit kan ses under med cURL som ændre title, text og imagelink ved id 12.
```
curl -X PUT -H "Content-Type: application/json" -H "Authorization: Bearer <JWT Token>" -d "{\"title\": \"Updated Title\", \"text\": \"Updated Text\", \"imagelink\": \"Updated Image Link\"}" http://localhost:5000/api/edit/<id>
```
### Resultat
```
{
  "Imagelink": "Updated Image Link",
  "Message": "Note edited successfully",
  "Text": "Updated Text",
  "Titel": "Updated Title"
}
```
## cURL til delete
Der bliver sendt en delete query som vil slette noten tilhørende det givne id eksempelvis 4.
Der skal bruges en valid token for at skabe sikkerhed.
```
curl -X DELETE -H "Authorization: Bearer <JWT Token>" http://localhost:5000/api/delete/<id>
```

## cURL request til login
Ved at bruge denne cURL, så vil man kunne bruge sit username og password fra databasen. Grundet sikkerhed, så viser jeg ikke et aktuelt username og password, så find en selv. Resultatet vil være at man modtager en JWT som er en string man skal bruge til at lave requests igennem API'en.

```
curl -X POST -H "Content-Type: application/json" -d "{\"username\":\"**my_username**\", \"password\":\"**my_password**\"}" http://localhost:5000/api/login
```
### Resultat
```
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxMTAxNDIwMSwianRpIjoiYTcxMGUwYjAtMDdhMi00MDg0LTk3ZDktNDAxZmQyMjM4MWMzIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6Ik1hcnRpbiIsIm5iZiI6MTcxMTAxNDIwMSwiY3NyZiI6IjM3ZDk0NDNiLTU1ODEtNDE5Mi05ODc5LWMwZjQyMDgxZjkwMyIsImV4cCI6MTcxMTAxNTEwMX0.nC7CjL7JMweXikSRz8Jni5BcmPytZBn-CUuMZ5DG2wU"
}
```

## cURL til test af token - protected endpoint
curl -X GET -H "Authorization: Bearer <JWT Token>" http://localhost:5000/api/protected

### Resultat
```
{
  "message": "Hello, Martin! You can only use this with a valid token"
}
```