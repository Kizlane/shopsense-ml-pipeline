
import numpy as np
import psycopg2
from faker import Faker
from datetime import datetime, timedelta

from config import (
    DB_CONFIG, NUM_CUSTOMERS, PERSONAS, 
    ACQUISITION_CHANNELS, REGIONS, START_DATE, END_DATE
)

fake = Faker()

fakers = {
    "AU": Faker('en_AU'),
    "US": Faker('en_US'),
    "UK": Faker('en_GB'),
    "EU": Faker('de_DE'),
    "APAC": Faker('ja_JP')
}

def assign_persona():
    """
    Randomly assigns a customer persona based on weights in config.
    
    Logic:
    - PERSONAS dict has {"loyal": 0.20, "gradual_churner": 0.25, ...}
    - Use np.random.choice to pick one persona based on those weights
    - Return the persona string
    """
    
    personas = list(PERSONAS.keys())
    weights = list(PERSONAS.values())
    persona = np.random.choice(personas,p=weights)
    return persona

def assign_acquisition_channel(persona):
    """
    Assigns an acquisition channel, influenced by persona.
    
    Logic:
    - Base weights come from ACQUISITION_CHANNELS in config
    - But the channel should correlate with persona:
        - "loyal" customers are more likely from "referral" or "organic"
        - "one_and_done" customers are more likely from "paid_ad"
        - "sudden_churner" can come from anywhere
        - "gradual_churner" slightly more likely from "paid_ad" or "social_media"
        - "casual" uses base weights as-is
    - Adjust the base weights based on persona, then normalize so they sum to 1.0
    - Use np.random.choice with the adjusted weights
    
    Args:
        persona: string like "loyal"
    
    Returns:
        string like "referral"
    
    Hint:
        - Start with a copy of the base weights as a dict
        - Multiply specific channel weights by a factor (e.g. 1.5 for more likely)
        - Normalize: divide each weight by the sum of all weights
        - Then use np.random.choice
    """
    base_weights = ACQUISITION_CHANNELS.copy()

    match persona:
        case "loyal":
            base_weights["organic"] *= 1.5
            base_weights["paid_ad"] *= 0.5
            base_weights["referral"] *= 2.0
            base_weights["social_media"] *= 0.9
            base_weights["email_campaign"] *= 0.7
        case "gradual_churner":
            base_weights["organic"] *= 0.6
            base_weights["paid_ad"] *= 1.8
            base_weights["referral"] *= 0.9
            base_weights["social_media"] *= 1.9
            base_weights["email_campaign"] *= 0.7
        case "sudden_churner":
            base_weights["organic"] *= 1.1
            base_weights["paid_ad"] *= 0.8
            base_weights["referral"] *= 1.1
            base_weights["social_media"] *= 1.2
            base_weights["email_campaign"] *= 0.9


    channels = list(base_weights.keys())
    weights = list(base_weights.values())
    total = sum(weights)
    weights = [w / total for w in weights]

    return np.random.choice(channels, p=weights)
        


def generate_signup_date(persona):
    """
    Generates a signup date within the simulation window.
    
    Logic:
    - Convert START_DATE and END_DATE strings to datetime objects
    - Loyal customers tend to sign up earlier (they've been around longer)
    - One-and-done customers can sign up anytime
    - Gradual churners sign up in the first half mostly
    - Sudden churners sign up in the first two-thirds
    - Casual customers sign up throughout
    
    Use np.random.beta to skew the distribution:
    - beta(2, 5) skews toward the start (loyal)
    - beta(2, 2) is roughly uniform (casual)
    - beta(1.5, 3) skews slightly early (gradual_churner)
    
    Args:
        persona: string like "loyal"
    
    Returns:
        a datetime.date object
    """
    start = datetime.strptime(START_DATE, "%Y-%m-%d")
    end = datetime.strptime(END_DATE, "%Y-%m-%d")
    total_days = (end - start).days
    skew = np.random.beta(1,1)
    if persona == "loyal":
        skew = np.random.beta(2, 5)
    elif persona == "gradual_churner":
        skew = np.random.beta(1.5, 3)
    elif persona == "sudden_churner":
        skew = np.random.beta(2, 3)
    elif persona == "casual":
        skew = np.random.beta(2, 2)
    elif persona == "one_and_done":
        skew = np.random.beta(1, 1)  # truly uniform
    sign_up = start + timedelta(days=int(total_days * skew))
    return sign_up.date()
    
