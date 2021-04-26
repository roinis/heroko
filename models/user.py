from db.db import db


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(30), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    @classmethod
    def get_username_by_name(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def get_username_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def create_username(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        return {"id":self.id,"username":self.username, "password":self.password}


