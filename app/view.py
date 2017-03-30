import requests
from flask.views import MethodView
from flask import request



ACCESS_TOKEN = "EAAYquG24IwkBAPigmNaZC7zKpnbmrjcxLinW9FZCKqmTkuuoN3Jaddb505v9FCWZAZBc5exqutYRKRWZBzoSmsohrpQ0K0qV621GTk4FGaISlky6qN9Gjx07sXXHVvg5HaVkj0ZBbEyyjnbmlZAILoc3kXR5HjV0XfUjabVyhtnAAZDZD"

class WebhookView(MethodView):
	def post(self):
		data = request.json
		sender = data['entry'][0]['messaging'][0]['sender']['id']
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