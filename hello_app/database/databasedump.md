# SQL statements for init af databasen
```
PRAGMA foreign_keys=OFF;

BEGIN TRANSACTION;

DROP TABLE role;
Drop table note;
drop table account;
drop table accountrole;

CREATE TABLE role (
roleID int primary key not null,
rolename varchar(255) not null);
insesert into role
values (1, "User")
values (2, "Admin");

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
        email varchar NOT NULL,
        roleID int NOT NULL,
        foreign key(roleID) references role(roleID)
);
INSERT into account (username, password, email, roleID)
values ("admin", "admin", "admin@root", 2)
COMMIT;
```