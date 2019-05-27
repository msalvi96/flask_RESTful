from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
            
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!",
    )
    parser.add_argument('store_id',
        type=int,
        required=True,
        help="Every Item needs a Store ID!",
    )

    @jwt_required()
    def get(self, name):
        try:
            item = ItemModel.find_by_name(name)
        except:
            return {'message': 'Search Query Failed!'}, 500
        
        if item:
            return item.json()

        return {'message': 'Item not found!'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': f'An item with name {name} already exists'}, 400


        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'], data['store_id'])
        
        try:
            ItemModel.save_to_db(item)

        except:
            return {'message': 'Internal Server Error!'}, 500

        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            try:
                item.delete_from_db()

            except:
                return {'message': 'Internal Server Error!'}, 500

            return {'message': 'Item deleted'}, 

        else:
            return {'message': 'Item not found!'}, 404

    def put(self, name):

        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, data['price'], data['store_id'])
        else:
            item.price = data['price']

        item.save_to_db()
        
        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}