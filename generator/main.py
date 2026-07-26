from generator.utils import generate_id, random_date
from generator.generators.categories import generate_categories
from generator.generators.suppliers import generate_suppliers
from generator.generators.stores import generate_stores
from generator.generators.stores import towns_df, counties_df

def main():
    print("=" * 50)
    print("Welcome to the Kenyan Retail Dataset Generator!")
    print("=" * 50)

    print("\nGenerating Categories...")
    generate_categories()
    print("Categories generated successfully!")

    print("\nGenerating Suppliers...")
    generate_suppliers()
    print("Suppliers generated successfully!")

    print("\nGenerating Stores...")
    generate_stores()
    print("Stores generated successfully!")

if __name__ == "__main__":
    main()