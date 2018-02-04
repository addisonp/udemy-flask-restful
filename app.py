from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'jose'
api = Api(app)

jwt = JWT(app, authenticate, identity)  # JWT creates a new end point /auth
# we send /auth a username/password and that is sent to the authenticate function
# if the u/p is valid the authenticate returns the user and that becomes the identity
# the auth endpoint returns a JWT token

# we can send the JWT token to the next request that we make
# when we send a JWT token, is that the JWT calls the identity function and uses the JWT token
#   to get the userid and the correct user for the userid that the JWT token represents
#   if it can do that, then the user was authenticated, the JWT token is valid
#   this is done with flask_jwt.jwt_required

# save internally for testing
items = []


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    @jwt_required()
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        # return {"item": item}, 200 if it is not None else 404
        return {"item": item}, 200 if item else 404
        # for item in items:
        #     if item['name'] == name:
        #         return item
        # return {"item": None}, 404  # error code for not found is 404


    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None):
            return {'message': f"An item with name: \'{name}\' already exists"}, 400  # bad request

        # data = request.get_json()
        data = Item.parser.parse_args()

        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201  # created code

    def delete(self, name):
        global items
        # this will overwrite the items by a new list that does not contain the name we want deleted
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'Item deleted'}

    def put(self, name):
        # parser = reqparse.RequestParser()  # run the request through it
        # list all possible arguments that we will be keeping/using
        # if the argument is not listed in the parser.add_arguments, it will be erased and not saved
        # parser.add_argument('price',
        #                     type=float,
        #                     required=True,
        #                     help="This field cannot be left blank!"
        #                     )

        # data = request.get_json()
        # we moved the previous parser setup and add_arguments up to the Item class level
        data = Item.parser.parse_args()

        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)
        return item


class Items(Resource):
    def get(self):
        return {"items": items}


api.add_resource(Item, '/item/<string:name>')
api.add_resource(Items, '/items')

app.run(port=5000, debug=True)
