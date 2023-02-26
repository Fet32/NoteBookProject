USE notebook;

CREATE TABLE field_type (
    id INT PRIMARY KEY,
    name VARCHAR(15) NOT NULL
);

INSERT INTO field_type(id, name) 
VALUES 
	(1, 'Date'),
	(2, 'Time'),
	(3, 'DateTime'),
	(4, 'Year'),
	(5, 'Int'),
	(6, 'Text'),
	(7, 'Phone'),
	(8, 'email');

CREATE TABLE table_type_link (
    id INT PRIMARY KEY AUTO_INCREMENT,
    table_name VARCHAR(30) NOT NULL,
	type_id INT,
    FOREIGN KEY (type_id) REFERENCES field_type (id) ON DELETE RESTRICT
);

INSERT INTO table_type_link(table_name, type_id) 
VALUES 
	('field_record_date', 		1),
	('field_record_time', 		2),
	('field_record_datetime', 	3),
	('field_record_year', 		4),
	('field_record_int', 		5),
	('field_record_text', 	6),
	('field_record_phone', 		7),
	('field_record_email', 		8);

CREATE TABLE user (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL
);

CREATE TABLE book (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
	user_id INT,
    FOREIGN KEY (user_id) REFERENCES user (id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE book_field (
    id INT PRIMARY KEY AUTO_INCREMENT,
    field_name VARCHAR(30) NOT NULL,
	book_id INT,
	type_id INT,
    FOREIGN KEY (book_id) REFERENCES book (id) ON DELETE CASCADE,
    FOREIGN KEY (type_id) REFERENCES field_type (id) ON DELETE RESTRICT
);

CREATE TABLE book_record (
    id INT PRIMARY KEY AUTO_INCREMENT,
	book_id INT,
    FOREIGN KEY (book_id) REFERENCES book (id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE field_record_date (
    id INT PRIMARY KEY AUTO_INCREMENT,
    value DATE NOT NULL,
	field_id INT,
	record_id INT,
    FOREIGN KEY (field_id) REFERENCES book_field (id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (record_id) REFERENCES book_record (id) ON DELETE CASCADE
);

CREATE TABLE field_record_time (
    id INT PRIMARY KEY AUTO_INCREMENT,
    value TIME NOT NULL,
	field_id INT,
	record_id INT,
    FOREIGN KEY (field_id) REFERENCES book_field (id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (record_id) REFERENCES book_record (id) ON DELETE CASCADE
);

CREATE TABLE field_record_datetime (
    id INT PRIMARY KEY AUTO_INCREMENT,
    value DATETIME NOT NULL,
	field_id INT,
	record_id INT,
    FOREIGN KEY (field_id) REFERENCES book_field (id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (record_id) REFERENCES book_record (id) ON DELETE CASCADE
);

CREATE TABLE field_record_year (
    id INT PRIMARY KEY AUTO_INCREMENT,
    value YEAR NOT NULL,
	field_id INT,
	record_id INT,
    FOREIGN KEY (field_id) REFERENCES book_field (id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (record_id) REFERENCES book_record (id) ON DELETE CASCADE
);

CREATE TABLE field_record_int (
    id INT PRIMARY KEY AUTO_INCREMENT,
    value INT NOT NULL,
	field_id INT,
	record_id INT,
    FOREIGN KEY (field_id) REFERENCES book_field (id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (record_id) REFERENCES book_record (id) ON DELETE CASCADE
);

CREATE TABLE field_record_text (
    id INT PRIMARY KEY AUTO_INCREMENT,
    value TEXT NOT NULL,
	field_id INT,
	record_id INT,
    FOREIGN KEY (field_id) REFERENCES book_field (id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (record_id) REFERENCES book_record (id) ON DELETE CASCADE
);

CREATE TABLE field_record_phone (
    id INT PRIMARY KEY AUTO_INCREMENT,
    value VARCHAR(12) NOT NULL CHECK (value REGEXP '(^\d|\+\d)((\d{10})|(\s\(\d{3}\)\s\d{3}\s\d{2}\s\d{2}))'), 
	field_id INT,
	record_id INT,
    FOREIGN KEY (field_id) REFERENCES book_field (id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (record_id) REFERENCES book_record (id) ON DELETE CASCADE
);

CREATE TABLE field_record_email (
    id INT PRIMARY KEY AUTO_INCREMENT,
    value VARCHAR(50) NOT NULL CHECK (value REGEXP '[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,63}$'),
	field_id INT,
	record_id INT,
    FOREIGN KEY (field_id) REFERENCES book_field (id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (record_id) REFERENCES book_record (id) ON DELETE CASCADE
);
