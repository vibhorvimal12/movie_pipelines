# 🎬 Movie Data Pipeline — Data Engineering Assignment (TS Works)

## 📖 Overview
This project implements a **Movie Data ETL (Extract, Transform, Load) pipeline** that integrates data from the **MovieLens dataset** and enriches it using the **OMDb API**.  
The goal is to create a structured **MySQL database** combining user ratings and enriched movie details such as director, box office, and plot.

The ETL process is written in **Python** using `pandas`, `SQLAlchemy`, and `requests`, and performs:
- Data extraction from local CSV files
- Data cleaning and transformation
- API enrichment via OMDb
- Loading into a MySQL database
- Analytical querying via SQL

---

## 🧱 Project Objectives
1. **Extract** movie and rating data from the MovieLens CSV files.  
2. **Transform** and clean the data to handle missing and inconsistent fields.  
3. **Enrich** the movie data using the OMDb API to fetch director, plot, and box office.  
4. **Load** the transformed data into MySQL tables.  
5. **Analyze** the dataset using SQL queries to answer business questions.

---

## 🗂️ Project Structure
Movie_Data_Pipeline_MySQL/
├── etl.py             # Main ETL pipeline script
├── schema.sql         # Database schema (CREATE TABLE statements)
├── queries.sql        # Analytical SQL queries
├── requirements.txt   # Python dependencies
├── data/
│   ├── movies.csv
│   ├── ratings.csv
│   └── links.csv
└── README.md          # Project documentation

---

## ⚙️ Environment Setup & Execution

