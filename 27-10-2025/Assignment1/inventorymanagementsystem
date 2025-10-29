

inventory = []


def printAll(inventory):
    if not inventory:
        print("Inventory is empty, please add products.")
        return

    print("\n" + "-" * 65)
    print(f"{'ID':<5} {'Name':<15} {'Stock':<10} {'Price (₹)':<12} {'Tag':<15}")
    print("-" * 65)

    for inventor in inventory:
        print(f"{inventor['Id']:<5} {inventor['name']:<15} {inventor['stock']:<10} {inventor['price']:<12.2f} {inventor['tag']:<15}")

    print("-" * 65)

def addProduct(inventory, product):
    
    for inventor in inventory:
        if inventor["Id"] == product["Id"] or inventor["name"] == product["name"]:
            print(" Product with this ID or Name already exists.")
            return
    inventory.append(product)
    print(f" Product '{product['name']}' added to inventory successfully.")


def updateInventory(inventory):
    while True:
        choice = input("1. Update Name\n2. Update Stock\n3. Update Product Price\n4. Exit\nEnter your choice: ")
        match choice:
            case '1':
                name = input("Enter product name to update: ")
                new_name = input("Enter new name: ")
                for inventor in inventory:
                    if inventor["name"] == name:
                        inventor["name"] = new_name
                        print("Name updated successfully.")
                        return
                print("Product not found.")

            case '2':
                pid = input("Enter product ID to update stock: ")
                new_stock = int(input("Enter new stock: "))
                for inventor in inventory:
                    if str(inventor["Id"]) == pid:
                        inventor["stock"] = new_stock
                        print("Stock updated successfully.")
                        return
                print("Product not found.")

            case '3':
                pid = input("Enter product ID to update price: ")
                new_price = float(input("Enter new price: "))
                for inventor in inventory:
                    if str(inventor["Id"]) == pid:
                        inventor["price"] = new_price
                        print("Price updated successfully.")
                        return
                print("Product not found.")

            case '4':
                print("Exiting update menu.")
                return
            case _:
                print("Invalid choice.")

def warning(inventory):
    for inventor in inventory:
        if inventor["stock"] <= 5:
            print(f" Warning: Stock for {inventor['name']} is low ({inventor['stock']} left).")


def buyProduct(inventory_list, product_id, quantity):
    found = False
    for inventor in inventory_list:
        if str(inventor["Id"]) == str(product_id) or inventor["name"] == product_id:
            found = True
            if inventor["stock"] >= quantity:
                if inventor["tag"]=="clearance":
                   purchase_total = ((inventor["price"]-(inventor["price"]*50)/100)) * quantity
                else:
                     purchase_total = inventor["price"] * quantity
                inventor["stock"] -= quantity
                print(f" Purchased {quantity} of {inventor['name']} for Price {purchase_total} ")
                warning(inventory_list)
            else:
                print(" Insufficient stock.")
            break
    if not found:
        print(" Product not found.")

def deleteProduct(inventory_list, product_id):
    for inventor in inventory_list:
        if str(inventor["Id"]) == str(product_id) or inventor["name"] == str(product_id):
            if inventor["stock"] == 0:
                inventory_list.remove(inventor)
                print(f" Product '{inventor['name']}' deleted successfully.")
                return
            else:
                print(" Cannot delete product with non-zero stock.")
                return
    print(" Product not found.")

def sumOfPrices(inventory_list):
    total = sum(i["price"] * i["stock"] for i in inventory_list)
    return total



def menu():
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
                printAll(inventory)

            case '2':
                pid = len(inventory) + 1
                name = input("Enter product name: ")
                stock = int(input("Enter product stock: "))
                price = float(input("Enter product price: "))
                tag = input("Enter product tag: ")
                product = {"Id": pid, "name": name, "stock": stock, "price": price, "tag": tag}
                addProduct(inventory, product)

            case '3':
                updateInventory(inventory)

            case '4':
                pid = input("Enter product name or ID: ")
                quantity = int(input("Enter quantity: "))
                buyProduct(inventory, pid, quantity)

            case '5':
                pid = input("Enter product name or ID to delete: ")
                deleteProduct(inventory, pid)

            case '6':
                total_price = sumOfPrices(inventory)
                print(f" Total inventory value: ₹{total_price}")

            case '7':
                print(" Exiting...")
                break

            case _:
                print(" Invalid choice. Try again.")



menu()
