from flask import request, render_template, Blueprint
import sys
from pathlib import Path
import pandas as pd
import plotly as px
import plotly.graph_objects as go
import json

file = Path(__file__).resolve()
package_root_directory = file.parents[1]
sys.path.append(str(package_root_directory))

currency = Blueprint('currency_news', __name__)

def get_currency_from_db():
	from flask_conf.models import db, Currency
	currency = Currency.query.all()
	return currency

def currency_plots(currency_from_db):
	from reporters.currency_reporter import CURRENCY_OF_INTEREST
	currency_from_db = [i.dict_object() for i in currency_from_db]
	currency_from_db = pd.DataFrame(currency_from_db)
	plots = go.Figure()
	for i in CURRENCY_OF_INTEREST:
		sorted_by_name = currency_from_db[currency_from_db['charcode']==i]
		plots.add_trace(go.Scatter(x = sorted_by_name['date'], y = sorted_by_name['value'], name = i))
	graphJSON = json.dumps(plots, cls=px.utils.PlotlyJSONEncoder)
	return graphJSON

@currency.route("/currency-news")
def currency_route():
	currency_from_db = get_currency_from_db()
	currency_plots_json = currency_plots(currency_from_db)
	return render_template('currency.html', title = 'Currency news', currency_plots_json = currency_plots_json)