from api.constants import PATH_MOVIE_LIST, PATH_MOVIE
import json

fake_movie_1 = {
    "title": "Fake Title",
    "description": "Fake Description",
    "release_year": 2000,
    "duration_minutes": 132,
    "rating": 9
}


fake_movie_2 = {
    "title": "Another Fake Movie Title",
    "description": "Another Fake Movie Description",
    "release_year": 2020,
    "duration_minutes": 102,
    "rating": 5
}


def test_create_movie(client):
    # When
    response = client.post(PATH_MOVIE_LIST, data=json.dumps(fake_movie_1), content_type='application/json')

    # Then
    response_json = response.get_json()
    assert response.status_code == 201
    assert response_json["id"] == 1
    assert response_json["title"] == fake_movie_1["title"]
    assert response_json["description"] == fake_movie_1["description"]
    assert response_json["release_year"] == fake_movie_1["release_year"]
    assert response_json["duration_minutes"] == fake_movie_1["duration_minutes"]
    assert response_json["rating"] == fake_movie_1["rating"]
    assert response_json["likes"] == 0
    assert response_json["dislikes"] == 0


def test_update_movie(client):
    # Given
    create_movie_response = client.post(PATH_MOVIE_LIST, data=json.dumps(fake_movie_1), content_type='application/json')
    movie_id = create_movie_response.get_json()['id']

    # When
    response = client.put(f"{PATH_MOVIE_LIST}/{movie_id}",
                          data=json.dumps(fake_movie_2),
                          content_type='application/json')

    # Then
    response_json = response.get_json()
    assert response.status_code == 200
    assert response_json["id"] == movie_id
    assert response_json["title"] == fake_movie_2["title"]
    assert response_json["description"] == fake_movie_2["description"]
    assert response_json["release_year"] == fake_movie_2["release_year"]
    assert response_json["duration_minutes"] == fake_movie_2["duration_minutes"]
    assert response_json["rating"] == fake_movie_2["rating"]
    assert response_json["likes"] == 0
    assert response_json["dislikes"] == 0


def test_update_movie_returns_409_when_movie_with_same_title_already_exist(client):
    # Given
    client.post(PATH_MOVIE_LIST, data=json.dumps(fake_movie_1), content_type='application/json')
    create_movie_response = client.post(PATH_MOVIE_LIST, data=json.dumps(fake_movie_2), content_type='application/json')
    movie_id = create_movie_response.get_json()['id']

    # When
    response = client.put(f"{PATH_MOVIE_LIST}/{movie_id}",
                          data=json.dumps(fake_movie_1),
                          content_type='application/json')

    # Then
    assert response.status_code == 409
    assert response.get_json() == {"message": "Movie with title 'Fake Title' already exists."}


def test_update_movie_creates_new_record_when_specified_movie_does_not_exist(client):
    # Given
    fake_movie_update = {
        "title": "Updated Fake Title",
        "description": "Updated Fake Description",
        "release_year": 2020,
        "duration_minutes": 102,
        "rating": 5
    }

    # When
    response = client.put(f"{PATH_MOVIE_LIST}/1",
                          data=json.dumps(fake_movie_update),
                          content_type='application/json')
    # Then
    response_json = response.get_json()
    assert response.status_code == 201
    assert response_json["id"]
    assert response_json["title"] == fake_movie_update["title"]
    assert response_json["description"] == fake_movie_update["description"]
    assert response_json["release_year"] == fake_movie_update["release_year"]
    assert response_json["duration_minutes"] == fake_movie_update["duration_minutes"]
    assert response_json["rating"] == fake_movie_update["rating"]
    assert response_json["likes"] == 0
    assert response_json["dislikes"] == 0


def test_get_movie_by_id(client):
    # Given
    create_movie_response = client.post(PATH_MOVIE_LIST, data=json.dumps(fake_movie_1), content_type='application/json')
    movie_id = create_movie_response.get_json()['id']

    # When
    response = client.get(f"{PATH_MOVIE_LIST}/{movie_id}")

    # Then
    response_json = response.get_json()
    assert response.status_code == 200
    assert response_json["id"] == 1
    assert response_json["title"] == fake_movie_1["title"]
    assert response_json["description"] == fake_movie_1["description"]
    assert response_json["release_year"] == fake_movie_1["release_year"]
    assert response_json["duration_minutes"] == fake_movie_1["duration_minutes"]
    assert response_json["rating"] == fake_movie_1["rating"]
    assert response_json["likes"] == 0
    assert response_json["dislikes"] == 0


def test_get_movie_by_id_returns_404_when_movie_does_not_exist(client):
    response = client.get(f"{PATH_MOVIE_LIST}/1")
    assert response.status_code == 404
    assert response.get_json() == {'message': 'Could not find movie with id 1'}


def test_get_all_movies(client):
    client.post(PATH_MOVIE_LIST, data=json.dumps(fake_movie_1), content_type='application/json')
    response = client.get(PATH_MOVIE_LIST)
    response_json = response.get_json()
    assert response.status_code == 200
    assert response_json == [
        {
            'id': 1, 'title': 'Fake Title', 'description': 'Fake Description', 'duration_minutes': 132,
            'rating': 9.0, 'release_year': 2000, 'likes': 0, 'dislikes': 0
        }
    ]


def test_search_movie_by_title(client):
    # Given
    client.post(PATH_MOVIE_LIST, data=json.dumps(fake_movie_1), content_type='application/json')

    # When
    response = client.get(f"{PATH_MOVIE_LIST}?title=Fake%20Title")

    # Then
    response_json = response.get_json()
    assert response.status_code == 200
    assert response_json["id"] == 1
    assert response_json["title"] == fake_movie_1["title"]
    assert response_json["description"] == fake_movie_1["description"]
    assert response_json["release_year"] == fake_movie_1["release_year"]
    assert response_json["duration_minutes"] == fake_movie_1["duration_minutes"]
    assert response_json["rating"] == fake_movie_1["rating"]
    assert response_json["likes"] == 0
    assert response_json["dislikes"] == 0


def test_search_movie_by_title_returns_404_when_movie_does_not_exist(client):
    response = client.get(f"{PATH_MOVIE_LIST}?title=Fake%20Title")
    assert response.status_code == 404
    assert response.get_json() == {"message": "Could not find movie with the title 'Fake Title'"}


def test_delete_movie(client):
    # Given
    create_movie_response = client.post(PATH_MOVIE_LIST, data=json.dumps(fake_movie_1), content_type='application/json')
    movie_id = create_movie_response.get_json()['id']

    # When
    delete_response = client.delete(f"{PATH_MOVIE_LIST}/{movie_id}")

    # Then
    assert delete_response.status_code == 204
    response = client.get(f"{PATH_MOVIE_LIST}/{movie_id}")
    assert response.status_code == 404


def test_delete_movie_returns_404_when_movie_does_not_exist(client):
    response = client.delete(f"{PATH_MOVIE_LIST}/1")
    assert response.status_code == 404
    assert response.get_json() == {'message': 'Could not find movie with id 1'}
