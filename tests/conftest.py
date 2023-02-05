import os

import pytest

from app import create_app, alembic


@pytest.fixture()
def app(mocker):
    mocker.patch.dict(os.environ, {"APP_CONFIG": "dev"})
    app = create_app()
    with app.app_context():
        alembic.upgrade()
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()
