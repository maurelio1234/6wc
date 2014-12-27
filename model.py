from datetime import date, datetime
import json

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
	
def initialize_challenge():
	global data
	
	data = {}
	today = date.today()
	data['year'] = today.year
	data['month'] = today.month
	data['day'] = today.day
	data['accumulated'] = 0
	
	save_data()
	
def get_reference_date():
	return datetime(int(data['year']), int(data['month']), int(data['day']))

def get_accumulated_minutes():
	return int(data['accumulated'])
	
def is_running_challenge():
	return data
		
def add_minutes(minutes):
	global data
	
	now = datetime.now()
	delta = (now - get_reference_date()).total_seconds()
	acc = get_accumulated_minutes() + int(minutes)
	data['accumulated'] = acc
	
	with open('current.6wc.csv', 'a') as f:
		f.write(str(delta)+';'+str(acc)+'\n')
	
	

