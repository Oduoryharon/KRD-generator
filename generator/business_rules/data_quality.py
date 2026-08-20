import random
import pandas as pd


# ==========================================================
# BASIC HELPERS
# ==========================================================

def chance(probability):
    return random.random() < probability


def random_case(value):
    if pd.isna(value):
        return value

    value = str(value)

    return random.choice([
        value.lower(),
        value.upper(),
        value.title(),
        value
    ])


def add_spaces(value):
    if pd.isna(value):
        return value

    value = str(value)

    return random.choice([
        value,
        f" {value}",
        f"{value} ",
        f" {value} "
    ])


def remove_value(value):
    if chance(0.50):
        return None

    return value


# ==========================================================
# PHONE QUALITY
# ==========================================================

def phone_format_variation(phone):

    if pd.isna(phone):
        return phone

    digits = "".join(
        filter(str.isdigit, str(phone))
    )

    if len(digits) < 9:
        return phone

    last9 = digits[-9:]

    formats = [
        "0" + last9,
        "254" + last9,
        "+254" + last9,
        last9,
        f"0{last9[:3]} {last9[3:6]} {last9[6:]}",
        f"0{last9[:3]}-{last9[3:6]}-{last9[6:]}"
    ]

    return random.choice(formats)


# ==========================================================
# EMAIL QUALITY
# ==========================================================

def email_typos(email):

    if pd.isna(email):
        return email

    email = str(email)

    mistakes = [
        lambda x: x.replace("@", ""),
        lambda x: x.replace("@", "@ "),
        lambda x: x.replace(".com", ""),
        lambda x: x.replace(".co.ke", ""),
        lambda x: x.replace(".", ",", 1),
        lambda x: x.replace("info", "Info"),
        lambda x: x + "."
    ]

    return random.choice(mistakes)(email)


# ==========================================================
# SUPPLIER NAME QUALITY
# ==========================================================

def supplier_name_variation(name):

    if pd.isna(name):
        return name

    name = str(name)

    replacements = [
        ("Ltd", "Limited"),
        ("Limited", "Ltd"),
        ("Ltd", "LTD"),
        ("LTD", "ltd"),
        ("LTD", "Ltd"),
        ("ltd", "Ltd"),
        ("&", "and"),
        ("and", "&"),
        ("Dairy", "Dairies")
    ]

    old, new = random.choice(replacements)

    return name.replace(old, new)


# ==========================================================
# COUNTY QUALITY
# ==========================================================

COUNTY_VARIATIONS = {

    "Nairobi": [
        "Nairobi County",
        "NRB",
        "Nrb"
    ],

    "Mombasa": [
        "Mombasa County",
        "MSA"
    ],

    "Kisumu": [
        "Kisumu County",
        "KSM"
    ],

    "Nakuru": [
        "Nakuru County"
    ],

    "Uasin Gishu": [
        "Eldoret",
        "Uasin-Gishu"
    ],

    "Kiambu": [
        "Kiambu County"
    ]
}


def county_variation(county):

    if pd.isna(county):
        return county

    county = str(county)

    if county in COUNTY_VARIATIONS:
        return random.choice(
            COUNTY_VARIATIONS[county]
        )

    return county


# ==========================================================
# DUPLICATE ROW GENERATOR
# ==========================================================

def duplicate_rows(df, percentage=0.01):

    df = df.copy()

    if df.empty:
        return df

    duplicate_count = max(
        1,
        int(len(df) * percentage)
    )

    source_rows = random.choices(
        list(df.index),
        k=duplicate_count
    )

    duplicate_data = df.loc[source_rows].copy()

    duplicate_data.index = range(
        len(df),
        len(df) + len(duplicate_data)
    )

    df = pd.concat(
        [df, duplicate_data],
        ignore_index=True
    )

    return df


# ==========================================================
# DUPLICATE PHONE
# ==========================================================

def duplicate_phone(df):

    df = df.copy()

    phone_column = None

    if "Phone" in df.columns:
        phone_column = "Phone"

    elif "PhoneNumber" in df.columns:
        phone_column = "PhoneNumber"

    if phone_column is None:
        return df

    if len(df) < 2:
        return df

    duplicate_count = max(
        1,
        int(len(df) * 0.02)
    )

    rows = random.sample(
        list(df.index),
        min(duplicate_count, len(df))
    )

    for row in rows:

        source = random.choice(
            list(df.index)
        )

        if row != source:

            df.at[row, phone_column] = (
                df.at[source, phone_column]
            )

    return df


# ==========================================================
# SUPPLIER QUALITY
# ==========================================================

