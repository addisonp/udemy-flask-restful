from models.users import UserModel
from werkzeug.security import safe_str_cmp


# function to get the user details without having to iterate over the users list
def authenticate(username, password):
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