def generate_single_customer():
    """
    Generates one complete customer record.
    
    Logic:
    - Assign a persona using assign_persona()
    - Generate fake first_name, last_name, email using Faker
    - Generate a fake address_line using Faker
    - Pick a region using np.random.choice from REGIONS
    - Assign acquisition_channel using assign_acquisition_channel(persona)
    - Generate signup_date using generate_signup_date(persona)
    
    For email: use a format like firstname.lastname.XXXX@example.com
    where XXXX is a random number. This avoids duplicates better than
    Faker's default email generator.
    
    For region: apply a slight NULL rate (~5%) to simulate missing data.
    Use np.random.random() < 0.05 to decide if region should be None.
    
    Args:
        customer_number: int, used for potential sequencing
    
    Returns:
        tuple of (customer_dict, persona)
        - customer_dict has keys: first_name, last_name, email, 
          address_line, created_date, region, acquisition_channel
        - persona is a string (kept separate because it won't go in the DB)
    """
    
    persona = assign_persona()
    first = fake.first_name()
    last = fake.last_name()
    email = f"{first.lower()}.{last.lower()}.{np.random.randint(1000,9999)}@example.com"
    region = None if np.random.random() < 0.05 else np.random.choice(REGIONS)
    if region is None:
        address = fake.street_address()
    else:
        address = fakers[region].street_address()
    created_date = generate_signup_date(persona)
    acquisition_channel = assign_acquisition_channel(persona)

    return (
    {
        'first_name': first,
        'last_name': last,
        'email': email,
        'address_line': address,
        'created_date': created_date,
        'region': region,
        'acquisition_channel': acquisition_channel
    },
    persona
)

def generate_all_customers():
    """
    Generates all customers and returns them with their personas.
    
    Logic:
    - Create two empty lists: customers and personas
    - Loop NUM_CUSTOMERS times, calling generate_single_customer each time
    - Append results to both lists
    - Print a summary: total customers and count per persona
    - Return (customers, personas) as a tuple
    
    The personas list is important — it maps 1:1 with customers and will 
    be used later by the transaction and event generators to simulate 
    behavior patterns.
    """
    customers = []
    personas = []

    for _ in range(NUM_CUSTOMERS):
        customer, persona = generate_single_customer()
        customers.append(customer)
        personas.append(persona)

    print(f"Generated {len(customers)} customers")
    for p in set(personas):
        print(f"  {p}: {personas.count(p)}")
    return customers, personas

def insert_customers(customers, db_connection):
    """
    Inserts generated customers into the PostgreSQL customer table.
    
    Logic:
    - Same pattern as seed_loader: cursor, execute in loop, commit
    - INSERT INTO customer (first_name, last_name, email, address_line, 
      created_date, region, acquisition_channel) VALUES (...)
    - Handle NULLs naturally — psycopg2 converts Python None to SQL NULL
    
    Args:
        customers: list of dicts from generate_all_customers()
        db_connection: psycopg2 connection object
    
    Returns:
        Nothing, but prints success/failure message
    """
    cursor = db_connection.cursor()

    try:
        for c in customers:
            cursor.execute(
                """INSERT INTO customer 
                (first_name, last_name, email, address_line, created_date, region, acquisition_channel) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                (c['first_name'], c['last_name'], c['email'], c['address_line'],
                 c['created_date'], c['region'], c['acquisition_channel'])
            )
        db_connection.commit()
        print(f"Successfully inserted {len(customers)} customers")
    except Exception as e:
        db_connection.rollback()
        print(f"Error: {e}")

    cursor.close()