def inject_supplier_quality(df):

    df = df.copy()

    for index in df.index:

        if "SupplierName" in df.columns:

            if chance(0.03):
                df.at[index, "SupplierName"] = add_spaces(
                    df.at[index, "SupplierName"]
                )

            if chance(0.02):
                df.at[index, "SupplierName"] = supplier_name_variation(
                    df.at[index, "SupplierName"]
                )

            if chance(0.01):
                df.at[index, "SupplierName"] = random_case(
                    df.at[index, "SupplierName"]
                )

        if "ContactPerson" in df.columns:

            if chance(0.02):
                df.at[index, "ContactPerson"] = add_spaces(
                    df.at[index, "ContactPerson"]
                )

        if "Email" in df.columns:

            if chance(0.03):
                df.at[index, "Email"] = email_typos(
                    df.at[index, "Email"]
                )

            if chance(0.01):
                df.at[index, "Email"] = None

        if "Phone" in df.columns:

            if chance(0.03):
                df.at[index, "Phone"] = phone_format_variation(
                    df.at[index, "Phone"]
                )

            if chance(0.01):
                df.at[index, "Phone"] = None

        if "County" in df.columns:

            if chance(0.02):
                df.at[index, "County"] = county_variation(
                    df.at[index, "County"]
                )

        if "Town" in df.columns:

            if chance(0.02):
                df.at[index, "Town"] = add_spaces(
                    df.at[index, "Town"]
                )

            if chance(0.02):
                df.at[index, "Town"] = random_case(
                    df.at[index, "Town"]
                )

    df = duplicate_phone(df)

    # Duplicate supplier records
    df = duplicate_rows(
        df,
        percentage=0.01
    )

    return df


# ==========================================================
# PRODUCT QUALITY
# ==========================================================

def inject_product_quality(df):

    df = df.copy()

    for index in df.index:

        if "ProductName" in df.columns:

            if chance(0.03):
                df.at[index, "ProductName"] = add_spaces(
                    df.at[index, "ProductName"]
                )

        if "Brand" in df.columns:

            if chance(0.02):
                df.at[index, "Brand"] = random_case(
                    df.at[index, "Brand"]
                )

        if "Unit" in df.columns:

            if chance(0.03):
                df.at[index, "Unit"] = random_case(
                    df.at[index, "Unit"]
                )

        if "PackSize" in df.columns:

            if chance(0.01):
                df.at[index, "PackSize"] = None

        if "Barcode" in df.columns:

            if chance(0.01):
                df.at[index, "Barcode"] = None

        if "BarCode" in df.columns:

            if chance(0.01):
                df.at[index, "BarCode"] = None

    # Duplicate products
    df = duplicate_rows(
        df,
        percentage=0.01
    )

    return df


# ==========================================================
# STORE QUALITY
# ==========================================================

def inject_store_quality(df):

    df = df.copy()

    for index in df.index:

        if "StoreName" in df.columns:

            if chance(0.03):
                df.at[index, "StoreName"] = add_spaces(
                    df.at[index, "StoreName"]
                )

        if "County" in df.columns:

            if chance(0.02):
                df.at[index, "County"] = random_case(
                    df.at[index, "County"]
                )

        if "Town" in df.columns:

            if chance(0.02):
                df.at[index, "Town"] = random_case(
                    df.at[index, "Town"]
                )

        if "FloorAreaSQM" in df.columns:

            if chance(0.02):
                df.at[index, "FloorAreaSQM"] = None

    # Duplicate stores
    df = duplicate_rows(
        df,
        percentage=0.01
    )

    return df


# ==========================================================
# CUSTOMER QUALITY
# ==========================================================

def inject_customer_quality(df):

    df = df.copy()

    for index in df.index:

        if "FullName" in df.columns:

            if chance(0.03):
                df.at[index, "FullName"] = add_spaces(
                    df.at[index, "FullName"]
                )

        if "County" in df.columns:

            if chance(0.02):
                df.at[index, "County"] = random_case(
                    df.at[index, "County"]
                )

        if "Town" in df.columns:

            if chance(0.02):
                df.at[index, "Town"] = random_case(
                    df.at[index, "Town"]
                )

        if "Phone" in df.columns:

            if chance(0.02):
                df.at[index, "Phone"] = None

        if "PhoneNumber" in df.columns:

            if chance(0.02):
                df.at[index, "PhoneNumber"] = None

        if "Email" in df.columns:

            if chance(0.02):
                df.at[index, "Email"] = None

    # Duplicate customer records
    df = duplicate_rows(
        df,
        percentage=0.01
    )

    # Duplicate phone numbers
    df = duplicate_phone(df)

    return df


# ==========================================================
# INVENTORY QUALITY
# ==========================================================

