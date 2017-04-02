import requests
from mongoengine import *
from flask.views import MethodView
from flask import request
from flask import current_app
from app.models.user import User
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
			user = User(fb_id=sender,state='new_user', name=fb_user.json()['first_name'])
			user.save()
		if not user.state:
			user.state = 'new_user'
			user.save()
		
		print('user state is: ', user.state)
		state = states_dict[user.state](user)

		print('the message is: ', data['entry'][0]['messaging'][0]['message'])
		
		try:
			message = data['entry'][0]['messaging'][0]['message']['text']
		except KeyError:
			self.reply(sender, 'oops, something went wrong')
			return 'ok'

		response = state.run(message)
		user.state = state.next_state()
		user.save()
		print('user id is: ', user.fb_id)
		self.reply(sender, 
		response)

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

    
# data = {
# 	        "recipient": {"id": user_id},
# 	        'message': {
# 		        'attachment': {
# 		        	'type': "template",
# 		        	'payload': {
# 		        		'template_type': "generic",
# 		        		'elements': [{
# 			        		'title': "rift",
# 			        		'subtitle': "Next-generation virtual reality",
# 			        		'item_url': "https://www.oculus.com/en-us/rift/",
# 			        		'image_url': "http://messengerdemo.parseapp.com/img/rift.png",
# 			        		'buttons': [{
# 			        			'type': "web_url",
# 			        			'url': "https://www.oculus.com/en-us/rift/",
# 			        			'title': "Open Web URL"
# 		        			}, 
# 		        			{
# 		        				'type': "postback",
# 		        				'title': "Call Postback",
# 		        				'payload': "Payload for first bubble",
# 	    				}],
# 						}, 
# 						{
# 							'title': "touch",
# 							'subtitle': "Your Hands, Now in VR",
# 							'item_url': "https://www.oculus.com/en-us/touch/",
# 							'image_url': "http://messengerdemo.parseapp.com/img/touch.png",
# 							'buttons': [{
# 								'type': "web_url",
# 								'url': "https://www.oculus.com/en-us/touch/",
# 								'title': "Open Web URL"
# 							}, 
# 							{
# 								'type': "postback",
# 								'title': "Call Postback",
# 								'payload': "Payload for second bubble",
# 							}]
# 						}]
# 					}
# 				}
# 		    }
# 	    }
	

