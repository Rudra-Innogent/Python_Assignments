class Product:
    def __init__(self, product_id, name, stock, price, tag):
        self.product_id = product_id
        self.name = name
        self.stock = stock
        self.price = price
        self.tag = tag

    def __str__(self):
        return f"{self.product_id:<5} {self.name:<15} {self.stock:<10} {self.price:<12.2f} {self.tag:<15}"
