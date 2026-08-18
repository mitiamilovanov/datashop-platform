from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'data_engineering',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}


def load_and_profile(**context):
    import pandas as pd

    df = pd.read_parquet('/home/giga/datashop-platform/data/parquet/datashop_transactions.parquet')

    stats = {
        'total_rows': len(df),
        'completed_count': len(df[df['status'] == 'completed']),
        'null_customer_count': int(df['customer_id'].isnull().sum()),
        'date_range': f"{df['timestamp'].min()} to {df['timestamp'].max()}"
    }

    # Передаём статистику вниз по пайплайну через XCom
    context['ti'].xcom_push(key='load_stats', value=stats)

    print(f"Loaded {stats['total_rows']} rows. Stats: {stats}")
    return stats


def clean_and_filter(**context):
    import pandas as pd

    df = pd.read_parquet('/home/giga/datashop-platform/data/parquet/datashop_transactions.parquet')

    cleaned = df[df['status'] == 'completed'].copy()
    cleaned = cleaned.dropna(subset=['customer_id', 'product_id', 'amount'])

    cleaned.to_parquet('/home/giga/datashop-platform/lab-09/output/cleaned_transactions.parquet', index=False)

    context['ti'].xcom_push(key='cleaned_count', value=len(cleaned))
    print(f"Cleaned: {len(df)} rows -> {len(cleaned)} rows")


def compute_daily_revenue(**context):
    import pandas as pd

    cleaned = pd.read_parquet('/home/giga/datashop-platform/lab-09/output/cleaned_transactions.parquet')

    daily_revenue = cleaned.groupby(
        [cleaned['timestamp'].dt.date, 'category', 'country']
    ).agg(
        total_revenue=('amount', 'sum'),
        order_count=('transaction_id', 'count')
    ).reset_index()

    daily_revenue.to_parquet('/home/giga/datashop-platform/lab-09/output/daily_revenue_summary.parquet', index=False)

    context['ti'].xcom_push(key='revenue_rows', value=len(daily_revenue))


def run_quality_checks(**context):
    import pandas as pd

    df = pd.read_parquet('/home/giga/datashop-platform/lab-09/output/daily_revenue_summary.parquet')

    checks = []
    checks.append(("row_count > 0", len(df) > 0))
    checks.append(("no_null_revenue", df['total_revenue'].isnull().sum() == 0))
    checks.append(("positive_revenue", (df['total_revenue'] >= 0).all()))
    checks.append(("valid_categories",
                   df['category'].isin(['Books', 'Clothing', 'Electronics',
                                        'Home & Garden', 'Sports']).all()))

    failures = [name for name, passed in checks if not passed]

    if failures:
        raise ValueError(f"Quality checks failed: {failures}")

    print(f"All {len(checks)} quality checks passed")


def notify_success(**context):
    ti = context['ti']
    load_stats = ti.xcom_pull(task_ids='load_and_profile', key='load_stats')
    cleaned_count = ti.xcom_pull(task_ids='clean_and_filter', key='cleaned_count')
    revenue_rows = ti.xcom_pull(task_ids='compute_daily_revenue', key='revenue_rows')

    print("Pipeline complete.")
    print(f"Loaded: {load_stats['total_rows']} rows")
    print(f"After cleaning: {cleaned_count} rows")
    print(f"Revenue rows: {revenue_rows}")


with DAG(
    dag_id='datashop_nightly_pipeline',
    default_args=default_args,
    description='DataShop nightly ETL pipeline',
    schedule='0 2 * * *',  # 2:00 AM daily
    catchup=False,
    tags=['datashop', 'nightly']
) as dag:
    t1 = PythonOperator(task_id='load_and_profile', python_callable=load_and_profile)
    t2 = PythonOperator(task_id='clean_and_filter', python_callable=clean_and_filter)
    t3 = PythonOperator(task_id='compute_daily_revenue', python_callable=compute_daily_revenue)
    t4 = PythonOperator(task_id='run_quality_checks', python_callable=run_quality_checks)
    t5 = PythonOperator(task_id='notify_success', python_callable=notify_success)

    t1 >> t2 >> t3 >> t4 >> t5
