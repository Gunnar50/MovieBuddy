from http import HTTPStatus
import re
from typing import Callable, Generator
import flask

import pytest

from utils import fixtures
from utils.services import auth

TEST_URL_USER = 'http://localhost:8080/test/user/'

TEST_URL_LIST_NONE = f'/test/requires_list/{fixtures.TEST_WATCHLIST1.id}/none/'


@pytest.fixture()
def test_auth_client(
    test_settings: None) -> Generator[flask.testing.FlaskClient, None, None]:
  import main
  app = main.create_app()

  def add_route(url: str, decorator: Callable) -> None:
    func = lambda **kwargs: 'ok'
    func.__name__ = re.sub(r'[/<:>]+', '', url)
    app.route(url)(decorator(func))

  add_route('/test/user/', auth.requires_user)
  add_route('/test/requires_list/<int:list_id>/none/',
            auth.requires_watchlist(user_types=()))

  with app.test_client() as test_client:
    yield test_client


class TestAuthDecorators:

  @pytest.mark.parametrize('url, expected_status_code', [
      (TEST_URL_USER, HTTPStatus.OK),
      (TEST_URL_LIST_NONE, HTTPStatus.NOT_FOUND),
  ])
  def test_user_nothing_exists(
      self,
      url: str,
      expected_status_code: int,
      test_auth_client: flask.testing.FlaskClient,
  ):
    response = test_auth_client.get(url)

    assert response.status_code == expected_status_code
