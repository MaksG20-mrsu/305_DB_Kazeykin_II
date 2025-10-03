import csv
import os
import re

SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "dataset")

FILE_PATHS = {
    "movies": os.path.join(DATA_DIR, "movies.csv"),
    "ratings": os.path.join(DATA_DIR, "ratings.csv"),
    "tags": os.path.join(DATA_DIR, "tags.csv"),
    "users": os.path.join(DATA_DIR, "users.txt"),
}

def sanitize_for_sql(text: str) -> str:
    """Заменяет одинарные кавычки на удвоенные для корректной вставки в SQL."""
    return text.replace("'", "''")

def parse_movie_title(title: str):
    """Извлекает год из названия фильма, если он указан в скобках в конце."""
    year_match = re.search(r"\((\d{4})\)$", title.strip())
    if year_match:
        extracted_year = int(year_match.group(1))
        clean_name = title[: year_match.start()].strip()
        return clean_name, extracted_year
    return title, None

def export_movies_to_sql(output_handle):
    output_handle.write("DROP TABLE IF EXISTS movies;\n")
    output_handle.write(
        "CREATE TABLE movies (\n"
        "    id INTEGER PRIMARY KEY,\n"
        "    title TEXT,\n"
        "    year INTEGER,\n"
        "    genres TEXT\n"
        ");\n\n"
    )

    with open(FILE_PATHS["movies"], encoding="utf-8") as movie_file:
        csv_reader = csv.reader(movie_file)
        next(csv_reader)
        for record in csv_reader:
            movie_id, raw_title, genre_list = record
            title_clean, release_year = parse_movie_title(raw_title)
            year_value = release_year if release_year is not None else "NULL"
            output_handle.write(
                f"INSERT INTO movies (id, title, year, genres) "
                f"VALUES ({movie_id}, '{sanitize_for_sql(title_clean)}', {year_value}, "
                f"'{sanitize_for_sql(genre_list)}');\n"
            )

def export_ratings_to_sql(output_handle):
    output_handle.write("DROP TABLE IF EXISTS ratings;\n")
    output_handle.write(
        "CREATE TABLE ratings (\n"
        "    id INTEGER PRIMARY KEY,\n"
        "    user_id INTEGER,\n"
        "    movie_id INTEGER,\n"
        "    rating REAL,\n"
        "    timestamp TEXT\n"
        ");\n\n"
    )

    with open(FILE_PATHS["ratings"], encoding="utf-8") as ratings_file:
        csv_reader = csv.reader(ratings_file)
        next(csv_reader)
        for idx, row in enumerate(csv_reader, start=1):
            user_id, movie_id, rating, timestamp = row
            output_handle.write(
                f"INSERT INTO ratings (id, user_id, movie_id, rating, timestamp) "
                f"VALUES ({idx}, {user_id}, {movie_id}, {rating}, '{timestamp}');\n"
            )

def export_tags_to_sql(output_handle):
    output_handle.write("DROP TABLE IF EXISTS tags;\n")
    output_handle.write(
        "CREATE TABLE tags (\n"
        "    id INTEGER PRIMARY KEY,\n"
        "    user_id INTEGER,\n"
        "    movie_id INTEGER,\n"
        "    tag TEXT,\n"
        "    timestamp TEXT\n"
        ");\n\n"
    )

    with open(FILE_PATHS["tags"], encoding="utf-8") as tags_file:
        csv_reader = csv.reader(tags_file)
        next(csv_reader)
        for idx, row in enumerate(csv_reader, start=1):
            user_id, movie_id, tag_text, timestamp = row
            output_handle.write(
                f"INSERT INTO tags (id, user_id, movie_id, tag, timestamp) "
                f"VALUES ({idx}, {user_id}, {movie_id}, '{sanitize_for_sql(tag_text)}', '{timestamp}');\n"
            )

def export_users_to_sql(output_handle):
    output_handle.write("DROP TABLE IF EXISTS users;\n")
    output_handle.write(
        "CREATE TABLE users (\n"
        "    id INTEGER PRIMARY KEY,\n"
        "    name TEXT,\n"
        "    email TEXT,\n"
        "    gender TEXT,\n"
        "    register_date TEXT,\n"
        "    occupation TEXT\n"
        ");\n\n"
    )

    with open(FILE_PATHS["users"], encoding="utf-8") as users_file:
        for line_num, line in enumerate(users_file, start=1):
            fields = line.strip().split("|")
            if len(fields) < 6:
                continue
            user_id, full_name, email_addr, gender_val, reg_date, job = fields
            output_handle.write(
                f"INSERT INTO users (id, name, email, gender, register_date, occupation) "
                f"VALUES ({user_id}, '{sanitize_for_sql(full_name)}', '{sanitize_for_sql(email_addr)}', "
                f"'{gender_val}', '{reg_date}', '{sanitize_for_sql(job)}');\n"
            )

def build_sql_script():
    sql_output_file = os.path.join(SCRIPT_DIR, "db_init.sql")
    with open(sql_output_file, "w", encoding="utf-8") as sql_out:
        export_movies_to_sql(sql_out)
        export_ratings_to_sql(sql_out)
        export_tags_to_sql(sql_out)
        export_users_to_sql(sql_out)

if __name__ == "__main__":
    build_sql_script()