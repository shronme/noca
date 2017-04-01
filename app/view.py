import requests
from mongoengine import *
from flask.views import MethodView
from flask import request
from flask import current_app
from app.models.user import User



ACCESS_TOKEN = "EAAYquG24IwkBAPigmNaZC7zKpnbmrjcxLinW9FZCKqmTkuuoN3Jaddb505v9FCWZAZBc5exqutYRKRWZBzoSmsohrpQ0K0qV621GTk4FGaISlky6qN9Gjx07sXXHVvg5HaVkj0ZBbEyyjnbmlZAILoc3kXR5HjV0XfUjabVyhtnAAZDZD"

class WebhookView(MethodView):
	def post(self):
		data = request.json
		sender = data['entry'][0]['messaging'][0]['sender']['id']

		
		user = User.objects(fb_id=sender)

		if (user):
			self.reply(sender, 'Hi, thanks for coming back')
		else:
			user.fb_id = sender
			user.save()
			print('user id is: ', user.fb_id)
			self.reply(sender, 'Hi, thanks for showing interest in NoCa Pay.\nWould you like to register for our service?')


		print('the message is: ', data['entry'][0]['messaging'][0]['message'])
		try:
		    message = data['entry'][0]['messaging'][0]['message']['text']

		except KeyError:
		    self.reply(sender, 'oops, something went wrong')
		    return 'ok'
		try:
		    self.reply(sender, 'Your message backwards is {}'.format(message[::-1]))
		except UnicodeEncodeError:
		    self.reply(sender, 'oops, something went wrong')
		    return 'ok'

		return 'ok'

	def get(self):
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
	


	def reply(self, user_id, msg):
	    data = {
	        "recipient": {"id": user_id},
	        "message": {"text": msg}
	    }
	    resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, json=data)
	    print(resp.content)


	# def handle_incoming_messages(self):
	#     data = request.json
	#     sender = data['entry'][0]['messaging'][0]['sender']['id']
	#     print('the message is: ', data['entry'][0]['messaging'][0]['message'])
	#     try:
	#         message = data['entry'][0]['messaging'][0]['message']['text']

	#     except KeyError:
	#         reply(sender, 'oops, something went wrong')
	#         return 'ok'
	#     try:
	#         reply(sender, 'Your message backwards is {}'.format(message[::-1]))
	#     except UnicodeEncodeError:
	#         reply(sender, 'oops, something went wrong')
	#         return 'ok'

	#     return "ok"

	def handle_verification(self):
	    return request.args['hub.challenge']