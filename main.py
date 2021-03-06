import model
import process
from datetime import datetime, timedelta
from sys import exit

model.load_data()

if not model.is_running_challenge():
	create_challenge = raw_input('No challenge running. Create a new one? (y/n)')
	
	if create_challenge == 'y':
		duration = raw_input('What is the duration of the new challenge (in weeks): ')
		model.initialize_challenge(duration)
	else:
		exit()
		
start_date = model.get_reference_date()
end_date = start_date + timedelta(weeks=model.get_duration())

if datetime.now() > end_date:
	print 'Current challenge is over!'
	print 'Last challenge started at {:%Y-%m-%d} '\
	      'and finished at {:%Y-%m-%d}'.format(start_date,end_date)

	my_acc = model.get_accumulated_minutes()
	opp_acc = process.compute_acc(model.get_reference_date(), duration=model.get_duration(), reference_end=end_date)
	
	if my_acc > opp_acc:
		print 'You won it!'
	else:
		print 'You lost it :(... better luck next time!'
		                     
	h,m = process.minutes2hm(my_acc)
	print 'You worked for {:02d}h{:02d}min'.format(h,m)
	h,m = process.minutes2hm(opp_acc)
	print 'Your opponent worked for {:02d}h{:02d}min'.format(h,m)
	
	save = raw_input('Do you want to save this challenge data? (y/n)')
	if save == 'y':
		process.normalize(model.get_duration(), fin='current.6wc.csv', fout='challenge.{:%Y%m%d}.csv'.format(start_date))
else:
	print 'Current challenge started at {:%Y-%m-%d} '\
	      'and will finish at {:%Y-%m-%d}'.format(start_date,end_date)

	print 'Time elapsed: '+str(datetime.now() - start_date)
	print 'Remaining time: '+str(end_date - datetime.now())

	h,m = process.minutes2hm(process.compute_acc(model.get_reference_date(), duration=model.get_duration()))
	print 'Your adversary has already worked for {:02d}h{:02d}min'.format(h,m)

	h,m = process.minutes2hm(
	                      process.compute_acc(reference_start=model.get_reference_date(),
	                                          reference_end=end_date, 
	                                          duration=model.get_duration()))
	print 'Target work time is {:02d}h{:02d}min'.format(h,m)

	h,m = process.minutes2hm(model.get_accumulated_minutes())
	print 'You have already worked for {:02d}h{:02d}min.'.format(h,m)

	tweet = raw_input('Tweet including XhYmin (empty for quit): ')
	if tweet:
		model.add_minutes(tweet)
	
		h,m = process.minutes2hm(model.get_accumulated_minutes())
		print 'Total time updated to {:02d}h{:02d}min.'.format(h,m)
	
		model.save_data()
