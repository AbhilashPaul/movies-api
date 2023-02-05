import os
from dotenv import load_dotenv
from flask import Flask
from flask_alembic import Alembic
from flask_restful import Api

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
    api.add_resource(MovieListResource, "/api/movies")
    api.add_resource(MovieResource, "/api/movies/<movie_id>")
    api.add_resource(MovieLikesResource, "/api/movies/<movie_id>/likes")
    api.add_resource(MovieDislikesResource, "/api/movies/<movie_id>/dislikes")
    return app


if __name__ == '__main__':
    load_dotenv()
    app = create_app()
    app.run(port=5100)
