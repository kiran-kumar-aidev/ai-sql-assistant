
import sqlite3
from pathlib import Path

# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Database location
DB_PATH = BASE_DIR / "data" / "ecommerce.db"


def initialize_database():

    # Ensure data directory exists
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DB_PATH)

    cursor = connection.cursor()

    # Customers table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY,
            customer_name TEXT NOT NULL,
            email TEXT UNIQUE,
            city TEXT
        )
    """)

    # Products table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY,
            product_name TEXT NOT NULL,
            category TEXT,
            price REAL NOT NULL
        )
    """)

    # Orders table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER,
            order_date TEXT,
            status TEXT,
            FOREIGN KEY (customer_id)
                REFERENCES customers(customer_id)
        )
    """)

    # Order items table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            item_id INTEGER PRIMARY KEY,
            order_id INTEGER,
            product_id INTEGER,
            quantity INTEGER,
            unit_price REAL,
            FOREIGN KEY (order_id)
                REFERENCES orders(order_id),
            FOREIGN KEY (product_id)
                REFERENCES products(product_id)
        )
    """)

    # Sample customers
    cursor.executemany("""
        INSERT OR IGNORE INTO customers
        VALUES (?, ?, ?, ?)
    """, [
        (1, "Rahul Sharma", "rahul@email.com", "Hyderabad"),
        (2, "Priya Reddy", "priya@email.com", "Bangalore"),
        (3, "Amit Kumar", "amit@email.com", "Chennai"),
        (4, "Sneha Rao", "sneha@email.com", "Hyderabad"),
        (5, "Vikram Singh", "vikram@email.com", "Mumbai"),
        (6, "Ananya Das", "ananya@email.com", "Pune")
    ])

    # Sample products
    cursor.executemany("""
        INSERT OR IGNORE INTO products
        VALUES (?, ?, ?, ?)
    """, [
        (1, "Laptop", "Electronics", 65000),
        (2, "Smartphone", "Electronics", 30000),
        (3, "Headphones", "Accessories", 2500),
        (4, "Office Chair", "Furniture", 8500),
        (5, "Keyboard", "Accessories", 1500),
        (6, "Monitor", "Electronics", 18000)
    ])

    # Sample orders
    cursor.executemany("""
        INSERT OR IGNORE INTO orders
        VALUES (?, ?, ?, ?)
    """, [
        (101, 1, "2026-01-10", "Completed"),
        (102, 2, "2026-01-15", "Completed"),
        (103, 1, "2026-02-05", "Completed"),
        (104, 3, "2026-02-12", "Pending"),
        (105, 4, "2026-02-20", "Completed"),
        (106, 5, "2026-03-02", "Completed"),
        (107, 2, "2026-03-10", "Completed"),
        (108, 6, "2026-03-15", "Pending")
    ])

    # Sample order items
    cursor.executemany("""
        INSERT OR IGNORE INTO order_items
        VALUES (?, ?, ?, ?, ?)
    """, [
        (1, 101, 1, 1, 65000),
        (2, 101, 3, 2, 2500),
        (3, 102, 2, 1, 30000),
        (4, 103, 6, 2, 18000),
        (5, 103, 5, 2, 1500),
        (6, 104, 4, 1, 8500),
        (7, 105, 1, 1, 65000),
        (8, 105, 5, 3, 1500),
        (9, 106, 2, 2, 30000),
        (10, 107, 3, 4, 2500),
        (11, 108, 6, 1, 18000)
    ])

    connection.commit()
    connection.close()

    print("Database initialized successfully!")
    print(f"Database location: {DB_PATH}")


if __name__ == "__main__":
    initialize_database()
