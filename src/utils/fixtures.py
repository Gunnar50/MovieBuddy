import json
import pytest
import pytest_mock
from src.utils.services import secrets


@pytest.fixture(autouse=True)
def mock_oauth_config(mocker: pytest_mock.MockerFixture) -> None:
  mock_get_secret = mocker.patch.object(secrets, 'get_secret')
  mock_get_secret.return_value = json.dumps({
      'web': {
          'client_id': 'test_client_id',
          'project_id': 'gweb-marketing-expert-testing',
          'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
          'token_uri': 'https://oauth2.googleapis.com/token',
          'auth_provider_x509_cert_url': 'https://www.googleapis.com/oauth2/v1/certs',
          'client_secret': 'abc123',
          'javascript_origins': ['http://localhost:8080'],
      }
  })
