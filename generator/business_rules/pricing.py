import random

# Category pricing rules

CATEGORY_PRICE_RULES = {

    "Dairy": {
        "cost": (40, 500),
        "markup": (0.10, 0.35)
    },

    "Beverages": {
        "cost": (30, 500),
        "markup": (0.10, 0.40)
    },

    "Bakery": {
        "cost": (30, 400),
        "markup": (0.10, 0.35)
    },

    "Fruits": {
        "cost": (20, 300),
        "markup": (0.10, 0.40)
    },

    "Vegetables": {
        "cost": (10, 250),
        "markup": (0.10, 0.40)
    },

    "Meat": {
        "cost": (100, 1500),
        "markup": (0.10, 0.35)
    },

    "Fish & Seafood": {
        "cost": (100, 1500),
        "markup": (0.10, 0.40)
    },

    "Frozen Foods": {
        "cost": (100, 1500),
        "markup": (0.10, 0.35)
    },

    "Household": {
        "cost": (50, 3000),
        "markup": (0.15, 0.45)
    },

    "Personal Care": {
        "cost": (50, 3000),
        "markup": (0.15, 0.50)
    },

    "Cleaning Products": {
        "cost": (50, 2500),
        "markup": (0.10, 0.40)
    },

    "Baby Products": {
        "cost": (50, 5000),
        "markup": (0.10, 0.40)
    },

    "Stationery": {
        "cost": (10, 1500),
        "markup": (0.15, 0.50)
    },

    "Electronics": {
        "cost": (500, 30000),
        "markup": (0.05, 0.30)
    },

    "Clothing": {
        "cost": (200, 5000),
        "markup": (0.15, 0.60)
    },

    "Footwear": {
        "cost": (300, 6000),
        "markup": (0.15, 0.60)
    },

    "Pet Supplies": {
        "cost": (100, 3000),
        "markup": (0.10, 0.40)
    },

    "Alcoholic Beverages": {
        "cost": (100, 3000),
        "markup": (0.10, 0.35)
    },

    "Non-Alcoholic Beverages": {
        "cost": (30, 500),
        "markup": (0.10, 0.40)
    }
}


# Default rule

DEFAULT_PRICE_RULE = {
    "cost": (20, 1000),
    "markup": (0.10, 0.40)
}


# Get category rule

def get_pricing_rule(category):

    category = str(category).strip()

    return CATEGORY_PRICE_RULES.get(
        category,
        DEFAULT_PRICE_RULE
    )

# Generate cost price

def generate_cost_price(category):

    rule = get_pricing_rule(category)

    minimum, maximum = rule["cost"]

    return round(
        random.uniform(
            minimum,
            maximum
        ),
        2
    )


# Generate selling price.

def generate_selling_price(
    category,
    cost_price
):

    rule = get_pricing_rule(category)

    minimum_markup, maximum_markup = rule["markup"]

    markup = random.uniform(
        minimum_markup,
        maximum_markup
    )

    selling_price = (
        cost_price
        * (1 + markup)
    )

    return round(
        selling_price,
        2
    )