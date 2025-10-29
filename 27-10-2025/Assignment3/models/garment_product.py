from product import Product

class GarmentProduct(Product):
    def __init__(self, product_id, name, stock, price, tag, size, fabric):
        super().__init__(product_id, name, stock, price, tag)
        self.size = size
        self.fabric = fabric

    def __str__(self):
        base = super().__str__()
        return f"{base} {self.size:<10} {self.fabric:<10}"
