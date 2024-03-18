# Domænemodel over noteprojektet

```mermaid
---

---
classDiagram

Note : titel
Note : text
Note : author

Role : rolename

Account : username
Account : password
Account : email

Role --|> Account
Account --|> Note

```