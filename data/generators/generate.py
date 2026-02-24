import os
import csv
import psycopg2
from config import DB_CONFIG
from seed_loader import load_products
from customers import generate_all_customers, insert_customers

def save_persona_mapping(personas):
    filepath = os.path.join(os.path.dirname(__file__), '..', 'seed', 'customer_personas.csv')
    with open(filepath, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['customer_id', 'persona'])
        for i, persona in enumerate(personas, start=1):
            writer.writerow([i, persona])
    print(f"Saved persona mapping for {len(personas)} customers")

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
    save_persona_mapping(personas)

    conn.close()
    print("\nDone! Database populated.")

if __name__ == "__main__":
    main()