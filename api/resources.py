from flask import request, abort
from flask_restful import Resource, reqparse
from marshmallow import ValidationError

from api.constants import PROPERTY_RATING, PROPERTY_DURATION_MINUTES, PROPERTY_RELEASE_YEAR, PROPERTY_DESCRIPTION, \
    PROPERTY_TITLE
from api.models import Movie
from api.schemas import MovieSchema, MovieLikesSchema, MovieDislikesSchema

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)
likes_schema = MovieLikesSchema()
dislikes_schema = MovieDislikesSchema()


def get_movie_from_db(movie_id):
    movie = Movie.query_movie_by_id(movie_id)
    if movie is None:
        abort(404, f"Could not find movie with id {movie_id}")
    return movie


class MovieResource(Resource):
    def get(self, movie_id):
        movie = get_movie_from_db(movie_id)
        response = movie_schema.dump(movie)
        return response, 200

    def delete(self, movie_id):
        movie = get_movie_from_db(movie_id)
        movie.delete()
        return '', 204

    def put(self, movie_id):
        try:
            data = movie_schema.load(request.get_json())
            if Movie.query_movie_by_title(data[PROPERTY_TITLE]):
                abort(409, f"Movie with title '{data[PROPERTY_TITLE]}' already exists.")
            existing_movie = Movie.query_movie_by_id(movie_id)
            if existing_movie is None:
                new_movie = Movie(
                    data[PROPERTY_TITLE], data[PROPERTY_DESCRIPTION], data[PROPERTY_RELEASE_YEAR],
                    data[PROPERTY_DURATION_MINUTES], data[PROPERTY_RATING]) \
                    .create()
                response = movie_schema.dump(new_movie)
                code = 201
            else:
                updated_movie = existing_movie.update(
                    data[PROPERTY_TITLE], data[PROPERTY_DESCRIPTION], data[PROPERTY_RELEASE_YEAR],
                    data[PROPERTY_DURATION_MINUTES], data[PROPERTY_RATING])
                response = movie_schema.dump(updated_movie)
                code = 200
            return response, code
        except ValidationError as err:
            abort(400, err.messages)


class MovieListResource(Resource):
    def post(self):
        try:
            data = movie_schema.load(request.get_json())
            if Movie.query_movie_by_title(data[PROPERTY_TITLE]):
                abort(422, f"Movie with title {data[PROPERTY_TITLE]} already exists.")
            new_movie = Movie(
                data[PROPERTY_TITLE], data[PROPERTY_DESCRIPTION], data[PROPERTY_RELEASE_YEAR],
                data[PROPERTY_DURATION_MINUTES], data[PROPERTY_RATING]) \
                .create()
            response = movie_schema.dump(new_movie)
            return response, 201
        except ValidationError as err:
            abort(400, err.messages)

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument(PROPERTY_TITLE, type=str, location='args')
        args = parser.parse_args()
        title = args[PROPERTY_TITLE]
        if title is not None:
            movie = Movie.query_movie_by_title(title)
            if movie is None:
                abort(404, f"Could not find movie with the title '{title}'")
            response = movie_schema.dump(movie)
        else:
            movies = Movie.query_movies()
            response = movies_schema.dump(movies)
        return response, 200


class MovieLikesResource(Resource):
    def get(self, movie_id):
        movie = get_movie_from_db(movie_id)
        response = likes_schema.dump(movie)
        return response, 200

    def post(self, movie_id):
        movie = get_movie_from_db(movie_id)
        movie.update(likes=movie.likes + 1)
        return '', 204

    def delete(self, movie_id):
        movie = get_movie_from_db(movie_id)
        if movie.likes > 0:
            movie.update(likes=movie.likes - 1)
        return '', 204


class MovieDislikesResource(Resource):
    def get(self, movie_id):
        movie = get_movie_from_db(movie_id)
        response = dislikes_schema.dump(movie)
        return response, 200

    def post(self, movie_id):
        movie = get_movie_from_db(movie_id)
        movie.update(dislikes=movie.dislikes + 1)
        return '', 204

    def delete(self, movie_id):
        movie = get_movie_from_db(movie_id)
        if movie.dislikes > 0:
            movie.update(dislikes=movie.dislikes - 1)
        return '', 204
