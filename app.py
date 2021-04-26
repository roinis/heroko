from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from routes.message import MessageAPI
from routes.user import UserAPI
from routes.auth import AuthAPI
from db.db import db
from security import authenticate,identity
import datetime
import create_tables



create_tables.create_base_tables()
app = Flask(__name__)
api = Api(app)
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_ACCESS_COOKIE_NAME'] = 'remember_token'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(seconds=1800)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = datetime.timedelta(days=15)
app.config['JWT_COOKIE_SECURE'] = False
app.config['JWT_COOKIE_CSRF_PROTECT'] = False
app.secret_key = 'roi123'


# /auth
jwt = JWTManager(app)


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

db.init_app(app)
api.add_resource(AuthAPI,'/auth')
api.add_resource(MessageAPI,'/message','/message/<int:message_id>')
api.add_resource(UserAPI,'/user','/user/<string:username>')

if __name__ == '__main__':
    app.run(port=5000)
