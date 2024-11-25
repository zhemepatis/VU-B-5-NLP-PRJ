import re


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