CREATE DATABASE IF NOT EXISTS movie_pipeline;
USE movie_pipeline;

CREATE TABLE IF NOT EXISTS movies (
    movie_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    genres VARCHAR(255),
    director VARCHAR(255),
    plot TEXT,
    box_office DECIMAL(15,2),
    release_year INT
);

CREATE TABLE IF NOT EXISTS ratings (
    rating_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    movie_id INT,
    rating FLOAT,
    timestamp DATETIME,
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id)
);

