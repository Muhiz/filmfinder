
class Theatre:
    def __init__(self, theatre_id, name, city, location):
        self.id = theatre_id
        self.name = name
        self.city = city
        self.location = location

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'location': self.location
        }


# Movie title, Genres, Description, Runtime, Show starts, IMDb rating
class Show:
    def __init__(self, show_id, title, genre, description, length, starttime, rating, poster_url):
        self.show_id = show_id
        self.title = title
        self.genre = genre
        self.description = description
        self.length = length
        self.starttime = starttime
        self.rating = rating
        self.poster = poster_url

    def serialize(self):
        return {
            'id': self.show_id,
            'title': self.title,
            'genre': self.genre,
            'description': self.description,
            'runtime': self.length,
            'start_time': self.starttime,
            'rating': self.rating,
            'poster_url': self.poster
        }
