import os

import pytest

from app import create_app, alembic


@pytest.fixture()
def app(mocker):
    mocker.patch.dict(os.environ, {"APP_CONFIG": "test"})
    app = create_app()
    with app.app_context():
        alembic.upgrade()
    yield app
    os.remove(os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), "test_movies.db"))


@pytest.fixture()
def client(app):
    with app.app_context():
        return app.test_client()
