import sqlite3
from flask_jwt import jwt_required
from flask_restful import Resource, reqparse


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
        item = self.find_by_name(name)
        if item:
            return item
        return {'message': f'Item [{name}] not found'}, 400

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'item': {'name': row[0], 'price': row[1]}}

    def post(self, name):
        if self.find_by_name(name):
            return {'message': f"An item with name: \'{name}\' already exists"}, 400  # bad request

        # data = request.get_json()
        data = Item.parser.parse_args()

        item = {'name': name, 'price': data['price']}
        try:
            self.insert(item)
        except:
            return {"message": "An error occurred inserting the item."}, 500 #internal server error

        return item, 201  # created code

    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (?,?)"

        cursor.execute(query, (item['name'], item['price']))

        connection.commit()
        connection.close()

    @classmethod
    def update(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE items SET price=? WHERE name=?"

        cursor.execute(query, (item['price'], item['name']))

        connection.commit()
        connection.close()

    def delete(self, name):
        if self.find_by_name(name):
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            query = "DELETE FROM items WHERE name=?"
            cursor.execute(query, (name,))

            connection.commit()
            connection.close()
            return {'message': 'Item deleted'}
        else:
            return {
                       'message': f"An item with name: \'{name}\' cannot be deleted, it does not exist"}, 400  # bad request

    def put(self, name):
        data = Item.parser.parse_args()
        item = self.find_by_name(name)
        updated_item = {'name':name, 'price':data['price']}
        if item is None:
            try:
                self.insert(updated_item)
            except:
                return {"message":"An error occurred inserting the item."}, 500
        else:
            try:
                self.update(updated_item)
            except:
                return {"message":"An error occurred updating the item."}, 500
        return updated_item




class Items(Resource):
    def get(self):
        return {"items": items}
