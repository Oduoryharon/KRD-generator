# Data Generation Process

## Kenyan Retail Dataset Generator

This document explains how the Kenyan Retail Dataset Generator creates synthetic retail datasets.

The project was designed to generate realistic but fictional Kenyan retail data for learning, portfolio development, data engineering, analytics, and data quality projects.

---

# Overview

The generator creates two main versions of the data:

1. Clean datasets
2. Raw datasets with controlled data quality issues

The general process is:

```text
Reference Data
        ↓
Business Rules
        ↓
Master Data Generation
        ↓
Transaction Generation
        ↓
Clean Dataset Output
        ↓
Data Quality Injection
        ↓
Raw Dataset Output
        ↓
Local Export
```

---

# Project Structure

```text
generator/
│
├── business_rules/
│   ├── customer_behavior.py
│   ├── data_quality.py
│   ├── inventory.py
│   ├── pricing.py
│   ├── promotion.py
│   └── seasonality.py
│
├── generators/
│   ├── categories.py
│   ├── customers.py
│   ├── inventory.py
│   ├── payment.py
│   ├── products.py
│   ├── promotions.py
│   ├── raw_export.py
│   ├── return.py
│   ├── sales.py
│   ├── sales_details.py
│   ├── stores.py
│   └── suppliers.py
│
├── reference_data/
│
├── output/
│   ├── master/
│   ├── transaction/
│   └── raw/
│
├── config.py
├── main.py
└── utils.py
```

---

# Step 1: Reference Data

Reference datasets provide the base information used during generation.

Examples include:

- Kenyan counties
- Kenyan towns
- Product brands
- Product templates
- Pricing rules
- VAT rates

Reference data helps maintain consistency between generated records.

For example:

```text
Product
    ↓
Category
    ↓
Supplier
    ↓
Brand
    ↓
Pricing Rule
```

This ensures that relationships between generated datasets remain valid.

---

# Step 2: Business Rules

Business rules define the logic used to generate realistic synthetic data.

Examples include:

- Customer age ranges
- Occupation-based income ranges
- Marital status distributions
- Customer activity status
- Product pricing ranges
- Inventory stock levels
- Payment status probabilities
- Return reasons

Business rules are separated from the generation scripts to improve maintainability and project organization.

---

# Step 3: Master Data Generation

Master datasets are generated before transactional datasets.

The generation order is approximately:

```text
Categories
    ↓
Suppliers
    ↓
Stores
    ↓
Customers
    ↓
Products
    ↓
Inventory
```

This order ensures that foreign key relationships can be maintained.

For example, products require:

- Category information
- Supplier information
- Brand information

Inventory records require:

- Product information
- Store information

---

# Step 4: Transaction Generation

Transactional datasets are generated after the required master data exists.

The transaction generation process follows:

```text
Customers
Products
Stores
    ↓
Sales
    ↓
Sales Details
    ↓
Payments
    ↓
Returns
```

Each transactional record references valid master or parent records.

For example:

```text
Sales.CustomerID
        ↓
Customers.CustomerID

Sales.StoreID
        ↓
Stores.StoreID

SalesDetails.ProductID
        ↓
Products.ProductID

Payments.SaleID
        ↓
Sales.SaleID

Returns.SaleID
        ↓
Sales.SaleID
```

---

# Step 5: Clean Dataset Generation

The generator first creates clean datasets.

Clean datasets are validated before being saved.

Validation checks include:

- Empty dataset detection
- Duplicate primary key detection
- Foreign key validation
- Required column validation
- Reference integrity checks

The clean datasets are stored in:

```text
output/master/
```

and

```text
output/transaction/
```

These datasets represent the clean version of the synthetic retail environment.

---

# Step 6: Data Quality Injection

After the clean dataset is created, controlled data quality issues are introduced into copies of the datasets.

The original clean datasets remain unchanged.

Examples of injected issues include:

## Missing Values

Some values may be removed from fields such as:

- Email
- Phone numbers
- Product pack size
- Inventory quantities

---

## Duplicate Information

Controlled duplicates may be introduced in selected fields.

Examples include:

- Duplicate phone numbers
- Duplicate batch numbers
- Duplicate records in selected datasets

---

## Formatting Inconsistencies

Text values may contain:

