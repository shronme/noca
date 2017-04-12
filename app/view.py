import requests
from mongoengine import *
from flask.views import MethodView
from flask import request
from flask import current_app
from app.models.user import User
from app.states.replies import reply
from app.states.user_states import *



ACCESS_TOKEN = "EAAYquG24IwkBAPigmNaZC7zKpnbmrjcxLinW9FZCKqmTkuuoN3Jaddb505v9FCWZAZBc5exqutYRKRWZBzoSmsohrpQ0K0qV621GTk4FGaISlky6qN9Gjx07sXXHVvg5HaVkj0ZBbEyyjnbmlZAILoc3kXR5HjV0XfUjabVyhtnAAZDZD"

class WebhookView(MethodView):
	

	def post(self):
		data = request.json
		sender = data['entry'][0]['messaging'][0]['sender']['id']
		fb_user = requests.get('https://graph.facebook.com/v2.6/' + str(sender) + '?access_token=' + ACCESS_TOKEN)
		print('fb user is: ', fb_user.json())
		user = User.objects(fb_id=sender).first()

		# self.reply(sender, 'Hi {}, thanks for coming back'.format(
		# 	fb_user.json()['first_name']))
		if not user:
			user = User(fb_id=sender,state='new_user', name=fb_user.json()['first_name'],attempt_counter=0)
			user.save()
		if not user.state:
			user.state = 'new_user'
			user.save()


		print('user state is: ', user.state)
		state = states_dict[user.state](user)

		print('the message is: ', data['entry'][0]['messaging'][0]['message'])
		
		if 'message' in data['entry'][0]['messaging'][0].keys():
			if 'text' in data['entry'][0]['messaging'][0]['message'].keys():
				message = data['entry'][0]['messaging'][0]['message']['text']
		elif 'postback' in data['entry'][0]['messaging'][0].keys():
			message = in data['entry'][0]['messaging'][0]['postback']['payload']
		else:
			reply(sender, 'oops, something went wrong')
			return 'ok'

		response = state.run(data)
		while response:
			if user.state != response:
				user.state = response
				user.save()

				print('user state is: ', user.state)
				state = states_dict[user.state](user)
		
			response = state.run(data)


		print('user id is: ', user.fb_id)
		
		try:
			self.reply(sender, 'Your message backwards is {}'.format(message[::-1]))
		except UnicodeEncodeError:
			self.reply(sender, 'oops, something went wrong')
			return 'ok'

		return 'ok'

	def get(self):
		return request.args['hub.challenge']

	def reply(self, user_id, msg):
	    data = {
	        "recipient": {"id": user_id},
	        "message": {"text": msg}
	    }
	    resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, json=data)
	    print(resp.content)

	def handle_verification(self):
	    return request.args['hub.challenge']

    
