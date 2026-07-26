import os
import random
from datetime import datetime, timedelta
from string import digits
from sys import prefix
import pandas as pd

def create_directory(path: str):
    os.makedirs(path, exist_ok=True)

def save_csv(df: pd.DataFrame, filepath: str):
    df.to_csv(filepath, index=False)

def save_excel(df: pd.DataFrame, filepath: str):
    df.to_excel(filepath, index=False)

def generate_id(prefix: str, number: int, digits: int = 3) -> str:
    return {f"{prefix}{number:0{digits}d}"}
 

def random_date(start_date: str, end_str: str):
    date_format = "%Y-%m-%d"
    start = datetime.strptime(start_date, date_format)
    end = datetime.strptime(end_str, date_format)
    days_between = (end - start).days
    random_days = random.randint(0, days_between)
    return (start + timedelta(days=random_days))
