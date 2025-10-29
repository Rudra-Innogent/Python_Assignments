from services.garment_service import GarmentService

class Helper:
    def __init__(self):
        self.service = GarmentService()

    def menu(self):
        while True:
            print("""
========= Garment Store =========
1. Add Garment
2. Display All Garments
3. Delete Garment
4. Update Stock
5. Stats Report (NumPy)
6. Exit
=================================
""")
            choice = input("Enter your choice: ").strip()

            if choice == "1":
                self.service.add_product()
            elif choice == "2":
                self.service.display_products()
            elif choice == "3":
                self.service.delete_product()
            elif choice == "4":
                self.service.update_stock()
            elif choice == "5":
                self.service.compute_stats()
            elif choice == "6":
                print("Exiting... Goodbye!")
                break
            else:
                print(" Invalid choice. Try again.\n")
