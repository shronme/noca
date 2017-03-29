from flask import Flask
from flask_bcrypt import Bcrypt
import os




def create_app():

    app = Flask(__name__)

    try:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('POSTGRES_CONNECTION') + os.environ.get('SQLALCHEMY_DATABASE_URI')
    except TypeError:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ron:admin@localhost/test'

    print 'app.config[SQLALCHEMY_DATABASE_URI] =', app.config['SQLALCHEMY_DATABASE_URI']

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SALT'] = '3W8y%,pP@)'
    app.app_context().push()
    init_views(app)
    app.bcrypt = Bcrypt(app)
    return app
