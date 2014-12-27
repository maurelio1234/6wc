from datetime import date, datetime
import json
from csv import writer
from process import get_time


data = None

def load_data():
	global data	
	try:
		with open('current.6wc.txt') as f:
			data = json.load(f)
	except BaseException:
		data = None 
	
def save_data():
	with open('current.6wc.txt', 'w') as f:
		json.dump(data, f, indent=4)
	
def initialize_challenge(duration=6):
	global data
	
	data = {}
	today = date.today()
	
	data = {
	    'year':  today.year,
	    'month': today.month,
	    'day':   today.day,
	    'accumulated': 0,
	    'duration': duration  
	}
	save_data()
	
def get_reference_date():
	return datetime(int(data['year']), int(data['month']), int(data['day']))

def get_accumulated_minutes():
	return int(data['accumulated'])
	
def is_running_challenge():
	return data

def get_duration():
	return int(data['duration'])
	
def add_minutes(line):
	global data
	minutes = get_time(line)
	
	now = datetime.now()
	delta = (now - get_reference_date()).total_seconds()
	acc = get_accumulated_minutes() + int(minutes)
	data['accumulated'] = acc
	
	with open('current.6wc.csv', 'ab') as f:
		w = writer(f, delimiter=';')
		w.writerow([delta, acc, line])
	
	

