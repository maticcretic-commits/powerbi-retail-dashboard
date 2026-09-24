#!/usr/bin/env python3
"""Generate data/retail_sales.csv — 1,500 synthetic retail transactions.

Columns: OrderID, Date, Store, Product, Category, Units, UnitPrice,
Revenue, Channel. Dates span 2024-01-01 to 2025-09-30 so YTD / MoM
DAX time-intelligence has something to chew on.

Run: python3 generate_data.py
"""

import csv
import os
import random
from datetime import date, timedelta

random.seed(21)
os.makedirs("data", exist_ok=True)

STORES = ["Koramangala", "Indiranagar", "HSR Layout", "Whitefield", "JP Nagar"]
PRODUCTS = {
    "Running Shoes": ("Footwear", 2999),
    "Sneakers": ("Footwear", 3999),
    "T-Shirt": ("Apparel", 799),
    "Jeans": ("Apparel", 1999),
    "Jacket": ("Apparel", 3499),
    "Backpack": ("Accessories", 1499),
    "Cap": ("Accessories", 499),
    "Watch": ("Accessories", 5999),
}
CHANNELS = ["Online", "Offline"]

FIRST = date(2024, 1, 1)
SPAN = (date(2025, 9, 30) - FIRST).days
N = 1500

with open("data/retail_sales.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["OrderID", "Date", "Store", "Product", "Category",
                "Units", "UnitPrice", "Revenue", "Channel"])
    for i in range(N):
        product = random.choices(
            list(PRODUCTS),
            weights=[18, 14, 20, 16, 8, 10, 8, 6])[0]
        category, price = PRODUCTS[product]
        # weekend + festive-season lift, so the trend looks real
        d = FIRST + timedelta(days=random.randint(0, SPAN))
        units = random.randint(1, 4)
        if d.month in (10, 11, 12):  # festive season
            units += random.randint(0, 2)
        revenue = units * price
        w.writerow([f"SO-{200001 + i}", d.isoformat(),
                    random.choice(STORES), product, category,
                    units, price, revenue,
                    random.choices(CHANNELS, weights=[45, 55])[0]])

print("Wrote data/retail_sales.csv")
