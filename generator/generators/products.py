import random
import pandas as pd

from generator.business_rules.data_quality import inject_product_quality

from generator.config import OUTPUT_DIR, NUM_PRODUCTS

from generator.utils import (
    create_directory,
    save_csv,
    save_excel,
    generate_id,
    random_date
)

random.seed(42)


# Helpers function.

def generate_barcode(number):
    return f"616100{number:07d}"


def generate_sku(category, number):
    prefix = category[:3].upper().replace(" ", "")
    return f"SKU-{prefix}-{number:06d}"


def get_reorder_level(category):

    reorder = {

        "Grocery": 200,
        "Dairy": 60,
        "Bakery": 70,
        "Fresh Produce": 80,
        "Meat & Poultry": 50,
        "Fish & Seafood": 40,
        "Frozen Foods": 40,

        "Beverages": 180,
        "Juices": 120,
        "Water": 200,
        "Tea & Coffee": 90,

        "Snacks": 100,
        "Confectionery": 120,

        "Cleaning Supplies": 70,
        "Laundry": 90,
        "Kitchenware": 25,

        "Personal Care": 80,
        "Baby Care": 60,
        "Health & Pharmacy": 40,

        "Stationery": 50,
        "Electronics": 10,
        "Pet Care": 25
    }

    return reorder.get(category, 50)

# Main

