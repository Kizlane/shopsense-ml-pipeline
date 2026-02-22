import pandas as pd
import os

file_path = os.path.join(os.path.dirname(__file__), '..', 'seed', 'product_list.csv')

def load_products(db_connection):
    product_df = pd.read_csv(file_path)
    cursor = db_connection.cursor()

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
        db_connection.commit()
        print(f"Successfully inserted {len(product_df)} products")
    except Exception as e:
        db_connection.rollback()
        print(f"Error: {e}")

    cursor.close()