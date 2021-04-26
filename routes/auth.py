from flask import request, jsonify
from flask_restful import Resource
from models.user import User
from flask_jwt_extended import create_access_token,set_access_cookies,unset_jwt_cookies

class AuthAPI(Resource):

    def get(self):
        response = jsonify({"error":False,"message": "logout successful"})
        unset_jwt_cookies(response)
        return response

    def post(self):
        user_json = request.get_json()
        if user_json is None or 'username' not in user_json or 'password' not in user_json:
            return {"error":True, "message": "wrong params"}, 404

        nuser = User.get_username_by_name(user_json['username'])
        if nuser.password != user_json['password']:
            return {"error":True, "message": "wrong crednitals"}, 404

        response = jsonify({"error":False, "message": "Logged in"})
        access_token = create_access_token(identity=nuser.json())
        set_access_cookies(response, access_token)
        return response
