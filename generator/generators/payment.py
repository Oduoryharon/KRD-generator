import random
from generator.config import OUTPUT_DIR
import pandas as pd

from generator.business_rules.data_quality import inject_payment_quality

from generator.utils import (
    create_directory,
    save_csv,
    save_excel,
    generate_id
)

random.seed(42)

# Load data
sales_df =pd.read_csv( f"{OUTPUT_DIR}/transaction/sales.csv")


# Basic Validation
if sales_df.empty:
    raise ValueError( "Empty sales.csv")


# reuired sales columns
required_sales_columns = [
    "SaleID",
    "SalesDateTime",
    "PaymentMethod",
    "SaleStatus"
]

for column in required_sales_columns:
    if column not in sales_df.columns:
        raise KeyError (f"sales is missing required column: {column}")

# Required sales details columns

print(f"Loaded {len(sales_df)} sales.")



PAYMENT_STATUS = [
    "Completed",
    "Failed",
    "Pending",
    "Reversed"
]

def generate_payment_status(sale_status):
    # cacelled sales

    if str(sale_status).lower() == "cancelled":
        return random.choices(
            PAYMENT_STATUS,
            weights= [
                15,
                10,
                5,
                70
            ],
            k=1
        )[0]

    # Refunded sales
    if str(sale_status).lower() == "refunded":
        return random.choices(
            PAYMENT_STATUS,
            weights= [
                20,
                5,
                5,
                70
            ],
            k=1
        )[0]

    # Normal completed sales
    return random.choices(
        PAYMENT_STATUS,
        weights= [
            97,
            1,
            1,
            1
        ],
        k=1
    )[0]

def generate_payment_reference(payment_number, payment_method):
    method = str(payment_method).strip().lower()
    if method == "m-pesa":
        return(
            f"MP"
            f"{random.randint(10000000, 99999999)}"
        )

    # card payment
    if "card" in method:
        return (
            f"Card"
            f"{random.randint(100000, 999999)}"
        )

    # cash payment
    if method == "cash":
        return None

    return (
        f"PAY"
        F"{payment_number: 08d}"
    )

# Payment datetime
def generate_payment_datetime(sales_datetime):
    sales_datetime = pd.to_datetime(sales_datetime)
    seconds_offset = random.randint(0, 180)
    return ( sales_datetime + pd.Timedelta(seconds= seconds_offset))

# Generate Paymnets
def generate_payments():
    records = []
    print("Generating payment transactions...")

    for _, sale in sales_df.iterrows():
        sale_id = sale["SaleID"]
        payment_method = sale["PaymentMethod"]
        sale_status = sale["SaleStatus"]
        sales_datetime = sale["SalesDateTime"]

        # Find sales details
        payment_status = generate_payment_status(sale_status)
        payment_refernce = generate_payment_reference(
            len(records) + 1,
            payment_method
        )
        payment_datetime = (generate_payment_datetime(sales_datetime))

        # Create payment method
        records.append({
            "PaymentID": generate_id("PAY", len(records) + 1),
            "SaleID": sale_id,
            "PaymentDateTime": payment_datetime,
            "PaymentStatus": payment_status,
            "PaymentReference": payment_refernce
        })
    # create dataframe
    payments_df = pd.DataFrame(records)

    # Basic validation
    if payments_df.empty:
        raise ValueError(
            "No payment method were generated."
        )

    # Payment id uniqueness
    if payments_df["PaymentID"].duplicated().any():
        raise ValueError(
            "Duplicate payment ID was found"
        )

    # Sale id validation
    valid_sale_ids = set(sales_df["SaleID"])
    invalid_sale_ids = (~payments_df["SaleID"].isin(valid_sale_ids))

    if invalid_sale_ids.any():
        raise ValueError (
            "payment contain invalid saleid values."
        )

   

    # Save
    create_directory(f"{OUTPUT_DIR}/transaction")
    save_csv(payments_df, f"{OUTPUT_DIR}/transaction/payment.csv")
    save_excel(payments_df, f"{OUTPUT_DIR}/transaction/payment.xlsx")

    # Create and save raw payments.
    payments_raw_df = inject_payment_quality(payments_df.copy())

    create_directory(f"{OUTPUT_DIR}/raw")
    save_csv(payments_raw_df, f"{OUTPUT_DIR}/raw/payment_raw.csv")
    save_excel(payments_raw_df, f"{OUTPUT_DIR}/raw/payment_raw.xlsx")

    # Summary

    print(
        f"Generated "
        f"{len(payments_df)} payment records.")

    print(
        f"Sales represented: "
        f"{payments_df['SaleID'].nunique()}"
    )

    print(
        "Payment status:"
    )

    print(
        payments_df[
            "PaymentStatus"
        ].value_counts()
    )

    print(
        "Payments saved successfully."
    )

    print(
            "payments saved successfully."
        )
    
    print(
                "Clean payments data saved successfully."
            )
        
    print(
                "Raw payments data saved successfully."
            )
    


    return payments_df

# Main

if __name__ == "__main__":

    generate_payments()




