import email
import json
from typing import NamedTuple, Optional
import pytest
import pytest_mock
from routes import watchlists
from src.utils.services import secrets
from utils import db_models


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

TEST_WATCHLIST1 = WatchlistData(
    id=200001,
    title='Test Watchlist 1',
    description='Description for Watchlist 1',
    items=[1000, 1001, 1002, 1003],
    watched_items=[1000, 1002],
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
