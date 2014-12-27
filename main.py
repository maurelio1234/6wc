import model
import process

model.load_data()

if not model.is_running_challenge():
	create_challenge = raw_input('No challenge running. Create a new one? (y/n)')
	
	if create_challenge == 'y':
		model.initialize_challenge()
	else:
		exit()
		
print 'Current challenge started at '+str(model.get_reference_date())

h,m = process.minutes2hm(process.compute_acc(model.get_reference_date()))
print 'Your adversary has already studied for {:02d}h{:02d}min'.format(h,m)

h,m = process.minutes2hm(model.get_accumulated_minutes())
print 'You have already studied for {:02d}h{:02d}min.'.format(h,m)

register = raw_input('Do you want to add more minutes? (y/n)')
if register == 'y':
	minutes = raw_input('XhYmin: ')
	model.add_minutes(process.get_time(minutes))
	
	h,m = process.minutes2hm(model.get_accumulated_minutes())
	print 'You have already studied for {:02d}h{:02d}min.'.format(h,m)
	
	model.save_data()
