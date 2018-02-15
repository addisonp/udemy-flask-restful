import sqlite3
from flask_restful import Resource, reqparse

from models.users import UserModel


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

        if UserModel.find_by_username(data['username']):
            return {"message": "user with that username already exists"}, 400

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
