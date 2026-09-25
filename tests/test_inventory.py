import pytest

from models import Product, PerishableProduct

from inventory import Inventory

from storage import (
    save_json,
    load_json,
    save_csv,
    load_csv
)

from exceptions import (
    InvalidProductError,
    ProductNotFoundError,
    InsufficientStockError
)


def sample_inventory():

    inventory = Inventory()

    inventory.add_product(
        Product(
            "P1",
            "Keyboard",
            500,
            10
        )
    )

    inventory.add_product(
        PerishableProduct(
            "P2",
            "Milk",
            60,
            5,
            "2026-10-01"
        )
    )

    return inventory


def test_product_validation_and_methods():

    product = Product(
        "P1",
        "Pen",
        10,
        5
    )

    product.restock(3)
    product.sell(2)

    assert product.quantity == 6

    assert product.to_dict()["name"] == "Pen"

    with pytest.raises(InvalidProductError):
        Product("", "Pen", 10, 5)

    with pytest.raises(InvalidProductError):
        Product("P", "Pen", -1, 5)

    with pytest.raises(InvalidProductError):
        Product("P", "Pen", 10, -1)

    with pytest.raises(InvalidProductError):
        product.restock(0)

    with pytest.raises(InvalidProductError):
        product.sell(0)

    with pytest.raises(InvalidProductError):
        product.sell(100)


def test_perishable_product():

    product = PerishableProduct(
        "P2",
        "Milk",
        60,
        5,
        "2026-10-01"
    )

    assert product.to_dict()["type"] == "perishable"

    assert (
        product.to_dict()["expiry_date"]
        == "2026-10-01"
    )

    with pytest.raises(InvalidProductError):

        PerishableProduct(
            "P",
            "Milk",
            10,
            1,
            ""
        )


def test_inventory_operations():

    inventory = sample_inventory()

    assert (
        inventory.get_product("P1").name
        == "Keyboard"
    )

    inventory.restock("P1", 2)

    inventory.sell("P1", 5)

    assert (
        inventory.get_product("P1").quantity
        == 7
    )

    assert len(
        inventory.all_products()
    ) == 2

    with pytest.raises(ProductNotFoundError):

        inventory.get_product("BAD")

    with pytest.raises(ProductNotFoundError):

        inventory.remove_product("BAD")

    with pytest.raises(InsufficientStockError):

        inventory.sell("P1", 100)

    inventory.remove_product("P1")

    assert len(
        inventory.all_products()
    ) == 1


def test_json_and_csv_persistence(tmp_path):

    inventory = sample_inventory()

    json_file = tmp_path / "inventory.json"

    csv_file = tmp_path / "inventory.csv"

    save_json(
        inventory,
        json_file
    )

    save_csv(
        inventory,
        csv_file
    )

    loaded_json = load_json(
        json_file
    )

    loaded_csv = load_csv(
        csv_file
    )

    assert len(
        loaded_json.all_products()
    ) == 2

    assert (
        loaded_json
        .get_product("P2")
        .expiry_date
        == "2026-10-01"
    )

    assert len(
        loaded_csv.all_products()
    ) == 2

    assert (
        loaded_csv
        .get_product("P1")
        .quantity
        == 10
    )


def test_from_list_for_normal_product():

    inventory = Inventory.from_list([
        {
            "product_id": "P9",
            "name": "Book",
            "price": "100",
            "quantity": "3"
        }
    ])

    assert (
        inventory
        .get_product("P9")
        .quantity
        == 3
    )
