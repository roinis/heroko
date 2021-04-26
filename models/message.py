import sqlite3
from db.db import db
from datetime import datetime
from sqlalchemy import and_

class Message(db.Model):
    __tablename__ = "message"

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    message = db.Column(db.String(300))
    subject = db.Column(db.String(30))
    creation_date = db.Column(db.DateTime, default=datetime.now)
    read = db.Column(db.Boolean, default=False)

    def __init__(self,sender_id,receiver_id,message,subject):
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.message = message
        self.subject = subject
        self.creation_date = datetime.now()
        self.read = False


    def create_message(self):
        db.session.add(self)
        db.session.commit()


    @classmethod
    def get_message_by_id(cls,id):
        return cls.query.filter_by(receiver_id=id)

    @classmethod
    def get_unread_message_by_id(cls,id):
        return cls.query.filter(and_(cls.receiver_id==id, cls.read==False))

    @classmethod
    def read_message(cls,id):
        first_message = Message.query.filter(and_(cls.receiver_id==id, cls.read==False)).first()
        first_message.read = True
        db.session.commit()
        return first_message

    @classmethod
    def delete_message(cls,id ,message_id):
        message = cls.query.filter_by(id=message_id).first()
        try:
            if id == message.receiver_id or id == message.sender_id:
                db.session.delete(message)
                db.session.commit()
                return True
        except Exception as e:
            return False
        return False

    def json(self):
        return {"sender_id": self.sender_id,
                "receiver_id": self.receiver_id,
                "subject": self.subject,
                "message": self.message,
                "creation_date": self.creation_date.isoformat(),
                "read": self.read}
