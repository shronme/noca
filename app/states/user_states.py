import requests
from app.states.replies import ACCESS_TOKEN, reply
from app.models.merchant import Merchant


class NewUserState():
	def __init__(self, user):
		self.user = user

	def run(self, message):
		sender = message['entry'][0]['messaging'][0]['sender']['id']
		if not self.user.name:
			fb_user = requests.get('https://graph.facebook.com/v2.6/' + str(sender) + '?access_token=' + ACCESS_TOKEN)
			self.user.name = fb_user.json()['first_name']
			self.user.save()
		reply(sender, 'Hi {}, Welcome to NoCa Pay'.format(self.user.name))
		reply(sender, 'As a new customer your first purchase, up to £10 is on us. After that we will ask you to register in order to make further purchases.')

		return self.next_state()

	def next_state(self):
		return 'get_payment'




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

	def run(self, data):

		try:
			message = data['entry'][0]['messaging'][0]['message']['text']
		except KeyError:
			self.reply(sender, 'oops, something went wrong')
			return 'ok'
		sender = message['entry'][0]['messaging'][0]['sender']['id']

		if not user.attempt_counter:
			merchant = Merchant.objects(merchant_id=message).first()
			if merchant:
				reply(sender, 'You are trying to make a payment at {}.\nIf not, please respond with the message: "N", otherwise please tell us how much would like to pay'.format(self.merchant.name))
				user.attempt_counter = 1
				user.save()
				return ''
		elif user.attempt_counter == 1:
			if message.lower() == 'n':
				reply(sender, 'Please try sendin the merchant number again.')
				user.attempt_counter = 2
				user.save()
				return ''
			else:
				try:
					amount = float(message)
				except ValueError:
					reply(sender, 'I didn\'t understand your message. I was expecting to recieve an amount. One of our agents will help you shortly.')
					user.attempt_counter = 0
					user.save()
					return ''
				reply(sender, 'To pay {amount} at {merchant} send "y" or send the amount again'.format(amount=amount, merchant=self.merchant.name))
				user.attempt_counter == 3
				user.save()
				return ''
		elif user.attempt_counter == 2:
			merchant = Merchant.objects(merchant_id=message).first()
			if merchant:
				reply(sender, 'You are trying to make a payment at {}.\n If so please send us the amount, otherwise one of our agents will help you shortly'.format(merchant=self.merchant.name))
				user.attempt_counter = 3
				user.save()
				return ''
		elif user.attempt_counter == 3:
			if message.lower() == 'y':
				reply(sender, 'Thank you for using Nocapay. See you soon.')
				user.attempt_counter = 0
				user.save()
				return ''
			else:
				try:
					amount = float(message)
				except ValueError:
					reply(sender, 'I didn\'t understand your message. I was expecting to recieve an amount. One of our agents will help you shortly.')
					user.attempt_counter = 0
					user.save()
					return ''
				reply(sender, 'To pay {amount} at {merchant} send "y", otherwise one of our agents will help you shortly'.format(amount=amount, merchant=self.merchant.name))
				return ''
				

	def process_input(self, input):
		print('You payment in the amount of {} was received\n'.format(input))
		return True

	def next_step(self):
		return 'get_payment'


states_dict = {
	'new_user': NewUserState,
	'get_payment': GetPaymentState
}
