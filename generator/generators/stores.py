import random
import pandas as pd
from generator.config import OUTPUT_DIR
from generator.utils import create_directory, save_csv, save_excel, generate_id, random_date

counties_df = pd.read_csv(f"generator/reference_data/counties.csv")
towns_df = pd.read_csv(f"generator/reference_data/towns.csv")

RETAIL_CHAINS = {
    "Naivas": 50,
    "Tuskys": 30,
    "Quickmart": 35,
    "Carrefour": 15,
    "Chandarana": 10,
    "cleanshelf": 12,
    "eastmart": 28,
    "Magunas": 20,
}

STORE_TYPES = {
    "Hypermarket": (8000, 10000),
    "Supermarket": (3000, 5000),
    "express": (1000, 2000)
}

STORE_TYPES_WEIGHTS = {
    "Hypermarket": 0.1,
    "Supermarket": 0.3,
    "express": 0.6
}

def generate_stores():
    records = []
    store_number = 1
    used_locations = set()
    for chain, number_of_branches in RETAIL_CHAINS.items():
        for _ in range(number_of_branches):
            while True:
                towns = towns_df.sample(1).iloc[0]
                county = towns['County']
                town_name = towns['Town']
                key = (chain, county, town_name)
                if key not in used_locations:
                    used_locations.add(key)
                    break
                region = counties_df.loc[
                    counties_df['County'] == county, 'Region'
                ].values[0]
                store_type = random.choices(
                    population=list(STORE_TYPES_WEIGHTS.keys()),
                    weights=list(STORE_TYPES_WEIGHTS.values()),
                    k=1
                )[0]
                minimum, maximum = STORE_TYPES[store_type]
                floor_area = random.randint(minimum, maximum)
                records.append({
                    "store_id": generate_id("STR", store_number),
                    "store_name": f"{chain} {town_name} Branch",
                    "retail_chain": chain,
                    "store_type": store_type,
                    "floor_area_sqm": floor_area,
                    "county": county,
                    "region": region,
                    "town": town_name,
                    "created_date": random_date("2015-01-01", "2020-01-01").date(),
                    "last_updated_date": random_date("2020-01-02", "2025-12-31").date(),
                    "is_active": True
                })
                    
                store_number += 1
                df = pd.DataFrame(records)
                create_directory(f"{OUTPUT_DIR}/master")
                save_csv(df, f"{OUTPUT_DIR}/master/stores.csv")
                save_excel(df, f"{OUTPUT_DIR}/master/stores.xlsx")
                print(f"Generated {len(df)} stores and saved to {OUTPUT_DIR}/master/stores.csv and stores.xlsx")

                return df