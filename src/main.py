from flask import Flask


def create_app():
  flask_app = Flask(__name__)
  return flask_app


def register_routes(flask_app):
  from routes import general

  flask_app.register_blueprint(general.GENERAL)


if __name__ == "__main__":
  app = create_app()
  register_routes(app)
  app.run(debug=True)
