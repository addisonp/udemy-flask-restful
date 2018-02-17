from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    # only argument that will be passed is the one listed below
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': f'Item [{name}] not found'}, 400

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': f"An item with name: \'{name}\' already exists"}, 400  # bad request

        # data = request.get_json()
        data = Item.parser.parse_args()

        item = ItemModel(name, data['price'])
        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500  # internal server error

        return item.json(), 201  # created code

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': "Item deleted"}

    def put(self, name):

        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, data['price'])
        else:
            item.price = data['price']
        item.save_to_db()

        return item.json()


class Items(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]} #list comprehension version
        # return {'items': list(map(lambda x: x.jsion(), ItemModel.query.all()))}
