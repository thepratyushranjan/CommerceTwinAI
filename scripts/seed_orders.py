import sqlite3
import json
import random
from datetime import datetime, timedelta
import os

# Ensure the data directory exists
os.makedirs('data', exist_ok=True)

# Database file path
DB_PATH = 'data/orders.db'

def create_database():
    """Creates the SQLite database and orders table."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create the orders table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            order_id TEXT PRIMARY KEY,
            customer_email TEXT NOT NULL,
            status TEXT NOT NULL,
            items TEXT NOT NULL,
            total REAL NOT NULL,
            order_date TEXT NOT NULL,
            ship_date TEXT,
            tracking_number TEXT
        )
    ''')
    
    # Clear existing data if running multiple times
    cursor.execute('DELETE FROM orders')
    conn.commit()
    return conn

def generate_mock_orders(conn):
    """Generates and inserts mock order data into the database."""
    cursor = conn.cursor()
    
    statuses = ['pending', 'shipped', 'delivered', 'cancelled']
    
    # Specific emails to ensure we have multiple orders for testing "show all my orders"
    frequent_customers = [
        'alice@example.com',
        'bob@example.com',
        'charlie@test.com',
        'diana@domain.com',
        'eve@sample.org'
    ]
    
    # Product catalog for generating realistic items
    products = [
        {"name": "Wireless Noise-Canceling Headphones", "price": 299.99},
        {"name": "Ergonomic Office Chair", "price": 199.50},
        {"name": "Mechanical Gaming Keyboard", "price": 129.99},
        {"name": "Smart Fitness Watch", "price": 249.00},
        {"name": "Ceramic Coffee Mug set", "price": 34.99},
        {"name": "Organic Cotton T-Shirt", "price": 24.50},
        {"name": "Stainless Steel Water Bottle", "price": 45.00},
        {"name": "Yoga Mat", "price": 65.00},
        {"name": "Bluetooth Speaker", "price": 89.99},
        {"name": "Running Shoes", "price": 145.00}
    ]

    orders_to_insert = []
    
    # Generate 30 mock orders
    for i in range(1, 31):
        order_id = f"ORD-{1000 + i}"
        
        # Force the first few orders to be for our target test emails
        if i <= len(frequent_customers):
            customer_email = frequent_customers[i-1]
        elif i <= 15:
            customer_email = random.choice(frequent_customers)
        else:
            customer_email = f"customer_{i}@example.com"
            
        status = random.choice(statuses)
        
        # Generate random items for the order
        num_items = random.randint(1, 3)
        order_items = random.sample(products, k=num_items)
        
        # Calculate total
        total = sum(item['price'] for item in order_items)
        
        # Dates
        days_ago = random.randint(1, 30)
        order_date_obj = datetime.now() - timedelta(days=days_ago)
        order_date = order_date_obj.strftime("%Y-%m-%d")
        
        # Logic for shipped/delivered items
        ship_date = None
        tracking_number = None
        
        if status in ['shipped', 'delivered']:
            ship_date_obj = order_date_obj + timedelta(days=random.randint(1, 3))
            ship_date = ship_date_obj.strftime("%Y-%m-%d")
            tracking_number = f"TRK{random.randint(100000000, 999999999)}"
            
        if status == 'cancelled':
            ship_date = None
            tracking_number = None

        orders_to_insert.append((
            order_id,
            customer_email,
            status,
            json.dumps(order_items),  # Store items as JSON string
            round(total, 2),
            order_date,
            ship_date,
            tracking_number
        ))

    # Insert data
    cursor.executemany('''
        INSERT INTO orders (order_id, customer_email, status, items, total, order_date, ship_date, tracking_number)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', orders_to_insert)
    
    conn.commit()
    print(f"✅ Successfully seeded 30 mock orders into {DB_PATH}")

if __name__ == "__main__":
    connection = create_database()
    generate_mock_orders(connection)
    connection.close()
