from flask.views import MethodView
 

class WebhookView(MethodView):
	def post(self):
		data = request.json
		sender = data['entry'][0]['messaging'][0]['sender']['id']
		print('the message is: ', data['entry'][0]['messaging'][0]['message'])
		try:
		    message = data['entry'][0]['messaging'][0]['message']['text']

		except KeyError:
		    reply(sender, 'oops, something went wrong')
		    return 'ok'
		try:
		    reply(sender, 'Your message backwards is {}'.format(message[::-1]))
		except UnicodeEncodeError:
		    reply(sender, 'oops, something went wrong')
		    return 'ok'

		return 'ok'

	def get(self):
		return request.args['hub.challenge']