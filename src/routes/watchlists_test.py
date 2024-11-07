from http import HTTPStatus

import flask

from utils import api
from utils import fixtures


class TestCreateWatchlist:

  URL = '/user/api/watchlist/create/'

  def test_create_watchlist(
      self,
      test_client: fixtures.TestClientWrapper,
  ):
    test_client.login()
    payload = api.WatchlistCreateRequest(
        title=fixtures.TEST_WATCHLIST1.title,
        description=fixtures.TEST_WATCHLIST1.description,
        members=[fixtures.TEST_USER2.email, fixtures.TEST_USER3.email],
    )

    expected_response = api.WatchlistResponse(
        watchlist=api.WatchlistDetail(
            title=fixtures.TEST_WATCHLIST1.title,
            description=fixtures.TEST_WATCHLIST1.description,
        ),
        owner=api.MemberDetail(email=fixtures.TEST_USER1.email,
                               member_type=api.MemberType.OWNER),
        members=[
            api.MemberDetail(email=fixtures.TEST_USER2.email,
                             member_type=api.MemberType.MEMBER),
            api.MemberDetail(email=fixtures.TEST_USER3.email,
                             member_type=api.MemberType.MEMBER)
        ],
    )

    response = test_client.post(self.URL, data=payload.model_dump(mode='json'))

    fixtures.assert_response_object(response, expected_response)


class TestListWatchlist:

  URL = f'/user/api/watchlist/{fixtures.TEST_WATCHLIST1.id}/'

  def test_owner_list(
      self,
      test_client: fixtures.TestClientWrapper,
  ):
    watchlist = fixtures.TEST_WATCHLIST1.create()
    fixtures.TEST_USER1.create_owner(watchlist)
    test_client.login()

    expected_response = api.WatchlistResponse(
        watchlist=api.WatchlistDetail(
            title=fixtures.TEST_WATCHLIST1.title,
            description=fixtures.TEST_WATCHLIST1.description,
        ),
        owner=api.MemberDetail(email=fixtures.TEST_USER1.email,
                               member_type=api.MemberType.OWNER),
        members=[],
    )

    response = test_client.get(self.URL)
    fixtures.assert_response_object(response, expected_response)

  def test_member_list(
      self,
      test_client: fixtures.TestClientWrapper,
  ):
    watchlist = fixtures.TEST_WATCHLIST1.create()
    fixtures.TEST_USER2.create_owner(watchlist)
    fixtures.TEST_USER1.create_member(watchlist)
    test_client.login()

    expected_response = api.WatchlistResponse(
        watchlist=api.WatchlistDetail(
            title=fixtures.TEST_WATCHLIST1.title,
            description=fixtures.TEST_WATCHLIST1.description,
        ),
        owner=api.MemberDetail(email=fixtures.TEST_USER2.email,
                               member_type=api.MemberType.OWNER),
        members=[
            api.MemberDetail(email=fixtures.TEST_USER1.email,
                             member_type=api.MemberType.MEMBER)
        ],
    )

    response = test_client.get(self.URL)
    fixtures.assert_response_object(response, expected_response)

  def test_owner_other_list(
      self,
      test_client: fixtures.TestClientWrapper,
  ):
    fixtures.TEST_WATCHLIST1.create()
    watchlist2 = fixtures.TEST_WATCHLIST2.create()
    fixtures.TEST_USER1.create_owner(watchlist2)
    test_client.login()

    response = test_client.get(self.URL)
    assert response.status_code == HTTPStatus.FORBIDDEN

  def test_member_other_list(
      self,
      test_client: fixtures.TestClientWrapper,
  ):
    fixtures.TEST_WATCHLIST1.create()
    watchlist2 = fixtures.TEST_WATCHLIST2.create()
    fixtures.TEST_USER1.create_member(watchlist2)
    test_client.login()

    response = test_client.get(self.URL)
    assert response.status_code == HTTPStatus.FORBIDDEN
