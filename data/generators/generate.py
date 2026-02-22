import psycopg2
from config import DB_CONFIG
from seed_loader import load_products
from customers import generate_all_customers, insert_customers

def main():
    conn = psycopg2.connect(**DB_CONFIG)
    print("Connected to database\n")

    # Step 1: Seed products
    print("--- Loading products ---")
    load_products(conn)

    # Step 2: Generate and insert customers
    print("\n--- Generating customers ---")
    customers, personas = generate_all_customers()
    insert_customers(customers, conn)

    # Steps 3-5 will go here later:
    # generate_transactions(customers, personas, conn)
    # generate_events(customers, personas, conn)
    # generate_support_tickets(customers, personas, conn)

    conn.close()
    print("\nDone! Database populated.")

if __name__ == "__main__":
    main()