from flask import request, render_template, Blueprint
import sys
from pathlib import Path
import pandas as pd
import plotly
import plotly.express as px
import plotly.graph_objects as go
import json

file = Path(__file__).resolve()
package_root_directory = file.parents[1]
sys.path.append(str(package_root_directory))

covid = Blueprint('covid_news', __name__)

from views.main_routes import create_news

def fetch_covid_data():
	results = create_news()
	fetch_results = next((filter(lambda i:'covid_news' in i.keys() ,results)))
	if not fetch_results:
		fetch_results = 'covid data is empty...'
	return fetch_results

def deaths_plot(covid_top5_deaths):
	covid_top5_deaths = [i.get('attributes') for i in covid_top5_deaths]
	data = pd.DataFrame(covid_top5_deaths)
	fig = px.bar(data, x = 'Deaths', y = data.Country_Region, height = 600, color = 'Deaths', orientation = 'h',
				color_continuous_scale = ['deepskyblue','red'])
	fig.update_layout(xaxis_title = None, yaxis_title=None)
	json_bar = fig.to_json()
	return json_bar

def active_plot(covid_top5_actives):
	covid_top5_actives = [i.get('attributes') for i in covid_top5_actives]
	data = pd.DataFrame(covid_top5_actives)
	fig = px.scatter(data, x = data.Country_Region, y = data.Active, size = 'Active', size_max = 60,
				color = data.index)
	fig.update_layout(xaxis_title = None, yaxis_title=None)
	json_scatter = fig.to_json()
	return json_scatter

def confirmed_plot(covid_top5_confirmed):
	covid_top5_confirmed = [i.get('attributes') for i in covid_top5_confirmed]
	data = pd.DataFrame(covid_top5_confirmed)
	fig = px.scatter(data, x = data.Country_Region, y = data.Confirmed, size = 'Confirmed', size_max = 60,
				color = data.index)
	fig.update_layout(xaxis_title = None, yaxis_title=None)
@covid.route("/covid-news")
def covid_route():
	covid_news = fetch_covid_data().get('covid_news')
	covid_deaths = deaths_plot(covid_news[0].get('deaths'))
	covid_active = active_plot(covid_news[1].get('active'))
	covid_confirmed = active_plot(covid_news[2].get('confirmed'))
	return render_template('covid.html', title = 'Covid news', covid_deaths_json = covid_deaths,
								covid_active_json = covid_active,
								covid_confirmed_json = covid_confirmed)
