import numpy as np
from models.garment_product import GarmentProduct

class GarmentService:
    def __init__(self):
        self.products = []

    def add_product(self):
        try:
            pid = int(input("Enter Product ID: "))
            name = input("Enter Name: ")
            stock = int(input("Enter Stock: "))
            price = float(input("Enter Price: "))
            tag = input("Enter Tag (e.g., new, clearance, festival): ")
            size = input("Enter Size: ")
            fabric = input("Enter Fabric Type: ")

            product = GarmentProduct(pid, name, stock, price, tag, size, fabric)
            self.products.append(product)
            print(" Garment added successfully!\n")
        except ValueError:
            print(" Invalid input. Please enter correct data types.\n")

    def display_products(self):
        if not self.products:
            print(" No garments found.\n")
            return

        print(f"\n{'ID':<5} {'Name':<15} {'Stock':<10} {'Price':<12} {'Tag':<15} {'Size':<10} {'Fabric':<10}")
        print("-" * 80)
        for p in self.products:
            print(p)
        print()

    def delete_product(self):
        pid = int(input("Enter Product ID to delete: "))
        for p in self.products:
            if p.product_id == pid:
                self.products.remove(p)
                print(" Product deleted successfully!\n")
                return
        print(" Product not found.\n")

    def update_stock(self):
        pid = int(input("Enter Product ID to update stock: "))
        for p in self.products:
            if p.product_id == pid:
                try:
                    new_stock = int(input("Enter new stock quantity: "))
                    p.stock = new_stock
                    print(" Stock updated successfully!\n")
                    return
                except ValueError:
                    print(" Invalid stock value.\n")
                    return
        print(" Product not found.\n")

    def compute_stats(self):
        if not self.products:
            print(" No garments to analyze.\n")
            return

        prices = np.array([p.price for p in self.products])
        stocks = np.array([p.stock for p in self.products])
        values = prices * stocks

        print("\n=== Statistics Report ===")
        print(f"Average Price: ₹{np.mean(prices):.2f}")
        print(f"Most Expensive Item Price: ₹{np.max(prices):.2f}")
        print(f"Total Count of All Items in Stock: {np.sum(stocks)}")
        print("\nTotal Inventory Value per Product:")
        for p in self.products:
            print(f"{p.name:<15} ₹{p.price * p.stock:.2f}")

        tag = input("\nEnter tag to compute specific stats (e.g., 'clearance'): ").strip()
        tagged_products = [p for p in self.products if p.tag == tag]
        if tagged_products:
            t_prices = np.array([p.price for p in tagged_products])
            t_values = np.array([p.price * p.stock for p in tagged_products])
            print(f"\n=== Stats for Tag '{tag}' ===")
            print(f"Average Price: ₹{np.mean(t_prices):.2f}")
            print(f"Total Value: ₹{np.sum(t_values):.2f}")
        else:
            print(f"No products found with tag '{tag}'.")
        print()
