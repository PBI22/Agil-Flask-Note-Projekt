## Curl
Curl kan bruges i cmd til at lave en request til en API som hermed vil lave en GET eller POST request.
De vil blive dokumenteret her for at kunne fremhæve test af API og at det virker

# Curl request til create
requesten laver en ny note som giver en titel, text og image link.
created og lastedited bruger lokalt datetime.now() og er dermed ikke eftersøgt
Author bliver givet id 1 (er ikke helt sikker på hvordan man vil tillade/verificere hvem authoren er når det er igennem API'en)
```
curl -X POST -H "Content-Type: application/json" -d "{\"title\":\"Title posted through API\",\"text\":\"Text posted through API\",\"imagelink\":\"Image posted through API\"}" http://localhost:5000/api/create
```