def inject_inventory_quality(df):

    df = df.copy()

    for index in df.index:

        if "QuantityOnHand" in df.columns:

            if chance(0.02):

                quantity = df.at[
                    index,
                    "QuantityOnHand"
                ]

                if pd.notna(quantity):

                    df.at[
                        index,
                        "QuantityOnHand"
                    ] = -abs(quantity)

            if chance(0.02):

                df.at[
                    index,
                    "QuantityOnHand"
                ] = None

        if "ExpiryDate" in df.columns:

            if chance(0.02):

                df.at[
                    index,
                    "ExpiryDate"
                ] = random_case(
                    df.at[index, "ExpiryDate"]
                )

        if "StockStatus" in df.columns:

            if chance(0.02):

                df.at[
                    index,
                    "StockStatus"
                ] = random.choice([
                    "instock",
                    "INSTOCK",
                    "out stock",
                    "Low Stock",
                    "low stock"
                ])

    # Duplicate inventory records
    df = duplicate_rows(
        df,
        percentage=0.01
    )

    return df


# ==========================================================
# SALES QUALITY
# ==========================================================

def inject_sales_quality(df):

    df = df.copy()

    for index in df.index:

        if "PaymentMethod" in df.columns:

            if chance(0.02):

                df.at[
                    index,
                    "PaymentMethod"
                ] = random.choice([
                    "M-Pesa",
                    "M-pesa",
                    "mpesa",
                    "Cash ",
                    "cash",
                    "Credit card",
                    "credit card"
                ])

        if "SaleStatus" in df.columns:

            if chance(0.02):

                df.at[
                    index,
                    "SaleStatus"
                ] = random.choice([
                    "completed",
                    "Completed ",
                    "COMPLETED",
                    "complete"
                ])

        if "CustomerID" in df.columns:

            if chance(0.01):

                df.at[
                    index,
                    "CustomerID"
                ] = None

        if "StoreID" in df.columns:

            if chance(0.01):

                df.at[
                    index,
                    "StoreID"
                ] = None

    # Duplicate transaction records
    df = duplicate_rows(
        df,
        percentage=0.01
    )

    return df


# ==========================================================
# SALES DETAILS QUALITY
# ==========================================================

def inject_sales_details_quality(df):

    df = df.copy()

    for index in df.index:

        if "Quantity" in df.columns:

            if chance(0.02):

                quantity = df.at[
                    index,
                    "Quantity"
                ]

                if pd.notna(quantity):

                    df.at[
                        index,
                        "Quantity"
                    ] = -abs(quantity)

        if "ProductID" in df.columns:

            if chance(0.01):

                df.at[
                    index,
                    "ProductID"
                ] = None

        if "SaleID" in df.columns:

            if chance(0.01):

                df.at[
                    index,
                    "SaleID"
                ] = None

    # Duplicate sales detail records
    df = duplicate_rows(
        df,
        percentage=0.01
    )

    return df


# ==========================================================
# PAYMENT QUALITY
# ==========================================================

def inject_payment_quality(df):

    df = df.copy()

    for index in df.index:

        if "PaymentStatus" in df.columns:

            if chance(0.02):

                df.at[
                    index,
                    "PaymentStatus"
                ] = random.choice([
                    "completed",
                    "Completed ",
                    "COMPLETED",
                    "pending",
                    "Pending "
                ])

        if "PaymentReference" in df.columns:

            if chance(0.02):

                df.at[
                    index,
                    "PaymentReference"
                ] = None

        if "SaleID" in df.columns:

            if chance(0.01):

                df.at[
                    index,
                    "SaleID"
                ] = None

    # Duplicate payment transactions
    df = duplicate_rows(
        df,
        percentage=0.01
    )

    return df


# ==========================================================
# RETURN QUALITY
# ==========================================================

def inject_return_quality(df):

    df = df.copy()

    for index in df.index:

        if "ReturnReason" in df.columns:

            if chance(0.03):

                df.at[
                    index,
                    "ReturnReason"
                ] = random_case(
                    df.at[index, "ReturnReason"]
                )

        if "ReturnStatus" in df.columns:

            if chance(0.02):

                df.at[
                    index,
                    "ReturnStatus"
                ] = random.choice([
                    "approved",
                    "Approved ",
                    "APPROVED",
                    "pending"
                ])

        if "QuantityReturned" in df.columns:

            if chance(0.02):

                quantity = df.at[
                    index,
                    "QuantityReturned"
                ]

                if pd.notna(quantity):

                    df.at[
                        index,
                        "QuantityReturned"
                    ] = -abs(quantity)

        if "SaleID" in df.columns:

            if chance(0.01):

                df.at[
                    index,
                    "SaleID"
                ] = None

    # Duplicate return transactions
    df = duplicate_rows(
        df,
        percentage=0.01
    )

    return df


# ==========================================================
# GENERIC TRANSACTION QUALITY
# ==========================================================

def inject_transaction_quality(df):

    df = df.copy()

    # Generic duplicate transaction records
    df = duplicate_rows(
        df,
        percentage=0.01
    )

    return df