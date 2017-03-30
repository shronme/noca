from flask import Flask
from flask_bcrypt import Bcrypt
import os

from view import WebhookView


ACCESS_TOKEN = "EAAYquG24IwkBAPigmNaZC7zKpnbmrjcxLinW9FZCKqmTkuuoN3Jaddb505v9FCWZAZBc5exqutYRKRWZBzoSmsohrpQ0K0qV621GTk4FGaISlky6qN9Gjx07sXXHVvg5HaVkj0ZBbEyyjnbmlZAILoc3kXR5HjV0XfUjabVyhtnAAZDZD"


def reply(user_id, msg):
    data = {
        "recipient": {"id": user_id},
        "message": {"text": msg}
    }
    resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, json=data)
    print(resp.content)


def handle_incoming_messages():
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

    return "ok"

def handle_verification():
    return request.args['hub.challenge']

def create_app():
    header_text = '''
    <html>\n<head> <title>EB Flask Test</title> </head>\n<body>'''
    instructions = '''
        <p><em>Hint</em>: Nocapay is coming soon!!.</p>\n'''
    home_link = '<p><a href="/">Back</a></p>\n'
    footer_text = '</body>\n</html>'

    app = Flask(__name__)

    # try:
    #     app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('POSTGRES_CONNECTION') + os.environ.get('SQLALCHEMY_DATABASE_URI')
    # except TypeError:
    #     app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ron:admin@localhost/test'

    # print 'app.config[SQLALCHEMY_DATABASE_URI] =', app.config['SQLALCHEMY_DATABASE_URI']

    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # app.config['SALT'] = '3W8y%,pP@)'
    # app.app_context().push()
    # init_views(app)
    # app.bcrypt = Bcrypt(app)


    # EB looks for an 'application' callable by default.
    # application = Flask(__name__)

    # add a rule for the pagez.
    app.add_url_rule('/', 'index', (lambda: header_text +
        instructions + footer_text))
    
    app.add_url_rule('/webhook', view_func=WebhookView.as_view('webhook_view'))


    return app
