from generator.utils import generate_id, random_date
from generator.generators.categories import generate_categories

def main():
    print("=" * 50)
    print("Welcome to the Kenyan Retail Dataset Generator!")
    print("=" * 50)

    print("\nGenerating Categories...")
    generate_categories()
    print("Categories generated successfully!")

if __name__ == "__main__":
    main()