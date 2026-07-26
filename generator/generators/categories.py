import pandas as pd
from generator.config import STARTDATE, ENDDATE, OUTPUT_DIR

from generator.utils import create_directory, save_csv, save_excel, generate_id, random_date

# initializing the different categories with their respective attributes
CATEGORY_DATA = [
    ("Maize Flour", "Grocery", 0, False),
    ("Rice", "Grocery", 16, False),
    ("Sugar", "Grocery", 16, False),
    ("Cooking Oil", "Grocery", 16, False),
    ("Salt", "Grocery", 16, False),
    ("Milk", "Fresh Foods", 16, True),
    ("Yoghurt", "Fresh Foods", 16, True),
    ("Cheese", "Fresh Foods", 16, True),
    ("Butter", "Fresh Foods", 16, True),
    ("Bread", "Bakery", 16, True),
    ("Cakes", "Bakery", 16, True),
    ("Soft Drinks", "Beverages", 16, False),
    ("Juices", "Beverages", 16, False),
    ("Water", "Beverages", 0, False),
    ("Tea", "Beverages", 16, False),
    ("Coffee", "Beverages", 16, False),
    ("Cleaning Supplies", "Household", 16, False),
    ("Laundry", "Household", 16, False),
    ("Toiletries", "Personal Care", 16, False),
    ("Baby Care", "Personal Care", 16, False),
    ("Stationery", "Office", 16, False),
    ("Electronics", "Electronics", 16, False),
    ("Kitchenware", "Home", 16, False),
    ("Pet Food", "Pets", 16, False),
    ("Frozen Foods", "Frozen", 16, True)
]

# creating a function to generate categories and save them to CSV and Excel files

def generate_categories():

    records = []
    for index, category in enumerate(CATEGORY_DATA, start=1):
        category_id = generate_id("CAT", index)
        category_name, category_type, tax_rate, is_perishable = category
        records.append({
            "category_id": category_id,
            "category_name": category_name,
            "category_type": category_type,
            "tax_rate": tax_rate,
            "is_perishable": is_perishable,
            "created_date": random_date(STARTDATE, "2020-01-01").date(),
            "Last_updated_date": random_date("2025-12-31", ENDDATE).date(),
            "is_active": True
        })
    df = pd.DataFrame(records)
    create_directory(f"{OUTPUT_DIR}/master")
    save_csv(df, f"{OUTPUT_DIR}/master/categories.csv")
    save_excel(df, f"{OUTPUT_DIR}/master/categories.xlsx")
    print(f"Generated {len(df)} categories and saved to {OUTPUT_DIR}/master/categories.csv and categories.xlsx")