### 1️⃣ Prerequisites
- Python 3.8+
- MySQL Server installed and running
- OMDb API key (get a free one from [http://www.omdbapi.com/](http://www.omdbapi.com/))

### 2️⃣ Setup Instructions
Clone the repository and install dependencies:
```bash
git clone <your_repo_link>
cd Movie_Data_Pipeline_MySQL
pip install -r requirements.txt

3️⃣ Configure MySQL Database
Create a new database:
CREATE DATABASE movie_db;

Update connection settings in etl.py:
DB_USER = "root"
DB_PASS = "your_password"
DB_HOST = "localhost"
DB_NAME = "movie_db"

4️⃣ Add OMDb API Key
Create a .env file in the root directory:
OMDB_API_KEY=your_api_key_here

5️⃣ Run the ETL Pipeline
Execute:
python etl.py

This will:


Extract and clean MovieLens data


Enrich it using OMDb API


Load it into your MySQL database


6️⃣ Run Analytical Queries
After the ETL process completes, open MySQL and execute:
SOURCE queries.sql;


🧩 Database Design
Tables Overview
TableDescriptionmoviesMovie information from MovieLens + OMDbratingsUser ratings of each moviegenres (optional)Normalized genre data (if expanded)
Example Schema (schema.sql)
CREATE TABLE movies (
  movie_id INT PRIMARY KEY,
  title VARCHAR(255),
  year INT,
  genres VARCHAR(255),
  director VARCHAR(255),
  plot TEXT,
  box_office VARCHAR(50)
);

CREATE TABLE ratings (
  user_id INT,
  movie_id INT,
  rating FLOAT,
  timestamp DATETIME,
  FOREIGN KEY (movie_id) REFERENCES movies(movie_id)
);


🔄 ETL Workflow
1. Extract


Read movies.csv and ratings.csv from MovieLens.


Optionally, use links.csv to fetch imdbId for OMDb queries.


2. Transform


Clean titles, parse genres (pipe-separated → comma-separated).


Extract release year from movie titles.


Convert timestamps to readable datetime format.


Handle missing or invalid entries.


3. Enrich


Query OMDb API for additional movie metadata.


Fetch Director, Plot, and BoxOffice.


Handle missing API results gracefully (NULL or default).


4. Load


Insert data into MySQL tables using SQLAlchemy.


Ensure idempotency — re-running the script won’t create duplicates.



📊 Analytical Queries (queries.sql)
-- 1️⃣ Highest average-rated movie
SELECT m.title, AVG(r.rating) AS avg_rating
FROM ratings r
JOIN movies m ON m.movie_id = r.movie_id
GROUP BY m.title
ORDER BY avg_rating DESC
LIMIT 1;

-- 2️⃣ Top 5 genres by average rating
SELECT m.genres, AVG(r.rating) AS avg_rating
FROM ratings r
JOIN movies m ON m.movie_id = r.movie_id
GROUP BY m.genres
ORDER BY avg_rating DESC
LIMIT 5;

-- 3️⃣ Director with the most movies
SELECT director, COUNT(*) AS total_movies
FROM movies
GROUP BY director
ORDER BY total_movies DESC
LIMIT 1;

-- 4️⃣ Average rating by release year
SELECT m.year, AVG(r.rating) AS avg_rating
FROM ratings r
JOIN movies m ON m.movie_id = r.movie_id
GROUP BY m.year
ORDER BY m.year;


💡 Design Choices & Assumptions


Database: Chose MySQL for its relational design and easy integration with SQLAlchemy.


Keys: Used movie_id as the consistent identifier across tables.


Genre Handling: Stored as comma-separated text for simplicity.


OMDb Lookup: Used imdbId for exact matches; fallback to movie title.


ETL Idempotency: Used conditional inserts (ON DUPLICATE KEY UPDATE) to avoid duplicates.



🚧 Challenges & Solutions
ChallengeSolutionTitles mismatched between MovieLens and OMDbUsed IMDb ID from links.csv for reliable lookupOMDb rate limitsAdded retry logic and small delays between requestsMissing OMDb fields (e.g., N/A)Stored as NULL and logged missing dataDuplicate insertionsUsed primary key checks and upsert logic

📈 Potential Improvements


Use multi-threaded API requests to speed up enrichment.


Implement logging and error handling for robustness.


Integrate Airflow or Prefect for orchestration.


Normalize genres into a separate lookup table.


Move analytics layer into a data warehouse (e.g., Redshift or BigQuery).



📚 Data Source Details
Summary
The dataset (ml-latest-small) describes 5-star rating and free-text tagging activity from MovieLens.
It contains 100,836 ratings and 3,683 tag applications across 9,742 movies, created by 610 users between March 29, 1996 and September 24, 2018.
Files


movies.csv — Movie titles and genres


ratings.csv — User ratings with timestamps


links.csv — IMDB and TMDB identifiers


tags.csv — User-generated tags (not used in this assignment)


License & Citation
The dataset is provided by GroupLens Research, University of Minnesota, under a free educational license.

F. Maxwell Harper and Joseph A. Konstan. 2015. The MovieLens Datasets: History and Context.
ACM Transactions on Interactive Intelligent Systems (TiiS) 5, 4: 19:1–19:19.
https://doi.org/10.1145/2827872


👨‍💻 Author
Developed by: [Your Name]
For: TS Works — Data Engineering Assignment
Database: MySQL
Contact: youremail@example.com
Date: November 2025

---

✅ **This final README.md covers:**
- All project overview and goals  
- Environment setup and execution  
- Schema, ETL logic, and analytical queries  
- Design choices, challenges, and improvements  
- Dataset license and citation  
1. Extract

Read movies.csv and ratings.csv from MovieLens.

Optionally, use links.csv to fetch imdbId for OMDb queries.

2. Transform

Clean titles, parse genres (pipe-separated → comma-separated).

Extract release year from movie titles.

Convert timestamps to readable datetime format.

Handle missing or invalid entries.

3. Enrich

Query OMDb API for additional movie metadata.

Fetch Director, Plot, and BoxOffice.

Handle missing API results gracefully (NULL or default).

4. Load

Insert data into MySQL tables using SQLAlchemy.

Ensure idempotency — re-running the script won’t create duplicates.
Design Choices & Assumptions

Database: Chose MySQL for its relational design and easy integration with SQLAlchemy.

Keys: Used movie_id as the consistent identifier across tables.

Genre Handling: Stored as comma-separated text for simplicity.

OMDb Lookup: Used imdbId for exact matches; fallback to movie title.

ETL Idempotency: Used conditional inserts (ON DUPLICATE KEY UPDATE) to avoid duplicates.

| **Challenge**                                | **Solution**                                        |
| -------------------------------------------- | --------------------------------------------------- |
| Titles mismatched between MovieLens and OMDb | Used IMDb ID from `links.csv` for reliable lookup   |
| OMDb rate limits                             | Added retry logic and small delays between requests |
| Missing OMDb fields (e.g., `N/A`)            | Stored as NULL and logged missing data              |
| Duplicate insertions                         | Used primary key checks and upsert logic            |
Summary

The dataset (ml-latest-small) describes 5-star rating and free-text tagging activity from MovieLens
.
It contains 100,836 ratings and 3,683 tag applications across 9,742 movies, created by 610 users between March 29, 1996 and September 24, 2018.

Files

movies.csv — Movie titles and genres

ratings.csv — User ratings with timestamps

links.csv — IMDB and TMDB identifiers

tags.csv — User-generated tags (not used in this assignment)

License & Citation

The dataset is provided by GroupLens Research, University of Minnesota, under a free educational license.

F. Maxwell Harper and Joseph A. Konstan. 2015. The MovieLens Datasets: History and Context.
ACM Transactions on Interactive Intelligent Systems (TiiS) 5, 4: 19:1–19:19.
https://doi.org/10.1145/2827872

Developed by: Vibhor Vimal
For: TS Works — Data Engineering Assignment
Database: MySQL
Contact: vibhorvimalinfo@gmail.com

I
