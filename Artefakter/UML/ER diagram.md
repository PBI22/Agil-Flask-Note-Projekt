# E/R Diagram over databasen
## Mangler rhombus der beskriver forholdet fordi mermaid mangler det (eller kunne måske ikke finde ud af det). Det samme gælder attributerne (ovalformen kunne ikke findes) Brugt også mindmap graphing. Beskrivelsen af forholdene følger.
- Role og Account: En role kan tilhøre 0 eller flere konti.
- Account og Note: En konto kan have 0 eller flere noter. 
- Den fysisk data modelen viser det tyde
```mermaid
mindmap
  [Account]
    ((accountID))
    ((username))
    ((password))
    ((email))
    ((roleID))
    
    [Role]
      ((roleID))
      ((rolename))
    
    [Note]
        ((noteID))
        ((title))
        ((text))
        ((created))
        ((lastedited))
        ((imagelink))
        ((author))
```
## Mulighed 2 er en ER diagram uden attributer. Attributerne kan ses i den fysiske model samt deres egenskaber. 
```mermaid
erDiagram
  ACCOUNT {
  }
  NOTE {}
  ROLE {}

  
  ACCOUNT ||--o{ NOTE : kan_have
  ROLE ||--o{ ACCOUNT : kan_tilhoer
```

# Physical data model

```mermaid
erDiagram
    ACCOUNT ||--o{ NOTE : creates
    ROLE ||--o{ ACCOUNT : is
    NOTE {
        INT noteID(PK)
        VARCHAR(255) title
        TEXT text
        DATETIME created
        DATETIME lastedited
        VARCHAR(255) imagelink
        INT author(FK)
    }
    ACCOUNT {
        INT accountID(PK)
        VARCHAR(255) username
        VARCHAR(255) password
        VARCHAR(255) email
        INT role
    }
    ROLE {
        INT roleID(PK)
        VARCHAR(255) rolename
    }
```