import os
import tempfile

import pytest
from www_eaveson_co_uk import create_app
from www_eaveson_co_uk.database import db


@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'DATABASE': "file:memory:"
    })

    with app.app_context():
        db.create_all()
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()