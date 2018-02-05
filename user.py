import sqlite3
from flask_restful import Resource, reqparse

class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username=?"
        # need to pass a tuple (value,)
        result = cursor.execute(query, (username,))

        row = result.fetchone()
        if row:
            user = cls(*row)# we can use #row since row[0] is the id, row[1] is the username and #row[2] is the password
        else:
            user = None

        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE id=?"
        # need to pass a tuple (value,)
        result = cursor.execute(query, (_id,))

        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user

    # tested with POSTMAN where the Header contains a key: Authorization
    # and a value: JWT <token>
    # <token> is retrieved from /auth where we pass the u/p


class UserRegister(Resource):

    # parser will parse through the JSON of the request
    parser = reqparse.RequestParser()
    # and verify that both u/p exist
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="Username required"
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="Password required"
                        )

    def post(self):
        # parse the arguements (parse_args)
        # using the UserRegister.parser
        # which expects a u/p
        data = UserRegister.parser.parse_args()
        # then connect to the database
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        # insert the values into the table users
        # with NULL as the id, so it auto-increments
        # and then a u/p
        query = "INSERT INTO users VALUES (NULL, ?, ?)"
        # the u/p must be in a TUPLE
        cursor.execute(query, (data['username'], data['password']))

        connection.commit()
        connection.close()

        return {"message": "user created successfully."}, 201
