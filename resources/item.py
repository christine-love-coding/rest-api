import sys
sys.path.append("/Users/christinewang/rest_api_course")



from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from section6.code.models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()  # initiate an object which we can use to parse the request
    parser.add_argument('price',
                        type=str,
                        required=True,
                        help='This field cannot be left blank')
    # add_argument tells parser to find the argument that we add
    # required= True: no request can come through without a price
    # it will look JSON payload and form payload

    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help='Every item needs a store id')

    # define the method the resource has, eg. get, post, delete, etc

    @jwt_required()
    # this means we have to authenticate before we call the get method
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "item already exists"}, 400

        data = Item.parser.parse_args() # this will parse the argument that come through JSON payload.

        item = ItemModel(name, data['price'], data['store_id'])

        try:
            item.save_to_db()
        except:
            return {'message': "An error occurred inserting the item"}, 500
        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': 'Item deleted.'}
        return {'message': 'Item does not exists.'}, 400


    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
            item.store_id = data['store_id']

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        items = ItemModel.query.all()
        return {'items': [item.json() for item in items]}, 200