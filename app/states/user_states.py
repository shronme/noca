import requests
from mongoengine import *
from app.states.replies import ACCESS_TOKEN, reply, reply_with_buttons
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



class GetPaymentState():

	def start_payment(self, message):
		print('starting payment')
		
		merchant = Merchant.objects(merchant_id=message).first()
		if merchant:
			print('in merchant2')
			self.user.state_dict['merchant'] = merchant.merchant_id
			fb_button = [
				{
					"type": "postback",
					"title": "No, that's not the place",
					"payload": "no"
				},
				{
					"type": "postback",
					"title": "Yes, that's the place",
					"payload": "yes"
				}
			]
			reply_with_buttons(self.user.fb_id,
				fb_button,
				'You are trying to make a payment at {}.\nIf not, \
				please respond with the message: "N", otherwise please tell us how much would like to pay'.format(merchant.name))
			self.user.state_dict['step'] = 'confirm_merchant'
			self.user.state_dict['attempts'] = 0
			self.user.save()
		else:
			if 'attempts' not in self.user.state_dict.keys():
				self.user.state_dict['attempts'] = 0
			if self.user.state_dict['attempts'] >= 2:
				reply(self.user.fb_id, 'It seems that something went wrong. One of our agent will help you shortly')
			else:
				reply(self.user.fb_id, 'Sorry we could not identify this merchant. Pleae try entring the merchant ID one more time.')
				self.user.state_dict['attempts'] = self.user.state_dict['attempts'] + 1
		return ''
	
	def confirm_merchant(self, message):
		if message == 'yes':
			reply(self.user.fb_id, 'How much would you like to pay?')
			self.user.state_dict['step'] = 'amount_requested'
		if message == 'no':
			if self.user.state_dict['attempts'] >= 2:
				reply(self.user.fb_id, 'It seems that something went wrong. One of our agent will help you shortly')
			else:
				reply(self.user.fb_id, 'Pleae try entring the merchant ID one more time')
				self.user.state_dict['step'] = 'start_payment'
				self.user.state_dict['attempts'] = self.user.state_dict['attempts'] + 1
		self.user.save()
		return ''

	def amount_requested(self, message):
		return ''
	
	def __init__(self, user):
		self.user = user
		self.run_dict = {
		'start_payment': self.start_payment,
		'confirm_merchant': self.confirm_merchant,
		'amount_requested': self.amount_requested
		}


	

	

	def run(self, data):

		if 'message' in data['entry'][0]['messaging'][0].keys():
			if 'text' in data['entry'][0]['messaging'][0]['message'].keys():
				message = data['entry'][0]['messaging'][0]['message']['text']
			else:
				reply(self.user.fb_id, 'oops, something went wrong')
				return 'ok'
		elif 'postback' in data['entry'][0]['messaging'][0].keys():
			message = data['entry'][0]['messaging'][0]['postback']['payload']
		else:
			reply(self.user.fb_id, 'oops, something went wrong')
			return 'ok'
		self.user.state_dict['state'] = 'get_payment'
		if self.user.state_dict['state'] != self.user.state:
			self.user.state_dict['step'] = 'start_payment'
		if 'step' not in self.user.state_dict.keys():
			self.user.state_dict['step'] = 'start_payment'
		self.user.save()	

		return self.run_dict[self.user.state_dict['step']](message)


		print('In payment run with attempt counter {}'.format(self.user.attempt_counter))
		if not self.user.attempt_counter:
			merchant = Merchant.objects(merchant_id=message).first()
			if merchant:
				reply(self.user.fb_id, 'You are trying to make a payment at {}.'.format(merchant.name))
				self.user.attempt_counter = 1
				self.user.save()
				return ''
		elif self.user.attempt_counter == 1:
			if message.lower() == 'n':
				reply(self.user.fb_id, 'Please try sendin the merchant number again.')
				self.user.attempt_counter = 2
				self.user.save()
				return ''
			else:
				try:
					amount = float(message)
				except ValueError:
					reply(self.user.fb_id, 'I didn\'t understand your message. I was expecting to recieve an amount. One of our agents will help you shortly.')
					self.user.attempt_counter = 0
					self.user.save()
					return ''
				reply(self.user.fb_id, 'To pay {amount} at {merchant} send "y" or send the amount again'.format(amount=amount, merchant=merchant.name))
				self.user.attempt_counter == 3
				self.user.save()
				return ''
		elif self.user.attempt_counter == 2:
			merchant = Merchant.objects(merchant_id=message).first()
			if merchant:
				reply(self.user.fb_id, 'You are trying to make a payment at {}.\n If so please send us the amount, otherwise one of our agents will help you shortly'.format(merchant=self.merchant.name))
				self.user.attempt_counter = 3
				self.user.save()
				return ''
		elif self.user.attempt_counter == 3:
			if message.lower() == 'y':
				reply(self.user.fb_id, 'Thank you for using Nocapay. See you soon.')
				self.user.attempt_counter = 0
				self.user.save()
				return ''
			else:
				try:
					amount = float(message)
				except ValueError:
					reply(self.user.fb_id, 'I didn\'t understand your message. I was expecting to recieve an amount. One of our agents will help you shortly.')
					self.user.attempt_counter = 0
					self.user.save()
					return ''
				reply(self.user.fb_id, 'To pay {amount} at {merchant} send "y", otherwise one of our agents will help you shortly'.format(amount=amount, merchant=self.merchant.name))
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
