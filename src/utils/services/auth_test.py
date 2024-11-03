from http import HTTPStatus
import re
from typing import Callable, Generator
from unittest import mock

import flask
from google.appengine.ext import testbed
import pytest

from utils import constants
from utils import fixtures
from utils.services import auth

TEST_URL_USER = 'http://localhost:8080/test/user/'

TEST_URL_LIST_NONE = f'/test/requires_list/{fixtures.TEST_WATCHLIST1.id}/none/'


@pytest.fixture()
def test_auth_client() -> Generator[fixtures.TestClientWrapper, None, None]:
  import main
  app = main.create_app()

  def add_route(url: str, decorator: Callable) -> None:
    func = lambda **kwargs: 'ok'
    func.__name__ = re.sub(r'[/<:>]+', '', url)
    app.route(url)(decorator(func))

  add_route('/test/user/', auth.requires_user)
  add_route('/test/requires_list/<int:watchlist_id>/none/',
            auth.requires_watchlist())

  with app.test_client() as test_client:
    client_wrapper = fixtures.TestClientWrapper(test_client)

    yield client_wrapper


class TestAuthDecorators:

  @pytest.mark.parametrize('url, expected_status_code', [
      (TEST_URL_USER, HTTPStatus.OK),
      (TEST_URL_LIST_NONE, HTTPStatus.FORBIDDEN),
  ])
  def test_user_nothing_exists(
      self,
      url: str,
      expected_status_code: int,
      test_auth_client: fixtures.TestClientWrapper,
  ):
    test_auth_client.login()
    fixtures.TEST_WATCHLIST1.create()
    response = test_auth_client.get(url)

    assert response.status_code == expected_status_code
