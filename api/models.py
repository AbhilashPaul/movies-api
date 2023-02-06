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

    def update(self, title=None, description=None, release_year=None,
               duration_minutes=None, rating=None, likes=None, dislikes=None):
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
        if likes is not None:
            self.likes = likes
        if dislikes is not None:
            self.dislikes = dislikes
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
