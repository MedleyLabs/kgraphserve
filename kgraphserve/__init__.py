import os
import yaml

from flask import Flask
from flask_cors import CORS

config_dir = os.path.dirname(__file__)
config_path = os.path.join(config_dir, 'config.yml')

with open(config_path, 'r') as f:
    config = yaml.safe_load(f)

cors = CORS()


def create_app():
    """ Creates the Flask app with an application factory pattern """

    app = Flask(__name__)

    cors.init_app(app)

    # Importing blueprints here avoids circular dependencies
    from kgraphserve.routes.fma import fma
    from kgraphserve.routes.language_models import language_models
    from kgraphserve.routes.website import website

    app.register_blueprint(fma)
    app.register_blueprint(language_models)
    app.register_blueprint(website)

    return app
