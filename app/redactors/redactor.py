from pathlib import Path
import sys
import os
import asyncio
import pandas as pd
import plotly.express as px

# need redactor class!!!!

covid_top5_deaths = [
		{'name':'russia','deaths':6000},{'name':'usa','deaths':2643},{'name':'india','deaths':3043},
		{'name':'UK','deaths':4000},{'name':'italy','deaths':5000}
	]

def fetch_covid_data(results):
	fetch_from_news_maker = next((filter(lambda i:'covid_news' in i.keys() ,results)))
	covid_news = fetch_from_news_maker.get('covid_news')
	if covid_news:
		covid_top5_countries = covid_news
	else:
		print('covid data is empty...')

def deaths_plot(covid_top5_deaths):
	data = pd.DataFrame(covid_top5_deaths)
	print(data)
	data.columns = ('name','deaths')
	fig1 = px.bar(data, x = 'deaths', y = data.name, height = 600, color = 'deaths', orientation = 'h',
            color_continuous_scale = ['deepskyblue','red'], title = 'Top 5 Death Cases Countries')
	fig1.show()

def active_plot(covid_top5_countries):
	data = pd.DataFrame(covid_top5_countries)
	print(data)
	data.columns = ('name','deaths')
	fig1 = px.scatter(data, x = data.name, y = 'deaths', size = 'deaths', size_max = 50,
                color = data.index, title = 'covid_top5_deaths')
	fig1.show()

def confirmed_plot(covid_top5_countries):
	data = pd.DataFrame(covid_top5_countries)
	print(data)
	data.columns = ('name','deaths')
	fig1 = px.scatter(data, x = data.name, y = 'deaths', size = 'deaths', size_max = 50,
                color = data.index, title = 'covid_top5_deaths')
	fig1.show()
