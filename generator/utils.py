import os
import random
from datetime import datetime, timedelta
from string import digits
from sys import prefix
import pandas as pd

KENYAN_FIRST_NAMES = [
    "James", "John", "Peter", "David", "Daniel", "Kevin", "Brian",
    "Faith", "Grace", "Mercy", "Joyce", "Mary", "Esther", "Ann",
    "Dorcas", "Lucy", "Samuel", "Dennis", "Victor", "Paul"
]

KENYAN_LAST_NAMES = [
    "Mwangi", "Otieno", "Odhiambo", "Wanjiku", "Njoroge",
    "Kiptoo", "Chebet", "Achieng", "Mutua", "Kamau",
    "Omondi", "Maina", "Kariuki", "Kimani", "Muthoni",
    "Wambui", "Kiprotich", "Cheruiyot", "Ouma", "Nyambura"
]

def generate_kenyan_phone():
    prefixes = [
        "700","701","702","703","704","705","706","707","708","709",
        "710","711","712","713","714","715","716","717","718","719",
        "720","721","722","723","724","725","726","727","728","729",
        "740","741","742","743","745","746","748","757","758","759",
        "760","761","762","768","769","790","791","792","793","794",
        "795","796","797","798","799"
    ]

    prefix = random.choice(prefixes)
    number = random.randint(100000, 999999)

    return f"+254{prefix}{number}"

import random

def generate_supplier_email(company):
    company = (
        company.lower()
        .replace(" ", "")
        .replace("&", "")
        .replace(",", "")
        .replace(".", "")
    )

    prefixes = [
        "info",
        "sales",
        "orders",
        "accounts",
        "support",
        "admin"
    ]

    domains = [
        "co.ke",
        "ke",
        "ac.ke"
    ]

    return (
        f"{random.choice(prefixes)}@"
        f"{company}."
        f"{random.choice(domains)}"
    )

    return f"info@{company}.{random.choice(domains)}"

def generate_customer_email(first_name, last_name):

    domains = [
        "gmail.com",
        "yahoo.com",
        "outlook.com",
        "hotmail.com"
    ]

    return (
        f"{first_name.lower()}."
        f"{last_name.lower()}"
        f"{random.randint(1,999)}@"
        f"{random.choice(domains)}"
    )

def generate_kenyan_name():
    return f"{random.choice(KENYAN_FIRST_NAMES)} {random.choice(KENYAN_LAST_NAMES)}"

def create_directory(path: str):
    os.makedirs(path, exist_ok=True)

def save_csv(df: pd.DataFrame, filepath: str):
    df.to_csv(filepath, index=False)

def save_excel(df: pd.DataFrame, filepath: str):
    df.to_excel(filepath, index=False)

def generate_id(prefix: str, number: int, digits: int = 3) -> str:
    return f"{prefix}{number:0{digits}d}"
 

def random_date(start_date: str, end_str: str):
    date_format = "%Y-%m-%d"
    start = datetime.strptime(start_date, date_format)
    end = datetime.strptime(end_str, date_format)
    days_between = (end - start).days
    random_days = random.randint(0, days_between)
    return (start + timedelta(days=random_days))

def random_bool(probability):
    return random.random() < probability

# Add leading and trailing spaces
def random_spaces(value):
    return random.choice([
        value,
        f" {value}",
        f"{value} ",
        f" {value} "
    ])

# Add randomize text casing
def random_case(value):
    return random.choice([
        value,
        value.upper(),
        value.lower(),
        value.title()
    ])
