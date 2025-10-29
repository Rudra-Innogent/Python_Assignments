from models.food_product import FoodProduct

class InventoryService:
    def __init__(self):
        self.inventory = []

    def print_all(self):
        if not self.inventory:
            print("Inventory is empty, please add products.")
            return

        print("\n" + "-" * 65)
        print(f"{'ID':<5} {'Name':<15} {'Stock':<10} {'Price (₹)':<12} {'Tag':<15}")
        print("-" * 65)
        for product in self.inventory:
            print(product)
        print("-" * 65)

    def add_product(self, name, stock, price, tag):
        new_id = len(self.inventory) + 1
        for p in self.inventory:
            if p.name == name or p.product_id == new_id:
                print("Product with this ID or Name already exists.")
                return
        product = FoodProduct(new_id, name, stock, price, tag)
        self.inventory.append(product)
        print(f"Product '{name}' added successfully.")

    def update_inventory(self):
        while True:
            choice = input("1. Update Name\n2. Update Stock\n3. Update Price\n4. Exit\nEnter choice: ")
            match choice:
                case '1':
                    name = input("Enter product name to update: ")
                    new_name = input("Enter new name: ")
                    for p in self.inventory:
                        if p.name == name:
                            p.name = new_name
                            print("Name updated successfully.")
                            return
                    print("Product not found.")
                case '2':
                    pid = input("Enter product ID: ")
                    new_stock = int(input("Enter new stock: "))
                    for p in self.inventory:
                        if str(p.product_id) == pid:
                            p.stock = new_stock
                            print("Stock updated successfully.")
                            return
                    print("Product not found.")
                case '3':
                    pid = input("Enter product ID: ")
                    new_price = float(input("Enter new price: "))
                    for p in self.inventory:
                        if str(p.product_id) == pid:
                            p.price = new_price
                            print("Price updated successfully.")
                            return
                    print("Product not found.")
                case '4':
                    print("Exiting update menu.")
                    return
                case _:
                    print("Invalid choice.")

    def warning(self):
        for p in self.inventory:
            if p.stock <= 5:
                print(f"Warning: Stock for {p.name} is low ({p.stock} left).")

    def buy_product(self, product_id_or_name, quantity):
        for p in self.inventory:
            if str(p.product_id) == str(product_id_or_name) or p.name == product_id_or_name:
                if p.stock >= quantity:
                    if p.tag.lower() == "clearance":
                        total = (p.price - (p.price * 0.5)) * quantity
                    else:
                        total = p.price * quantity
                    p.stock -= quantity
                    print(f"Purchased {quantity} of {p.name} for ₹{total:.2f}")
                    self.warning()
                else:
                    print("Insufficient stock.")
                return
        print("Product not found.")

    def delete_product(self, product_id_or_name):
        for p in self.inventory:
            if str(p.product_id) == str(product_id_or_name) or p.name == product_id_or_name:
                if p.stock == 0:
                    self.inventory.remove(p)
                    print(f"Product '{p.name}' deleted successfully.")
                else:
                    print("Cannot delete product with non-zero stock.")
                return
        print("Product not found.")

    def total_value(self):
        total = sum(p.price * p.stock for p in self.inventory)
        print(f"Total inventory value: ₹{total:.2f}")
