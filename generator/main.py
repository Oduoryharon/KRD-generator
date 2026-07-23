from generator.generators import suppliers
from generator.generators import categories
from generator.generators.categories import generate_categories
from generator.generators.suppliers import generate_suppliers
from generator.generators.products import generate_products    

def main():
    # Generate categories
    print("Generating categories...")
    generate_categories()
    
    # Generate suppliers
    print("Generating suppliers...")
    generate_suppliers()
    
    # Generate products
    print("Generating products...")
    generate_products(categories, suppliers)

if __name__ == "__main__":
    main()
    # You can add more generation functions here for stores, customers, employees, promotions, and sales