import pandas as pd
import psycopg2
import os

file_path = os.path.join(os.path.dirname(__file__), '..', 'seed', 'product_list.csv')

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="shopsense",
    user="shopsense",
    password="shopsense123"
)

product_df = pd.read_csv(file_path)

cursor = conn.cursor()

try:
    for index, row in product_df.iterrows():
        cursor.execute(
            """INSERT INTO product 
               (product_name, category, price, sku, item_description, avg_rating, weight_kg, stock_status, created_at) 
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            (row['product_name'], row['category'], row['price'], row['sku'],
             row['item_description'], row['avg_rating'], row['weight_kg'],
             row['stock_status'], row['created_at'])
        )
    conn.commit()
    print(f"Successfully inserted {len(product_df)} products")
except Exception as e:
    conn.rollback()
    print(f"Error: {e}")

cursor.close()
conn.close()
