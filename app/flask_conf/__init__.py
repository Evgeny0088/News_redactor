from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_conf.config import Config
from pathlib import Path
import sys

file = Path(__file__).resolve()
package_root_directory = file.parents[1]
sys.path.append(str(package_root_directory))

TEMPLATE_DIR = str(package_root_directory)+'/templates'
STATIC_DIR = str(package_root_directory)+'/static'

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
app.config.from_object(Config)
db = SQLAlchemy(app)
REPORTERS_CONNECTION_ERROR = {'connection_error':'check internet connection or page not found...'}

from views.main_routes import main
from views.currency_routes import currency
from views.covid_routes import covid
from errors.handlers import errors

app.register_blueprint(main)
app.register_blueprint(currency)
app.register_blueprint(covid)
app.register_blueprint(errors)


def database_is_exists(url = app.config['SQLALCHEMY_DATABASE_URI']):
	"""
	check if database is exists, if not -> being created
	"""
	from sqlalchemy import create_engine
	from sqlalchemy_utils.functions import database_exists, create_database
	engine = create_engine(url, echo = True)
	if not database_exists(url):
		create_database(engine.url)

def create_app(config_class = Config):
	return app