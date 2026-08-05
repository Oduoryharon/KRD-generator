import random
from datetime import datetime, timedelta
import pandas as pd

# Customer occupations
OCCUPATION_INCOME = {
    "Teacher": (50000, 150000),
    "Student": (0, 50000),
    "Lecturer": (80000, 200000),
    "Doctor": (200000, 500000),
    "Nurse": (80000, 200000),
    "Clinical Officer": (60000, 150000),
    "Software Developer": (100000, 400000),
    "Data Analyst": (80000, 250000),
    "Data Engineer": (100000, 300000),
    "Database Administrator": (90000, 250000),
    "Accountant": (70000, 200000),
    "Auditor": (70000, 200000),
    "Business Owner": (100000, 1000000),
    "Farmer": (30000, 150000),
    "Driver": (30000, 100000),
    "Police Officer": (50000, 150000),
    "Engineer": (80000, 300000),
    "Mechanic": (40000, 150000),
    "Electrician": (40000, 150000),
    "Plumber": (40000, 150000),
    "Carpenter": (40000, 150000),
    "Sales representative": (40000, 150000),
    "Cashier": (30000, 100000),
    "unskilled laborer": (20000, 80000),
    "unemployed": (0, 20000),
}

# Loyalty tiers
LOYALTY_TIERS = {
    "Bronze": 0.45,
    "Silver": 0.30,
    "Gold": 0.18,
    "Platinum": 0.07,
}

# Marital status 
MARITAL_STATUS = [
    "Single",
    "Married",
    "Divorced",
    "Widowed"
]

# Shoping frequency
SHOPPING_FREQUENCY = {
    "Daily": 0.05,
    "Weekly": 0.55,
    "Bi-weekly": 0.20,
    "Monthly": 0.20,
    "Yearly": 0.10
}

# Monthly Income
# generate realistic monthly income based on occupation
def generate_monthly_income(occupation):
    minimum, maximum = OCCUPATION_INCOME.get(occupation, (20000, 100000))
    return random.randint(minimum, maximum)

# loyalty tier
def generate_loyalty_tier():
    return random.choices(
        population=list(LOYALTY_TIERS.keys()),
        weights=list(LOYALTY_TIERS.values()),
        k=1
    )[0]

# Marital status
def generate_marital_status():
    return random.choice(MARITAL_STATUS)

# Shopping frequency
def generate_shopping_frequency():
    return random.choices(
        population=list(SHOPPING_FREQUENCY.keys()),
        weights=list(SHOPPING_FREQUENCY.values()),
        k=1
    )[0]

# Registration date
def generate_registration_date():
    start_date = datetime(2020, 1, 1)
    end_date = datetime(2025, 12, 31)
    difference = (end_date - start_date).days
    return (start_date + timedelta(days=random.randint(0, difference))).date()

# generate last purchase date
def generate_last_purchase_date(registration_date):
    if isinstance(registration_date, str):
        registration_date = datetime.strptime(registration_date, "%Y-%m-%d").date()
    today = datetime.today().date()
    difference = (today - registration_date).days
    return (registration_date + timedelta(days=random.randint(0, difference)))

# Customer status
def generate_customer_status():
    return random.choices(
        population=["Active", "Inactive"],
        weights=[95, 5],
        k=1
    )[0]

# customer age
def generate_customer_age():
    return random.randint(18, 70)

# date of birth
def generate_date_of_birth(age):
    today = datetime.today()
    birth_year = today.year - age
    birth_month = random.randint(1, 12)
    birth_day = random.randint(1, 28)  # To avoid issues with February
    return datetime(birth_year, birth_month, birth_day).date()

# customer segment
def generate_customer_segment(monthly_income):
    if monthly_income < 50000:
        return "Budget"
    elif monthly_income < 150000:
        return "Mid-range"
    elif monthly_income < 300000:
        return "Premium"
    return "VIP"

# Credit limit
def generate_credit_limit(segment):
    limits = {
        "Budget": (0, 5000),
        "Mid-range": (5000, 30000),
        "Premium": (30000, 100000),
        "VIP": (100000, 500000)
    }

    minimum, maximum = limits[segment]
    return random.randint(minimum, maximum)

# preferred shopping day
def generate_preferred_shopping_day():
    return random.choices(
        population=[
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday"
        ],
        weights=[0.08, 0.08, 0.09, 0.10, 0.18, 0.25, 0.22],
        k=1
    )[0]

# Monthly Visit
def generate_monthly_visits(frequency):
    visits = {
        "Daily": random.randint(20, 30),
        "Weekly": random.randint(4, 5),
        "Bi-weekly": random.randint(2, 3),
        "Monthly": 1,
        "Yearly": 0
    }
    return visits[frequency]

# Average basket value
def generate_average_basket_value(segment):
    values = {
        "Budget": (500, 2500),
        "Mid-range": (2500, 7000),
        "Premium": (7000, 20000),
        "VIP": (20000, 60000)
    }

    minimum, maximum = values[segment]
    return round(random.uniform(minimum, maximum), 2)
   

