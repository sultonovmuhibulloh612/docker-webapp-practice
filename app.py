import os
import time
import psycopg2
from flask import Flask

app = Flask(__name__)

def get_db_connection():
    for attempt in range(10):
        try:
            return psycopg2.connect(
                host="db",
                database="mydb",
                user="postgres",
                password="secret"
            )
        except psycopg2.OperationalError:
            print(f"База ещё не готова, попытка {attempt + 1}...")
            time.sleep(2)
    raise Exception("Не удалось подключиться к базе данных")

@app.route("/")
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS visits (id SERIAL PRIMARY KEY, count INTEGER)")
    cur.execute("SELECT count FROM visits LIMIT 1")
    row = cur.fetchone()
    if row is None:
        cur.execute("INSERT INTO visits (count) VALUES (1)")
        count = 1
    else:
        count = row[0] + 1
        cur.execute("UPDATE visits SET count = %s WHERE id = (SELECT id FROM visits LIMIT 1)", (count,))
    conn.commit()
    cur.close()
    conn.close()
    return f"Количество посещений: {count}\n"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
