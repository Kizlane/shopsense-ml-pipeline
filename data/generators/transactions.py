import numpy as np
import psycopg2
from datetime import datetime, timedelta

from config import DB_CONFIG, START_DATE, END_DATE


def get_product_catalogue(db_connection):
    """
    Fetches all products from the database to use when building orders.
    
    Logic:
    - Query the product table for product_id, price, and category
    - Return as a list of dicts
    
    We need this so that when we create order_items, we're referencing 
    real product_ids that exist in the database.
    
    Hint:
        - cursor.execute("SELECT product_id, price, category FROM product")
        - cursor.fetchall() returns a list of tuples
        - Convert to list of dicts for easier access
    """
    cursor = db_connection.cursor()
    try:
        cursor.execute("SELECT product_id, price, category FROM product;")
        rows = cursor.fetchall()
        products = [{'product_id': r[0], 'price': float(r[1]), 'category': r[2]} for r in rows]
    except Exception as e:
        db_connection.rollback()
        print(f"Error: {e}")
    cursor.close()
conn = psycopg2.connect(**DB_CONFIG)    
get_product_catalogue(conn)

def get_order_frequency(persona, months_active):
    """
    Returns the probability of a customer ordering in any given week.
    
    This is the heart of the churn simulation. The persona determines
    the base frequency, and for churners it decays over time.
    
    Args:
        persona: string like "loyal"
        months_active: how many months since this customer signed up
    
    Returns:
        float between 0 and 1 (probability of ordering this week)
    
    Logic:
        - "loyal": ~0.35 (orders roughly every 3 weeks), stays consistent
        - "casual": ~0.12 (orders roughly every 8 weeks), stays consistent
        - "one_and_done": 0.0 (handled separately, they just get 1 order)
        - "gradual_churner": starts at ~0.30, decays over time
            - Use a decay formula: base * (decay_rate ** months_active)
            - e.g. 0.30 * (0.85 ** months_active) 
            - After 6 months: 0.30 * 0.85^6 = 0.11
            - After 12 months: 0.30 * 0.85^12 = 0.04 (barely ordering)
        - "sudden_churner": ~0.30 until a trigger month, then drops to 0.0
            - Pick a trigger month (random between 3 and 12 months in)
            - Before trigger: normal frequency
            - After trigger: 0 (they're gone)
    
    Hint:
        - For gradual churner: return base_rate * (decay_rate ** months_active)
        - For sudden churner: you'll need to store/pass the trigger month
          Consider adding it as a parameter or generating it elsewhere
    """
    # TODO: Implement this function
    pass


def generate_order_items(products, persona):
    """
    Generates the items for a single order.
    
    Logic:
    - Decide how many items (weighted toward fewer items)
    - Randomly select that many products from the catalogue
        - Don't pick the same product twice in one order
    - For each item, assign a quantity (usually 1, sometimes 2-3)
    - Calculate total_amount as sum of (price * quantity) for all items
    
    Args:
        products: list of product dicts from get_product_catalogue()
        persona: string (loyal customers might have slightly larger baskets)
    
    Returns:
        tuple of (items_list, total_amount)
        - items_list: list of dicts with keys: product_id, quantity, unit_price
        - total_amount: float, sum of all items
    
    Hint:
        - selected = np.random.choice(len(products), size=num_items, replace=False)
        - For quantity: np.random.choice([1,1,1,2,2,3]) gives realistic distribution
    """

    # 1. How many items in this order? (geometric distribution, capped)
    max_items = 12 if persona == "loyal" else 8 if persona == "casual" else 10
    num_items = min(np.random.geometric(p=0.4), max_items)

    # 2. Pick a primary category for this order
    categories = list(set(p['category'] for p in products))
    primary_category = np.random.choice(categories)

    # 3. Split products into primary category and everything else
    primary_products = [p for p in products if p['category'] == primary_category]
    other_products = [p for p in products if p['category'] != primary_category]

    # 4. Decide how many items from primary vs other categories (~70-90% primary)
    num_primary = max(1, int(num_items * np.random.uniform(0.7, 0.9)))
    num_other = num_items - num_primary

    # 5. Select products (no duplicates within the order)
    num_primary = min(num_primary, len(primary_products))
    primary_indices = np.random.choice(len(primary_products), size=num_primary, replace=False)
    selected = [primary_products[i] for i in primary_indices]

    if num_other > 0 and len(other_products) > 0:
        num_other = min(num_other, len(other_products))
        other_indices = np.random.choice(len(other_products), size=num_other, replace=False)
        selected += [other_products[i] for i in other_indices]

    # 6. Build the items list with quantities and calculate total
    items = []
    total_amount = 0.0

    for product in selected:
        quantity = np.random.choice([1, 1, 1, 2, 2, 3])  # mostly 1, sometimes 2-3
        item = {
            'product_id': product['product_id'],
            'quantity': int(quantity),
            'unit_price': product['price']
        }
        items.append(item)
        total_amount += product['price'] * quantity

    total_amount = round(total_amount, 2)

    return items, total_amount


