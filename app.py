from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

# save internally for testing
items = []


class Item(Resource):
    def get(self, name):
        for item in items:
            if item['name'] == name:
                return item
        return {"item": None}, 404  # error code for not found is 404

    def post(self, name):
        data = request.get_json()

        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201  # created code


class Items(Resource):
    def get(self):
        return {"items": items}


api.add_resource(Item, '/item/<string:name>')
api.add_resource(Items, '/items')

app.run(port=5000, debug=True)