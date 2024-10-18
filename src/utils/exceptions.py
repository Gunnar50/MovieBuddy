from http import HTTPStatus
from werkzeug import exceptions


class EntityNotFoundException(exceptions.HTTPException):
  code = HTTPStatus.NOT_FOUND
  description = 'Entity not found.'


class InvalidParameterException(exceptions.HTTPException):
  code = HTTPStatus.BAD_REQUEST
  description = 'Invalid parameters.'


class NotAuthenticatedException(exceptions.HTTPException):
  code = HTTPStatus.UNAUTHORIZED
  description = 'User is not autheticated.'


class EntityNotInListException(exceptions.HTTPException):
  code = HTTPStatus.CONFLICT
  description = 'Entity not found in list'


class InvalidAuthenticationException(exceptions.HTTPException):
  code = HTTPStatus.FORBIDDEN
  description = 'Failed validation.'


class NoAccessException(exceptions.HTTPException):
  """Raised when the user does not have access to this resource."""
  code = HTTPStatus.FORBIDDEN
  description = 'No access to this resource.'
