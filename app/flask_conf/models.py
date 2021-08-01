import os
import sys  
from pathlib import Path
from functools import wraps

file = Path(__file__).resolve() 
package_root_directory = file.parents[1]
sys.path.append(str(package_root_directory))

from flask_conf import db

class Currency(db.Model):
	id = db.Column(db.Integer(),primary_key = True)
	charcode = db.Column(db.String(20), unique = False, nullable = False)
	value = db.Column(db.Float(), unique = False, nullable = False)
	date = db.Column(db.Integer(), unique = False, nullable = False)

	def __init__(self,*args,**kwargs):
		super(Currency,self).__init__(*args,**kwargs)

	@property
	def get_id(self):
		return self.id

	@property
	def get_charcode(self):
		return self.charcode

	@property
	def get_value(self):
		return self.value

	def date_decorator(func):
		from utils.utils import number_to_date
		@wraps(func)
		def wrapper(*args,**kwargs):
			date_number = func(*args,**kwargs)
			str_date = number_to_date(date_number)
			return str_date
		return wrapper

	@property
	@date_decorator
	def get_date(self):
		return self.date

	def dict_object(self):
		return {'charcode':self.charcode, 'value':self.value, 'date':self.get_date}


	def __repr__(self):
		return f'id={self.id}, charcode={self.charcode},value={self.value}, date={self.get_date}'

class Covid(db.Model):
	id = db.Column(db.Integer(),primary_key = True)
	Province_State = db.Column(db.String(50),unique = False, nullable = True)
	Country_Region = db.Column(db.String(50), unique = False, nullable = False)
	Confirmed = db.Column(db.Integer(), unique = False, nullable = True)
	Recovered = db.Column(db.Integer(), unique = False, nullable = True)
	Deaths = db.Column(db.Integer(), unique = False, nullable = True)
	Active = db.Column(db.Integer(), unique = False, nullable = True)
	Last_update = db.Column(db.Integer(), unique = False, nullable = False)

	def __init__(self, *args,**kwargs):
		super(Covid,self).__init__(*args,**kwargs)

	def __repr__(self):
		return (
				f'''id = {self.id}, Province_State = {self.Province_State}, Country_Region = {self.Country_Region}'
				Confirmed = {self.Confirmed}, Recovered = {self.Recovered}, Deaths = {self.Deaths},
				Active = {self.Active}, Last_update = {self.Last_update}'''
				)
