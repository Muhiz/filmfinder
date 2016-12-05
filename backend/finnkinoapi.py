import requests
from xml.etree import ElementTree
from models import Theatre, Show
from omdbapi import fetch_movie_rating
from locationapi import fetch_location


def fetch_cities():
    """Fetches theatre cities from Finnkino XML API"""

    response = requests.get("http://www.finnkino.fi/xml/TheatreAreas/", timeout=1.000)

    root = ElementTree.fromstring(response.content)

    cities = {}

    for theatre in root.findall('TheatreArea'):
        area_id = int(theatre.find('ID').text)
        area_name = theatre.find('Name').text
        area_name = area_name.split(':')

        # Remove 1029 Valitse teatteri/kaupunki and choose only cities
        if not area_id == 1029 and len(area_name) == 1:
            cities[area_name[0]] = area_id

    return cities


def fetch_theatres(city=None):
    """Fetches theatres from Finnkino XML API"""
    response = requests.get("http://www.finnkino.fi/xml/TheatreAreas/", timeout=1.000)

    root = ElementTree.fromstring(response.content)

    theatres = []

    for theatre in root.findall('TheatreArea'):
        area_id = int(theatre.find('ID').text)
        area_name = theatre.find('Name').text
        area_name = area_name.split(':')

        if city and area_name[0] != city:
            continue

        if area_id == 1029 or area_id == 1014 or area_id == 1012 or area_id == 1002 or area_id == 1021:
            continue

        if len(area_name) > 1:
            area_name[1] = area_name[1].lstrip()
            theatres.append(Theatre(area_id, area_name[1], area_name[0], fetch_location(area_name[0])))
        else:
            theatres.append(Theatre(area_id, area_name[0], area_name[0], fetch_location(area_name[0])))

    return theatres


def fetch_event(event_id):
    query = {'eventID': event_id}
    response = requests.get("http://www.finnkino.fi/xml/Events/", params=query, timeout=1.000)
    root = ElementTree.fromstring(response.content)

    description = ""

    event = root[0]

    description = event.find('Synopsis').text

    return description


def fetch_shows_in(theatre_id):
    query = {'area': theatre_id}  # , 'dt': date_arg}
    response = requests.get("http://www.finnkino.fi/xml/Schedule/", params=query, timeout=1.000)

    root = ElementTree.fromstring(response.content)

    shows = []

    for show in root.findall('Shows/Show'):
        show_id = int(show.find('EventID').text)
        original_title = show.find('OriginalTitle').text
        title = show.find('Title').text
        description = fetch_event(show_id)
        genres = show.find('Genres').text
        startutc = show.find('dttmShowStartUTC').text
        length = int(show.find('LengthInMinutes').text)
        rating = fetch_movie_rating(original_title)
        poster_url = show.find('Images').find('EventMediumImagePortrait').text
        shows.append(Show(show_id, title, genres, description, length, startutc, rating, poster_url))

    return shows
