import model
import process

model.load_data()

if not model.is_running_challenge():
	create_challenge = raw_input('No challenge running. Create a new one? (y/n)')
	#TODO: ask for duration
	
	if create_challenge == 'y':
		model.initialize_challenge()
	else:
		exit()
		
print 'Current challenge started at '+str(model.get_reference_date())

h,m = process.minutes2hm(process.compute_acc(model.get_reference_date(), model.get_duration()))
print 'Your adversary has already studied for {:02d}h{:02d}min'.format(h,m)

h,m = process.minutes2hm(model.get_accumulated_minutes())
print 'You have already studied for {:02d}h{:02d}min.'.format(h,m)

tweet = raw_input('Tweet including XhYmin (empty for quit): ')
if tweet:
	model.add_minutes(tweet)
	
	h,m = process.minutes2hm(model.get_accumulated_minutes())
	print 'You have already studied for {:02d}h{:02d}min.'.format(h,m)
	
	model.save_data()
