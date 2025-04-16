import psycopg2
from elasticsearch import Elasticsearch

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="airflow",
    user="postgres",
    password="chaitu",
    host="postgres",  # Use service name from docker-compose
    port="5432"
)

cursor = conn.cursor()
cursor.execute("SELECT * FROM your_table_name")  # <-- Replace with actual table
columns = [desc[0] for desc in cursor.description]

# Connect to Elasticsearch
es = Elasticsearch("http://elasticsearch:9200")

for row in cursor.fetchall():
    doc = dict(zip(columns, row))
    es.index(index="your_index_name", document=doc)

cursor.close()
conn.close()
