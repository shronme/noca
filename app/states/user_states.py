

class NewUserState():
	def __init__(self, user):
		self.user = user

	def run(self, message):

		return 'Hi {}, Welcome to NoCa Pay'

	def next_state(self):
		return 'new_user'




class GetInfoState():

	user_info = {
		'name': 'May I have your Name?\n',
		'post_code': 'What is your postcode?\n',
		'house_number': 'What is you house number?\n'
		}
	def __init__(self, user):
		self.user = user
		self.info = user.info
		self.info_to_process = 'name'
		self.step = 'info'
	
	def run(self):

		for detail in self.user_info.keys():
			if detail not in self.info.keys():
				self.info_to_process = detail
				return self.user_info[detail]
		
		self.step = 'get_payment'

	def process_input(self, input):
		self.user.info[self.info_to_process] = input
		return True

	def next_step(self):
		return self.step


class GetPaymentState():

	def __init__(self, user):
		self.user = user

	def run(self):
		return "How much would you like to pay?\n"

	def process_input(self, input):
		print('You payment in the amount of {} was received\n'.format(input))
		return True

	def next_step(self):
		return 'get_payment'


states_dict = {
	'new_user': NewUserState,
}
