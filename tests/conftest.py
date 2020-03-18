import pytest
from library import create_app
from library.cache import get_cache


@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'CACHE_HOST': 'localhost',
        'CACHE_PORT': 6379,
        'CACHE_DB': 9,
    })

    with app.app_context():
        get_cache()

    yield app


@pytest.fixture
def client(app):
    return app.test_client()
