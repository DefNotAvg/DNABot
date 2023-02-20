import os
import math
import json
from time import localtime, strftime

def center(text, padding=' ', length=100, clear=False, display=True):
	'''Center text at specified length with specified padding surrounding.

	Args:
		text: Text to center.
		padding: Padding used to center text.
		length: Length of text after centering.
		clear: True to clear previous output, False otherwise.
		display: True to print centered text, False to return.

	Returns:
		None if display is set to True, otherwise centered text.
	'''
	if clear:
		os.system('cls' if os.name == 'nt' else 'clear')
	padding_count = int(math.ceil((length - len(text)) / 2))
	if padding_count > 0:
		if display:
			print(padding * padding_count + text + padding * padding_count)
		else:
			return (padding * padding_count + text + padding * padding_count)
	else:
		if display:
			print(text)
		else:
			return text

def header():
	'''Clear previous output and display header text.'''
	os.system('cls' if os.name == 'nt' else 'clear')
	center('DNABot by @DefNotAvg')
	center('-', '-')

def load_from_json(file):
	'''Load JSON file into a dictionary. If file doesn't exist, blank dictionary is written to file and returned.

	Args:
		file: JSON filename.

	Returns:
		Dictionary representation of JSON file contents.
	'''
	try:
		with open(file, 'r') as myfile:
			return json.load(myfile)
	except IOError:
		with open(file, 'w') as myfile:
			json.dump({}, myfile)
		return {}

def smart_time():
	'''Return the local time in YYYY-MM-DD HH:MM:SS 24hr format.'''
	return str(strftime('%Y-%m-%d %H:%M:%S', localtime()))