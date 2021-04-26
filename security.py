from models.user import User


def authenticate(username, password):
    user = User.get_username_by_name(username=username)
    if user and user.password == password:
        return user



def identity(payload):
    user_id = payload['identity']
    return User.get_username_by_name(user_id)