from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__='user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    watchlist = db.relationship('Movie', secondary='watchlist', back_populates='watchlist')

class Movie(db.Model):
    __tablename__='movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    release = db.Column(db.Integer, nullable=True)
    watchlist = db.relationship('User', secondary='watchlist', back_populates='watchlist')
    genres = db.relationship('Genre', secondary='movie_genre', back_populates='movies')

class Genre(db.Model):
    __tablename__='genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    movies = db.relationship('Movie', secondary='movie_genre', back_populates='genres')

class Review(db.Model):
    __tablename__='review'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    rating = db.Column(db.Integer, nullable=False)
    review_text = db.Column(db.Text, nullable=True)

# Link Table Movie <-> Genre
class MovieGenre(db.Model):
    __tablename__='movie_genre'
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), primary_key=True)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'), primary_key=True)

# Link Table User <-> Movie    (Movies the user has added to watch in future)
class Watchlist(db.Model):
    __tablename__='watchlist'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), primary_key=True)

