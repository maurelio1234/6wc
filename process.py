import csv
from datetime import datetime, timedelta
import string
import re

def get_time(s):
	""" interprets time based expressions in s and returns it as a number of minutes """
	
	def get_match_int(res, s, g=1):
		match = re.search(res, s)
		if match:
			return int(match.group(g))
		else:
			return 0
			
	hours = get_match_int(r'(?P<hours>[0-9]+)\s*(h|hour(s)?)', s)
	minutes = get_match_int(r'(?P<minutes>[0-9]+)\s*(min|minute(s)?)', s)

	return hours*60 + minutes

def extract_6wcbot():
	with open('tweets.csv') as f:
		with open('tweets_6wcbot.csv', 'w') as g:
			for line in csv.reader(f, delimiter=','):
				if line[0] == 'tweet_id': continue

				timestamp = datetime.strptime(line[5][:-6], "%Y-%m-%d %H:%M:%S")
				text      = line[7].lower()

				if '@6wcbot' in text and \
					('#chinese' in text or \
					 '#zh' in text or \
					 '#mandarin' in text):
						time = get_time(text)
						if time:
							if 'yesterday' in text:
								timestamp = timestamp - timedelta(days=1)
							g.write(str(timestamp) + ';' + str(time) + '\n')
						else:
							print 'huh? ' + text

def reverse(fin='tweets_6wcbot.csv', fout='tweets_6wcbot_r.csv'):
	with open(fin) as f:   
		with open(fout, 'w') as g:
			for line in reversed(f.readlines()):
				g.write(line + '\n')

def accumulative(fin='tweets_6wcbot_r.csv', fout='tweets_6wcbot_r_a.csv'):
	with open(fin) as f:
		with open(fout, 'w') as g:
			acc = 0
			first_ts = None
			for line in csv.reader(f, delimiter=';'):
				if line:
					ts = datetime.strptime(line[0], "%Y-%m-%d %H:%M:%S") 
					if not first_ts:
									first_ts = ts
					acc = acc + int(line[1])
					delta = ts - first_ts
					g.write(str(delta.total_seconds()) + ';' + str(acc)+'\n')

def compute_acc(reference_start, reference_end=None, duration=6):
	"""computes the number of minutes accumulated in the reference CSV
	 	 taking reference start and end dates, and a challenge duration in weeks"""
	if not reference_end:
		reference_end = datetime.now()
		
	current_ts = (reference_end - reference_start).total_seconds()

	with open('tweets_6wcbot_r_a.csv') as f:
		last_ts = None
		last_acc = 0
		for line in csv.reader(f, delimiter=';'):
				ts = float(line[0])*duration / 6.0
				acc = int(line[1])*duration/6.0
				
				if current_ts < ts:
					return last_acc

				last_ts = ts
				last_acc = acc
		return 0

def minutes2hm(min):
	""" returns hour,minute from an int representing an amount of minutes """
	return min/60, min%60
	
def normalize(in_duration, fin='current.6wc.csv',fout='current.norm.6wc.csv'):
	with open(fin) as f:
		with open(fout, 'w') as g:
			for line in csv.reader(f, delimiter=';'):
				ts = float(line[0])*6.0/in_duration
				acc = int(line[1])*6.0/in_duration
				g.write(str(ts)+';'+str(int(acc))+'\n')
	
normalize(1)

# usage	
#print compute_acc(datetime(2014,12,05))
#print get_time(raw_input())
