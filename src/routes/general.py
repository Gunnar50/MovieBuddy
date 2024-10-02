import flask

GENERAL = flask.Blueprint('general', __name__)


@GENERAL.route('/_ah/warmup')
def warmup() -> str:
  # Nothing to do, just to make sure Flask etc. is ready to serve requests
  return 'Warmup complete!'
