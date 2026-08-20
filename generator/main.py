
from generator.generators.categories import generate_categories
from generator.generators.suppliers import generate_suppliers
from generator.generators.stores import generate_stores
from generator.generators.products import generate_products
from generator.generators.customers import generate_customers
from generator.generators.inventory import generate_inventory
from generator.generators.sales import generate_sales
from generator.generators.sales_details import generate_sales_details
from generator.generators.payment import generate_payments
from generator.generators.returns import generate_returns

def main():
    print("=" * 60)
    print("Welcome to the Kenyan Retail Dataset Generator!")
    print("=" * 60)

    print("\nGenerating Categories...")
    generate_categories()
    print("Categories generated successfully!")

    print("\nGenerating Suppliers...")
    generate_suppliers()
    print("Suppliers generated successfully!")

    print("\nGenerating Stores...")
    generate_stores()
    print("Stores generated successfully!")

    print("\nGenerating Products...")
    generate_products()
    print("Products generated successfully!")

    print("\nGenerating customers...")
    generate_customers()
    print("Customers generated successfully!")

    print("\nGenerating Inventory...")
    generate_inventory()
    print("Inventory generated successfully!")

    print("\nGenerating Sales...")
    generate_sales()
    print("Sales generated successfully!")

    print("\nGenerating Sales_details...")
    generate_sales_details()
    print("Sales_details generated successfully!")

    print("\nGenerating Payments...")
    generate_payments()
    print("payments generated successfully!")

    print("\nGenerating returns...")
    generate_returns()
    print("returns generated successfully!")

    print("\n" + "=" * 60)
    print("Kenyan retail Dataset generated successfully!")
    print("=" * 60)

    print("\nGenerated datasets are available in:")
    print("generator/output/master/")
    print("generator/output/transaction/")
    print("generator/output/raw/")


    

if __name__ == "__main__":
    main()