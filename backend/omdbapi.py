import requests


def fetch_movie_rating(name):
    """Fetches movie rating from OMDB API"""
    query = {'t': name, 'y': 'plot', 'r': 'json'}
    r = requests.get("http://www.omdbapi.com/", params=query).json()

    if 'imdbRating' in r:
        rating = r['imdbRating']
    else:
        rating = None

    return rating
