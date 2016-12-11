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

    return name


def split_movie_name(name):
    names = name.split('-')
    if len(names) == 1:
        names = name.split(':')
        return names[1]

    return names[0]


def make_query(name):
    query = {'t': name, 'y': 'plot', 'r': 'json'}
    return requests.get("http://www.omdbapi.com/", params=query).json()


def query_movie_rating(name):
    """Queries movie rating form OMDB API"""
    name = sanitize_movie_name(name)

    r = make_query(name)
    if r['Response'] == 'False':
        # Try again by splitting extra part out
        r = make_query(split_movie_name(name))

    return r


def fetch_movie_rating(name):
    """Fetches movie rating from OMDB API"""
    r = query_movie_rating(name)

    if 'imdbRating' in r:
        rating = r['imdbRating']
    else:
        rating = None

    return rating
