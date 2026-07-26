import pandas as pd
from datetime import datetime, timedelta
from generator.config import OUTPUT_DIR
from generator.utils import create_directory, save_csv, save_excel, generate_id, random_date

def generate_promotions():
    promotions = pd.read_csv(f"generator/reference_data/promotions.csv")
    records = []
    promotion_number = 1
     # Promotion calendar
    promotion_dates = {

        "Back to School": ("01-05", "01-31"),

        "Valentine's Sale": ("02-08", "02-14"),

        "Easter Deals": ("03-20", "04-05"),

        "Labour Day Sale": ("04-28", "05-05"),

        "Madaraka Sale": ("05-28", "06-05"),

        "Mid-Year Sale": ("07-01", "07-20"),

        "August School Rush": ("08-01", "08-25"),

        "Mashujaa Sale": ("10-10", "10-25"),

        "Black Friday": ("11-20", "11-30"),

        "Christmas Mega Sale": ("12-10", "12-31"),

        "New Year Sale": ("12-26", "01-10"),

        "Ramadan Specials": ("03-10", "04-10"),

        "Customer Loyalty Week": ("09-10", "09-17")

    }
    for year in range(2020, 2026):
        for promotion_name, (start_str, end_str) in promotion_dates.items():
            start_date = datetime.strptime(f"{year}-{start_str}", "%Y-%m-%d")
            end_date = datetime.strptime(f"{year}-{end_str}", "%Y-%m-%d")
            records.append({
                "promotion_id": generate_id("PROMO", promotion_number),
                "promotion_name": promotion_name,
                "start_date": start_date.date(),
                "end_date": end_date.date(),
                "is_active": True
            })
            promotion_number += 1
            df = pd.DataFrame(records)
            create_directory(f"{OUTPUT_DIR}/master")
            save_csv(df, f"{OUTPUT_DIR}/master/promotions.csv")
            save_excel(df, f"{OUTPUT_DIR}/master/promotions.xlsx")  
            print(f"Generated {len(df)} promotions and saved to {OUTPUT_DIR}/master/promotions.csv and promotions.xlsx")
            return df


