"""DataShop fraud detection consumer.

Reads payment_transactions and alerts when a customer's cumulative
spending exceeds the threshold.
"""

import json

from kafka import KafkaConsumer

TOPIC = "payment_transactions"
GROUP_ID = "fraud-detection"
SPENDING_THRESHOLD = 1000.0

consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers="localhost:9092",
    group_id=GROUP_ID,
    auto_offset_reset="earliest",
    value_deserializer=lambda v: json.loads(v.decode("utf-8")),
)

print(f"Fraud detector started (group={GROUP_ID}, threshold=${SPENDING_THRESHOLD:.0f})")
print(f"Assigned partitions: {consumer.partitions_for_topic(TOPIC)}")

customer_spending = {}  # { customer_id: cumulative_amount }
processed = 0

for message in consumer:
    event = message.value
    customer_id = event["customer_id"]
    amount = float(event["amount"])

    customer_spending[customer_id] = customer_spending.get(customer_id, 0) + amount
    processed += 1

    if processed % 10000 == 0:
        print(f"... processed {processed} events, tracking {len(customer_spending)} customers")

    if customer_spending[customer_id] > SPENDING_THRESHOLD:
        print(
            f"FRAUD ALERT: Customer {customer_id} spent "
            f"${customer_spending[customer_id]:.2f} "
            f"(partition {message.partition}, offset {message.offset})"
        )
        customer_spending[customer_id] = 0  # Reset after alert
