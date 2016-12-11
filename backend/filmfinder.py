import os
from flask import Flask, request, jsonify, make_response
from flask_restplus import Resource, Api, fields
from flask_cors import CORS
from flask_sslify import SSLify
from finnkinoapi import *

app = Flask(__name__)
api = Api(app)
CORS(app)


if 'DYNO' in os.environ:  # only trigger SSLify if the app is running on Heroku
    app.debug = False
    sslify = SSLify(app)


ns = api.namespace('api', description='Filmfinder API')


def get_cities():
    cities = fetch_cities()

    return jsonify({'cities': cities})


def get_theatres_in(city):
    cities = fetch_cities()
    if city in cities:
        theatres = fetch_theatres(city)
        return jsonify({'theatres': [t.serialize() for t in theatres]})
    return jsonify(None)


def get_shows_in(city):
    cities = fetch_cities()
    if city in cities:
        shows = fetch_shows_in(cities[city])
        return jsonify({'shows': [s.serialize() for s in shows]})
    return jsonify(None)


def get_theatres():
    theatres = fetch_theatres()

    return jsonify({'theatres': [t.serialize() for t in theatres]})


def get_shows(theatre_id):
    # date_arg = request.args['date']
    shows = fetch_shows_in(theatre_id)

    return jsonify({'shows': [s.serialize() for s in shows]})


def get_show_in(theatre_id, show_id):
    query = {'t': 'Luokkakokous 2', 'y': 'plot', 'r': 'json'}
    r = requests.get("http://www.omdbapi.com/", params=query)
    return r.text


def get_show(show_id):
    pass


@ns.route('/theatres/<int:theatre_id>/shows/<int:show_id>')
@ns.response(404, 'Theatre or show not found')
@ns.param('theatre_id', 'The theatre\'s ID')
@ns.param('show_id', 'The show\'s ID')
class ShowsInTheatre(Resource):
    """Show/Movie in theatre"""
    @staticmethod
    def get(theatre_id, show_id):
        return get_show_in(theatre_id, show_id)

@ns.route('/cities')
class CityList(Resource):
    """Shows a list of all available cities"""
    @staticmethod
    def get():
        return get_cities()


@ns.route('/cities/<string:city>/theatres')
@ns.response(404, 'City not found')
@ns.param('city', 'The city\'s name')
class TheatresInCityList(Resource):
    """Shows a list of theatres in the city"""
    @staticmethod
    def get(city):
        return get_theatres_in(city)


@ns.route('/cities/<string:city>/shows')
@ns.response(404, 'City not found')
@ns.param('city', 'The city\'s name')
class ShowsInCityList(Resource):
    """Shows a list of shows in city theatres"""
    @staticmethod
    def get(city):
        return get_shows_in(city)


@ns.route('/theatres')
class TheatresList(Resource):
    """Shows a list of theatres"""
    @staticmethod
    def get():
        return get_theatres()


@app.errorhandler(404)
def not_found(_):
    return make_response(jsonify({'error': 'Not found'}), 404)


@ns.route('/theatres/<int:theatre_id>/shows')
@ns.response(404, 'Theatre not found')
@ns.param('theatre_id', 'The theatre\'s ID')
class ShowsInTheatreList(Resource):
    """Shows a list of theatres"""
    @staticmethod
    def get(theatre_id):
        return get_shows(theatre_id)


@ns.route('/theatres/shows/<int:show_id>', '/theatres/<int:theatre_id>/shows/<int:show_id>')
@ns.response(404, 'Theatre or show not found')
@ns.param('theatre_id', 'The theatre\'s ID')
@ns.param('show_id', 'The show\'s ID')
class Show(Resource):
    """Show/Movie in theatre"""

    @staticmethod
    def get(theatre_id, show_id):
        return get_show_in(theatre_id, show_id)

    @staticmethod
    def get(show_id):
        return get_show(show_id)


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
