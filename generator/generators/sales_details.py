import random
import pandas as pd

from generator.config import (
    OUTPUT_DIR
)

from generator.business_rules.data_quality import inject_sales_details_quality
from generator.utils import (
    create_directory,
    save_csv,
    save_excel,
    generate_id
)

random.seed(42)

sales_df = pd.read_csv(f"{OUTPUT_DIR}/transaction/sales.csv")
products_df = pd.read_csv(f"{OUTPUT_DIR}/master/products.csv")
inventory_df = pd.read_csv(f"{OUTPUT_DIR}/master/inventory.csv")

# Basic validation
if sales_df.empty:
    raise ValueError(
        "sales.csv is empty"
    )

if products_df.empty:
    raise ValueError(
        "products.csv is empty"
    )

if inventory_df.empty:
    raise ValueError(
        "inventory.csv is empty"
    )

# Required sales column
required_sales_columns = [
    "SaleID"
]
for column in required_sales_columns:
    if column not in sales_df:
        raise KeyError(
            f"sales data is missing required sales column: {column}"
        )

# Required product column
required_product_columns = [ "ProductID"]

for column in required_product_columns:
    if column not in products_df:
        raise KeyError(
            f"product data is missing required sales column: {column}"
        )

# Required inventory column
required_inventory_columns = ["ProductID"]

for column in required_inventory_columns:
    if column not in inventory_df:
        raise KeyError(
            f"inventory data is missing required sales column: {column}"
        )


print(
    f"Loaded {len(sales_df)} sales."
)

print(
    f"Loaded {len(products_df)} products."
)

print(
    f"Loaded {len(inventory_df)} inventory records."
)

# product selection
def get_available_product():
    available_products = products_df[
        products_df["Status"].astype(str).str.lower() == "active"
    ].copy()
    if available_products.empty:
        raise ValueError ("No active products are available")
    return available_products

def choose_products(number_of_products):
    available_products = get_available_product()
    number_of_products = min(number_of_products, len(available_products))
    selected_products = available_products.sample(
        n= number_of_products,
        replace= False
    )
    return selected_products

def generate_basket_size():
    return random.choices(
        population=[
            1,2,
            3,4,
            5,6,
            7
        ],
        weights=[
            35,25,
            16,10,
            6,5,
            3
        ],
        k=1
    )[0]

# quantity
def generate_quantity(product):
    unit = str(
        product["Unit"]
    ).lower()
    if unit in [
        "kg",
        "kilogram",
        "litre",
        "liter",
        "ltr"
    ]:
        return random.choices(
            population=[
                1,2,
                3,4,
                5
            ],
            weights=[
                55,25,
                12,6,
                2
            ],
            k=1
        )[0]
    # General package programs
    return random.choices(
        population=[
            1,2,
            3,4,
            5,6
        ],
        weights=[
            50,25,
            12,7,
            4,2
        ],
        k=1
    )[0]
# Discount

def generate_discount():

    discount_probability = random.random()

    if discount_probability < 0.75:

        return 0.0

    elif discount_probability < 0.95:

        return float(
            random.choice([
                5,
                10,
                15
            ])
        )

    else:

        return float(
            random.choice([
                20,
                25,
                30
            ])
        )

# Generate sales details
def generate_sales_details():
    records = []
    print("Generating sales details...")

    # process each sale
    for _, sale in sales_df.iterrows():
        sale_id = sale["SaleID"]
        basket_size = generate_basket_size()
        selected_products = choose_products(basket_size)

        # Generate product for this sale
        for _, product in selected_products.iterrows():
            product_id = product["ProductID"]
            quantity = generate_quantity(product)
            unit_price = float(product["SellingPrice"])
            discount_percent = generate_discount()

            records.append({

                "SalesDetailID": generate_id(
                        "SD",
                        len(records) + 1
                    ),
    
                "SaleID": sale_id,
                "ProductID": product_id,
                "Quantity": quantity,
                "UnitPrice": round(
                        unit_price,
                        2
                    ),
                "DiscountPercent": discount_percent
         })

    # Create dataframe

    sales_details_df = pd.DataFrame(records)

    # Basic validation

    if sales_details_df.empty:
        raise ValueError(
            "No sales detail records were generated."
        )

    # Sale id validation
    valid_sales = set(
        sales_df["SaleID"]
    )

    invalid_sales = (
        ~sales_details_df["SaleID"].isin(
            valid_sales
        )
    )

    if invalid_sales.any():

        raise ValueError(
            "Sales details contain invalid SaleID values."
        )

    # Product id validation

    valid_products = set(
        products_df["ProductID"]
    )

    invalid_products = (
        ~sales_details_df["ProductID"].isin(
            valid_products
        )
    )

    if invalid_products.any():

        raise ValueError(
            "Sales details contain invalid ProductID values."
        )
    # Quantity validation

    if (
        sales_details_df["Quantity"] <= 0
    ).any():

        raise ValueError(
            "Sales details contain zero or negative quantities."
        )

    # Unit price validation

    if (
        sales_details_df["UnitPrice"] < 0
    ).any():

        raise ValueError(
            "Sales details contain negative unit prices."
        )

    # Discount validation

    discount_values = pd.to_numeric(
    sales_details_df["DiscountPercent"],
    errors="coerce"
    )

    if discount_values.isna().any():

        raise ValueError(
            "Sales details contain invalid discount values."
        )


    if (
        (discount_values < 0)
        |
        (discount_values > 100)
    ).any():

        raise ValueError(
            "Invalid discount percentage detected."
        )

    # Save transaction data

    create_directory(
        f"{OUTPUT_DIR}/transaction"
    )

    save_csv(
        sales_details_df,
        f"{OUTPUT_DIR}/transaction/sales_details.csv"
    )

    save_excel(
        sales_details_df,
        f"{OUTPUT_DIR}/transaction/sales_details.xlsx"
    )
    # create and save dirty sales details.
    sales_raw_details_df = inject_sales_details_quality(sales_details_df.copy())
    create_directory(
            f"{OUTPUT_DIR}/raw"
        )
    
    save_csv(
            sales_raw_details_df,
            f"{OUTPUT_DIR}/raw/sales_details_raw.csv"
        )
    
    save_excel(
            sales_raw_details_df,
            f"{OUTPUT_DIR}/raw/sales_details_raw.xlsx"
        )


    # summary

    print(
        f"Generated "
        f"{len(sales_details_df)} sales detail records."
    )

    print(
        f"Sales represented: "
        f"{sales_details_df['SaleID'].nunique()}"
    )

    print(
        f"Products represented: "
        f"{sales_details_df['ProductID'].nunique()}"
    )

    print(
        "Sales details saved successfully."
    )

    print(
            "Sales_details saved successfully."
        )
    
    print(
                "Clean sales_details data saved successfully."
            )
        
    print(
                "Raw sales_details data saved successfully."
            )
    
    return sales_details_df

if __name__ == "__main__":
    generate_sales_details()

           