- Leading spaces
- Trailing spaces
- Mixed capitalization
- Alternative phone number formats

Examples:

```text
Nairobi
NAIROBI
nairobi
 Nairobi
Nairobi 
```

---

## Invalid or Inconsistent Values

Examples include:

```text
In Stock
instock
INSTOCK
Low Stock
low stock
out stock
```

Other quality issues may include:

- Negative inventory quantities
- Invalid email formatting
- Missing contact information
- County name variations

---

# Step 7: Raw Dataset Creation

The data quality injection process creates raw datasets.

The process is:

```text
Clean Dataset
      ↓
Copy Dataset
      ↓
Inject Controlled Data Quality Issues
      ↓
Raw Dataset
```

The raw datasets are stored in:

```text
output/raw/
```

Examples include:

```text
customers_raw.csv
products_raw.csv
suppliers_raw.csv
stores_raw.csv
inventory_raw.csv
sales_raw.csv
sales_details_raw.csv
payment_raw.csv
returns_raw.csv
```

Excel versions are also generated where configured.

---

# Step 8: Data Export

The project includes a raw export process that allows generated datasets to be copied or exported to a local destination.

This makes the generated data easier to use with tools such as:

- Microsoft Excel
- SQL Server
- Power BI
- Python
- Jupyter Notebook
- Apache Spark
- Data warehouse environments

The datasets can also be prepared for upload to platforms such as Kaggle.

---

# Data Relationships

The generated datasets follow a relational structure.

```text
                    Categories
                        │
                        │ CategoryID
                        ▼
                    Products
                   /    |     \
                  /     |      \
                 ▼      ▼       ▼
            Inventory  SalesDetails  Returns
                           │
                           │ SaleID
                           ▼
                         Sales
                       /       \
                      /         \
                     ▼           ▼
                Customers      Payments
                     │
                     │
                    Stores
```

---

# Design Principles

The generator follows several design principles.

## Referential Integrity

Generated foreign keys are linked to existing parent records.

Examples:

```text
ProductID → Products
CustomerID → Customers
StoreID → Stores
SaleID → Sales
SupplierID → Suppliers
CategoryID → Categories
```

---

## Separation of Concerns

The project separates:

```text
Reference Data
Business Rules
Data Generation
Data Quality
Utilities
Output
```

This makes the project easier to maintain and extend.

---

## Clean and Raw Data Separation

Clean datasets are not overwritten when dirty datasets are generated.

```text
Clean Data
    ↓
Copy
    ↓
Inject Quality Issues
    ↓
Raw Data
```

This allows users to practice:

- Data cleaning
- ETL
- Data validation
- Data quality monitoring
- Data transformation

---

## Analytical Flexibility

Where possible, analytical metrics are not permanently stored in the generated data.

This allows analysts to calculate their own metrics.

Examples include:

- Revenue
- Profit margin
- Inventory turnover
- Reorder indicators
- Customer spending patterns
- Return rates
- Average order value
- Sales trends
- Seasonality analysis

This approach avoids unnecessarily storing derived values that can be calculated from the available data.

---

# Reproducibility

The project uses random generation with controlled random seeds in selected modules.

For example:

```python
random.seed(42)
```

This improves reproducibility during development and testing.

However, modifying the generation logic, dataset size, or execution order may result in different outputs.

---

# Synthetic Data Notice

All data generated by this project is synthetic.

The project may generate realistic-looking:

- Names
- Phone numbers
- Email addresses
- Suppliers
- Stores
- Products
- Transactions

However, these records are generated for educational and development purposes.

The dataset does not intentionally represent real customers, actual businesses, or real commercial transactions.

---

# Intended Use

This project is suitable for:

- Portfolio projects
- SQL practice
- Data engineering practice
- Data warehousing
- ETL development
- Data cleaning exercises
- Data quality analysis
- Business intelligence dashboards
- Exploratory data analysis
- Database design
- Machine learning experimentation

---

# Limitations

Although the generator attempts to create realistic relationships and distributions, it is not intended to simulate the Kenyan retail industry with statistical accuracy.

The generated data should not be used for:

- Financial forecasting
- Government reporting
- Official statistics
- Real market analysis
- Commercial decision-making involving real customers or businesses

The dataset is primarily designed for technical learning and portfolio development.