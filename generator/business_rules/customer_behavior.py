import random
from datetime import datetime , timedelta   

# customer occupation and income
OCCUPATION_INCOME = {
    "Teacher": (10000, 150000),

    "Student": (0, 50000),

    "Lecturer": (80000, 200000),

    "Doctor": (200000, 500000),

    "Nurse" : (50000, 150000),

    "Clinical Officer": (60000, 150000),

    "Software Developer": (100000, 400000),

    "Database Administrator": (90000, 250000),

    "Accountant": (70000, 200000),

    "Auditor": (70000, 200000),

    "Business Owner": (50000, 1000000),

    "Farmer": (30000, 150000),

    "Driver": (30000, 100000),

    "Police Officer": (50000, 150000),

    "Engineer": (80000, 300000),

    "Mechanic": (40000, 150000),

    "Electrician": (40000, 150000),

    "Plumber": (40000, 150000),

    "Carpenter": (40000, 150000),

    "Sales Representative": (40000, 150000),

    "Cashier": (30000, 100000),

    "Unskilled Laborer": (20000, 80000),

    "UnEmployed": (0, 20000)

}

MARITAL_STATUS = [
    "Single",
    "Married",
    "Divorced",
    "Widowed"
]

# Customer Status
CUSTOMER_STATUS = [
    "Active",
    "Inactive"
]

def generate_monthly_income(occupation):
    minimum, maximum = OCCUPATION_INCOME.get(
        occupation,
        (20000, 100000)
    )
    return random.randint(
        minimum,
        maximum
    )

def generate_marital_status():
    return random.choices(
        population= MARITAL_STATUS,
        weights= [
            55,
            38,
            4,
            3
        ],
        k=1
    )[0]

# Generate customer status
def generate_customer_status():
    return random.choices(
        population= CUSTOMER_STATUS,
        weights= [
            95,
            5
        ],
        k=1
    )[0]

# customer age
def generate_customer_age():
    return random.randint (
        18,
        70
    )

# generate date of birth
def generate_date_of_birth(age):
    today = datetime.today()
    birth_year = today.year - age
    birth_month = random.randint (1, 12)
    birth_day = random.randint(1, 28)

    return datetime (
        birth_year,
        birth_month,
        birth_day
    ).date()

# Generate registration date
def generate_registration_date():
    start_date = datetime(
        2020,
        1,
        1
    )

    end_date = datetime(
        2025,
        12,
        31
    )

    difference = (end_date-start_date).days
    return(start_date + timedelta(days= random.randint(0, difference))).date()

# Normalize registraton date
def normalize_regstration_date(registration_date):
    if isinstance(
        registration_date,
        str
    ):
        return datetime.strptime(
            registration_date,
            "%Y-%m-%d"
        ).date()

    if isinstance(
        registration_date,
        datetime
    ):
        return registration_date.date()
    return registration_date


