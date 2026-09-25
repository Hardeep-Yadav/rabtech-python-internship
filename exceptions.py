class InventoryError(Exception):
    """Base exception for inventory errors."""


class InvalidProductError(InventoryError):
    """Raised when product data is invalid."""


class ProductNotFoundError(InventoryError):
    """Raised when a product does not exist."""


class InsufficientStockError(InventoryError):
    """Raised when requested stock exceeds available stock."""
