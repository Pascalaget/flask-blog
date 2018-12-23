from blog import db

class Movie_cast(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'), primary_key=False)
    actor_id = db.Column(db.Integer, db.ForeignKey('actors.actor_id'), primary_key=False)
    role = db.Column(db.String(100))


class Movie_genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'), primary_key=False)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.genre_id'), primary_key=False)
    updated = db.Column(db.Integer)


class Movies(db.Model):
    __searchable__ = ['title', 'plot', 'studio']
    movie_id = db.Column(db.Integer, primary_key=True)
    videopath = db.Column(db.String(300), nullable=False)
    imagepath = db.Column(db.String(300), nullable=False)
    thumbpath = db.Column(db.String(300), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer)
    duration = db.Column(db.Integer)
    width = db.Column(db.Integer)
    height = db.Column(db.Integer)
    location = db.Column(db.String(250))
    plot = db.Column(db.String(1000))
    studio = db.Column(db.String(100))

    actors = db.relationship("Actors", secondary='movie_cast')
    genres = db.relationship("Genre", secondary='movie_genre')


class Actors(db.Model):
    actor_id = db.Column(db.Integer, nullable=False, primary_key=True)
    actor = db.Column(db.String(100), nullable=False)
    role = db.relationship("Movie_cast")


class Genre(db.Model):
    genre_id = db.Column(db.Integer, primary_key=True)
    genre = db.Column(db.String(100),  default='None')
