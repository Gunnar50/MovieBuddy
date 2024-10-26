from http import HTTPStatus
import json
from typing import Generator, NamedTuple, Optional
from unittest import mock

import flask
from google.appengine.api import memcache
from google.appengine.ext import ndb
from google.appengine.ext import testbed
from google.oauth2 import id_token
import pydantic
import pytest
import pytest_mock

from routes import watchlists
from utils.services import secrets
from utils import constants, db_models


@pytest.fixture(autouse=True)
def mock_oauth_config(mocker: pytest_mock.MockerFixture) -> None:
  mock_get_secret = mocker.patch.object(secrets, 'get_secret')
  mock_get_secret.return_value = json.dumps({
      'web': {
          'client_id': 'test_client_id',
          'project_id': 'testing',
          'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
          'token_uri': 'https://oauth2.googleapis.com/token',
          'auth_provider_x509_cert_url': 'https://www.googleapis.com/oauth2/v1/certs',
          'client_secret': 'abc123',
          'javascript_origins': ['http://localhost:8080'],
      }
  })


class UserData(NamedTuple):
  id: int
  email: str
  name: str

  def create_owner(self,
                   watchlist: db_models.Watchlist) -> db_models.WatchlistOwner:
    owner = db_models.WatchlistOwner(
        name=self.name,
        email=self.email,
        watchlist=watchlist.key,
    ).put()
    return owner

  def create_member(
      self, watchlist: db_models.Watchlist) -> db_models.WatchlistMember:
    member = db_models.WatchlistMember(
        name=self.name,
        email=self.email,
        watchlist=watchlist.key,
    ).put()
    return member


class WatchlistData(NamedTuple):
  id: int
  title: str
  description: str = ''
  items: Optional[list[int]] = None
  watched_items: Optional[list[int]] = None

  def create(self) -> db_models.Watchlist:
    watchlist = db_models.Watchlist(
        id=self.id,
        title=self.title,
        description=self.description,
        items=self.items,
        watched_items=self.watched_items,
    ).put()
    return watchlist


TEST_USER1 = UserData(id=100001, email='user_1@example.com', name='User 1')
TEST_USER2 = UserData(id=100002, email='user_2@example.com', name='User 2')
TEST_USER3 = UserData(id=100003, email='user_3@example.com', name='User 3')
TEST_USER4 = UserData(id=100004, email='user_4@example.com', name='User 4')

TEST_ITEM_ID1 = 1001
TEST_ITEM_ID2 = 1002
TEST_ITEM_ID3 = 1003
TEST_ITEM_ID4 = 1004

TEST_WATCHLIST1 = WatchlistData(
    id=200001,
    title='Test Watchlist 1',
    description='Description for Watchlist 1',
    items=[TEST_ITEM_ID1, TEST_ITEM_ID2, TEST_ITEM_ID3, TEST_ITEM_ID4],
    watched_items=[TEST_ITEM_ID1, TEST_ITEM_ID3],
)

TEST_WATCHLIST2 = WatchlistData(
    id=200002,
    title='Test Watchlist 2',
)

TEST_WATCHLIST3 = WatchlistData(
    id=200003,
    title='Test Watchlist 3',
)


def create_test_lists() -> None:
  watchlist1 = TEST_WATCHLIST1.create()
  TEST_USER1.create_owner(watchlist1)
  TEST_USER2.create_member(watchlist1)
  TEST_USER3.create_member(watchlist1)

  watchlist2 = TEST_WATCHLIST2.create()
  TEST_USER2.create_owner(watchlist2)
  TEST_USER1.create_member(watchlist2)


@pytest.fixture(autouse=True)
def mock_ndb() -> Generator:
  _testbed = testbed.Testbed()
  _testbed.activate()
  _testbed.init_datastore_v3_stub()
  _testbed.init_memcache_stub()
  yield
  _testbed.deactivate()


@pytest.fixture
def test_client() -> Generator[flask.testing.FlaskClient, None, None]:
  import main
  with main.app.test_client() as test_client:
    yield test_client


@pytest.fixture
def test_login_client(
    test_client: flask.testing.FlaskClient) -> flask.testing.FlaskClient:
  # Simulate login a user by setting session data
  with test_client.session_transaction() as session:
    session[constants.SESSION_USER_ID] = TEST_USER1.id
  return test_client
