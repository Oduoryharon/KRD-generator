import random
import pandas as pd

from generator.config import (
    OUTPUT_DIR
)

from generator.business_rules.data_quality import inject_return_quality

from generator.utils import (
    create_directory,
    save_csv,
    save_excel,
    generate_id
)

random.seed(42)

# Load Source data
sales_df = pd.read_csv(f"{OUTPUT_DIR}/transaction/sales.csv")
sales_details_df = pd.read_csv(f"{OUTPUT_DIR}/transaction/sales_details.csv")
products_df = pd.read_csv(f"{OUTPUT_DIR}/master/products.csv")

# Basic Validation
if sales_df.empty:
    raise ValueError (
       " sales.csv is empty."
    )

if sales_details_df.empty:
    raise ValueError (
        "sales_details.csv is empty"
    )

if products_df.empty:
    raise ValueError (
        "products.csv is empty."
    )


# Required Columns
required_sales_columns = [
    "SaleID",
    "SalesDateTime",
    "SaleStatus"
]

for column in required_sales_columns:
    if column not in sales_df.columns:
        raise KeyError(
            f"sales data is missing required column: {column}"
        )

required_sales_details_columns = [
    "SalesDetailID",
    "SaleID",
    "ProductID",
    "Quantity"
]

for column in required_sales_details_columns:
    if column not in sales_details_df.columns:
        raise KeyError(
            f"sales_details data is missing required column: {column}"
        )

required_products_columns = [
    "ProductID",
    "ProductName"
]

for column in required_products_columns:
    if column not in products_df.columns:
        raise KeyError(
            f"product data is missing required column: {column}"
        )

print(
    f"Loaded {len(sales_df)} sales."
)

print(
    f"Loaded {len(sales_details_df)} sales detail records."
)

print(
    f"Loaded {len(products_df)} products."
)

RETURN_REASONS = [
    "Damaged Products",
    "Wrong Product",
    "Expired Product",
    "Defective Product",
    "Poor Quality",
    "Wrong Size",
    "Customer Changed mind",
    "Duplicate Purchase",
    "Product Not as Expected",
    "Package damaged",
    "Missing Parts"
]
# Return methods
RETURN_METHODS = [
    "Store return",
    "Customer Serrvice Desk",
    "Exchange",
    "Delivery return"
]

RETURN_CONDITION = [
    "unopened",
    "opened",
    "Damaged",
    "Defective",
    "Expired",
    "Used"
]

# Return Status
RETURN_STATUSES = [
    "Approved",
    "Pending",
    "Rejected"
]

def generate_return_reason():
    return random.choices(
        population= RETURN_REASONS,
        weights= [
            18,10,8,
            15,12,5,
            10,5,7,
            6,4
        ],
        k=1
    )[0]
def generate_return_condition():
    return random.choices(
        population= RETURN_CONDITION,
        weights= [
            25,20,15,
            15,10,15
        ],
        k=1
    )[0]


def generate_return_method():
    return random.choices(
        population= RETURN_METHODS,
        weights= [
            65,
            15,
            15,
            5
        ],
        k=1
    )[0]

def generate_return_statuses():
    return random.choices(
        population= RETURN_STATUSES,
        weights= [
            90,
            6,4
        ],
        k=1
    )[0]

def generate_return_date(sale_datetime):
    sale_datetime = pd.to_datetime(sale_datetime)
    days_after_sale = random.choices(
        population= [
            1,2,3,
            5,7,14,
            21,30
        ],
        weights= [
            15,18,18,
            15,12,10,
            7,5
        ],
        k=1
    )[0]
    return (sale_datetime + pd.Timedelta(days = days_after_sale))

# Quantity returned
def generate_quantity_returned(purchased_quantity):
    purchased_quantity = int(purchased_quantity)
    if purchased_quantity <= 1:
        return 1

    possible_quantities = list(range(1, purchased_quantity + 1))
    return random.choice(possible_quantities)

# Determined whether can be returned
def get_eligible_sales():
    eligible_sales = sales_df[
        sales_df["SaleStatus"]
        .astype(str)
        .str.strip()
        .str.lower()
        == "completed"
    ].copy()
    return eligible_sales

