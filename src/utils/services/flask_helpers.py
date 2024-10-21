import functools
import json
import logging
from typing import Any, Callable, Type, TypeVar

import flask
import pydantic

from utils import exceptions

LOGGER = logging.getLogger(__name__)

PydanticModelType = TypeVar('PydanticModelType', bound=pydantic.BaseModel)


def json_handler(func: Callable[..., Any]):
  """This lets us return Pydantic models from flask routes"""

  @functools.wraps(func)
  def inner(*args, **kwargs):
    try:
      result = func(*args, **kwargs)
    except exceptions.HttpExceptionWithBody as ex:
      response = flask.jsonify(ex.body.model_dump(mode='json'))
      response.status_code = ex.code
      return response
    if isinstance(result, pydantic.BaseModel):
      return flask.jsonify(result.model_dump(mode='json'))
    # Check if this is a model with a status code
    elif (isinstance(result, tuple) and len(result) == 2 and
          isinstance(result[0], pydantic.BaseModel) and
          isinstance(result[1], int)):
      model, status = result
      response = flask.jsonify(model.model_dump(mode='json'))
      response.status_code = status
      return response
    elif result is None:
      # Flask expects us to always return a value, so just send an empty dict
      return flask.jsonify({})
    else:
      return result

  return inner


def get_parameters(
    ParametersClass: Type[PydanticModelType],
    json_wrapped: bool = False,
) -> tuple[PydanticModelType, dict[str, Any]]:
  if json_wrapped and (json_data := flask.request.values.get('body')):
    remaining_data = json.loads(json_data)
  else:
    remaining_data = get_request_data()
  values = {}
  for attr, field in ParametersClass.model_fields.items():
    if attr in remaining_data:
      value = remaining_data.pop(attr)
      # Check if we need to convert anything to a list
      if (str(field.annotation).startswith('list[') and
          not isinstance(value, list)):
        values[attr] = [value]
      else:
        values[attr] = value

  # Let Pydantic check if it has all the required data
  try:
    result = ParametersClass(**values)
  except pydantic.ValidationError:
    LOGGER.exception('Invalid parameters!')
    raise exceptions.InvalidParameterException

  return result, remaining_data


def get_request_data() -> dict[str, Any]:
  request_data = {}
  for key in flask.request.values:
    # Get everything as a list & assume that 1-length lists are single values
    values = flask.request.values.getlist(key)
    if len(values) == 1:
      request_data[key] = values[0]
    else:
      request_data[key] = values
  request_data.update(flask.request.get_json(silent=True) or {})
  return request_data
