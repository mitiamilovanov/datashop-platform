SELECT
    transaction_id,
    customer_id,
    product_id,
    category,
    CAST(amount AS DOUBLE) AS amount,
    CAST(quantity AS INTEGER) AS quantity,
    CAST(timestamp AS TIMESTAMP) AS transaction_ts,
    country,
    payment_method
FROM {{ source('raw', 'transactions') }}
WHERE status = 'completed'
