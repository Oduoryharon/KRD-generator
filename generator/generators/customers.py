import random
import pandas as pd
from faker import Faker
from generator.config import OUTPUT_DIR, NUM_CUSTOMERS
from generator.utils import (
    create_directory, 
    save_csv, 
    save_excel, 
    generate_id, 
    generate_kenyan_name, 
    generate_kenyan_phone, 
    generate_customer_email,
    random_date)

from generator.business_rules.customer_behavior import(
    OCCUPATION_INCOME,
    generate_customer_age,
    generate_date_of_birth,
    generate_monthly_income,
    generate_marital_status,
    generate_registration_date,
    generate_customer_status
)
from generator.business_rules.data_quality import inject_customer_quality

faker = Faker()
Faker.seed(42)
random.seed(42)

# load data

counties_df = pd.read_csv(
    "generator/reference_data/counties.csv")

towns_df = pd.read_csv(
    "generator/reference_data/towns.csv")

stores_df = pd.read_csv(
    f"{OUTPUT_DIR}/master/stores.csv")

GENDERS = ["Male", "Female"]

# Helpers
def choose_location():
    town = towns_df.sample(1).iloc[0]
    county = town["County"]
    town_name = town["Town"]
    region = counties_df.loc[counties_df["County"] == county, "Region"].values[0]
    return county, town_name, region

def choose_preferred_store():
    store = stores_df.sample(1).iloc[0]
    return store["StoreID"], store["StoreName"]

def generate_customer_name():
    full_name = generate_kenyan_name()
    first_name, last_name = full_name.split(" ", 1)
    return first_name, last_name, full_name

# Generate customers
def generate_customers():
    records = []
    customer_number = 1

    for i in range(NUM_CUSTOMERS):
        gender = random.choice(GENDERS)
        first_name, last_name, full_name = generate_customer_name()

        # Age and date of birth
        age = generate_customer_age()
        date_of_birth = generate_date_of_birth(age)

        # contact
        phone_number = generate_kenyan_phone()
        email = generate_customer_email(first_name, last_name)

        # location and income and occupation
        county, town, region = choose_location()
        occupation = random.choice(list(OCCUPATION_INCOME.keys()))
        monthly_income = generate_monthly_income(occupation)

        # customer profile
        marital_status = generate_marital_status()

        # Dates
        registration_date = generate_registration_date()
        

        # preferred store
        preferred_store_id, preferred_store_name = choose_preferred_store()

        # status
        status = generate_customer_status()

        # customer record
        records.append({
            "CustomerID": generate_id("CUS", customer_number, digits=6),
            "FirstName": first_name,
            "LastName": last_name,
            "FullName": full_name,
            "Gender": gender,
            "DateOfBirth": date_of_birth,
            "Age": age, 
            "PhoneNumber": phone_number,
            "Email": email,
            "County": county,
            "Town": town,
            "Region": region,
            "Occupation": occupation,
            "MonthlyIncome": monthly_income,
            "MaritalStatus": marital_status,
            "RegistrationDate": registration_date,
            "PreferredStoreID": preferred_store_id,
            "PreferredStoreName": preferred_store_name,
            "Status": status
        })

        customer_number += 1

    customers_df = pd.DataFrame(records)

  # Create dataframe

    customers_df = pd.DataFrame(records)
    customer_df = inject_customer_quality(customers_df)

    # ======================================================
    # AUDIT COLUMNS
    # ======================================================

    customers_df["CreatedDate"] = [
        random_date(
            "2018-01-01",
            "2023-12-31"
        )
        for _ in range(len(customers_df))
    ]

    customers_df["LastUpdatedDate"] = [
        random_date(
            "2024-01-01",
            "2025-12-31"
        )
        for _ in range(len(customers_df))
    ]

    # ======================================================
    # VALIDATION
    # ======================================================

    if customers_df.empty:

        raise ValueError(
            "No customer records generated."
        )

    if customers_df["CustomerID"].duplicated().any():

        raise ValueError(
            "Duplicate CustomerID detected."
        )

    # Save Clean data

    create_directory(
        f"{OUTPUT_DIR}/master"
    )

    save_csv(
        customers_df,
        f"{OUTPUT_DIR}/master/customers.csv"
    )

    save_excel(
        customers_df,
        f"{OUTPUT_DIR}/master/customers.xlsx"
    )

    # Create dirty dataset
    customers_raw_df = inject_customer_quality(
        customers_df.copy()
    )

    create_directory(
        f"{OUTPUT_DIR}/raw"
    )

    save_csv(
        customers_raw_df,
        f"{OUTPUT_DIR}/raw/customers_raw.csv"
    )

    save_excel(
        customers_raw_df,
        f"{OUTPUT_DIR}/raw/customers_raw.xlsx"
    )

    print(
        f"Generated {len(customers_df)} customers successfully."
    )

    print(
            "Clean customer data saved successfully."
        )
    
    print(
            "Raw customer data saved successfully."
        )

    return customers_df


# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":

    generate_customers()
    
