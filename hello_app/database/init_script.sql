PRAGMA foreign_keys=OFF;

BEGIN TRANSACTION;

DROP TABLE role;
Drop table note;
drop table account;

CREATE TABLE role (
roleID int primary key not null,
rolename varchar(255) not null);
insert into role (roleID, rolename)
values (1, "User"), (2, "Admin");

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
values ("admin", "pbkdf2:sha256:600000$1beh7uKXcX5l47Gm$4b89fe13ee30c2d813a91fc6153e3b0c3f2237750af652015916293da4b4283d", "admin@root", 2);
COMMIT;