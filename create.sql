Drop table if exists OrderItems;
Drop table if exists Books ;
Drop table if exists Publishers ;
Drop table if exists Authors ;
Drop table if exists Orders ;
Drop table if exists Employees ;
Drop table if exists Customers ;

CREATE TABLE Customers(
customer_Id integer Primary key NOT NULL,
first_name varchar NOT NULL,
last_name varchar NOT NULL,
contact_no numeric(10),
email varchar,
address varchar
);

CREATE TABLE Employees(
employee_Id integer Primary key NOT NULL,
first_name varchar NOT NULL,
last_name varchar NOT NULL,
contact_no numeric(10),
roles varchar,
shifts varchar
);

CREATE TABLE Orders(
order_Id integer Primary key NOT NULL,
customer_Id integer NOT NULL,
employee_Id integer NOT NULL,
order_type varchar NOT NULL,
payment_method varchar NOT NULL,
order_date date,
status VARCHAR,
constraint fk_customers Foreign key(customer_Id) references Customers(customer_Id),
constraint fk_employee Foreign key(employee_Id) references Employees(employee_Id)
);

CREATE TABLE Authors(
Id integer Primary key NOT NULL,
name varchar,
website varchar
);

CREATE TABLE Publishers(
Id integer Primary key NOT NULL,
name varchar,
address varchar,
email varchar,
website varchar
);

CREATE TABLE Books(
book_Id numeric(13,0) Primary key NOT NULL,
author_Id integer NOT NULL,
publisher_Id integer NOT NULL,
title varchar NOT NULL,
genre varchar,
price numeric(10,2),
quantity_store integer,
constraint fk_authors Foreign key(author_Id) references Authors(Id),
constraint fk_publishers Foreign key(publisher_Id) references Publishers(Id)
);

CREATE TABLE OrderItems(
order_Id integer NOT NULL,
book_Id numeric(13,0) NOT NULL,
quantity_purchased integer,
primary key(book_Id,order_Id),
constraint fk_books Foreign key(book_Id) references Books(book_Id),
constraint fk_orders Foreign key(order_Id) references Orders(order_Id)
);

