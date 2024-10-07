import cachetools
from google.cloud import secretmanager

from src.utils import constants

ONE_HOUR_IN_SECONDS = 60 * 60
SECRET_CACHE = cachetools.TTLCache(maxsize=16384, ttl=ONE_HOUR_IN_SECONDS)


@cachetools.cached(cache=SECRET_CACHE)
def get_secret(secret_id: str, secret_version: str = 'latest') -> str:
  client = secretmanager.SecretManagerServiceClient()
  name = client.secret_version_path(constants.GAE_PROJECT, secret_id,
                                    secret_version)
  response = client.access_secret_version(name=name)
  return response.payload.data.decode('UTF-8')
