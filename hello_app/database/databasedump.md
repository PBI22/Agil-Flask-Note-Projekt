# SQL statements for init af databasen
```
PRAGMA foreign_keys=OFF;

BEGIN TRANSACTION;

CREATE TABLE role (
roleID int primary key not null,
rolename varchar(255) not null);

CREATE TABLE accountrole (
id int primary key not null,
accountID int not null,
roleID int not null,
foreign key(accountID) references account(accountID),
foreign key(roleID) references role(roleID));

CREATE TABLE note (
noteID integer primary key autoincrement not null,
title varchar(255) not null,
text text not null,
created datetime not null,
lastedited datetime,
imagelink varchar(255),
author int not null,
foreign key(author) references account(accountID)
);

CREATE TABLE account (
        accountID INTEGER PRIMARY KEY AUTOINCREMENT,
        username varchar NOT NULL,
        password varchar NOT NULL,
        email varchar NOT NULL
);
COMMIT;
```