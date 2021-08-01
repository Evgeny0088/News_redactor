import os

class Config:
	DEBUG = True
	SQLALCHEMY_TRACK_MODIFICATIONS=False
	SECRET_KEY = 'aafbe25d5ad1c06615ed4864ea7a912d'
	MYSQL_HOST = 'db'
	MYSQL_USER = 'evgeny88'
	MYSQL_PASSWORD = 'Primera77!'
	MYSQL_DB = 'News_redactor'
	SQLALCHEMY_DATABASE_URI=f'mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:3306/{MYSQL_DB}'
