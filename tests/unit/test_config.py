from api.config import BaseConfig, DevelopmentConfig, ProductionConfig, TestConfig


def test_base_config():
    config = BaseConfig()
    assert config.SQLALCHEMY_TRACK_MODIFICATIONS is False
    assert config.TESTING is False


def test_dev_config():
    config = DevelopmentConfig()
    assert 'movies-api/dev_movies.db' in config.SQLALCHEMY_DATABASE_URI
    assert config.SQLALCHEMY_TRACK_MODIFICATIONS is False
    assert config.TESTING is False


def test_prod_config():
    config = ProductionConfig()
    assert 'movies-api/prod_movies.db' in config.SQLALCHEMY_DATABASE_URI
    assert config.SQLALCHEMY_TRACK_MODIFICATIONS is False
    assert config.TESTING is False


def test_test_config():
    config = TestConfig()
    assert 'movies-api/test_movies.db' in config.SQLALCHEMY_DATABASE_URI
    assert config.SQLALCHEMY_TRACK_MODIFICATIONS is False
    assert config.TESTING
