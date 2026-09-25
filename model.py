from dataclasses import dataclass, asdict

from exceptions import InvalidProductError


@dataclass
class Product:
    product_id: str
    name: str
    price: float
    quantity: int

    def __post_init__(self):
        if not self.product_id.strip() or not self.name.strip():
            raise InvalidProductError(
                "Product ID and name are required."
            )

        if self.price < 0:
            raise InvalidProductError(
                "Price cannot be negative."
            )

        if self.quantity < 0:
            raise InvalidProductError(
                "Quantity cannot be negative."
            )

    def restock(self, amount: int):
        if amount <= 0:
            raise InvalidProductError(
                "Restock amount must be positive."
            )

        self.quantity += amount

    def sell(self, amount: int):
        if amount <= 0:
            raise InvalidProductError(
                "Sale quantity must be positive."
            )

        if amount > self.quantity:
            raise InvalidProductError(
                "Not enough stock."
            )

        self.quantity -= amount

    def to_dict(self):
        return asdict(self)


class PerishableProduct(Product):

    def __init__(
        self,
        product_id,
        name,
        price,
        quantity,
        expiry_date
    ):
        super().__init__(
            product_id,
            name,
            price,
            quantity
        )

        if not expiry_date.strip():
            raise InvalidProductError(
                "Expiry date is required."
            )

        self.expiry_date = expiry_date

    def to_dict(self):
        data = super().to_dict()

        data["expiry_date"] = self.expiry_date
        data["type"] = "perishable"

        return data
