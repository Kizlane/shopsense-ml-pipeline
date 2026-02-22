import os
import numpy as np
import pandas as pd

from config import PRODUCT_CATEGORIES, PRICE_RANGES, NUM_PRODUCTS

file_path = os.path.join(os.path.dirname(__file__), 'product_list.csv')

def generate_product_names():
    """
    Creates a dictionary of realistic product names for each category.
    
    Logic:
    - For each category in PRODUCT_CATEGORIES, define a list of 15-20 
      possible product names. These should sound like real products.
    - For example, "electronics" might have names like 
      "Wireless Bluetooth Headphones", "USB-C Charging Cable", etc.
    - "books" might have "The Art of Cooking", "Python for Beginners", etc.
    - Return a dict where keys are category names and values are lists of 
      product name strings.
    
    Hint: Just hardcode these. It's a catalogue, not random data.
    You want enough names per category so that when we pick from them,
    there's variety.
    """
    products_df = pd.read_csv(file_path)
    product_names = products_df.groupby('category')['product_name'].apply(list).to_dict()
    return product_names


def generate_price(category):
    """
    Generates a single realistic price for a product in the given category.
    
    Logic:
    - Look up the (min, max) range for this category from PRICE_RANGES
    - Use numpy's random to generate a price, but NOT uniformly
    - Real product prices cluster toward the lower end (more cheap items 
      than expensive ones). A log-normal or skewed distribution works well.
    - Round to 2 decimal places (it's money)
    
    Args:
        category: string like "electronics"
    
    Returns:
        float like 49.99
    
    Hint:
        - np.random.uniform(min, max) would work but gives flat distribution
        - Better approach: generate a random number between 0 and 1 using 
          np.random.beta(2, 5) which skews toward lower values, then scale 
          it to your price range: min + (max - min) * skewed_value
        - Round with round(price, 2)
    """
    # TODO: Implement this function
    pass


def build_product_catalogue():
    """
    Orchestrator function that builds the full product catalogue.
    
    Logic:
    - Call allocate_products_per_category to get counts per category
    - Call generate_product_names to get the name options
    - For each category, loop through its allocated count:
        - Randomly pick a name from that category's name list (without 
          repeating names within the same category)
        - Generate a price using generate_price
        - Store as a dict with keys matching your SQL columns:
          product_name, category, price, created_at
    - created_at should be a random date BEFORE your simulation starts
      (products exist before customers start buying). Use dates between
      "2023-06-01" and "2023-12-31"
    - Return a list of dicts, one per product
    
    Hint:
        - Use np.random.choice(name_list, size=count, replace=False) 
          to pick names without repeats
        - For random dates, you can pick a random number of days to add
          to the start date using np.random.randint()
        - Don't include product_id — remember SERIAL handles that
    """
    # TODO: Implement this function
    pass


def insert_products(products, db_connection):
    """
    Inserts the generated products into the PostgreSQL product table.
    
    Logic:
    - Create a cursor from the db_connection
    - Write an INSERT INTO statement for the product table
    - Loop through the products list and execute the insert for each one
    - Commit the transaction
    - Close the cursor
    
    Args:
        products: list of dicts from build_product_catalogue()
        db_connection: a psycopg2 connection object
    
    Hint:
        - The SQL looks like:
          INSERT INTO product (product_name, category, price, created_at)
          VALUES (%s, %s, %s, %s)
        - Use cursor.execute(sql, (dict['product_name'], dict['category'], ...))
        - Don't forget db_connection.commit() at the end or nothing saves
        - Wrap in try/except to catch errors and rollback if something fails
    """
    # TODO: Implement this function
    pass