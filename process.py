import csv
from datetime import datetime, timedelta
import string
import re

def get_time(s):
	match = re.search(r'((?P<hours>[0-9]+)\s*(h|hour(s)?)\s*)?(?P<minutes>[0-9]+)\s*(min|minutes)?', s)
	if match:
		hours = match.group('hours')
		minutes = match.group('minutes')
		def toint(s):
			if s: return int(s)
			return 0
		return toint(hours)*60 + toint(minutes)
	return None

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

def reverse():
	with open('tweets_6wcbot.csv') as f: 
		with open('tweets_6wcbot_r.csv', 'w') as g:
			for line in reversed(f.readlines()):
				g.write(line + '\n')

def accumulative():
	with open('tweets_6wcbot_r.csv') as f:
		with open('tweets_6wcbot_r_a.csv', 'w') as g:
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

def compute_acc(reference_date):
	current_ts = (datetime.now() - reference_date).total_seconds()

	with open('tweets_6wcbot_r_a.csv') as f:
		last_ts = None
		last_acc = 0
		for line in csv.reader(f, delimiter=';'):
				ts = float(line[0])
				acc = int(line[1])
				if current_ts < ts:
					return last_acc

				last_ts = ts
				last_acc = acc
		return 0

def minutes2hm(min):
	return min/60, min%60
	
#print compute_acc(datetime(2014,12,05))
