import random
import pandas as pd

from generator.config import (
    OUTPUT_DIR,
    NUM_SALES,
    STARTDATE,
    ENDDATE
)

from generator.business_rules.data_quality import inject_sales_quality
from generator.utils import (
    create_directory,
    save_csv,
    save_excel,
    generate_id,
    random_date
)

random.seed(42)

customers_df = pd.read_csv(f"{OUTPUT_DIR}/master/customers.csv")
stores_df = pd.read_csv(f"{OUTPUT_DIR}/master/stores.csv")
product_df = pd.read_csv(f"{OUTPUT_DIR}/master/products.csv")
inventory_df = pd.read_csv(f"{OUTPUT_DIR}/master/inventory.csv")

# Basic validation
if customers_df.empty:
    raise ValueError(
        "customer.csv is empty"
    )
if stores_df.empty:
    raise ValueError(
        "stores.csv is empty"
    )
if product_df.empty:
    raise ValueError(
        "product.csv is empty"
    )
if inventory_df.empty:
    raise ValueError(
        "inventory.csv is empty"
    )

# Validate required customer columns
required_customer_columns = [
    "CustomerID"
]

for column in required_customer_columns:
    if column not in required_customer_columns:
        raise KeyError(
            f"customer data is missing required error: {column}"
        )


# Validate required store columns
required_store_columns = [
    "StoreID"
]

for column in required_store_columns:
    if column not in required_store_columns:
        raise KeyError(
            f"store data is missing required error: {column}"
        )


# Validate required product columns
required_product_columns = [
    "ProductID"
]

for column in required_product_columns:
    if column not in required_product_columns:
        raise KeyError(
            f"product data is missing required error: {column}"
        )

# validate required inventory columns
required_inventory_columns = [
    "InventoryID"
]

for column in required_inventory_columns:
    if column not in required_inventory_columns:
        raise KeyError(
            f"inventory data is missing required error: {column}"
        )


# Active customers
if "IsActive" in customers_df.columns:
    active_customer_df = customers_df[
        customers_df["IsActive"] == True
    ].copy()
else:
    active_customer_df = customers_df.copy()

if active_customer_df.empty:
    raise ValueError(
        "No active customers are available."
    )

# Acive Stores
if "is_active" in stores_df.columns:
    active_stores_df = stores_df[
        stores_df["is_active"] == True
    ].copy()
elif "IsActive" in stores_df.columns:
    active_stores_df = stores_df[
        stores_df["IsActive"] == True
    ].copy()

else:
    active_stores_df = stores_df.copy()

if active_stores_df.empty:
    raise ValueError(
        "No Active stores are available"
    )

# Receipt number
def generate_reciept_mumber(number):
    return f"RCPT{number:08d}"

def generate_sales_datetime():
    sales_date = random_date(
        STARTDATE,
        ENDDATE
    )

    hour = random.choices(
        population = [
            7,8,9,
            10,11,12,
            13,14,15,
            16,17,18,
            19,20,21
        ],
        weights=[
            2,3,4,
            5,5,6,
            6,6,5,
            6,8,10,
            12,10,7
        ],
        k=1
    )[0]
    minute = random.randint(
        0,
        59
    )
    second = random.randint(
        0,
        59
    )
    return sales_date.replace(
        hour = hour,
        minute = minute,
        second = second
    )

# Payment method
PAYMENT_METHODS = [
    "M-pesa",
    "Cash",
    "Debit Card",
    "Credit Card"
]

SALE_STATUS = [
    "Completed",
    "Cancelled",
    "Refunded"
]

# Payment method generator
def generate_payment_method():
    return random.choices(
        population= PAYMENT_METHODS,
        weights= [
            65,
            20,
            10,
            5
        ],
        k=1
    )[0]

# Generate sales status
def generate_sale_status():
    return random.choices(
        population= SALE_STATUS,
        weights= [
            97,
            2,
            1
        ],
        k=1
    )[0]

# Sales Header generator
def choose_customer():
    if active_customer_df.empty:
        raise ValueError(
            "No active customer found"
        )
    customer = active_customer_df.sample(
        n=1
    ).iloc[0]
    return customer

def choose_store():
    if active_stores_df.empty:
        raise ValueError(
            ("No active stores asre available")
        )
    store = active_stores_df.sample(
        n= 1
    ).iloc[0]
    return store

def generate_sales():
    records = []
    print("Generating sales transaction")
    for sale_number in range(1, NUM_SALES + 1):
        customer = choose_customer()
        customer_id = customer["CustomerID"]
        store = choose_store()
        store_id = store["StoreID"]
        sale_datetime = generate_sales_datetime()
        sale_id = generate_id(
            "SAL",
            sale_number
        )
        receipt_number = generate_reciept_mumber(
            sale_number
        )
        payment_method = generate_payment_method()
        sale_status = generate_sale_status()

        records.append({
            "SaleID": sale_id,
            "ReceiptNumber": receipt_number,
            "SalesDateTime": sale_datetime,
            "CustomerID": customer_id,
            "StoreID": store_id,
            "PaymentMethod": payment_method,
            "SaleStatus": sale_status
        })

    sales_df = pd.DataFrame(records)

        # Validation
    if sales_df.empty:
        raise ValueError(
            "No Sales are generated."
        )

    # SaleID uniquenes
    if sales_df["SaleID"].duplicated().any():
        raise ValueError (
            "duplicate saleid were found."
        )
    # Receipt uniqueness
    if sales_df["ReceiptNumber"].duplicated().any():
        raise ValueError (
            "Duplicated receipt number were found"
        )

    # customer foreign key validation
    valid_customers = set(customers_df["CustomerID"])
    invalid_customers = (~sales_df["CustomerID"].isin(valid_customers))
    if invalid_customers.any():
        raise ValueError(
            "Sales contain invalid customerID values"
        )

    # store foreign key validation
    valid_stores = set(stores_df["StoreID"])
    invalid_stores = (~stores_df["StoreID"].isin(valid_stores))
    if invalid_stores.any():
        raise ValueError(
            "Sales contain invalid StoreID values."
        )

        # save clean sales data
    create_directory(f"{OUTPUT_DIR}/transaction")
    save_csv(sales_df, f"{OUTPUT_DIR}/transaction/sales.csv")
    save_excel(sales_df, f"{OUTPUT_DIR}/transaction/sales.xlsx")
    print( f"Generated {len(sales_df)} sales transactions.")
    print(f"Saved clean sales data to "
        f"{OUTPUT_DIR}/transaction/sales.csv"
    )

    # create and store raw data.
    sales_raw_df = inject_sales_quality(sales_df.copy())

    create_directory(f"{OUTPUT_DIR}/raw")
    save_csv(sales_raw_df, f"{OUTPUT_DIR}/raw/sales.csv")
    save_excel(sales_raw_df, f"{OUTPUT_DIR}/raw/sales.xlsx")

    # summary
    print(
            "Sales saved successfully."
        )
    
    print(
                "Clean sales data saved successfully."
            )
        
    print(
                "Raw sales data saved successfully."
            )


    return sales_df

if __name__ == "__main__":
    generate_sales()
                             