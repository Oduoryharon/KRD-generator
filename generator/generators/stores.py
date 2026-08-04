import random
import pandas as pd

from generator.config import OUTPUT_DIR, NUM_STORES
from generator.utils import (
    create_directory,
    save_csv,
    save_excel,
    generate_id,
    random_date
)

random.seed(42)

# =====================================================
# LOAD REFERENCE DATA
# =====================================================

counties_df = pd.read_csv(
    "generator/reference_data/counties.csv"
)

towns_df = pd.read_csv(
    "generator/reference_data/towns.csv"
)

# =====================================================
# RETAIL CHAINS
# =====================================================

RETAIL_CHAINS = [
    "Naivas",
    "Tuskys",
    "Quickmart",
    "Carrefour",
    "Chandarana",
    "Cleanshelf",
    "Eastmatt",
    "Magunas"
]

# =====================================================
# STORE TYPES
# =====================================================

STORE_TYPES = {
    "Hypermarket": (8000, 10000),
    "Supermarket": (3000, 5000),
    "Express": (1000, 2000)
}

STORE_TYPE_WEIGHTS = {
    "Hypermarket": 0.10,
    "Supermarket": 0.30,
    "Express": 0.60
}

# =====================================================
# GENERATE STORES
# =====================================================

def generate_stores():

    records = []

    used_locations = set()

    store_number = 1

    for _ in range(NUM_STORES):

        chain = random.choice(RETAIL_CHAINS)

        # -----------------------------------------
        # Pick unique location for this chain
        # -----------------------------------------

        while True:

            town_row = towns_df.sample(1).iloc[0]

            county = town_row["County"]
            town = town_row["Town"]

            key = (chain, county, town)

            if key not in used_locations:

                used_locations.add(key)

                break

        # -----------------------------------------
        # Region
        # -----------------------------------------

        region = counties_df.loc[
            counties_df["County"] == county,
            "Region"
        ].iloc[0]

        # -----------------------------------------
        # Store Type
        # -----------------------------------------

        store_type = random.choices(

            population=list(STORE_TYPE_WEIGHTS.keys()),

            weights=list(STORE_TYPE_WEIGHTS.values()),

            k=1

        )[0]

        minimum_area, maximum_area = STORE_TYPES[store_type]

        floor_area = random.randint(
            minimum_area,
            maximum_area
        )

        # -----------------------------------------
        # Store Record
        # -----------------------------------------

        records.append({

            "StoreID": generate_id(
                "STR",
                store_number
            ),

            "StoreName": f"{chain} {town} Branch",

            "RetailChain": chain,

            "StoreType": store_type,

            "FloorAreaSQM": floor_area,

            "County": county,

            "Region": region,

            "Town": town,

            "CreatedDate": random_date(
                "2015-01-01",
                "2020-01-01"
            ),

            "LastUpdatedDate": random_date(
                "2020-01-02",
                "2025-12-31"
            ),

            "IsActive": True

        })

        store_number += 1

    # =====================================================
    # CREATE DATAFRAME
    # =====================================================

    stores_df = pd.DataFrame(records)

    # =====================================================
    # VALIDATION
    # =====================================================

    if stores_df.empty:
        raise ValueError("No stores were generated.")

    if stores_df["StoreID"].duplicated().any():
        raise ValueError("Duplicate StoreID detected.")

    # =====================================================
    # SAVE FILES
    # =====================================================

    create_directory(f"{OUTPUT_DIR}/master")

    save_csv(
        stores_df,
        f"{OUTPUT_DIR}/master/stores.csv"
    )

    save_excel(
        stores_df,
        f"{OUTPUT_DIR}/master/stores.xlsx"
    )

    print(
        f"Generated {len(stores_df)} stores successfully."
    )

    return stores_df


# =====================================================
# MAIN
# =====================================================

if __name__ == "__main__":
    generate_stores()