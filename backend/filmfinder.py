import os
import requests
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from xml.etree import ElementTree
from models import Theatre, Show

app = Flask(__name__)
CORS(app)


def fetch_location(address):
    query = {'address': address, 'sensor': False}
    r = requests.get("https://maps.googleapis.com/maps/api/geocode/json", params=query).json()

    if r['status'] == 'OK':
        rs = r['results'][0]
        gm = rs['geometry']
        location = gm['location']
    else:
        location = None

    print(location)

    return location


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
            cities[area_id] = area_name[0]

    return cities


def fetch_theatres():
    """Fetches theatres from Finnkino XML API"""
    response = requests.get("http://www.finnkino.fi/xml/TheatreAreas/", timeout=1.000)

    root = ElementTree.fromstring(response.content)

    theatres = []

    for theatre in root.findall('TheatreArea'):
        area_id = int(theatre.find('ID').text)
        area_name = theatre.find('Name').text
        area_name = area_name.split(':')

        # Remove 1029 Valitse teatteri/kaupunki, remove areas and choose only theatres
        # TODO: remove hard-coding
        if area_id == 1029 or area_id == 1014 or area_id == 1012 or area_id == 1002 or area_id == 1021:
            continue

        if len(area_name) > 1:
            area_name[1] = area_name[1].lstrip()
            theatres.append(Theatre(area_id, area_name[1], area_name[0], fetch_location(area_name[0])))
        else:
            theatres.append(Theatre(area_id, area_name[0], area_name[0], fetch_location(area_name[0])))

    return theatres


def fetch_movie_rating(name):
    """Fetches movie rating from OMDB API"""
    query = {'t': name, 'y': 'plot', 'r': 'json'}
    r = requests.get("http://www.omdbapi.com/", params=query).json()

    if 'imdbRating' in r:
        rating = r['imdbRating']
    else:
        rating = None

    return rating


@app.route('/api/cities', methods=['GET'])
def get_cities():
    cities = fetch_cities()

    return jsonify(cities)


# returns Theatre -list.
@app.route('/api/theatres', methods=['GET'])
def get_theatres():
    theatres = fetch_theatres()

    return jsonify({'theatres': [t.serialize() for t in theatres]})


# Movie title, Genres, Description, Runtime, Show starts, IMDb rating
@app.route('/api/theatres/<int:theatre_id>/shows', methods=['GET'])
def get_shows(theatre_id):
    # date_arg = request.args['date']
    query = {'area': theatre_id}  # , 'dt': date_arg}
    response = requests.get("http://www.finnkino.fi/xml/Schedule/", params=query, timeout=1.000)

    root = ElementTree.fromstring(response.content)

    shows = []

    for show in root.findall('Shows/Show'):
        show_id = int(show.find('EventID').text)
        original_title = show.find('OriginalTitle').text
        title = show.find('Title').text
        genres = show.find('Genres').text
        startutc = show.find('dttmShowStartUTC').text
        length = int(show.find('LengthInMinutes').text)
        rating = fetch_movie_rating(original_title)
        shows.append(Show(show_id, title, genres, "Lorem ipsum", length, startutc, rating))

    return jsonify({'shows': [s.serialize() for s in shows]})


# Movie title, Genres, Description, Runtime, Show starts, IMDb rating, Free seats
@app.route('/api/theatres/<int:theatre_id>/shows/<int:show_id>', methods=['GET'])
def get_show_in(theatre_id, show_id):
    query = {'t': 'Luokkakokous 2', 'y': 'plot', 'r': 'json'}
    r = requests.get("http://www.omdbapi.com/", params=query)
    return r.text


@app.route('/api/theatres/shows/<int:show_id>', methods=['GET'])
def get_show(show_id):
    query = {'t': 'Luokkakokous 2', 'y': 'plot', 'r': 'json'}
    r = requests.get("http://www.omdbapi.com/", params=query)
    return r.text


@app.errorhandler(404)
def not_found(_):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
