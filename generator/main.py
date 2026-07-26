from utils import generate_id, random_date

def main():
    print(generate_id("CAT", 1))
    print(generate_id("SUP", 25))
    print(generate_id("CUS", 15, 5))

    print(random_date("2020-01-01", "2025-12-31"))

if __name__ == "__main__":
    main()