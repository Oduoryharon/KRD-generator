import random
import pandas as pd

from generator.config import (
    OUTPUT_DIR,
    NUM_INVENTORY_RECORDS
)

from generator.utils import (
    create_directory,
    save_csv,
    save_excel,
    generate_id,
    random_date
)

random.seed(42)

# =====================================================
# LOAD MASTER DATA
# =====================================================

products_df = pd.read_csv(
    f"{OUTPUT_DIR}/master/products.csv"
)

stores_df = pd.read_csv(
    f"{OUTPUT_DIR}/master/stores.csv"
)

# =====================================================
# HELPER FUNCTIONS
# =====================================================

def generate_batch_number(number):
    """
    Generate inventory batch number.
    Example: BAT000001
    """
    return f"BAT{number:06d}"


def generate_quantity(category):
    """
    Generate realistic quantity depending on category.
    """

    ranges = {

        "Grocery": (150, 600),
        "Dairy": (20, 120),
        "Bakery": (15, 80),
        "Fresh Produce": (20, 150),
        "Meat & Poultry": (10, 80),
        "Fish & Seafood": (10, 60),
        "Frozen Foods": (20, 120),

        "Beverages": (200, 1000),
        "Juices": (120, 600),
        "Water": (300, 1500),
        "Tea & Coffee": (60, 300),

        "Snacks": (80, 400),
        "Confectionery": (100, 500),

        "Cleaning Supplies": (40, 250),
        "Laundry": (40, 250),
        "Kitchenware": (10, 80),

        "Personal Care": (40, 200),
        "Baby Care": (20, 120),
        "Health & Pharmacy": (20, 100),

        "Stationery": (30, 200),
        "Electronics": (2, 20),
        "Pet Care": (10, 80)

    }

    minimum, maximum = ranges.get(category, (20, 100))

    return random.randint(minimum, maximum)


def calculate_safety_stock(reorder_level):
    """
    Safety stock is 50% of reorder level.
    """
    return max(5, int(reorder_level * 0.5))


def determine_stock_status(quantity, reorder_level):

    if quantity == 0:
        return "Out of Stock"

    elif quantity <= reorder_level:
        return "Low Stock"

    else:
        return "In Stock"


def calculate_inventory_value(quantity, unit_cost):

    return round(quantity * unit_cost, 2)


def generate_expiry_date(
    manufacture_date,
    shelf_life_days,
    is_perishable
):
    """
    Generate expiry date for perishable products only.
    """

    if not is_perishable:
        return None

    return manufacture_date + pd.Timedelta(
        days=int(shelf_life_days)
    )

# =====================================================
# GENERATE INVENTORY
# =====================================================

def generate_inventory():

    print("Loading master data...")

    records = []

    used_pairs = set()

    inventory_number = 1

    while len(records) < NUM_INVENTORY_RECORDS:

        # ------------------------------------------
        # Select Product
        # ------------------------------------------

        product = products_df.sample(1).iloc[0]

        # ------------------------------------------
        # Select Store
        # ------------------------------------------

        store = stores_df.sample(1).iloc[0]

        product_id = product["ProductID"]
        store_id = store["StoreID"]

        # Prevent duplicate Product-Store combination

        pair = (product_id, store_id)

        if pair in used_pairs:
            continue

        used_pairs.add(pair)

        # ------------------------------------------
        # Product Information
        # ------------------------------------------

        product_name = product["ProductName"]

        category = product["CategoryName"]

        cost_price = float(product["CostPrice"])

        reorder_level = int(product["ReorderLevel"])

        shelf_life = int(product["ShelfLifeDays"])

        is_perishable = bool(product["IsPerishable"])

        # ------------------------------------------
        # Store Information
        # ------------------------------------------

        store_name = store["StoreName"]

        # ------------------------------------------
        # Generated Values
        # ------------------------------------------

        batch_number = generate_batch_number(
            inventory_number
        )

        quantity = generate_quantity(
            category
        )

        safety_stock = calculate_safety_stock(
            reorder_level
        )

        inventory_value = calculate_inventory_value(
            quantity,
            cost_price
        )

        stock_status = determine_stock_status(
            quantity,
            reorder_level
        )

        manufacture_date = random_date(
            "2024-01-01",
            "2025-06-30"
        )

        expiry_date = generate_expiry_date(
            manufacture_date,
            shelf_life,
            is_perishable
        )

        last_restock = random_date(
            "2025-01-01",
            "2025-12-31"
        )

        # ------------------------------------------
        # Inventory Record
        # ------------------------------------------

        records.append({

            "InventoryID": generate_id(
                "INV",
                inventory_number,
                digits=6
            ),

            "ProductID": product_id,

            "ProductName": product_name,

            "StoreID": store_id,

            "StoreName": store_name,

            "BatchNumber": batch_number,

            "QuantityOnHand": quantity,

            "ReorderLevel": reorder_level,

            "SafetyStock": safety_stock,

            "UnitCost": cost_price,

            "InventoryValue": inventory_value,

            "ManufacturingDate": manufacture_date,

            "ExpiryDate": expiry_date,

            "LastRestockDate": last_restock,

            "StockStatus": stock_status

        })

        inventory_number += 1

            # =====================================================
    # CREATE DATAFRAME
    # =====================================================

    inventory_df = pd.DataFrame(records)

    # =====================================================
    # VALIDATION
    # =====================================================

    if inventory_df.empty:
        raise ValueError("No inventory records generated.")

    if inventory_df["InventoryID"].duplicated().any():
        raise ValueError("Duplicate InventoryID detected.")

    if inventory_df.duplicated(
        subset=["ProductID", "StoreID"]
    ).any():
        raise ValueError(
            "Duplicate Product-Store combination found."
        )

    # =====================================================
    # SORT DATA
    # =====================================================

    inventory_df = inventory_df.sort_values(
        by=["StoreID", "ProductID"]
    ).reset_index(drop=True)

    # =====================================================
    # SAVE FILES
    # =====================================================

    create_directory(f"{OUTPUT_DIR}/master")

    save_csv(
        inventory_df,
        f"{OUTPUT_DIR}/master/inventory.csv"
    )

    save_excel(
        inventory_df,
        f"{OUTPUT_DIR}/master/inventory.xlsx"
    )

    print(
        f"Generated {len(inventory_df)} inventory records successfully."
    )

    return inventory_df


# =====================================================
# MAIN
# =====================================================

if __name__ == "__main__":
    generate_inventory()
