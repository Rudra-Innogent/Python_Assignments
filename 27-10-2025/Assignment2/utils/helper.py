from services.inventory_service import InventoryService

class Helper:
    def __init__(self):
        self.service = InventoryService()

    def menu(self):
        while True:
            print("\n1. Print All")
            print("2. Add Product")
            print("3. Update Inventory")
            print("4. Buy Product")
            print("5. Delete Product")
            print("6. Total Price of all products")
            print("7. Exit")

            choice = input("Enter your choice: ")

            match choice:
                case '1':
                    self.service.print_all()
                case '2':
                    name = input("Enter product name: ")
                    stock = int(input("Enter product stock: "))
                    price = float(input("Enter product price: "))
                    tag = input("Enter product tag: ")
                    self.service.add_product(name, stock, price, tag)
                case '3':
                    self.service.update_inventory()
                case '4':
                    pid = input("Enter product name or ID: ")
                    quantity = int(input("Enter quantity: "))
                    self.service.buy_product(pid, quantity)
                case '5':
                    pid = input("Enter product name or ID to delete: ")
                    self.service.delete_product(pid)
                case '6':
                    self.service.total_value()
                case '7':
                    print("Exiting...")
                    break
                case _:
                    print("Invalid choice. Try again.")
