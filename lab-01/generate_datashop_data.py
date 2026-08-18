"""DataShop seed data generator — Lab 01.

Generates the three foundational CSV files used throughout the course:
  - datashop_customers.csv     (5,000 rows)
  - datashop_products.csv      (100 rows)
  - datashop_transactions.csv  (100,000 rows)

Fixed random seed => everyone gets the identical dataset.
"""

import csv
import random
import uuid
from datetime import datetime, timedelta
from pathlib import Path

from faker import Faker

SEED = 42
random.seed(SEED)
Faker.seed(SEED)
fake = Faker()

OUTPUT_DIR = Path.home() / "datashop-platform" / "data" / "raw"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

N_CUSTOMERS = 5_000
N_PRODUCTS = 100
N_TRANSACTIONS = 100_000

COUNTRIES = ["USA", "UK", "Germany", "France", "Canada"]

# Category -> (price_min, price_max). Electronics is deliberately the
# most expensive category so aggregations have a clear "winner".
CATEGORIES = {
    "Electronics": (50.0, 2000.0),
    "Clothing": (10.0, 200.0),
    "Home & Garden": (15.0, 500.0),
    "Sports": (20.0, 400.0),
    "Books": (5.0, 60.0),
}

STATUSES = ["completed", "pending", "failed", "refunded"]
STATUS_WEIGHTS = [0.85, 0.07, 0.05, 0.03]

PAYMENT_METHODS = ["credit_card", "paypal", "debit_card", "gift_card"]
PAYMENT_WEIGHTS = [0.50, 0.25, 0.20, 0.05]

START_DATE = datetime(2025, 1, 1)
END_DATE = datetime(2025, 12, 31, 23, 59, 59)


def generate_customers():
    customers = []
    for i in range(1, N_CUSTOMERS + 1):
        customers.append(
            {
                "customer_id": f"CUST-{i:05d}",
                "name": fake.name(),
                "email": fake.email(),
                "country": random.choice(COUNTRIES),
                "signup_date": fake.date_between(
                    start_date="-3y", end_date="today"
                ).isoformat(),
            }
        )
    return customers


def generate_products():
    products = []
    category_names = list(CATEGORIES)
    for i in range(1, N_PRODUCTS + 1):
        # Even spread: 20 products per category
        category = category_names[(i - 1) % len(category_names)]
        lo, hi = CATEGORIES[category]
        products.append(
            {
                "product_id": f"PROD-{i:04d}",
                "product_name": f"{fake.word().title()} {fake.word().title()}",
                "category": category,
                "price": round(random.uniform(lo, hi), 2),
            }
        )
    return products


def generate_transactions(customers, products):
    span_seconds = int((END_DATE - START_DATE).total_seconds())
    transactions = []
    for _ in range(N_TRANSACTIONS):
        customer = random.choice(customers)
        product = random.choice(products)
        quantity = random.choices([1, 2, 3, 4, 5], weights=[60, 20, 10, 6, 4])[0]
        amount = round(product["price"] * quantity, 2)
        timestamp = START_DATE + timedelta(
            seconds=random.randint(0, span_seconds)
        )
        transactions.append(
            {
                "transaction_id": str(uuid.uuid4()),
                "customer_id": customer["customer_id"],
                "product_id": product["product_id"],
                "category": product["category"],
                "amount": amount,
                "quantity": quantity,
                "timestamp": timestamp.isoformat(sep=" "),
                "status": random.choices(STATUSES, weights=STATUS_WEIGHTS)[0],
                "country": customer["country"],
                "payment_method": random.choices(
                    PAYMENT_METHODS, weights=PAYMENT_WEIGHTS
                )[0],
            }
        )
    return transactions


def write_csv(filename, rows):
    path = OUTPUT_DIR / filename
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f"  {path}  ({len(rows):,} rows)")


def main():
    print("Generating DataShop seed data...")
    customers = generate_customers()
    products = generate_products()
    transactions = generate_transactions(customers, products)

    print("Writing CSV files:")
    write_csv("datashop_customers.csv", customers)
    write_csv("datashop_products.csv", products)
    write_csv("datashop_transactions.csv", transactions)
    print("Done.")


if __name__ == "__main__":
    main()