def generate_products():

    print("Loading reference data...")

    categories_df = pd.read_csv(
        "generator/output/master/categories.csv"
    )

    suppliers_df = pd.read_csv(
        "generator/output/master/suppliers.csv"
    )

    brands_df = pd.read_csv(
        "generator/reference_data/brands.csv"
    )

    templates_df = pd.read_csv(
        "generator/reference_data/product_templates.csv"
    )

    pricing_df = pd.read_csv(
        "generator/reference_data/pricing_rules.csv"
    )

    vat_df = pd.read_csv(
        "generator/reference_data/vat_rates.csv"
    )

    # Clean all text column.

    categories_df.columns = categories_df.columns.str.strip()
    suppliers_df.columns = suppliers_df.columns.str.strip()
    brands_df.columns = brands_df.columns.str.strip()
    templates_df.columns = templates_df.columns.str.strip()
    pricing_df.columns = pricing_df.columns.str.strip()
    vat_df.columns = vat_df.columns.str.strip()

    for df in [
        categories_df,
        suppliers_df,
        brands_df,
        templates_df,
        pricing_df,
        vat_df
    ]:

        for col in df.columns:

            if pd.api.types.is_string_dtype(df[col]):

                df[col] = df[col].str.strip()

    records = []

    # Generate products

    for product_number in range(1, NUM_PRODUCTS + 1):

        # Pick a random template

        template = templates_df.sample(1).iloc[0]

        brand = template["Brand"]
        category = template["Category"]
        product = template["Product"]
        unit = template["Unit"]
        pack_size = template["PackSize"]
        shelf_life_days = int(
            template["ShelfLifeDays"]
        )

        # Brand -> Supplier.

        brand_match = brands_df.loc[
            brands_df["Brand"] == brand
        ]

        if brand_match.empty:

            raise ValueError(
                f"Brand '{brand}' not found in brands.csv"
            )

        supplier_name = brand_match.iloc[0][
            "SupplierName"
        ]

        # supplier -> SupplierID.

        supplier_match = suppliers_df.loc[
            suppliers_df["SupplierName"]
            == supplier_name
        ]

        if supplier_match.empty:

            raise ValueError(
                f"Supplier '{supplier_name}' "
                f"not found in suppliers.csv"
            )

        supplier_id = supplier_match.iloc[0][
            "SupplierID"
        ]

        # Category

        category_match = categories_df.loc[
            categories_df["CategoryName"]
            == category
        ]

        if category_match.empty:

            raise ValueError(
                f"Category '{category}' "
                f"not found in categories.csv"
            )

        category_row = category_match.iloc[0]

        category_id = category_row["CategoryID"]

        is_perishable = category_row[
            "IsPerishable"
        ]

        # Pricing

        pricing_match = pricing_df.loc[
            pricing_df["Category"] == category
        ]

        if pricing_match.empty:

            raise ValueError(
                f"Pricing rule missing "
                f"for '{category}'"
            )

        pricing_row = pricing_match.iloc[0]

        min_cost = float(
            pricing_row["MinCost"]
        )

        max_cost = float(
            pricing_row["MaxCost"]
        )

        margin = float(
            pricing_row["MarginPercent"]
        )

        cost_price = round(
            random.uniform(
                min_cost,
                max_cost
            ),
            2
        )

        selling_price = round(
            cost_price *
            (1 + margin / 100),
            2
        )

       # VAT

        vat_match = vat_df.loc[
            vat_df["Category"] == category
        ]

        if vat_match.empty:

            raise ValueError(
                f"VAT rate missing "
                f"for '{category}'"
            )

        vat_rate = vat_match.iloc[0][
            "VATRate"
        ]

       # Generate ID.

        product_id = generate_id(
            "PRD",
            product_number,
            digits=6
        )

        sku = generate_sku(
            category,
            product_number
        )

        barcode = generate_barcode(
            product_number
        )

        product_name = (
            f"{brand} "
            f"{product} "
            f"{pack_size}"
        )

        reorder_level = get_reorder_level(
            category
        )

        status = random.choices(
            [
                "Active",
                "Inactive"
            ],
            weights=[
                98,
                2
            ],
            k=1
        )[0]

        created_date = random_date(
            "2018-01-01",
            "2023-12-31"
        ).date()

        last_updated_date = random_date(
            "2024-01-01",
            "2025-12-31"
        ).date()

        records.append({

            "ProductID": product_id,

            "SKU": sku,

            "Barcode": barcode,

            "ProductName": product_name,

            "Brand": brand,

            "CategoryID": category_id,

            "CategoryName": category,

            "SupplierID": supplier_id,

            "SupplierName": supplier_name,

            "PackSize": pack_size,

            "Unit": unit,

            "CostPrice": cost_price,

            "SellingPrice": selling_price,

            "VATRate": vat_rate,

            "ShelfLifeDays": shelf_life_days,

            "ReorderLevel": reorder_level,

            "IsPerishable": is_perishable,

            "Status": status,

            "CreatedDate": created_date,

            "LastUpdatedDate": last_updated_date

        })

    # create dataframe.

    products_df = pd.DataFrame(
        records
    )


    # Basic validation.

    if products_df.empty:

        raise ValueError(
            "No products were generated."
        )

    if products_df[
        "ProductID"
    ].duplicated().any():

        raise ValueError(
            "Duplicate ProductID found."
        )

    if products_df[
        "SKU"
    ].duplicated().any():

        raise ValueError(
            "Duplicate SKU found."
        )

    if products_df[
        "Barcode"
    ].duplicated().any():

        raise ValueError(
            "Duplicate Barcode found."
        )


    # Save clean data.

    create_directory(
        f"{OUTPUT_DIR}/master"
    )

    save_csv(
        products_df,
        f"{OUTPUT_DIR}/master/products.csv"
    )

    save_excel(
        products_df,
        f"{OUTPUT_DIR}/master/products.xlsx"
    )


   # Create raw dataset

    products_raw_df = inject_product_quality(
        products_df.copy()
    )

    create_directory(
        f"{OUTPUT_DIR}/raw"
    )

    save_csv(
        products_raw_df,
        f"{OUTPUT_DIR}/raw/products_raw.csv"
    )

    save_excel(
        products_raw_df,
        f"{OUTPUT_DIR}/raw/products_raw.xlsx"
    )


    # Summary

    print(
        f"Generated "
        f"{len(products_df)} "
        f"products successfully."
    )

    print(
        "Clean product data saved successfully."
    )

    print(
        "Raw product data saved successfully."
    )


    return products_df


# Main.

if __name__ == "__main__":

    generate_products()