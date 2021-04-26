from flask import request, jsonify
from flask_restful import Resource
from models.user import User

class UserAPI(Resource):
    # @login_required()
    def get(self,username=None):
        if not username:
            return {"error":True, "message": "wrong params"}
        user_to_find = User.get_username_by_name(username)
        return user_to_find.json(), 200

    # @login_required()
    def post(self,username=None):
        user_json = request.get_json()
        if user_json is None or 'username' not in user_json or 'password' not in user_json:
            return {"error":True, "message": "wrong params"}, 404
        new_user = User(username=user_json['username'], password=user_json['password'])
        new_user.create_username()
        return {"error":False, "message": "user created"}, 201
