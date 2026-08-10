import random
import pandas as pd

# Basic Helpers
def chance(probability):
    return random.random() < probability

def random_case(value):
    if pd.isna(value):
        return value
    value = str(value)
    return random.choice([value.lower(), value.upper(), value.title(), value])

def add_spaces(value):
    if pd.isna(value):
        return value
    value = str(value)
    return random.choice([value, f" {value}", f"{value} ", f" {value} "])

def remove_value(value):
    if chance(0.50):
        return None
    return value

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

def phone_format_variation(phone):
    if pd.isna(phone):
        return phone
    digits = "".join(filter(str.isdigit, str(phone)))
    if len(digits) < 9:
        return phone

    last9 = digits[-9:]
    formats = [
        "0" + last9,
        "254" + last9,
        "+254" + last9,
        last9,
        f"0{last9[:3]} {last9[3:6]} {last9[6:]}"
         f"0{last9[:3]}-{last9[3:6]}-{last9[6:]}"
    ]
    return random.choices(formats)

# Email typos
def email_typos(email):
    if pd.isna(email):
        return email

    email = str(email)

    mistakes = [
        lambda x: x.replace("@", ""),
        lambda x: x.replace("@", "@ "),
        lambda x: x.replace(".com", ""),
        lambda x: x.replace(".co.ke",""),
        lambda x: x.replace(".",",",1),
        lambda x: x.replace("info", "Info"),
        lambda x: x + "."
    ]
    return random.choice(mistakes)(email)

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
        return random.choice(COUNTY_VARIATIONS[county])
    return county

def duplicate_phone(df):
    duplicate_count = max(1, int(len(df) * 0.02))
    rows = random.sample(list(df.index), duplicate_count)
    for rows in rows:
        source = random.choice(list(df.index))
        df.at["row", "Phone"] = df.at[source, "Phone"]
    return df



# Supplier Helpers
def inject_supplier_quality(df):
    df = df.copy()
    for index in df.index:
        if chance(0.03):
            df.at[index, "SupplierName"] = add_spaces(df.at[index, "SupplierName"])
        if chance(0.02):
            df.at[index, "SupplierName"] = supplier_name_variation(df.at[index, "SupplierName"])
        if chance(0.01):
            df.at[index, "SupplierName"] = random_case(df.at[index, "SupplierName"])

        # contact person
        if chance(0.01):
            df.at[index, "ContactPerson"] = add_spaces(df.at[index, "ContactPerson"])

        if chance(0.03):
            df.at[index, "Email"] = email_typos(df.at[index, "Email"])
        if chance(0.01):
            df.at[index, "Email"] = None
        if chance(0.03):
            df.at[index, "Phone"] = phone_format_variation(df.at[index, "Phone"])
        if chance(0.01):
            df.at[index, "Phone"] = None
        if chance(0.02):
            df.at[index, "County"] = county_variation(df.at[index, "County"])
        if chance(0.02):
            df.at[index, "Town"] = add_spaces(df.at[index, "Town"])
        if chance(0.02):
            df.at[index, "Town"] = random_case(df.at[index, "Town"])

    df = duplicate_phone(df)
    return df

# Product Helpers
def inject_product_quality(df):
    df = df.copy()
    for index in df.index:
        if chance(0.03):
            df.at[index, "ProductName"] = add_spaces(df.at[index, "ProductName"])
        if chance(0.02):
            df.at[index, "Brand"] = random_case(df.at[index, "Brand"])

        if chance(0.03):
            df.at[index, "Unit"] = random_case(df.at[index, "Unit"])
        if chance(0.01):
            df.at[index, "PackSize"] = None
        if chance(0.01):
            df.at[index, "BarCode"] = None

    return df

# Store Helpers
def inject_store_quality(df):
    df = df.copy()
    for index in df.index:
        if chance(0.03):
            df.at[index, "StoreName"] = add_spaces(df.at[index, "StoreName"])
        if chance(0.02):
            df.at[index, "County"] = random_case(df.at[index, "County"])
        if chance(0.02):
            df.at[index, "Town"] = random_case(df.at[index, "Town"])
        if chance(0.02):
            df.at[index, "FloorAreaSQM"] = None
    return df

# inventory Helpers
def inject_inventory_quality(df):
    df = df.copy()
    for index in df.index:
        if chance(0.02):
            quantity = abs(df.at[index, "QuantityOnHand"])
            df.at[index, "QuantityOnHand"] = -quantity
        if chance(0.02):
            df.at[index, "QuantityOnHand"] = None
        if chance(0.02):
            df.at[index, "ExpiryDate"] = random_case(df.at[index, "ExpiryDate"])
        if chance(0.02):
            df.at[index, "StockStatus"] = random.choice(["instock", "INSTOCK","out stock", "Low Stock", "low stock"])

        duplicate_count = int(len(df) * 0.01)
        rows = random.sample(list(df.index), duplicate_count)
        for row in rows:
            source = random.choice(list(df.index))
            df.at[row, "BatchNumber"] = df.at[source, "BatchNumber"]

    return df

# Customer Helpers
def inject_customer_quality(df):
    df = df.copy()
    for index in df.index:
        if chance(0.03):
            df.at[index, "FullName"] = add_spaces(df.at[index, "FullName"])
        if chance(0.02):
            df.at[index, "County"] = random_case(df.at[index, "County"])
        if chance(0.02):
            df.at[index, "Town"] = random_case(df.at[index, "Town"])
        if chance(0.02):
            df.at[index, "Phone"] = None
        if chance(0.02):
            df.at[index, "Email"] = None

    return df