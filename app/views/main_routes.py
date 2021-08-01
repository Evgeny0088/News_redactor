from flask import request, render_template, Blueprint
import sys
import asyncio
from pathlib import Path

file = Path(__file__).resolve()
package_root_directory = file.parents[1]
sys.path.append(str(package_root_directory))

main = Blueprint('main', __name__)


def create_news():
	from redactors.newsmaker import newsmaker_run
	from flask_conf import database_is_exists
	database_is_exists()
	results = asyncio.run(newsmaker_run())
	return results

def parce_results():
	results = create_news()
	parced_results = {}
	parced_results['covid_news'] = next((filter(lambda i:'covid_news' in i.keys() ,results)))
	parced_results['currency_news'] = next((filter(lambda i:'currency_news' in i.keys() ,results)))
	return parced_results

@main.route("/")
def index():
	results = parce_results()
	covid = results.get('covid_news').get('covid_news')[0].get('deaths')
	currency = results.get('currency_news').get('currency_news')
	currency_latest_update = currency.pop('Date')
	return render_template('main.html', title = 'News page', 
						currency_latest_update = currency_latest_update,
						currency = currency,
						covid = covid)

@main.route("/about")
def about():
	return render_template('about.html', title = 'About page')