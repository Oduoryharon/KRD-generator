import pandas as pd
import random
from datetime import datetime, timedelta
from generator.config import OUTPUT_DIR, NUM_PROMOTIONS
from generator.utils import create_directory, save_csv, save_excel, generate_id, random_date

def generate_promotions():
    promotions = pd.read_csv(f"generator/reference_data/promotions.csv")
    records = []
    selected_promotions = promotions.sample(n=NUM_PROMOTIONS,replace=True)
    

    for promotion_number, (_, promotion) in enumerate(
        selected_promotions.iterrows(),
        start=1):

        promotion_name = promotion["PromotionName"]
        start_str = promotion["start_date"]
        end_str = promotion["end_date"]
        discount_type = promotion["PromotionType"]
        min_discount = int(promotion["MinDiscount"])
        max_discount = int(promotion["MaxDiscount"])


        year = random.randint(2020, 2025)

        start_date = datetime.strptime(f"{year}-{start_str}", "%Y-%m-%d")

        if start_str > end_str:
            end_date = datetime.strptime(f"{year + 1}-{end_str}", "%Y-%m-%d")
        else:
            end_date = datetime.strptime(f"{year}-{end_str}", "%Y-%m-%d")   

        discount_value = random.randint(min_discount, max_discount)

        records.append({
            "promotion_id": generate_id("PROMO", promotion_number),
            "promotion_name": promotion_name,
            "discount_type": discount_type,
            "Discount_value": discount_value,
            "start_date": start_date.date(),
            "end_date": end_date.date(),
            "is_active": True
        })

    
    df = pd.DataFrame(records)
    create_directory(f"{OUTPUT_DIR}/master")
    save_csv(df, f"{OUTPUT_DIR}/master/promotions.csv")
    save_excel(df, f"{OUTPUT_DIR}/master/promotions.xlsx")  
    print(f"Generated {len(df)} promotions and saved to {OUTPUT_DIR}/master/promotions.csv and promotions.xlsx")
    return df

if __name__ == "__main__":
    generate_promotions()


