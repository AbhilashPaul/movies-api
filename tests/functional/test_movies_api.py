from api.constants import PATH_MOVIE_LIST


def test_get_all_movies(client):
    response = client.get(PATH_MOVIE_LIST)
    response_json = response.get_json()
    assert response.status_code == 200
    assert response_json == []


def test_create_movie(client):
    response = client.post(PATH_MOVIE_LIST, data={
        "title": "Fake Title",
        "description": "Fake Description",
        "release_year": "2000",
        "duration_minutes": "132",
        "rating": "9"
    })
    assert response.status_code == 200
