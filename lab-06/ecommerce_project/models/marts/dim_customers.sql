SELECT
    c.customer_id,
    c.customer_name,
    c.email,
    c.country,
    c.signup_date,
    COUNT(t.transaction_id) AS total_orders,
    COALESCE(ROUND(SUM(t.amount), 2), 0) AS lifetime_value
FROM {{ ref('stg_customers') }} c
LEFT JOIN {{ ref('stg_transactions') }} t USING (customer_id)
GROUP BY 1, 2, 3, 4, 5
