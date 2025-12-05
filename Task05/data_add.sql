INSERT INTO users (first_name, last_name, email, gender, register_date, occupation_id)
VALUES
('Иван', 'Казейкин', 'kazeikin@gmail.com', 'male', date('now'), (SELECT id FROM occupations WHERE name = 'student')),
('Максим', 'Иванов', 'ivanov@gmail.com', 'male', date('now'), (SELECT id FROM occupations WHERE name = 'student')),
('Артём', 'Ивенин', 'ivenin@gmail.com', 'male', date('now'), (SELECT id FROM occupations WHERE name = 'student')),
('Александр', 'Колыганов', 'koliganov@gmail.com', 'male', date('now'), (SELECT id FROM occupations WHERE name = 'student')),
('Артём', 'Кочнев', 'kochnev@gmail.com', 'female', date('now'), (SELECT id FROM occupations WHERE name = 'student'));


INSERT INTO movies (title, year)
VALUES ('Дюна: Часть вторая', 2024);

INSERT INTO movies (title, year)
VALUES ('Оппенгеймер', 2023);

INSERT INTO movies (title, year)
VALUES ('Барби', 2023);


INSERT OR IGNORE INTO genres (name) VALUES ('Sci-Fi'), ('Drama'), ('Comedy');


INSERT INTO movie_genres (movie_id, genre_id)
SELECT m.id, g.id 
FROM movies m, genres g 
WHERE m.title = 'Дюна: Часть вторая' AND g.name = 'Sci-Fi';

INSERT INTO movie_genres (movie_id, genre_id)
SELECT m.id, g.id 
FROM movies m, genres g 
WHERE m.title = 'Оппенгеймер' AND g.name = 'Drama';

INSERT INTO movie_genres (movie_id, genre_id)
SELECT m.id, g.id 
FROM movies m, genres g 
WHERE m.title = 'Барби' AND g.name = 'Comedy';


INSERT INTO ratings (user_id, movie_id, rating, timestamp)
SELECT 
    (SELECT id FROM users WHERE email = 'kazeikin@gmail.com'),
    (SELECT id FROM movies WHERE title = 'Дюна: Часть вторая'),
    5.0,
    strftime('%s', 'now');

INSERT INTO ratings (user_id, movie_id, rating, timestamp)
SELECT 
    (SELECT id FROM users WHERE email = 'kazeikin@gmail.com'),
    (SELECT id FROM movies WHERE title = 'Оппенгеймер'),
    4.7,
    strftime('%s', 'now');

INSERT INTO ratings (user_id, movie_id, rating, timestamp)
SELECT 
    (SELECT id FROM users WHERE email = 'kazeikin@gmail.com'),
    (SELECT id FROM movies WHERE title = 'Барби'),
    4.0,
    strftime('%s', 'now');