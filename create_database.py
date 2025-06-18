import sqlite3

SCHEMA_INFO = """
Table: customers (customer_id, registration_date, city, gender)
Table: orders (order_id, customer_id, order_date, total_amount, status)
Table: order_items (item_id, order_id, product_name, quantity, unit_price)
"""

table_info = """
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INTEGER PRIMARY KEY,
        registration_date DATE,
        city VARCHAR(50),
        gender CHAR(1)
    );

    CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        order_date DATE,
        total_amount DECIMAL(10,2),
        status VARCHAR(20),
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
    );

    CREATE TABLE IF NOT EXISTS order_items (
        item_id INTEGER PRIMARY KEY,
        order_id INTEGER,
        product_name VARCHAR(100),
        quantity INTEGER,
        unit_price DECIMAL(10,2),
        FOREIGN KEY (order_id) REFERENCES orders(order_id)
    );
"""

def create_database():
    connection = sqlite3.connect('retail_db.sqlite')
    cursor = connection.cursor()

    # Enable foreign key constraints
    cursor.execute("PRAGMA foreign_keys = ON;")

    # Create tables
    cursor.executescript(table_info)

    # Insert sample data
    sample_data = '''
    INSERT OR IGNORE INTO customers (customer_id, registration_date, city, gender) VALUES
        (1, '2023-01-01', 'New York', 'M'),
        (2, '2023-01-02', 'Los Angeles', 'F'),
        (3, '2023-01-03', 'Chicago', 'M'),
        (4, '2023-01-04', 'Houston', 'F'),
        (5, '2023-01-05', 'Phoenix', 'M'),
        (6, '2025-05-06', 'Philadelphia', 'F');

    INSERT OR IGNORE INTO orders (order_id, customer_id, order_date, total_amount, status) VALUES
        (1, 1, '2023-02-01', 100.00, 'completed'),
        (2, 2, '2023-02-02', 150.00, 'pending'),
        (3, 1, '2023-02-03', 200.00, 'completed'),
        (4, 3, '2023-03-04', 300.00, 'completed'),
        (5, 4, '2023-04-05', 250.00, 'pending'),
        (6, 2, '2023-05-01', 180.00, 'completed'),
        (7, 5, '2023-06-01', 220.00, 'completed');

    INSERT OR IGNORE INTO order_items (item_id, order_id, product_name, quantity, unit_price) VALUES
        (1, 1, 'Widget', 2, 50.00),
        (2, 2, 'Gadget', 3, 50.00),
        (3, 3, 'Widget', 4, 50.00),
        (4, 4, 'Device', 2, 150.00),
        (5, 5, 'Gadget', 5, 50.00),
        (6, 6, 'Widget', 2, 90.00),
        (7, 7, 'Gadget', 4, 55.00);
    '''

    cursor.executescript(sample_data)
    
    print("Database created with sample data!")
    print("\nSchema Information:")
    print(SCHEMA_INFO)

    connection.commit()
    connection.close()

if __name__ == "__main__":
    create_database()
