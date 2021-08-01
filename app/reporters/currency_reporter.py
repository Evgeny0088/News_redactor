from urllib.request import urlopen
from urllib.error import URLError, HTTPError
from pathlib import Path
import json
import re
import sys
import asyncio

file = Path(__file__).resolve()
package_root_directory = file.parents[1]
sys.path.append(str(package_root_directory))

from sqlalchemy import create_engine
from utils.utils import date_to_number
from flask_conf import app, REPORTERS_CONNECTION_ERROR
from flask_conf.models import db, Currency

NAME = 'Currency reporter'
VERSION = '0.0.1'
MAIN_URL = 'https://www.cbr-xml-daily.ru/daily_json.js'
CURRENCY_OF_INTEREST = ['USD','EUR','SEK']

def get_news(main_url = MAIN_URL):
	try:
		responce = urlopen(MAIN_URL)
		data = json.loads(responce.read().decode('utf8'))
		target_data = {
		'Date':date_to_number(data['Date']),
		CURRENCY_OF_INTEREST[0]:data['Valute']['USD'],
		CURRENCY_OF_INTEREST[1]:data['Valute']['EUR'],
		CURRENCY_OF_INTEREST[2]:data['Valute']['SEK'],		
		}
	except URLError as e:
		return REPORTERS_CONNECTION_ERROR
	return target_data

async def create_new_set_of_currency(target_data):
	"""
	returns latest currency values from source site for representation
	on our main page
	and record them into db if conditions fulfilled 
	"""
	for i in CURRENCY_OF_INTEREST:
		print('creating an new object...')
		new_record = Currency(charcode = i,value = target_data[i]['Value'],\
												date = target_data['Date'])
		db.session.add(new_record)
		print('writing into currency table...')
		db.session.commit()
		await asyncio.sleep(0.01)

async def currency_news(target_data, database = app.config['SQLALCHEMY_DATABASE_URI']):
	currency_news = {}
	currency_news['currency_news'] = target_data
	engine = create_engine(database, echo = True)
	if not engine.dialect.has_table(engine.connect(), "currency"): # check if table does not exists
		db.create_all()
		print('currency table is created...')
	if db.session.query(Currency).first() is None:  # check if no any records in table yet
		await create_new_set_of_currency(target_data)
		print('first record is submitted in currency table')
	elif target_data.get('Date')>Currency.query.order_by(Currency.id.desc()).first().date:  # check if latest record in database
																							# earlier than current we writing it in db
		await create_new_set_of_currency(target_data)
	else:
		print('no new records in currency table!...')
	return currency_news
