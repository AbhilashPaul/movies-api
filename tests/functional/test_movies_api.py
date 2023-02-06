import json
from datetime import date

from api.constants import PATH_MOVIE_LIST

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

fake_movie_with_invalid_release_year = {
    "title": "Another Fake Movie Title",
    "description": "Another Fake Movie Description",
    "release_year": date.today().year + 1,
    "duration_minutes": 102,
    "rating": 5
}

fake_movie_with_invalid_title = {
    "title": "fake long title: Lorem ipsum dolor sit amet, consectetur adipiscing elit, "
             "sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
    "description": "Another Fake Movie Description",
    "release_year": 2020,
    "duration_minutes": 102,
    "rating": 5
}

fake_movie_with_invalid_description = {
    "title": "Fake Title",
    "description": '''fake long description: Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod 
    tempor incididunt ut labore et dolore magna aliqua. Tristique risus nec feugiat in fermentum posuere urna nec 
    tincidunt. Odio morbi quis commodo odio aenean sed adipiscing diam. Rhoncus dolor purus non enim praesent elementum 
    facilisis leo vel. Habitant morbi tristique senectus et netus et malesuada. Quisque id diam vel quam. Non curabitur 
    gravida arcu ac. Ultricies mi quis hendrerit dolor.''',
    "release_year": 2000,
    "duration_minutes": 132,
    "rating": 9
}

fake_movie_with_invalid_duration_minutes = {
    "title": "Fake Title",
    "description": "Fake Description",
    "release_year": 2000,
    "duration_minutes": "a",
    "rating": 9
}

