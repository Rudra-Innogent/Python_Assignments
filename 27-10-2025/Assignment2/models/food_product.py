from models.product import Product

class FoodProduct(Product):
    def __init__(self, product_id, name, stock, price, tag):
        super().__init__(product_id, name, stock, price, tag)
