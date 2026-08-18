"""Create the four DataShop policy documents for the RAG pipeline (Lab 12)."""

POLICIES = {
    "annual_leave_policy.txt": """DataShop Annual Leave Policy

Entitlement: All full-time DataShop employees are entitled to 24 days of paid
annual leave per calendar year. Part-time employees receive leave on a pro-rata
basis calculated from their contracted weekly hours.

Accrual: Annual leave accrues monthly at a rate of 2 days per month of
completed service. New employees begin accruing leave from their first day of
employment. Leave accrued during a probation period may be taken only after
the probation period is successfully completed.

Carryover: A maximum of 5 unused leave days may be carried over into the next
calendar year. Carried-over days must be used before March 31, after which
they expire without compensation. Exceptions require written approval from
both the department head and the HR director.

Requesting Leave: Leave requests must be submitted through the HR portal at
least 10 working days in advance for absences longer than 3 days. Shorter
absences require 3 working days of notice. Managers must respond to leave
requests within 5 working days.

Sick Leave: Sick leave is separate from annual leave. Employees receive 10
paid sick days per year. A doctor's note is required for absences of 3 or
more consecutive days.

Public Holidays: DataShop observes all national public holidays. When a
public holiday falls on a weekend, the following Monday is granted as a
substitute day off.
""",
    "travel_expense_policy.txt": """DataShop Travel and Expense Policy

Booking: All business travel must be booked through the corporate travel
portal at least 14 days before departure. Bookings made outside the portal
are reimbursed only with prior written approval from the finance team.

Per-Diem Rates: Domestic travel carries a per-diem of 60 EUR per day.
International travel within Europe carries a per-diem of 85 EUR per day.
Intercontinental travel carries a per-diem of 110 EUR per day. Per-diems
cover meals and incidental expenses; no receipts are required for per-diem
claims.

Accommodation: Hotel costs are capped at 150 EUR per night for domestic
travel and 200 EUR per night for international travel. Bookings above the
cap require pre-approval from the department head.

Transportation: Economy class is required for all flights under 6 hours.
Premium economy is permitted for flights over 6 hours. Business class
requires CFO approval. Train travel is first class for journeys over 3
hours. Taxi and ride-sharing expenses are reimbursed with receipts.

Reimbursement: Expense reports must be submitted within 30 days of the trip
through the finance portal, with itemized receipts attached. Approved
reimbursements are paid with the next monthly payroll run. Reports submitted
after 60 days are not reimbursed.
""",
    "office_policy.txt": """DataShop Office and Remote Work Policy

Remote Work: DataShop operates a hybrid model. Employees may work remotely
up to 3 days per week. Fully remote arrangements require approval from the
department head and a review every 6 months. Employees must be reachable
during core hours, 10:00 to 16:00 local time.

Desk Booking: Office desks are not assigned. Desks must be reserved through
the desk booking app no earlier than 7 days in advance. Unclaimed
reservations are released at 10:30. Teams may reserve project rooms for
recurring meetings up to one quarter in advance.

Equipment: Every employee receives a company laptop and one external
monitor for home use. Additional equipment such as ergonomic chairs or
standing desks can be requested through the IT portal with manager approval.
Company equipment must be returned within 5 working days of employment
ending.

Security: Laptops must be locked when unattended. Visitors must be
registered at reception and accompanied at all times. Confidential
documents must be stored in lockable cabinets, never left on desks
overnight (clean desk policy).

Office Hours: The office building is accessible with a badge from 06:00 to
22:00 on working days. Weekend access requires prior notice to facilities.
""",
    "data_platform_policy.txt": """DataShop Data Platform Policy

Approved Environments: All data platform work must run in one of the
approved conda environments: bde_env for core processing with Spark,
DuckDB, dbt and Kafka clients; flink-env for Flink stream processing;
airflow-env for pipeline orchestration; gx-env for Great Expectations data
quality checks; superset-env for the Superset analytics dashboard; and
rag-env for AI and vector search workloads. Mixing environments or
installing lab dependencies into the base environment is prohibited.

Approved Tools: The approved platform stack is: Apache Spark for
distributed processing, Apache Iceberg for lakehouse table management, dbt
with DuckDB for SQL transformations, Apache Kafka for event streaming,
Apache Flink for stateful stream processing, Apache Airflow for
orchestration, Great Expectations for data quality validation, Apache
Superset for dashboards, and ChromaDB with SentenceTransformers for
semantic search.

Data Storage: Analytical datasets must be stored in Parquet format.
CSV files are permitted only as an ingestion source and must be converted
before downstream use. Production tables live in the Iceberg lakehouse.

Data Quality: Every scheduled pipeline must include a Great Expectations
validation step. Pipelines that fail validation must halt before the
serving layer is updated.

Access: Credentials and API tokens must never be committed to version
control. Secrets are managed through environment variables.
""",
}

for filename, text in POLICIES.items():
    with open(filename, "w") as f:
        f.write(text)
    print(f"Created {filename} ({len(text)} chars)")

print(f"\n{len(POLICIES)} policy documents created.")
