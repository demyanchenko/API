from utils import json_to_dict_list, dict_list_to_json

class Product:
    def __init__(self, title, price, quantity):
        self.id = str(uuid.uuid4())
        self.title = title
        self.price = price
        self.quantity = quantity


# для поиска продукта в списке products
def find_products(id):
    for product in products:
        if product["id"] == id:
            return product
    return None