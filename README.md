# KRD-generator
The scripts inside here are generating synthetic dataset for retail data in kenya from 2020-2025
# Overview
The Kenyan Retail Dataset Generator is a Python-based synthetic data generation project designed to simulate realistic retail operations within a Kenyan retail environment.

The project generates interconnected master and transactional datasets representing customers, products, suppliers, stores, inventory, sales, payments, and returns.

The generated data can be used for:

 -  Data analytics
 -  SQL practice
 -  Data cleaning
 -  ETL pipelines
 -  Data warehousing
 -  Dashboard development
 -  Business intelligence
 -  Data quality testing
 -  Portfolio projects
# Project Objectives
The main objective of this project is to create a realistic synthetic retail dataset that can be used to practice end-to-end data workflows.

The project focuses on generating:

 - Structured master data
 - Transactional retail data
 - Referential relationships between datasets
 - Realistic business rules
 - Clean datasets
 - Raw datasets containing controlled data quality issues
# Dataset Architecture
The dataset is divided into three main layers:
   ### master data
Master data contains relatively stable business entities;  
This include:  
   > categories  
   > suppliers  
   > stores  
   customers  
   products  
   inventory  
### Transaction data
Transaction datasets represent retail activities:  
> Sales  
Sales details  
payment  
returns  

# Raw Data
Raw datasets contain controlled data quality issues designed for data cleaning and ETL practice.

Examples include:

 - Missing values
 - Duplicate values
 - Inconsistent text casing
 - Extra spaces
 - Phone number formatting differences
 - Email formatting errors
 - Location name variations
- Invalid inventory quantities
- Inconsistent stock status values
# Data Relationship 
```
Categories
    │
    └──── Products
              │
              ├──── Inventory
              │
              └──── Sales Details
                       │
Customers ───── Sales ───── Payments
                   │
                   └──── Returns

Suppliers ───── Products

Stores ───── Inventory
     │
     └──── Sales
```
# Data Generation Process
The project follows the following workflow:  
```
Reference Data
      ↓
Master Data Generation
      ↓
Business Rules
      ↓
Transaction Generation
      ↓
Data Validation
      ↓
Clean Dataset
      ↓
Data Quality Injection
      ↓
Raw Dataset
      ↓
Local Export
```
# Generated Datasets
### Master Data
```
| Dataset    | Description                                  |
| ---------- | -------------------------------------------- |
| Categories | Product categories                           |
| Suppliers  | Supplier and supplier branch information     |
| Stores     | Retail store locations                       |
| Customers  | Customer demographic and profile information |
| Products   | Product catalog                              |
| Inventory  | Product inventory across stores              |
```
### Transaction Data
```
| Dataset       | Description                          |
| ------------- | ------------------------------------ |
| Sales         | Retail sales transactions            |
| Sales Details | Individual products within each sale |
| Payments      | Payment records                      |
| Returns       | Returned products                    |
```
# Technology Used
- Python  
- Pandas  
- Faker  
- OpenPyXL 
- CSV
- Excel
# Installation
```
Clone the repository:

git clone YOUR_REPOSITORY_URL

Move into the project directory:

cd Kenyan-Retail-Dataset-Generator

Install dependencies:

pip install -r requirements.txt

Run the project:

python -m generator.main
```
# Data Quality Simulation
```
The project generates both clean and raw versions of selected datasets.

The raw datasets contain intentionally introduced data quality issues to simulate real-world data problems.

Examples include:

Clean:
Nairobi


Raw:
NAIROBI
Nairobi County
Nairobi 
 NRB

This allows users to practice:

Data cleaning
Standardization
Deduplication
Missing value handling
Data validation
ETL processes
```
# Important Disclaimer
```
This project generates synthetic data.
The dataset does not represent actual transactions, customers, suppliers, employees, or confidential business information from any real organization.

Names of locations, companies, brands, and products may be inspired by publicly known entities or
realistic business structures. However, all generated relationships, transactions, customer
records, financial values, and business activities are synthetic and should not be interpreted as
real business data.
```

