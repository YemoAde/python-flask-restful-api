from flask_jwt_extended import jwt_required
from flask_restplus import Namespace, Resource, fields, reqparse
from flask import request
from Models.store import Store
from Util.response import ResponseHandler

store_ns = Namespace('store', description='Item related operations')
store = store_ns.model('store', {
    'name': fields.String(required=True, description='unique item name'),
})

@store_ns.route('/<string:name>')
@store_ns.param('name', 'Unique Item name')
@store_ns.response(404, 'Item not found.')
class Stores(Resource):
    @jwt_required
    @store_ns.doc('get a store')
    @store_ns.marshal_with(store)
    def get(self, name):
        store = Store.get_item(name)
        if store:
            return ResponseHandler.success('store', 200, data=store.json())
        return ResponseHandler.error('store not found', 404)
    
    def delete(self, name):
        store = Store.get_item(name)
        store.delete()
        return ResponseHandler.success('store deleted', 200)

    def put(self, name):
        data = request.json()
        store = Store.get_item(name)
        if store is None:
            store = Store(name)
        else:
            store.name = data['name']

        return ResponseHandler.success('store updated', 200, data=store.json())

@store_ns.route('')
class StoreList(Resource):

    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument('name', type=str, required=True, help="name field is missing")

    @jwt_required
    def get(self):
        results = Store.get_items()
        if results:
            return ResponseHandler.success('stores', ResponseHandler.OK, 
            data=[result.json() for result in results])
        return ResponseHandler.error('stores not found', ResponseHandler.BAD_REQUEST)


    @store_ns.response(201, 'Store Added')
    @store_ns.response(400, 'Store Not Added')
    @store_ns.doc('create a new store')
    @store_ns.expect(store, validate=True)
    def post(self):
        # Check if name exists  
        data = StoreList.parser.parse_args()
        result = Store.get_item(data.name)
        if result:
            return ResponseHandler.error('store exists', ResponseHandler.BAD_REQUEST)
        
        store = Store(**data)
        store.save()
        
        return ResponseHandler.success('store added', 201, data=store.json())