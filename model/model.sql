USE notebook;

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
	field_type CHAR(3),
	book_id INT,
    FOREIGN KEY (book_id) REFERENCES book (id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE book_record (
    id INT PRIMARY KEY AUTO_INCREMENT,
	record_id INT,
    field_id INT,
	value_num DECIMAL(15, 2),
	value_txt TEXT,
    FOREIGN KEY (field_id) REFERENCES book_field (id) ON DELETE CASCADE ON UPDATE CASCADE
);

