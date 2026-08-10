import pandas as pd
from generator.config import STARTDATE, ENDDATE, OUTPUT_DIR

from generator.utils import create_directory, save_csv, save_excel, generate_id, random_date

# initializing the different categories with their respective attributes
CATEGORY_DATA = [

    # Grocery
    ("Grocery", "Food", 16, False),

    # Fresh Foods
    ("Dairy", "Fresh Foods", 0, True),
    ("Bakery", "Fresh Foods", 0, True),
    ("Fresh Produce", "Fresh Foods", 0, True),
    ("Meat & Poultry", "Fresh Foods", 0, True),
    ("Fish & Seafood", "Fresh Foods", 0, True),

    # Frozen
    ("Frozen Foods", "Frozen", 16, True),

    # Drinks
    ("Beverages", "Beverages", 16, False),
    ("Juices", "Beverages", 16, False),
    ("Water", "Beverages", 0, False),
    ("Tea & Coffee", "Beverages", 16, False),

    # Snacks
    ("Snacks", "Snacks", 16, False),
    ("Confectionery", "Snacks", 16, False),

    # Household
    ("Cleaning Supplies", "Household", 16, False),
    ("Laundry", "Household", 16, False),
    ("Kitchenware", "Household", 16, False),

    # Personal Care
    ("Personal Care", "Health & Beauty", 16, False),
    ("Baby Care", "Health & Beauty", 16, False),
    ("Health & Pharmacy", "Health & Beauty", 16, False),

    # Other Departments
    ("Stationery", "Office", 16, False),
    ("Electronics", "Electronics", 16, False),
    ("Pet Care", "Pets", 16, False)
]

# creating a function to generate categories and save them to CSV and Excel files

def generate_categories():

    records = []
    for index, category in enumerate(CATEGORY_DATA, start=1):
        category_id = generate_id("CAT", index)
        category_name, category_type, tax_rate, is_perishable = category
        records.append({
            "CategoryID": category_id,
            "CategoryName": category_name,
            "CategoryType": category_type,
            "VATRate": tax_rate,
            "IsPerishable": is_perishable,
            "CreatedDate": random_date(STARTDATE, "2020-01-01").date(),
            "LastUpdatedDate": random_date("2025-12-31", ENDDATE).date(),
            "IsActive": True
        })
    df = pd.DataFrame(records)
    create_directory(f"{OUTPUT_DIR}/master")
    save_csv(df, f"{OUTPUT_DIR}/master/categories.csv")
    save_excel(df, f"{OUTPUT_DIR}/master/categories.xlsx")
    print(f"Generated {len(df)} categories and saved to {OUTPUT_DIR}/master/categories.csv and categories.xlsx")

if __name__ == "__main__":
    generate_categories()