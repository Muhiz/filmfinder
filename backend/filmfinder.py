import requests
from flask import Flask, request
from xml.etree import ElementTree

app = Flask(__name__)


# id, name, city, location x,y
@app.route('/api/theatres', methods=['GET'])
def get_theatres():
    r = requests.get("http://www.finnkino.fi/xml/TheatreAreas/")
    return r.text


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


