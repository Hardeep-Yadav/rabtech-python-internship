from models import Product, PerishableProduct

from exceptions import (
    ProductNotFoundError,
    InsufficientStockError
)


class Inventory:

    def __init__(self):
        self._products = {}

    def add_product(self, product):
        self._products[product.product_id] = product

    def get_product(self, product_id):

        if product_id not in self._products:
            raise ProductNotFoundError(
                f"Product {product_id} not found."
            )

        return self._products[product_id]

    def remove_product(self, product_id):

        if product_id not in self._products:
            raise ProductNotFoundError(
                f"Product {product_id} not found."
            )

        del self._products[product_id]

    def restock(self, product_id, amount):
        product = self.get_product(product_id)
        product.restock(amount)

    def sell(self, product_id, amount):

        product = self.get_product(product_id)

        if amount > product.quantity:
            raise InsufficientStockError(
                "Requested quantity is greater than available stock."
            )

        product.sell(amount)

    def all_products(self):
        return list(self._products.values())

    def to_list(self):
        return [
            product.to_dict()
            for product in self.all_products()
        ]

    @classmethod
    def from_list(cls, data):

        inventory = cls()

        for item in data:

            if (
                item.get("type") == "perishable"
                or "expiry_date" in item
            ):

                product = PerishableProduct(
                    item["product_id"],
                    item["name"],
                    float(item["price"]),
                    int(item["quantity"]),
                    item["expiry_date"]
                )

            else:

                product = Product(
                    item["product_id"],
                    item["name"],
                    float(item["price"]),
                    int(item["quantity"])
                )

            inventory.add_product(product)

        return inventory
