from flask import Flask
from mongoengine import *
from app.view import WebhookView, AuthenticateView
from app.models.merchant import Merchant


def create_mock_merchant():
    merchant = Merchant.objects(merchant_id='12345').first()
    if not merchant:
        merchant = Merchant(merchant_id='12345', name='Noca Store')
        merchant.save()

def create_app():
    header_text = '''
    <html>\n<head> <title>EB Flask Test</title> </head>\n<body>'''
    instructions = '''
        <p>Nocapay is coming soon!!.</p>\n'''
    home_link = '<p><a href="/">Back</a></p>\n'
    footer_text = '</body>\n</html>'

    app = Flask(__name__)

    app.db = connect('noca_db', host='mongodb://ec2-52-209-229-216.eu-west-1.compute.amazonaws.com', port=27017)
    create_mock_merchant()
    # add a rule for the pagez.
    app.add_url_rule('/', 'index', (lambda: header_text +
        instructions + footer_text))
    
    app.add_url_rule('/webhook', view_func=WebhookView.as_view('webhook_view'))
    app.add_url_rule('/authenticate', view_func=AuthenticateView.as_view('authenticate_view'))
    

    return app

