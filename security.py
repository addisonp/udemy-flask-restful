from user import User
from werkzeug.security import safe_str_cmp

# users = [
#     {
#         'id': 1,
#         'username': 'bob',
#         'password': 'asdf'
#     }
# ]

# create a class to store the user data
users = [
    User(1, 'bob', 'asdf')
]

# then we can use dict comprehension
username_mapping = {u.username: u for u in users}

# username_mapping = {'bob': {
#     'id': 1,
#     'username': 'bob',
#     'password': 'asdf'
# }}

userid_mapping = {u.id: u for u in users}


# userid_mapping = {1: {
#     'id': 1,
#     'username': 'bob',
#     'password': 'asdf'
# }}

# function to get the user details without having to iterate over the users list
def authenticate(username, password):
    user = username_mapping.get(username, None)
    # if user and user.password == password:
    # python 2.7, not safe to use == for string comparision, use safe_str_cmp to not worry about encodings
    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload):
    user_id = payload['identity']
    return userid_mapping.get(user_id, None)
