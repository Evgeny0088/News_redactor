from urllib.request import urlopen
from urllib.error import URLError, HTTPError
from pathlib import Path
import json
import re
import sys
import asyncio
import heapq
from threading import Thread
from datetime import datetime

file = Path(__file__).resolve()
package_root_directory = file.parents[1]
sys.path.append(str(package_root_directory))

from sqlalchemy import create_engine
from flask_conf import app, REPORTERS_CONNECTION_ERROR
from flask_conf.models import db, Covid

NAME = 'Covid reporter'
VERSION = '0.0.1'
MAIN_URL = ('https://services1.arcgis.com/0MSEUqKaxRlEPj5g/arcgis/rest/services/Coronavirus_2019_nCoV_Cases/FeatureServer/1/query?where=1%3D1&outFields=OBJECTID,Country_Region,Last_Update,Confirmed,Recovered,Deaths,Active,Province_State&returnGeometry=false&outSR=4326&f=json')

def get_news(main_url = MAIN_URL):
	try:
		responce = urlopen(MAIN_URL)
		data = json.loads(responce.read().decode('utf8'))
		target_data = data
	except URLError as e:
		return REPORTERS_CONNECTION_ERROR
	return target_data

def correct_date(epoch_time):
	epoch_time = int(str(epoch_time)[:-3])
	time = datetime.utcfromtimestamp(epoch_time).strftime('%Y-%m-%d %H:%M:%S')
	pattern = r'\d\d\d\d[-]\d\d[-]\d\d'
	edit_date = int(re.match(pattern,time).group().replace('-',''))
	return edit_date

def top5_deaths(data,top5_countries_for_db, top5_countries_for_redactor):
	deaths = {}
	deaths_list = []
	deaths_list = heapq.nlargest(5,data.get('features'), key = lambda x:x.get('attributes').get('Deaths'))
	for i in deaths_list:
		i['attributes']['Last_Update'] = correct_date(i.get('attributes').get('Last_Update'))
		if not any(map(lambda x: x.get('attributes').get('OBJECTID') == i.get('attributes').get('OBJECTID'),top5_countries_for_db)):
			top5_countries_for_db.append(i)
	deaths['deaths'] = deaths_list
	top5_countries_for_redactor.append(deaths)

def top5_active(data,top5_countries_for_db, top5_countries_for_redactor):
	active = {}
	active_list = []
	active_list = heapq.nlargest(5,data.get('features'), key = lambda x:x.get('attributes').get('Active'))
	for i in active_list:
		i['attributes']['Last_Update'] = correct_date(i.get('attributes').get('Last_Update'))
		if not any(map(lambda x: x.get('attributes').get('OBJECTID') == i.get('attributes').get('OBJECTID'),top5_countries_for_db)):
			top5_countries_for_db.append(i)
	active['active'] = active_list
	top5_countries_for_redactor.append(active)

def top5_confirmed(data,top5_countries_for_db, top5_countries_for_redactor):
	confirmed = {}
	confirmed_list = []
	confirmed_list = heapq.nlargest(5,data.get('features'), key = lambda x:x.get('attributes').get('Confirmed'))
	for i in confirmed_list:
		i['attributes']['Last_Update'] = correct_date(i.get('attributes').get('Last_Update'))
		if not any(map(lambda x: x.get('attributes').get('OBJECTID') == i.get('attributes').get('OBJECTID'),top5_countries_for_db)):
			top5_countries_for_db.append(i)
	confirmed['confirmed'] = confirmed_list
	top5_countries_for_redactor.append(confirmed)

def top5_countries_sort(data, top5_countries_for_db = None, top5_countries_for_redactor = None):
	if top5_countries_for_db is None:
		top5_countries_for_db = []
	if top5_countries_for_redactor is None:
		top5_countries_for_redactor = []
	t1 = Thread(target = top5_deaths, args = (data,top5_countries_for_db, top5_countries_for_redactor))
	t2 = Thread(target = top5_active, args = (data,top5_countries_for_db, top5_countries_for_redactor))
	t3 = Thread(target = top5_confirmed, args = (data,top5_countries_for_db, top5_countries_for_redactor))
	t1.start()
	t2.start()
	t3.start()
	t1.join()
	t2.join()
	t3.join()
	return top5_countries_for_db, top5_countries_for_redactor

class Covid_Country:

	def __init__(self,**kwargs):
		self.Province_State = kwargs['Province_State']
		self.Country_Region = kwargs['Country_Region']
		self.Confirmed = kwargs['Confirmed']
		self.Recovered = kwargs['Recovered']
		self.Deaths = kwargs['Deaths']
		self.Active = kwargs['Active']
		self.Last_update = kwargs['Last_Update']

	async def db_object(self):
		new_record = Covid(
		Province_State = self.Province_State,Country_Region = self.Country_Region, 
		Confirmed = self.Confirmed,Recovered = self.Recovered,
		Deaths = self.Deaths, Active = self.Active, 
		Last_update = self.Last_update
		)
		db.session.add(new_record)
		db.session.commit()
		await asyncio.sleep(0.01)

async def covid_news(data, database = app.config['SQLALCHEMY_DATABASE_URI']):
	"""
	saving all countries which are fullfiled all criterias
	"""
	covid_news = {}
	top5_countries_for_db = []
	top5_countries_for_redactor = []
	top5_countries_for_db, top5_countries_for_redactor = top5_countries_sort(data)
	print('covid countries are sorted...')
	covid_news['covid_news'] = top5_countries_for_redactor
	engine = create_engine(database, echo = True)
	if not engine.dialect.has_table(engine.connect(),'covid'):
		db.create_all()
		print('covid table is created...')
	if db.session.query(Covid).first() is None:
		for i in top5_countries_for_db:
			await Covid_Country(**i.get('attributes')).db_object()
			print('first records in covid table')
	elif top5_countries_for_db[0]['attributes']['Last_Update']>Covid.query.order_by(Covid.id.desc()).first().Last_update: # check if latest record in database
		for i in top5_countries_for_db:
			await Covid_Country(**i.get('attributes')).db_object()
			print('new records in covid table')
	else:
		print('no new records in covid table!...')
	return covid_news