def generate_order_date(last_order_date, persona, weeks_gap):
    """
    Generates the next order date based on when the last order was.
    
    Logic:
    - Start from last_order_date
    - Add weeks_gap weeks (roughly)
    - Add some random noise (1-5 days either way) so orders aren't
      perfectly spaced
    - Make sure the date doesn't exceed END_DATE
    
    Args:
        last_order_date: datetime.date of the previous order
        persona: string (not used much here, but available)
        weeks_gap: int, approximate weeks between orders
    
    Returns:
        datetime.date or None if past END_DATE
    """
    # TODO: Implement this function
    pass


def simulate_customer_orders(customer_id, persona, signup_date, products):
    """
    Simulates the entire order history for one customer.
    
    This is the main simulation loop for a single customer.
    
    Logic:
    - Start from signup_date
    - For one_and_done: generate exactly 1 order (maybe 2 with small probability)
      within the first 2 weeks, then stop
    - For all other personas:
        - Walk through time week by week from signup to END_DATE
        - Each week, calculate order probability using get_order_frequency()
        - Roll a random number: if < probability, they order that week
        - Generate the order using generate_order_items()
        - Track the date for spacing
    - For sudden_churner: pick a random trigger_month (3-12 months after signup)
      After that month, no more orders
    - Add order_status: ~90% "completed", ~7% "returned", ~3% "cancelled"
    
    Args:
        customer_id: int (from database)
        persona: string
        signup_date: datetime.date
        products: list of product dicts
    
    Returns:
        tuple of (orders_list, order_items_list)
        - orders_list: list of dicts with keys: customer_id, order_date, 
          total_amount, order_status
        - order_items_list: list of dicts with keys: order_id (placeholder),
          product_id, quantity, unit_price
    """
    # TODO: Implement this function
    pass


def generate_all_transactions(customers, personas, db_connection):
    """
    Orchestrates transaction generation for all customers.
    
    Logic:
    - Fetch product catalogue from DB
    - Query customer table to get customer_ids and signup dates
      (we need the DB-assigned IDs, not just the dicts)
    - For each customer, call simulate_customer_orders()
    - Collect all orders and order_items
    - Insert orders first (need the DB-assigned order_ids)
    - Then insert order_items using those order_ids
    - Print summary stats
    
    The tricky part: order_items need to reference real order_ids from
    the database. So you insert each order, get back the id using
    cursor.fetchone() with RETURNING, then use that id for the items.
    
    Hint for getting the order_id back after insert:
        cursor.execute(
            "INSERT INTO orders (...) VALUES (...) RETURNING order_id",
            (values,)
        )
        order_id = cursor.fetchone()[0]
    
    Args:
        customers: list of customer dicts
        personas: list of persona strings (parallel to customers)
        db_connection: psycopg2 connection
    """
    # TODO: Implement this function
    pass