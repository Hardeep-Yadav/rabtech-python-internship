from models import Product, PerishableProduct
from inventory import Inventory

from storage import (
    save_json,
    load_json,
    save_csv,
    load_csv
)

from exceptions import InventoryError


def main():

    inventory = Inventory()

    try:

        # Normal product
        keyboard = Product(
            "P001",
            "Keyboard",
            799.0,
            10
        )

        # Inherited product
        milk = PerishableProduct(
            "P002",
            "Milk",
            60.0,
            20,
            "2026-10-01"
        )

        inventory.add_product(keyboard)
        inventory.add_product(milk)

        # Restock
        inventory.restock("P001", 5)

        # Sell
        inventory.sell("P001", 2)

        # Save data
        save_json(
            inventory,
            "inventory.json"
        )

        save_csv(
            inventory,
            "inventory.csv"
        )

        # Load data
        loaded_json = load_json(
            "inventory.json"
        )

        loaded_csv = load_csv(
            "inventory.csv"
        )

        print("Inventory saved successfully.")

        print(
            "JSON products:",
            len(loaded_json.all_products())
        )

        print(
            "CSV products:",
            len(loaded_csv.all_products())
        )

    except InventoryError as error:

        print(
            "Inventory error:",
            error
        )


if __name__ == "__main__":
    main()
