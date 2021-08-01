from pathlib import Path
import sys
import os
import asyncio

file = Path(__file__).resolve()
package_root_directory = file.parents[1]
reporters_location = '/reporters'
string_path = str(package_root_directory) + reporters_location
sys.path.append(string_path)
reporter_files = os.listdir(string_path)


def get_reporters():
	reporters = {}
	for i in reporter_files:
		if os.path.isfile(string_path+'/'+i) and '__' not in i:
			file_without_extension = Path(i).stem
			m = __import__(file_without_extension)
			if file_without_extension == 'covid_reporter' and file_without_extension\
												not in reporters:
				reporters['covid_reporter'] = m	
			else:
				reporters['currency_reporter'] = m
			print(m)
	return reporters

async def newsmaker_run():
	"""
	here all reporters will be run asynchroniously
	"""
	reporters = get_reporters()
	covid_data = reporters['covid_reporter'].get_news()
	currency_data = reporters['currency_reporter'].get_news()
	from flask_conf import REPORTERS_CONNECTION_ERROR as error
	if covid_data!=error and currency_data!=error:
		task1 = asyncio.create_task(reporters['covid_reporter'].covid_news(covid_data), name = 'covid_news')
		task2 = asyncio.create_task(reporters['currency_reporter'].currency_news(currency_data), name = 'currency_news')
		results = await asyncio.gather(task1,task2)
	else:
		results = error
		return results
	return results