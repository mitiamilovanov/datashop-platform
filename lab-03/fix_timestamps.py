import pyarrow.parquet as pq

for name in ["transactions", "customers", "products"]:
    path = f"/home/giga/datashop-platform/data/parquet/datashop_{name}.parquet"
    table = pq.read_table(path)
    pq.write_table(
        table, path,
        compression="zstd",
        coerce_timestamps="us",            # наносекунды -> микросекунды
        allow_truncated_timestamps=True,   # разрешаем отбросить лишнюю точность
    )
    print(f"{name}: rewritten")
