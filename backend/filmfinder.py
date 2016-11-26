import requests
from flask import Flask, request, jsonify
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
    response = requests.get("http://www.finnkino.fi/xml/TheatreAreas/",  timeout=1.000)

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
    # Check if date arg exists, if it's date or "today"
    date_arg = request.args['date']
    print(request.args)
    return date_arg


# Movie title, Genres, Description, Runtime, Show starts, IMDb rating, Free seats
@app.route('/api/theatres/<int:theatre_id>/shows/<int:show_id>', methods=['GET'])
def get_show(theatre_id, show_id):
    query = {'t' : 'Luokkakokous 2', 'y' : 'plot', 'r' : 'json'}
    r = requests.get( "http://www.omdbapi.com/", params=query)
    return r.text


if __name__ == '__main__':
    app.run()


