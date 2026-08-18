SELECT
    customer_id,
    name AS customer_name,
    email,
    country,
    CAST(signup_date AS DATE) AS signup_date
FROM {{ source('raw', 'customers') }}
