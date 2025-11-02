USE movie_pipeline;

-- Find the highest rated movie
SELECT 
    m.title, 
    AVG(r.rating) AS avg_rating
FROM movies m
JOIN ratings r ON m.movie_id = r.movie_id
GROUP BY m.title
ORDER BY avg_rating DESC
LIMIT 1;

-- Get top 5 genres by average rating
-- This splits the pipe-separated genres and calculates avg rating for each
SELECT 
    SUBSTRING_INDEX(SUBSTRING_INDEX(m.genres, '|', n.n), '|', -1) AS genre,
    AVG(r.rating) AS avg_rating
FROM movies m
JOIN ratings r ON m.movie_id = r.movie_id
JOIN (
    -- Generate numbers 1-100 to split genres
    SELECT a.N + b.N * 10 AS n
    FROM (
        SELECT 0 AS N UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 
        UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL 
        SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9
    ) a,
    (
        SELECT 0 AS N UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 
        UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL 
        SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9
    ) b
) n ON n.n <= 1 + LENGTH(m.genres) - LENGTH(REPLACE(m.genres, '|', ''))
GROUP BY genre
ORDER BY avg_rating DESC
LIMIT 5;

-- Find the most prolific director
SELECT 
    director, 
    COUNT(*) AS total_movies
FROM movies
WHERE director IS NOT NULL
GROUP BY director
ORDER BY total_movies DESC
LIMIT 1;

-- Average rating trend over the years
SELECT 
    m.release_year, 
    AVG(r.rating) AS avg_rating
FROM movies m
JOIN ratings r ON m.movie_id = r.movie_id
GROUP BY m.release_year
ORDER BY m.release_year;
