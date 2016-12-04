import os
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from finnkinoapi import *

app = Flask(__name__)
CORS(app)


@app.route('/api/cities', methods=['GET'])
def get_cities():
    cities = fetch_cities()

    return jsonify({'cities': cities})


@app.route('/api/cities/<string:city>/theatres', methods=['GET'])
def get_theatres_in(city):
    cities = fetch_cities()
    if city in cities:
        theatres = fetch_theatres(city)
        return jsonify({'theatres': [t.serialize() for t in theatres]})
    return jsonify(None)


@app.route('/api/cities/<string:city>/shows', methods=['GET'])
def get_shows_in(city):
    cities = fetch_cities()
    if city in cities:
        shows = fetch_shows_in(cities[city])
        return jsonify({'shows': [s.serialize() for s in shows]})
    return jsonify(None)


# returns Theatre -list.
@app.route('/api/theatres', methods=['GET'])
def get_theatres():
    theatres = fetch_theatres()

    return jsonify({'theatres': [t.serialize() for t in theatres]})


# Movie title, Genres, Description, Runtime, Show starts, IMDb rating
@app.route('/api/theatres/<int:theatre_id>/shows', methods=['GET'])
def get_shows(theatre_id):
    # date_arg = request.args['date']
    shows = fetch_shows_in(theatre_id)

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
