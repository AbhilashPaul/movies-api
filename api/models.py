from flask_sqlalchemy import SQLAlchemy

from api.constants import CHARACTER_LIMIT_DESCRIPTION, CHARACTER_LIMIT_TITLE

db = SQLAlchemy()


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(CHARACTER_LIMIT_TITLE), unique=True, nullable=False)
    description = db.Column(db.String(CHARACTER_LIMIT_DESCRIPTION), nullable=False)
    release_year = db.Column(db.Integer, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Float(1), nullable=False)
    likes = db.Column(db.Integer)
    dislikes = db.Column(db.Integer)

    def __init__(self, title, description, release_year, duration_minutes, rating):
        self.title = title
        self.description = description
        self.release_year = release_year
        self.duration_minutes = duration_minutes
        self.rating = rating
        self.likes = 0
        self.dislikes = 0

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, title=None, description=None, release_year=None, duration_minutes=None, rating=None):
        if title is not None:
            self.title = title
        if description is not None:
            self.description = description
        if release_year is not None:
            self.release_year = release_year
        if duration_minutes is not None:
            self.duration_minutes = duration_minutes
        if rating is not None:
            self.rating = rating
        db.session.commit()
        return self

    @staticmethod
    def query_movie_by_title(title):
        return Movie.query.filter_by(title=title).first()

    @staticmethod
    def query_movie_by_id(movie_id):
        return Movie.query.filter(Movie.id == movie_id).one_or_none()

    @staticmethod
    def query_movies():
        return Movie.query.all()

    @staticmethod
    def increment_likes(movie_id):
        movie = Movie.query.filter(Movie.id == movie_id).first()
        movie.likes = Movie.likes + 1
        db.session.commit()

    @staticmethod
    def decrement_likes(movie_id):
        movie = Movie.query.filter(Movie.id == movie_id).first()
        if movie.likes > 0:
            movie.likes = Movie.likes - 1
            db.session.commit()

    @staticmethod
    def increment_dislikes(movie_id):
        movie = Movie.query.filter(Movie.id == movie_id).first()
        movie.dislikes = Movie.dislikes + 1
        db.session.commit()

    @staticmethod
    def decrement_dislikes(movie_id):
        movie = Movie.query.filter(Movie.id == movie_id).first()
        if movie.dislikes > 0:
            movie.dislikes = Movie.dislikes - 1
            db.session.commit()
