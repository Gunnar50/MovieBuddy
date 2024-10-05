import flask

ROUTES = flask.Blueprint('general', __name__)


@ROUTES.route('/_ah/warmup')
def warmup() -> str:
  # Nothing to do, just to make sure Flask etc. is ready to serve requests
  return 'Warmup complete!'


@ROUTES.route('/')
def home():
  return flask.render_template('index.html')
