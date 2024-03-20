## cURL
cURL kan bruges i cmd til at lave en request til en API som hermed vil lave en GET eller POST request.
De vil blive dokumenteret her for at kunne fremhæve test af API og at det virker.
cURL bruge som en løsning til test af implementation af API. Der kan være muligheder for at indføre en anden løsning som muligvis postman eller swagger. Swagger kan eksempelvis implementeres med flasgger library.

## cURL request til create
Requesten laver en ny note som giver en titel, text og image link.
created og lastedited bruger lokalt datetime.now() og er dermed ikke eftersøgt
Author bliver givet id 1 (er ikke helt sikker på hvordan man vil tillade/verificere hvem authoren er når det er igennem API'en)
```
curl -X POST -H "Content-Type: application/json" -d "{\"title\":\"Title posted through API\",\"text\":\"Text posted through API\",\"imagelink\":\"Image posted through API\",\"author\": 1 }" http://localhost:5000/api/create
```

## cURL request til edit
Requesten tager noten med id givet i URL parameter. Hermed vil man kunne indsætte title, text og imagelink. Hvis noget ikke bliver indsat, så ændre den det ikke. Så hvis text er tom, men title og imagelink har noget skrevet, så vil title og imagelink ændres og text forblive det samme. Lastedited vil også automatisk blive ændret til det nye tidspunkt. Eksempel på en edit kan ses under med cURL som ændre title, text og imagelink ved id 12.
```
curl -X PUT -H "Content-Type: application/json" -d "{\"title\": \"Updated Title\", \"text\": \"Updated Text\", \"imagelink\": \"Updated Image Link\"}" http://localhost:5000/api/edit/12
```

## cURL til delete og view
Bruger ikke noget input andet end id i URL så cURL behøves ikke
Skal dog noteres at alle kan bruge delete medmindre JWT anvendes
