import requests


def sanitize_movie_name(name):
    """Removes any extra info from movie name added by Finnkino"""
    name = name.rstrip()
    # Remove dub and 2D / 3D from the end of name and remove trailing space
    if name.endswith('(dub)'):
        name = name[:-5].rstrip()

    if name.endswith('(2D)') or name.endswith('(3D)'):
        name = name[:-4].rstrip()

    if name.endswith('2D') or name.endswith('3D'):
        name = name[:-2].rstrip()

    print(name)
    return name


def query_movie_rating(name):
    """Queries movie rating form OMDB API"""
    query = {'t': name, 'y': 'plot', 'r': 'json'}
    return requests.get("http://www.omdbapi.com/", params=query).json()


def fetch_movie_rating(name):
    """Fetches movie rating from OMDB API"""
    name = sanitize_movie_name(name)
    r = query_movie_rating(name)

    if r['Response'] == 'False':
        # Try again by splitting extra part out
        print('Not found')
        r = query_movie_rating(name.split('-')[0])
        print(name.split('-')[0])

    if 'imdbRating' in r:
        rating = r['imdbRating']
    else:
        rating = None

    return rating
