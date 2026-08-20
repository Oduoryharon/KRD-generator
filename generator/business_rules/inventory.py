import random

# Inventory stock status
STOCK_STATUS = [
    "In Stock",
    "Low Stock",
    "Out of Stock"
]

STOCK_STATUS_WEIGHTS = [
    75,
    20,
    5
]

# Generate stock status
def generate_stock_status():
    return random.choices(
        population= STOCK_STATUS,
        weights= STOCK_STATUS_WEIGHTS,
        k=1
    )[0]

# Generate stock quality
def generate_stock_quantity(stock_status, reorder_level):
    reorder_level = int(reorder_level)
    if stock_status == "Out of Stock":
        return 0
    if stock_status == "Low Stock":
        minimum = 1
        maximum = max(1, reorder_level - 1)
        return random.randint(minimum, maximum)
    if stock_status == "In Stock":
        minimum = max(1, reorder_level)
        maximum = max(minimum + 1, reorder_level * 4)
        return random.randint(minimum, maximum)

