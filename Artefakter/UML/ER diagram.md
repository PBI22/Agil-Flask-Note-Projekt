# E/R Diagram over databasen
## Mangler rhombus der beskriver forholdet fordi mermaid mangler det (eller kunne ikke finde ud af det). Brugt også mindmap graphing. 
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
# Physical data model
```mermaid
erDiagram
    ACCOUNT ||--o{ NOTE : creates
    ROLE ||--o{ ACCOUNT : is
    NOTE {
        INT noteID
        VARCHAR(255) title
        TEXT text
        DATETIME created
        DATETIME lastedited
        VARCHAR(255) imagelink
        INT author(FK)
    }
    ACCOUNT {
        INT accountID
        VARCHAR(255) username
        VARCHAR(255) password
        VARCHAR(255) email
        INT role
    }
    ROLE {
        INT roleID
        VARCHAR(255) rolename
    }
```