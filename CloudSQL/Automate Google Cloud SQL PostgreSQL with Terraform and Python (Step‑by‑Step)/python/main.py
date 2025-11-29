import psycopg2

DB_HOST = "127.0.0.1"  # Cloud SQL public IP. "127.0.0.1" 
DB_PORT = "5432"
DB_NAME = "appdb"
DB_USER = "appuser"
DB_PASS = "admin@123"

def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        connect_timeout=10
    )

def create_table():
    query = """
    CREATE TABLE IF NOT EXISTS employees_2 (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        role VARCHAR(100),
        salary INTEGER
    );
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query)
    conn.commit()
    cur.close()
    conn.close()
    print("Table created.")

def insert_data():
    query = """
    INSERT INTO employees_2 (name, role, salary)
    VALUES (%s, %s, %s)
    RETURNING id;
    """
    values = [
        ("Alice", "Engineer", 85000),
        ("Bob", "Manager", 95000),
        ("Charlie", "Analyst", 65000)
    ]
    conn = get_connection()
    cur = conn.cursor()
    for v in values:
        cur.execute(query, v)
        print("Inserted ID:", cur.fetchone()[0])
    conn.commit()
    cur.close()
    conn.close()

def run_queries():
    conn = get_connection()
    cur = conn.cursor()

    print("\nEmployees_2 Table Data:")
    cur.execute("SELECT * FROM employees_2;")
    print(cur.fetchall())

    cur.close()
    conn.close()

if __name__ == "__main__":
    create_table()
    insert_data()
    run_queries()
