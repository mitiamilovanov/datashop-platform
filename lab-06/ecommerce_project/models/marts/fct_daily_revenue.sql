SELECT
    DATE_TRUNC('day', t.transaction_ts) AS sale_date,
    t.category,
    t.country,
    COUNT(*) AS order_count,
    ROUND(SUM(t.amount), 2) AS total_revenue
FROM {{ ref('stg_transactions') }} t
GROUP BY 1, 2, 3
ORDER BY 1 DESC
