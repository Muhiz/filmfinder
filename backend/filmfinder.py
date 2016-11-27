import os
import requests
from flask import Flask, request, jsonify, make_response
from xml.etree import ElementTree

app = Flask(__name__)


class Theatre:
    def __init__(self, theatre_id, name, city):
        self.id = theatre_id
        self.name = name
        self.city = city
        # self.location x, y

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'city': self.city
        }

# Movie title, Genres, Description, Runtime, Show starts, IMDb rating
class Show:
    def __init__(self, show_id, title, genre, description, length, starttime, rating):
        self.show_id = show_id
        self.title = title
        self.genre = genre
        self.description = description
        self.length = length
        self.starttime = starttime
        self.rating = rating

    def serialize(self):
        return {
            'id': self.show_id,
            'title': self.title,
            'genre': self.genre,
            'description': self.description,
            'runtime': self.length,
            'start_time': self.starttime,
            'rating': self.rating
        }


@app.route('/api/cities', methods=['GET'])
def get_cities():
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

    return jsonify(cities)


# returns Theatre -list.
@app.route('/api/theatres', methods=['GET'])
def get_theatres():
    response = requests.get("http://www.finnkino.fi/xml/TheatreAreas/", timeout=1.000)

    root = ElementTree.fromstring(response.content)

    theatres = []

    for theatre in root.findall('TheatreArea'):
        area_id = int(theatre.find('ID').text)
        area_name = theatre.find('Name').text
        area_name = area_name.split(':')

        # Remove 1029 Valitse teatteri/kaupunki and choose only cities
        if not area_id == 1029 and len(area_name) > 1:
            area_name[1] = area_name[1].lstrip()
            theatres.append(Theatre(area_id, area_name[1], area_name[0]))

    return jsonify({'theatres': [t.serialize() for t in theatres]})


# Movie title, Genres, Description, Runtime, Show starts, IMDb rating
@app.route('/api/theatres/<int:theatre_id>/shows', methods=['GET'])
def get_shows(theatre_id):
    # date_arg = request.args['date']
    query = {'area': theatre_id}  #, 'dt': date_arg}
    response = requests.get("http://www.finnkino.fi/xml/Schedule/", params=query, timeout=1.000)

    root = ElementTree.fromstring(response.content)

    shows = []

    for show in root.findall('Shows/Show'):
        show_id = int(show.find('EventID').text)
        title = show.find('Title').text
        genres = show.find('Genres').text
        startutc = show.find('dttmShowStartUTC').text
        length = int(show.find('LengthInMinutes').text)
        shows.append(Show(show_id, title, genres, "", length, startutc, 0))

    return jsonify({'shows': [s.serialize() for s in shows]})


# Movie title, Genres, Description, Runtime, Show starts, IMDb rating, Free seats
@app.route('/api/theatres/<int:theatre_id>/shows/<int:show_id>', methods=['GET'])
def get_show_in(theatre_id, show_id):
    query = {'t' : 'Luokkakokous 2', 'y': 'plot', 'r': 'json'}
    r = requests.get("http://www.omdbapi.com/", params=query)
    return r.text


@app.route('/api/theatres/shows/<int:show_id>', methods=['GET'])
def get_show(show_id):
    query = {'t' : 'Luokkakokous 2', 'y': 'plot', 'r': 'json'}
    r = requests.get( "http://www.omdbapi.com/", params=query)
    return r.text


@app.errorhandler(404)
def not_found(_):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)


