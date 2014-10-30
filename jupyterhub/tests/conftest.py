"""py.test fixtures"""

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

import logging

from pytest import fixture
from tornado import ioloop

from .. import orm
from ..utils import getuser_unicode

from .mocking import MockHubApp


# global db session object
_db = None

@fixture
def db():
    """Get a db session"""
    global _db
    if _db is None:
        _db = orm.new_session_factory('sqlite:///:memory:', echo=True)()
        user = orm.User(
            name=getuser_unicode(),
            server=orm.Server(),
        )
        hub = orm.Hub(
            server=orm.Server(),
        )
        _db.add(user)
        _db.add(hub)
        _db.commit()
    return _db


@fixture
def io_loop():
    """Get the current IOLoop"""
    loop = ioloop.IOLoop()
    loop.make_current()
    return loop


@fixture(scope='module')
def app(request):
    app = MockHubApp.instance(log_level=logging.DEBUG)
    app.start([])
    request.addfinalizer(app.stop)
    return app
