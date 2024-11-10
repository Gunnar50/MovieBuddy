import email
from http import HTTPStatus

import flask

from utils import api
from utils import constants
from utils import fixtures


class TestLogin:

  URL = '/user/api/auth/login'

  def test_valid_login(
      self,
      mock_verify_token: dict,
      test_client: fixtures.TestClientWrapper,
  ):
    payload = api.LoginRequest(access_token=fixtures.TEST_ACCESS_TOKEN)
    expected_response = api.UserDetails(
        user_id=fixtures.TEST_USER1.id,
        email=fixtures.TEST_USER1.email,
        name=fixtures.TEST_USER1.name,
    )

    response = test_client.post(self.URL, data=payload.model_dump(mode='json'))

    fixtures.assert_response_object(response, expected_response)
    assert (flask.session.get(
        constants.SESSION_USER_ID) == fixtures.TEST_USER1.id)

  def test_invalid_login_raises(
      self,
      mock_verify_token: dict,
      test_client: fixtures.TestClientWrapper,
  ):
    payload = api.LoginRequest(access_token='invalid-token')

    response = test_client.post(self.URL, data=payload.model_dump(mode='json'))

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert constants.SESSION_USER_ID not in flask.session


class TestLogout:

  URL = '/user/api/auth/logout'

  def test_not_logged_in_raises(
      self,
      test_client: fixtures.TestClientWrapper,
  ):
    response = test_client.post(self.URL)

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert constants.SESSION_USER_ID not in flask.session

  def test_logout_removes_session(
      self,
      test_client: fixtures.TestClientWrapper,
  ):
    test_client.login()
    response = test_client.post(self.URL)

    assert response.status_code == HTTPStatus.OK
    assert constants.SESSION_USER_ID not in flask.session
