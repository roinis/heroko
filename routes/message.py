from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from flask_jwt_extended.utils import get_jwt_identity
from models.message import Message
import datetime
class MessageAPI(Resource):


    @jwt_required()
    def get(self,message_id=None):
        user = get_jwt_identity()
        query_params = dict(request.args)
        if not query_params:
            return {"error": True, "message": "wrong params"}, 404
        try:
            if 'all' in query_params:
                print()
            if 'all' in query_params and query_params['all'].lower() == "true":
                return jsonify([message.json() for message in Message.get_message_by_id(id=user['id'])]), 200
            elif 'unread' in query_params and query_params['unread'].lower() == "true":
                return jsonify([message.json() for message in Message.get_unread_message_by_id(id=user['id'])]), 200
            elif 'read' in query_params and query_params['read'].lower() == "true":
                return Message.read_message(id=user['id']).json(), 200
        except AttributeError as e:
            return {"error": False, "message": "There is no messages for this query"}, 404

        return {"error": True, "message": "wrong params"}, 401

    @jwt_required()
    def post(self,message_id=None):
        current_user = get_jwt_identity()
        user_json = request.get_json()
        if user_json is None or 'receiver_id' not in user_json:
            return {"error": True, "message": "wrong params"}, 404
        new_message = Message(sender_id=current_user['id'],receiver_id=user_json['receiver_id'],message=user_json['message'],subject=user_json['subject'])
        Message.create_message(new_message)
        return {"error": False, "message": "message created"}, 200

    @jwt_required()
    def delete(self,message_id=None):
        user = get_jwt_identity()
        if not message_id:
            return {"error": True, "message": "wrong params"}, 404
        if Message.delete_message(id=user['id'],message_id=message_id):
            return {"error": False, "message": "Message deleted successfully"}, 200
        return {"error": True, "message": "Could not delete message"}, 404

