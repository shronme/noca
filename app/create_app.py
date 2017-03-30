from flask import Flask
import os

from view import WebhookView


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