# Generate Returns
def generate_returns():
    records = []
    print("Generating return transaction...")

    eligible_sales = get_eligible_sales()

    if eligible_sales.empty:
        raise KeyError (
            "No completed sales are available for returns."
        )
    eligible_details = sales_details_df.merge(eligible_sales[
        [
            "SaleID",
            "SalesDateTime"
        ]
    ],
    on= "SaleID",
    how= "inner")
    if eligible_details.empty:
        raise KeyError (
            "No eligible sales details are available for returns."
        )

    for _, detail in eligible_details.iterrows():
        if random.random() > 0.03:
            continue

        sale_id = detail["SaleID"]
        sales_detail_id = detail["SalesDetailID"]
        product_id = detail["ProductID"]
        purchased_quantity = detail["Quantity"]
        return_quantity = generate_quantity_returned(purchased_quantity)
        return_date = generate_return_date(detail["SalesDateTime"])
        return_reason = generate_return_reason()
        return_condition = generate_return_condition()
        return_method = generate_return_method()
        return_status = generate_return_statuses()
        return_id = generate_id("RET", len(records) + 1)

        records.append({
            "ReturnID": return_id,
            "SaleID": sale_id,
            "SalesDetailID": sales_detail_id,
            "ProductID": product_id,
            "ReturnDate": return_date,
            "QuantityReturned": return_quantity,
            "ReturnReason": return_reason,
            "ReturnMethod": return_method,
            "RetrunCondition": return_condition,
            "ReturnStatus": return_status

        })
    # create dataframe
    returns_df = pd.DataFrame(records)

    # basic validation
    if returns_df.empty:
        raise ValueError(
            "No retrun records were generated"
        )

    # return id uniqueness
    if returns_df["ReturnID"].duplicated().any():
        raise ValueError("Duplicate ReturnID were found.")

    # saleID Validation

    valid_sale_ids = set(sales_df["SaleID"])
    invalid_sale_ids = (~returns_df["SaleID"].isin(valid_sale_ids))
    if invalid_sale_ids.any():
        return ValueError ("Return contains invalid salesID values.")

    # sales_details id validation
    valid_sales_detail_ids = set(sales_details_df["SalesDetailID"])
    invalid_sales_detail_ids = (~returns_df["SalesDetailID"].isin(valid_sales_detail_ids))
    if invalid_sales_detail_ids.any():
        return ValueError ("Return contains invalid salesDetailsID values.")
    
    # product id validation
    valid_products_ids = set(products_df["ProductID"])
    invalid_product_ids = (~returns_df["ProductID"].isin(valid_products_ids))
    if invalid_product_ids.any():
        return ValueError ("Return contains invalid ProductID values")

    # Quantity validation
    if (
        returns_df["QuantityReturned"] <= 0
    ).any():
        raise ValueError("Return contains zero or negative quantities")

    # Return date validation
    returns_df["ReturnDate"] = pd.to_datetime(returns_df["ReturnDate"])

    sales_dates = sales_df[["SaleID", "SalesDateTime"]].copy()

    sales_dates["SalesDateTime"] = pd.to_datetime(sales_dates["SalesDateTime"])

    returns_with_sales = returns_df.merge( sales_dates, on="SaleID", how="left")

    invalid_dates = (
        returns_with_sales["ReturnDate"] < returns_with_sales["SalesDateTime"])

    if invalid_dates.any():

        raise ValueError(
            "Return date cannot be before the sale date."
        )

    # Return quantity cannot exceed purchased quantity.

    purchase_quantities = sales_details_df[
        [
            "SalesDetailID",
            "Quantity"
        ]
    ]

    quantity_check = returns_df.merge(
        purchase_quantities,
        on="SalesDetailID",
        how="left"
    )

    invalid_quantities = (
        quantity_check["QuantityReturned"]
        > quantity_check["Quantity"]
    )

    if invalid_quantities.any():

        raise ValueError(
            "Returned quantity exceeds purchased quantity."
        )

    # Save

    create_directory(
        f"{OUTPUT_DIR}/transaction"
    )

    save_csv(
        returns_df,
        f"{OUTPUT_DIR}/transaction/returns.csv"
    )

    save_excel(
        returns_df,
        f"{OUTPUT_DIR}/transaction/returns.xlsx"
    )

    # create and save raw data.

    returns_raw_df = inject_return_quality(returns_df.copy())

    create_directory(
            f"{OUTPUT_DIR}/raw"
        )
    
    save_csv(
            returns_raw_df,
            f"{OUTPUT_DIR}/raw/return_raw.csv"
        )
    
    save_excel(
            returns_raw_df,
            f"{OUTPUT_DIR}/raw/returns_raw.xlsx")

    # Summary

    print(
        f"Generated "
        f"{len(returns_df)} return records."
    )

    print(
        f"Sales represented: "
        f"{returns_df['SaleID'].nunique()}"
    )

    print(
        f"Products returned: "
        f"{returns_df['ProductID'].nunique()}"
    )

    print(
        "Return reasons:"
    )

    print(
        returns_df[
            "ReturnReason"
        ].value_counts()
    )

    print(
        "Return transactions saved successfully."
    )

    print(
                "Returns saved successfully."
            )
        
    print(
                    "Clean returns data saved successfully."
                )
            
    print(
                    "Raw returns data saved successfully."
                )

    return returns_df

# Main

if __name__ == "__main__":

    generate_returns()
