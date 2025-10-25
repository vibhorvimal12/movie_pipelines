import pandas as pd
import requests
import mysql.connector
from mysql.connector import Error
from time import sleep
from dotenv import load_dotenv
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

load_dotenv()
API_KEY = os.getenv("API_KEY = dd6fbba7")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASS = os.getenv("DB_PASS", "802159123#")
DB_NAME = os.getenv("DB_NAME", "movie_pipeline")
MAX_THREADS = 10

def get_connection():
    try:
        return mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME)
    except Error:
        return None

def fetch_omdb_data(title, retries=3):
    for _ in range(retries):
        try:
            url = f"http://www.omdbapi.com/?t={title}&apikey={API_KEY}"
            r = requests.get(url, timeout=20)
            data = r.json()
            if data.get("Response") == "True":
                box_office = data.get("BoxOffice")
                if box_office and box_office != "N/A":
                    box_office = box_office.replace("$","").replace(",","")
                else:
                    box_office = None
                release_year = pd.to_numeric(data.get("Year"), errors="coerce")
                return {"title": title, "director": data.get("Director"), "plot": data.get("Plot"),
                        "box_office": box_office, "release_year": release_year}
        except requests.exceptions.RequestException:
            sleep(2)
    return {"title": title, "director": None, "plot": None, "box_office": None, "release_year": None}

def run_etl():
    movies = pd.read_csv("movies.csv")
    ratings = pd.read_csv("ratings.csv")
    tags = pd.read_csv("tags.csv")
    print("Starting ETL process...")
    print(f"Movies loaded: {len(movies)}")
    print(f"Ratings loaded: {len(ratings)}")
    print(f"Tags loaded: {len(tags)}")
    details = []
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        futures = {executor.submit(fetch_omdb_data, title): title for title in movies["title"]}
        for future in tqdm(as_completed(futures), total=len(futures), desc="Fetching OMDB data"):
            details.append(future.result())
    movies = pd.merge(movies, pd.DataFrame(details), on="title", how="left")
    movies["release_year"] = pd.to_numeric(movies["release_year"], errors="coerce")
    movies["box_office"] = pd.to_numeric(movies["box_office"], errors="coerce")
    ratings["timestamp"] = pd.to_datetime(ratings["timestamp"], unit="s")
    conn = get_connection()
    if not conn:
        return
    cursor = conn.cursor()
    print("Inserting movies into database...")
    for _, row in movies.iterrows():
        try:
            cursor.execute("""
                INSERT INTO movies (title, genres, director, plot, box_office, release_year)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    genres=VALUES(genres),
                    director=VALUES(director),
                    plot=VALUES(plot),
                    box_office=VALUES(box_office),
                    release_year=VALUES(release_year);
            """, (row["title"], row["genres"], row["director"], row["plot"], row["box_office"], row["release_year"]))
        except Error:
            continue
    conn.commit()
    print("Movies table loaded successfully.")
    print("Inserting ratings into database...")
    for _, row in ratings.iterrows():
        try:
            cursor.execute("INSERT INTO ratings (user_id, movie_id, rating, timestamp) VALUES (%s,%s,%s,%s)",
                           (int(row["userId"]), int(row["movieId"]), float(row["rating"]), row["timestamp"]))
        except Error:
            continue
    conn.commit()
    print("Ratings table loaded successfully.")
    print("Inserting tags into database...")
    for _, row in tags.iterrows():
        try:
            cursor.execute("INSERT INTO tags (user_id, movie_id, tag, timestamp) VALUES (%s,%s,%s,%s)",
                           (int(row["userId"]), int(row["movieId"]), row["tag"], pd.to_datetime(row["timestamp"], unit="s")))
        except Error:
            continue
    conn.commit()
    print("Tags table loaded successfully.")
    cursor.close()
    conn.close()
    print("ETL completed successfully!")

if __name__ == "__main__":
    run_etl()
