import random
import pandas as pd

from generator.config import OUTPUT_DIR

from generator.business_rules.data_quality import inject_inventory_quality
from generator.utils import (
    create_directory,
    save_csv,
    save_excel,
    generate_id,
    random_date
)

from generator.business_rules.inventory import (
    generate_stock_status,
    generate_stock_quantity
)

random.seed(42)

# Load the data

products_df = pd.read_csv(
    f"{OUTPUT_DIR}/master/products.csv"
)

stores_df = pd.read_csv(
    f"{OUTPUT_DIR}/master/stores.csv"
)

# Basic Validation

if products_df.empty:

    raise ValueError(
        "products.csv is empty."
    )


if stores_df.empty:

    raise ValueError(
        "stores.csv is empty."
    )


# Required product column.

required_product_columns = [
    "ProductID",
    "ReorderLevel"
]

for column in required_product_columns:

    if column not in products_df.columns:

        raise KeyError(
            f"products.csv is missing required column: {column}"
        )


# Required store column.

required_store_columns = [
    "StoreID"
]

for column in required_store_columns:

    if column not in stores_df.columns:

        raise KeyError(
            f"stores.csv is missing required column: {column}"
        )


print(
    f"Loaded {len(products_df)} products."
)

print(
    f"Loaded {len(stores_df)} stores."
)


# Generate inventory.

def generate_inventory():

    records = []

    print(
        "Generating inventory records..."
    )

    inventory_number = 1

    # Create inventory for products and store.

    for _, product in products_df.iterrows():

        product_id = product["ProductID"]

        reorder_level = product["ReorderLevel"]

        for _, store in stores_df.iterrows():

            store_id = store["StoreID"]

            stock_status = generate_stock_status()

            stock_quantity = generate_stock_quantity(
                stock_status,
                reorder_level
            )

            inventory_date = random_date(
                "2024-01-01",
                "2025-12-31"
            ).date()

            last_restock_date = random_date(
                "2023-01-01",
                "2025-12-31"
            ).date()

            # Inventory records

            records.append({

                "InventoryID": generate_id(
                    "INV",
                    inventory_number,
                    digits=6
                ),

                "ProductID": product_id,

                "StoreID": store_id,

                "StockQuantity": stock_quantity,

                "StockStatus": stock_status,

                "InventoryDate": inventory_date,

                "LastRestockDate": last_restock_date

            })

            inventory_number += 1

    # Create dataframe

    inventory_df = pd.DataFrame(
        records
    )


    # Basic Validation

    if inventory_df.empty:

        raise ValueError(
            "No inventory records were generated."
        )


    # Iventory id validation.

    if inventory_df[
        "InventoryID"
    ].duplicated().any():

        raise ValueError(
            "Duplicate InventoryID detected."
        )


    # Product ID validation.

    valid_product_ids = set(
        products_df["ProductID"]
    )

    invalid_product_ids = (
        ~inventory_df["ProductID"].isin(
            valid_product_ids
        )
    )

    if invalid_product_ids.any():

        raise ValueError(
            "Inventory contains invalid ProductID values."
        )


    # Store validation id.

    valid_store_ids = set(
        stores_df["StoreID"]
    )

    invalid_store_ids = (
        ~inventory_df["StoreID"].isin(
            valid_store_ids
        )
    )

    if invalid_store_ids.any():

        raise ValueError(
            "Inventory contains invalid StoreID values."
        )


    # Stock quantity validation.

    if (
        inventory_df["StockQuantity"] < 0
    ).any():

        raise ValueError(
            "Inventory contains negative stock quantities."
        )


    # Stock status validation.

    valid_statuses = {
        "In Stock",
        "Low Stock",
        "Out of Stock"
    }

    invalid_statuses = (
        ~inventory_df["StockStatus"].isin(
            valid_statuses
        )
    )

    if invalid_statuses.any():

        raise ValueError(
            "Inventory contains invalid stock status values."
        )


    # Save clean inventory.

    create_directory(
        f"{OUTPUT_DIR}/master"
    )

    save_csv(
        inventory_df,
        f"{OUTPUT_DIR}/master/inventory.csv"
    )

    save_excel(
        inventory_df,
        f"{OUTPUT_DIR}/master/inventory.xlsx"
    )

    inventory_raw_df = inject_inventory_quality(
                inventory_df.copy()
            )

    # save dirty inventory data.
    create_directory(
            f"{OUTPUT_DIR}/master"
        )
    
    save_csv(
            inventory_raw_df,
            f"{OUTPUT_DIR}/raw/inventory_raw.csv"
        )
    
    save_excel(
            inventory_raw_df,
            f"{OUTPUT_DIR}/raw/inventory_raw.xlsx"
        )


    # Summary

    print(
        f"Generated "
        f"{len(inventory_df)} inventory records."
    )

    print(
        f"Products represented: "
        f"{inventory_df['ProductID'].nunique()}"
    )

    print(
        f"Stores represented: "
        f"{inventory_df['StoreID'].nunique()}"
    )

    print(
        "Stock status distribution:"
    )

    print(
        inventory_df[
            "StockStatus"
        ].value_counts()
    )

    # summary

    print(
        "Inventory saved successfully."
    )

    print(
            "Clean inventory data saved successfully."
        )
    
    print(
            "Raw inventory data saved successfully."
        )


    return inventory_df


# Summary

if __name__ == "__main__":

    generate_inventory()