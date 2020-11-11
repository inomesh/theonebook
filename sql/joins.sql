CREATE TABLE readers (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    Book_id INTEGER REFERENCES Books
);

INSERT INTO readers (name, Book_id) VALUES ('Alice', 1);
INSERT INTO readers (name, Book_id) VALUES ('Bob', 1);
INSERT INTO readers (name, Book_id) VALUES ('Charlie', 2);
INSERT INTO readers (name, Book_id) VALUES ('Dave', 3);
INSERT INTO readers (name, Book_id) VALUES ('Erin', 4);
INSERT INTO readers (name, Book_id) VALUES ('Frank', 6);
INSERT INTO readers (name, Book_id) VALUES ('Grace', 6);


SELECT title, author, name FROM Books INNER JOIN readers ON readers.Book_id = Books.id;
SELECT title, author, first_name, last_name FROM Books JOIN readers ON readers.Book_id = Books.id;
SELECT title, author, name FROM Books LEFT OUTER JOIN readers ON readers.Book_id = Books.id;
SELECT title, author, name FROM Books RIGHT OUTER JOIN readers ON readers.Book_id = Books.id;
