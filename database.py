import psycopg2

# Replace these with your actual credentials
conn = psycopg2.connect(
    dbname="airflow",
    user="postgres",
    password="chaitu",
    host="localhost",
    port="5432"
)
cur = conn.cursor()
cur.execute("SELECT version();")
print(cur.fetchone())
import pandas as pd
import psycopg2
from datetime import datetime

# Step 1: Read CSV
df = pd.read_csv('his.csv')



# Step 3: Create table (with PRIMARY KEY on id)
create_table_query = """
CREATE TABLE IF NOT EXISTS data (
    id TEXT PRIMARY KEY,
    date DATE,
    upvotes NUMERIC,
    comment_text TEXT,
    sentiment_score NUMERIC(5, 4)
);
"""
cur.execute(create_table_query)
conn.commit()

cur.execute(create_table_query)
conn.commit()

insert_query = """
INSERT INTO data (id, date, upvotes, comment_text, sentiment_score)
VALUES (%s, %s, %s, %s, %s)
ON CONFLICT (id) DO NOTHING;
"""

# 5. Build list of tuples from DataFrame
records = []
for _, row in df.iterrows():
    cid   = str(row['id'])
    cdate = datetime.strptime(str(row['date']), '%Y-%m-%d').date()
    ups   = float(row['upvotes'])
    text  = str(row['comment_text'])
    sent  = round(float(row['sentiment_score']), 4)
    records.append((cid, cdate, ups, text, sent))

# 6. Bulk‑insert with error handling
try:
    cur.executemany(insert_query, records)
    conn.commit()
    print(f"Inserted {len(records)} rows into oo (duplicates skipped).")
except Exception as e:
    conn.rollback()
    print(f"Error inserting records: {e}")