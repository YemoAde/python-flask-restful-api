from flask_jwt_extended import jwt_required, fresh_jwt_required
from flask_restplus import Namespace, Resource, fields, reqparse
from Models.item import Item
from Util.response import ResponseHandler

item_ns = Namespace('item', description='Item related operations')
item = item_ns.model('item', {
    'name': fields.String(required=True, description='unique item name'),
    'price': fields.Float(required=True, description='item price'),
})

@item_ns.route('/<string:name>')
@item_ns.param('name', 'Unique Item name')
@item_ns.response(404, 'Item not found.')
class Items(Resource):
    @jwt_required
    @item_ns.doc('get an item')
    @item_ns.marshal_with(item)
    def get(self, name):
        result = Item.get_item(name)
        if result:
            return ResponseHandler.success('item', 200, data=result)
        return ResponseHandler.error('item not found', 404)
    
    def delete(self, name):
        if Item.delete_item(name):
            return ResponseHandler.success('item', 200)
        return ResponseHandler.error('item not found', 404)

    def put(self, name):
        pass


@item_ns.route('')
class ItemList(Resource):

    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument('name', type=str, required=True, help="name field is missing")
    parser.add_argument('price', type=int, required=True, help="price field is missing")

    @jwt_required
    def get(self):
        results = Item.get_items()
        if results:
            return ResponseHandler.success('items', ResponseHandler.OK, data=results)
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
        
        item = Item.create_item(data.name, data.price)
        if item:
            return ResponseHandler.success('item added', 201)
        return ResponseHandler.error('item not added', 400)
