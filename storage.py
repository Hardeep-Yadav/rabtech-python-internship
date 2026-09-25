import csv
import json

from inventory import Inventory


def save_json(inventory, filename):

    with open(
        filename,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            inventory.to_list(),
            file,
            indent=4
        )


def load_json(filename):

    with open(
        filename,
        "r",
        encoding="utf-8"
    ) as file:

        data = json.load(file)

    return Inventory.from_list(data)


def save_csv(inventory, filename):

    rows = inventory.to_list()

    fieldnames = [
        "product_id",
        "name",
        "price",
        "quantity",
        "expiry_date",
        "type"
    ]

    with open(
        filename,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()

        for row in rows:

            writer.writerow({
                field: row.get(field, "")
                for field in fieldnames
            })


def load_csv(filename):

    rows = []

    with open(
        filename,
        "r",
        newline="",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            item = {
                "product_id": row["product_id"],
                "name": row["name"],
                "price": row["price"],
                "quantity": row["quantity"]
            }

            if row.get("expiry_date"):

                item["expiry_date"] = row["expiry_date"]
                item["type"] = "perishable"

            rows.append(item)

    return Inventory.from_list(rows)
