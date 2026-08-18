"""DataShop transaction producer.

Replays datashop_transactions.csv into the payment_transactions topic
as a live stream at ~500 events/second.
"""

import csv
import json
import time
from datetime import datetime
from pathlib import Path

from kafka import KafkaProducer

CSV_PATH = Path.home() / "datashop-platform" / "data" / "raw" / "datashop_transactions.csv"
TOPIC = "payment_transactions"
SLEEP_BETWEEN_MESSAGES = 0.002  # ~500 events/second


def to_epoch_ms(ts: str) -> int:
    return int(datetime.strptime(ts, "%Y-%m-%d %H:%M:%S").timestamp() * 1000)


def main():
    producer = KafkaProducer(
        bootstrap_servers="localhost:9092",
        key_serializer=lambda k: k.encode("utf-8"),
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )

    sent = 0
    start = time.time()

    with open(CSV_PATH, newline="") as f:
        for row in csv.DictReader(f):
            event = {
                "transaction_id": row["transaction_id"],
                "customer_id": row["customer_id"],
                "product_id": row["product_id"],
                "category": row["category"],
                "amount": float(row["amount"]),
                "quantity": int(row["quantity"]),
                "timestamp": to_epoch_ms(row["timestamp"]),
                "status": row["status"],
                "country": row["country"],
                "payment_method": row["payment_method"],
            }

            producer.send(TOPIC, key=event["customer_id"], value=event)
            sent += 1

            if sent % 5000 == 0:
                rate = sent / (time.time() - start)
                print(f"Sent {sent:>6} events  ({rate:.0f} events/sec)")

            time.sleep(SLEEP_BETWEEN_MESSAGES)

    producer.flush()
    elapsed = time.time() - start
    print(f"Done: {sent} events in {elapsed:.1f}s ({sent / elapsed:.0f} events/sec)")


if __name__ == "__main__":
    main()
