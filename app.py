import os
from dotenv import load_dotenv
from flask import Flask
from flask_alembic import Alembic
from flask_restful import Api

from api.constants import PATH_MOVIE_LIST, PATH_MOVIE, PATH_MOVIE_LIKES, PATH_MOVIE_DISLIKES
from api.resources import MovieResource, MovieListResource, MovieLikesResource, MovieDislikesResource
from api.models import db, Movie
from config import configurations

alembic = Alembic()


def create_app():
    app = Flask(__name__)
    app.config.from_object(configurations.get(os.getenv('APP_CONFIG') or 'default'))
    db.init_app(app)
    alembic.init_app(app)
    api = Api(app)
    api.add_resource(MovieListResource, PATH_MOVIE_LIST)
    api.add_resource(MovieResource, PATH_MOVIE)
    api.add_resource(MovieLikesResource, PATH_MOVIE_LIKES)
    api.add_resource(MovieDislikesResource, PATH_MOVIE_DISLIKES)
    return app


if __name__ == '__main__':
    load_dotenv()
    app = create_app()
    app.run(port=5100)
