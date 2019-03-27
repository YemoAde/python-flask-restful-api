from Database.db import Connection

class Item:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    @classmethod
    def create_item(cls, name, price):
        connection = Connection()
        query = "INSERT INTO items (name, price) values (?, ?)"
        connection.insert(query, (name, price))
        connection.close()
        return True

    @ classmethod
    def get_item(cls, name):
        connection = Connection()
        query = "SELECT * FROM items WHERE name = ?"
        result  = connection.select(query, (name,))
        connection.close()
        if result:
            return {
                'id': result[0],
                'name': result[1],
                'price': result[2]
            }
        else:
            return None
    
    @ classmethod
    def get_items(cls):
        connection = Connection()
        query = "SELECT * FROM items WHERE 1=1"
        results  = connection.select(query)
        connection.close()
        if results:
            return [{
                'id': result[0],
                'name': result[1],
                'price': result[2]
            } for result in results]
        else:
            return None

    @ classmethod
    def delete_item(cls, name):
        connection = Connection()
        query = "DELETE FROM items WHERE name=?"
        result  = connection.delete(query, (name,))
        connection.close()
        if result:
            return True
        else:
            return None