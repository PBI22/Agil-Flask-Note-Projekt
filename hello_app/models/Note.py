
""""
I want to make a model for my note taking app, first im making the model "Note", which has the following fields:
- id INT
- title VARCHAR(255)
- text TEXT
- created DATETIME
- LastEdited DATETIME 
- imagelink VARCHAR(255)
- account_ID INT (FK)
"""

class Note:
    def __init__(self, id, title, text, created, lastEdited, imagelink, account_ID):
        self.id = id
        self.title = title
        self.text = text
        self.created = created
        self.lastEdited = lastEdited
        self.imagelink = imagelink
        self.account_ID = account_ID