fake_movie_with_invalid_rating = {
    "title": "Fake Title",
    "description": "Fake Description",
    "release_year": 2000,
    "duration_minutes": 97,
    "rating": "a"
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


def test_create_movie_returns_422_given_movie_with_same_title_already_exist(client):
    # Given
    client.post(PATH_MOVIE_LIST, data=json.dumps(fake_movie_1), content_type='application/json')

    # When
    response = client.post(PATH_MOVIE_LIST, data=json.dumps(fake_movie_1), content_type='application/json')

    # Then
    assert response.status_code == 422
    assert response.get_json() == {'message': "Movie with title 'Fake Title' already exists."}


def test_create_movie_returns_400_given_invalid_release_year(client):
    response = client.post(PATH_MOVIE_LIST,
                           data=json.dumps(fake_movie_with_invalid_release_year),
                           content_type='application/json')
    assert response.status_code == 400
    assert response.get_json() == {
        'message': {'release_year': ['Year of release must be less than or equal to current year.']}}


def test_create_movie_returns_400_given_invalid_title(client):
    response = client.post(PATH_MOVIE_LIST,
                           data=json.dumps(fake_movie_with_invalid_title),
                           content_type='application/json')
    assert response.status_code == 400
    assert response.get_json() == {'message': {'title': ['Text input must be less than 100 characters.']}}


def test_create_movie_returns_400_given_invalid_description(client):
    response = client.post(PATH_MOVIE_LIST,
                           data=json.dumps(fake_movie_with_invalid_description),
                           content_type='application/json')
    assert response.status_code == 400
    assert response.get_json() == {'message': {'description': ['Text input must be less than 300 characters.']}}


def test_create_movie_returns_400_given_invalid_duration_minutes(client):
    response = client.post(PATH_MOVIE_LIST,
                           data=json.dumps(fake_movie_with_invalid_duration_minutes),
                           content_type='application/json')
    assert response.status_code == 400
    assert response.get_json() == {'message': {'duration_minutes': ['Not a valid integer.']}}


def test_create_movie_returns_400_given_invalid_rating(client):
    response = client.post(PATH_MOVIE_LIST,
                           data=json.dumps(fake_movie_with_invalid_rating),
                           content_type='application/json')
    assert response.status_code == 400
    assert response.get_json() == {'message': {'rating': ['Not a valid number.']}}


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


def test_update_movie_returns_400_given_invalid_release_year(client):
    # Given
    create_movie_response = client.post(PATH_MOVIE_LIST, data=json.dumps(fake_movie_1), content_type='application/json')
    movie_id = create_movie_response.get_json()['id']

    # When
    response = client.put(f"{PATH_MOVIE_LIST}/{movie_id}",
                          data=json.dumps(fake_movie_with_invalid_release_year),
                          content_type='application/json')

    # Then
    assert response.status_code == 400
    assert response.get_json() == {
        'message': {'release_year': ['Year of release must be less than or equal to current year.']}
    }


def test_update_movie_returns_409_given_movie_with_same_title_already_exist(client):
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


def test_update_movie_creates_new_record_given_specified_movie_does_not_exist(client):
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


def test_get_movie_by_id_returns_404_given_movie_does_not_exist(client):
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


def test_search_movie_by_title_returns_404_given_movie_does_not_exist(client):
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


def test_delete_movie_returns_404_given_movie_does_not_exist(client):
    response = client.delete(f"{PATH_MOVIE_LIST}/1")
    assert response.status_code == 404
    assert response.get_json() == {'message': 'Could not find movie with id 1'}


def test_like_movie(client):
    # Given
    create_movie_response = client.post(PATH_MOVIE_LIST, data=json.dumps(fake_movie_1), content_type='application/json')
    created_movie = create_movie_response.get_json()
    movie_id = created_movie['id']
    likes = created_movie['likes']

    # When
    response = client.post(f"{PATH_MOVIE_LIST}/{movie_id}/likes")

    # Then
    assert response.status_code == 204
    get_response = client.get(f"{PATH_MOVIE_LIST}/{movie_id}/likes")
    assert get_response.get_json()['likes'] == likes + 1


def test_get_like_count(client):
    # Given
    create_movie_response = client.post(PATH_MOVIE_LIST, data=json.dumps(fake_movie_1), content_type='application/json')
    created_movie = create_movie_response.get_json()
    movie_id = created_movie['id']
    client.post(f"{PATH_MOVIE_LIST}/{movie_id}/likes")
    client.post(f"{PATH_MOVIE_LIST}/{movie_id}/likes")

    # When
    response = client.get(f"{PATH_MOVIE_LIST}/{movie_id}/likes")

    # Then
    assert response.status_code == 200
    assert response.get_json()['likes'] == 2


def test_delete_like_from_a_movie(client):
    # Given
    create_movie_response = client.post(PATH_MOVIE_LIST, data=json.dumps(fake_movie_1), content_type='application/json')
    created_movie = create_movie_response.get_json()
    movie_id = created_movie['id']
    client.post(f"{PATH_MOVIE_LIST}/{movie_id}/likes")
    likes = created_movie['likes'] + 1

    # When
    delete_response = client.delete(f"{PATH_MOVIE_LIST}/{movie_id}/likes")

    # Then
    assert delete_response.status_code == 204
    get_response = client.get(f"{PATH_MOVIE_LIST}/{movie_id}/likes")
    assert get_response.get_json()['likes'] == likes - 1


def test_delete_like_does_not_remove_like_given_movie_was_never_liked(client):
    # Given
    create_movie_response = client.post(PATH_MOVIE_LIST, data=json.dumps(fake_movie_1), content_type='application/json')
    created_movie = create_movie_response.get_json()
    movie_id = created_movie['id']

    # When
    delete_response = client.delete(f"{PATH_MOVIE_LIST}/{movie_id}/likes")

    # Then
    assert delete_response.status_code == 204
    get_response = client.get(f"{PATH_MOVIE_LIST}/{movie_id}/likes")
    assert get_response.get_json()['likes'] == 0


def test_dislike_movie(client):
    # Given
    create_movie_response = client.post(PATH_MOVIE_LIST, data=json.dumps(fake_movie_1), content_type='application/json')
    created_movie = create_movie_response.get_json()
    movie_id = created_movie['id']
    dislikes = created_movie['dislikes']

    # When
    response = client.post(f"{PATH_MOVIE_LIST}/{movie_id}/dislikes")

    # Then
    assert response.status_code == 204
    get_response = client.get(f"{PATH_MOVIE_LIST}/{movie_id}")
    assert get_response.get_json()['dislikes'] == dislikes + 1


def test_get_dislike_count(client):
    # Given
    create_movie_response = client.post(PATH_MOVIE_LIST, data=json.dumps(fake_movie_1), content_type='application/json')
    created_movie = create_movie_response.get_json()
    movie_id = created_movie['id']
    client.post(f"{PATH_MOVIE_LIST}/{movie_id}/dislikes")
    client.post(f"{PATH_MOVIE_LIST}/{movie_id}/dislikes")

    # When
    response = client.get(f"{PATH_MOVIE_LIST}/{movie_id}/dislikes")

    # Then
    assert response.status_code == 200
    assert response.get_json()['dislikes'] == 2


def test_delete_dislike(client):
    # Given
    create_movie_response = client.post(PATH_MOVIE_LIST, data=json.dumps(fake_movie_1), content_type='application/json')
    created_movie = create_movie_response.get_json()
    movie_id = created_movie['id']
    client.post(f"{PATH_MOVIE_LIST}/{movie_id}/dislikes")
    dislikes = created_movie['dislikes'] + 1

    # When
    delete_response = client.delete(f"{PATH_MOVIE_LIST}/{movie_id}/dislikes")

    # Then
    assert delete_response.status_code == 204
    get_response = client.get(f"{PATH_MOVIE_LIST}/{movie_id}/dislikes")
    assert get_response.get_json()['dislikes'] == dislikes - 1


def test_delete_dislike_does_not_remove_dislike_given_movie_was_never_disliked(client):
    # Given
    create_movie_response = client.post(PATH_MOVIE_LIST, data=json.dumps(fake_movie_1), content_type='application/json')
    created_movie = create_movie_response.get_json()
    movie_id = created_movie['id']

    # When
    delete_response = client.delete(f"{PATH_MOVIE_LIST}/{movie_id}/dislikes")

    # Then
    assert delete_response.status_code == 204
    get_response = client.get(f"{PATH_MOVIE_LIST}/{movie_id}/dislikes")
    assert get_response.get_json()['dislikes'] == 0
