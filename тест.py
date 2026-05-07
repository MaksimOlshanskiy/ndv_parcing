import psycopg2

conn = psycopg2.connect(
    host="192.168.252.134",
    port=5432,
    database="postgres",
    user="postgres",
    password="PassToPostgres$"
)

cur = conn.cursor()
cur.execute("SELECT version();")
print(cur.fetchone())

conn.close()