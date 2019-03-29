from flask import request
from flask_jwt_extended import fresh_jwt_required, jwt_required
from flask_restplus import Namespace, Resource, fields, reqparse
from Models.item import Item
from Util.response import ResponseHandler

item_ns = Namespace('item', description='Item related operations')
item = item_ns.model('item', {
    'name': fields.String(required=True, description='unique item name'),
    'price': fields.Float(required=True, description='item price'),
    'store_id': fields.Integer(required=True, description='Store ID'),
})

@item_ns.route('/<string:name>')
@item_ns.param('name', 'Unique Item name')
@item_ns.response(404, 'Item not found.')
class Items(Resource):

    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument('name', type=str, required=True, help="name field is missing")
    parser.add_argument('price', type=int, required=True, help="price field is missing")
    parser.add_argument('store_id', type=int, required=True, help="Item Store ID")

    @jwt_required
    @item_ns.doc('get an item')
    @item_ns.marshal_with(item)
    def get(self, name):
        item = Item.get_item(name)
        if item:
            return ResponseHandler.success('item', 200, data=item.json())
        return ResponseHandler.error('item not found', 404)
    
    def delete(self, name):
        item = Item.get_item(name)
        item.delete()
        return ResponseHandler.success('item_deleted', 200)

    def put(self, name):
        data = self.parser.parse_args()
        item = Item.get_item(name)
        if item is None:
            item = Item(name, data['price'], data['store_id'])
        else:
            item.price = data['price']
            item.store_id = data['store_id']
        item.save()

        return ResponseHandler.success('item_updated', 200, data=item.json())


@item_ns.route('')
class ItemList(Resource):

    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument('name', type=str, required=True, help="name field is missing")
    parser.add_argument('price', type=int, required=True, help="price field is missing")
    parser.add_argument('store_id', type=int, required=True, help="Item Store ID")

    @jwt_required
    def get(self):
        results = Item.get_items()
        if results:
            return ResponseHandler.success('items', ResponseHandler.OK, 
            data=[result.json() for result in results])
        return ResponseHandler.error('item not found', ResponseHandler.BAD_REQUEST)
    
    @item_ns.response(201, 'Item Added')
    @item_ns.response(400, 'Item Not Added')
    @item_ns.doc('create a new item')
    @item_ns.expect(item, validate=True)
    def post(self):
        # Check if name exists  
        data = ItemList.parser.parse_args()
        result = Item.get_item(data.name)
        if result:
            return ResponseHandler.error('item exists', ResponseHandler.BAD_REQUEST)
        
        item = Item(**data)
        item.save()
        
        return ResponseHandler.success('item added', 201, data=item.json())
