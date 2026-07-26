import pandas as pd
from faker import Faker

from generator.config import OUTPUT_DIR
from generator.utils import create_directory, save_csv, save_excel, generate_id, random_date

faker = Faker()
Faker.seed(42)


supplier_reference = pd.read_csv(f"generator/reference_data/suppliers.csv")

def generate_suppliers():
    records = []
    for index, row in supplier_reference.iterrows():
        supplier_name = row['SupplierName']
        category = row['CategorySupplied']

    record = {

        "SupplierID": generate_id("SUP", index + 1),

        "SupplierName": supplier_name,

        "CategorySupplied": category,

        "ContactPerson": faker.name(),

        "Phone": faker.phone_number(),

        "Email": faker.company_email(),

        "County": faker.city(),

        "PostalAddress": faker.address(),

        "PaymentTerms": "Net 30",

        "IsActive": True

    }

    records.append(record)
    df = pd.DataFrame(records)
    create_directory(f"{OUTPUT_DIR}/master")
    save_csv(df, f"{OUTPUT_DIR}/master/suppliers.csv")
    save_excel(df, f"{OUTPUT_DIR}/master/suppliers.xlsx")
    print(f"Generated {len(df)} suppliers and saved to {OUTPUT_DIR}/master/suppliers.csv and suppliers.xlsx")
    return df