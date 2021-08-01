import os
import re
import sys
from PIL import Image
from pathlib import Path

file = Path(__file__).resolve()
package_root_directory = file.parents[1]
sys.path.append(str(package_root_directory))

image_path = str(package_root_directory)+'/static/'+'covid_label.jpg'

def date_to_number(date_from_json):
	pattern = r'\d\d\d\d[-]\d\d[-]\d\d'
	edit_date = int(re.match(pattern,date_from_json).group().replace('-',''))
	return edit_date

def number_to_date(number):
	string = []
	string[:0] = str(number)
	string.insert(4,'-')
	string.insert(7,'-')
	date = ''.join(string)
	return date

def save_picture(image_path = image_path):
	output_size = (500,500)
	i = Image.open(image_path)
	i.thumbnail(output_size)
	i.save(image_path)
	return -1

if __name__ == '__main__':
	save_picture()