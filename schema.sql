-- Create the database
CREATE DATABASE IF NOT EXISTS movie_pipeline;
USE movie_pipeline;

-- Movies table - stores basic movie info and OMDB data
CREATE TABLE IF NOT EXISTS movies (
    movie_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    genres VARCHAR(255),           -- pipe-separated list like "Action|Drama"
    director VARCHAR(255),          -- from OMDB API
    plot TEXT,                      -- movie plot summary from OMDB
    box_office DECIMAL(15,2),       -- box office earnings in dollars
    release_year INT
);

-- Ratings table - user ratings for movies
CREATE TABLE IF NOT EXISTS ratings (
    rating_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    movie_id INT,
    rating FLOAT,                   -- rating score (usually 0-5)
    timestamp DATETIME,             -- when the rating was given
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id)
);
