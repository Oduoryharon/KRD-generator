import random
import pandas as pd
from faker import Faker
from generator.business_rules.data_quality import inject_supplier_quality

from generator.config import OUTPUT_DIR, NUM_SUPPLIERS, STARTDATE, ENDDATE

from generator.utils import (
    create_directory,
    save_csv,
    save_excel,
    generate_id,
    generate_kenyan_name,
    generate_kenyan_phone,
    generate_supplier_email,
    random_date
)

faker = Faker()
Faker.seed(42)
random.seed(42)

# ===========================================
# LOAD REFERENCE DATA
# ===========================================

supplier_reference = pd.read_csv(
    "generator/reference_data/suppliers.csv"
)

county_df = pd.read_csv(
    "generator/reference_data/counties.csv"
)

town_df = pd.read_csv(
    "generator/reference_data/towns.csv"
)

# ===========================================
# BRANCH NAMES
# ===========================================

BRANCH_NAMES = [
    "Nairobi Branch",
    "Mombasa Branch",
    "Kisumu Branch",
    "Nakuru Branch",
    "Eldoret Branch",
    "Meru Branch",
    "Nyeri Branch",
    "Thika Branch",
    "Kitale Branch",
    "Machakos Branch",
    "Kakamega Branch",
    "Kisii Branch"
]


# ===========================================
# HELPER
# ===========================================

def build_supplier_record(
    supplier_number,
    supplier_name,
    category
):

    county = random.choice(
        county_df["County"].tolist()
    )

    towns = town_df[
        town_df["County"] == county
    ]

    if towns.empty:
        town = "Unknown"
    else:
        town = random.choice(
            towns["Town"].tolist()
        )

    return {

        "SupplierID":
            generate_id(
                "SUP",
                supplier_number
            ),

        "SupplierName":
            supplier_name,

        "CategorySupplied":
            category,

        "ContactPerson":
            generate_kenyan_name(),

        "Phone":
            generate_kenyan_phone(),

        "Email":
            generate_supplier_email(
                supplier_name.split(" - ")[0]
            ),

        "County":
            county,

        "Town":
            town,

        "PaymentTerms":
            random.choice([
                "Net 7",
                "Net 15",
                "Net 30",
                "Net 45",
                "Net 60",
                "Cash on Delivery",
                "Advance Payment"
            ]),

        "CreatedDate": random_date(STARTDATE, "2020-01-01").date(),
        "LastUpdatedDate": random_date("2025-12-31", ENDDATE).date(),

        "LeadTimeDays":
            random.randint(2, 14),


        "IsActive":
            random.choices(
                [True, False],
                weights=[95, 5],
                k=1
            )[0]
    }


# ===========================================
# MAIN FUNCTION
# ===========================================

def generate_suppliers():

    records = []

    supplier_number = 1

    reference_rows = supplier_reference.to_dict("records")

    print("Generating base suppliers...")

    # ---------------------------------------
    # FIRST: EVERY SUPPLIER ONCE
    # ---------------------------------------

    for row in reference_rows:

        supplier_name = row["SupplierName"].strip()

        category = row["CategorySupplied"].strip()

        records.append(

            build_supplier_record(
                supplier_number,
                supplier_name,
                category
            )

        )

        supplier_number += 1

    print(
        f"Generated {len(records)} base suppliers."
    )

        # ---------------------------------------
    # GENERATE BRANCH SUPPLIERS
    # ---------------------------------------

    print("Generating branch suppliers...")

    while supplier_number <= NUM_SUPPLIERS:

        row = random.choice(reference_rows)

        supplier_name = (
            f"{row['SupplierName'].strip()} - "
            f"{random.choice(BRANCH_NAMES)}"
        )

        category = row["CategorySupplied"].strip()

        records.append(
            build_supplier_record(
                supplier_number,
                supplier_name,
                category
            )
        )

        supplier_number += 1

    # ---------------------------------------
    # CREATE DATAFRAME
    # ---------------------------------------

    suppliers_df = pd.DataFrame(records)
    suppliers_df = inject_supplier_quality(suppliers_df)

    # ---------------------------------------
    # VALIDATION
    # ---------------------------------------

    if suppliers_df.empty:
        raise ValueError("No suppliers were generated.")

    if suppliers_df["SupplierID"].duplicated().any():
        raise ValueError("Duplicate SupplierID found.")

    if suppliers_df["SupplierName"].duplicated().any():
        print("Warning: Duplicate supplier names detected (expected for branch suppliers).")

    # ---------------------------------------
    # SAVE FILES
    # ---------------------------------------

    create_directory(f"{OUTPUT_DIR}/master")

    save_csv(
        suppliers_df,
        f"{OUTPUT_DIR}/master/suppliers.csv"
    )

    save_csv(
        suppliers_df,
        f"{OUTPUT_DIR}/raw/suppliers_raw.csv"
    )

    save_excel(
        suppliers_df,
        f"{OUTPUT_DIR}/master/suppliers.xlsx"
    )

    save_excel(
        suppliers_df,
        f"{OUTPUT_DIR}/raw/suppliers_raw.xlsx"
    )

    print(f"Generated {len(suppliers_df)} suppliers successfully.")

    return suppliers_df


# ===========================================
# MAIN
# ===========================================

if __name__ == "__main__":
    generate_suppliers()