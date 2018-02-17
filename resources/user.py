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

        user = UserModel(**data)
        user.save_to_db()

        return {"message": "user created successfully."}, 201
