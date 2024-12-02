import re
import pandas as pd
import requests
import json
import os


def extract_movie_year(title_cell):
    pattern = r"\((\d{4})\)"
    match = re.search(pattern, title_cell)

    if match:
        return int(match.group(1))
    
    return None


def extract_movie_genres(genres_cell):
    genre_list = genres_cell.split("|")
    return genre_list


def clean_movie_title(title_cell):
    pattern = r"([\w\W]+) \(\d{4}\)"
    match = re.search(pattern, title_cell)

    if match:
        return match.group(1)
    
    return None


def check_data_type(df, expected_data_type):
    df = df.apply(lambda value: value if isinstance(value, expected_data_type) else pd.NA)
    return df


def get_movie_details(movie_id, access_token):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        #print(f"Error {response.status_code} for movie ID {movie_id}: {response.text}")
        return None

def process_movie_list(movie_list, token_file, output_csv):
    with open(token_file, 'r') as file:
        data = json.load(file)
        access_token = data.get("access_token")
    
    if not access_token:
        raise ValueError("Access token not found in the JSON file.")
    
    if os.path.exists(output_csv):
        existing_data = pd.read_csv(output_csv)
        processed_ids = set(existing_data['movieId'])
        last_processed_id = max(existing_data['movieId'])
    else:
        existing_data = pd.DataFrame()
        processed_ids = set()
        last_processed_id = -1
    
    movie_list = sorted(
        movie_id for movie_id in set(movie_list) 
        if movie_id not in processed_ids and movie_id > last_processed_id
    )
    
    with open(output_csv, 'a', newline='', encoding='utf-8') as file:
        for movie_id in movie_list:
            details = get_movie_details(movie_id, access_token)
            if details:
                extracted_details = {
                    "movieId": details.get("id"),
                    "title": details.get("title"),
                    "original_title": details.get("original_title"),
                    "release_date": details.get("release_date"),
                    "runtime": details.get("runtime"),
                    "genres": ", ".join([genre["name"] for genre in details.get("genres", [])]),
                    "production_companies": ", ".join([company["name"] for company in details.get("production_companies", [])]),
                    "popularity": details.get("popularity"),
                    "vote_average": details.get("vote_average"),
                    "vote_count": details.get("vote_count"),
                    "overview": details.get("overview"),
                    "status": details.get("status"),
                    "budget": details.get("budget"),
                    "revenue": details.get("revenue")
                }
                #print(f"m_id:{movie_id}::200")
                pd.DataFrame([extracted_details]).to_csv(file, header=file.tell() == 0, index=False)
            #else:
            #    print(f"m_id:{movie_id}::404")
    
    print(f"Movie details saved to {output_csv} incrementally.")


def preprocess_text(text, nlp, stop_words):
    if not isinstance(text, str) or not text.strip():
        return ""
    
    doc = nlp(text.lower())

    cleaned_tokens = [
        token.lemma_ for token in doc 
        if token.is_alpha and token.lemma_ not in stop_words
    ]
    return " ".join(cleaned_tokens)