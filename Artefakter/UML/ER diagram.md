# E/R Diagram over databasen
## Mangler rhombus der beskriver forholdet fordi mermaid mangler det (eller kunne måske ikke finde ud af det). Det samme gælder attributerne (ovalformen kunne ikke findes) Brugt også mindmap graphing. Beskrivelsen af forholdene følger.
- Role og Account: En role kan tilhøre 0 eller flere konti men en konto behøver ikke nogen role. 
- Account og Note: En konto kan have 0 eller flere noter. Men en note skal tilhøre en konto.  
- Den fysisk data modelen viser det tydeligt. 
```mermaid
mindmap
  [Account]
    ((accountID))
    ((username))
    ((password))
    ((email))
    ((rolename))
    
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
        INT noteID(PK_not_null)
        VARCHAR(255) title(not_null)
        TEXT text(not_null)
        DATETIME created(not_null)
        DATETIME lastedited
        VARCHAR(255) imagelink(not_null)
        INT author(FK_not_null)
    }
    ACCOUNT {
        INT accountID(PK_not_null)
        VARCHAR(255) username(not_null)
        VARCHAR(255) password(not_null)
        VARCHAR(255) email(not_null)
        INT roleID(FK)
    }
    ROLE {
        INT roleID(PK_not_null)
        VARCHAR(255) rolename(not_null)
    }

```