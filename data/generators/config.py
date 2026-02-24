import os
from dotenv import load_dotenv

load_dotenv()

# Database connection
DB_CONFIG = {
    "host": os.getenv("POSTGRES_HOST", "localhost"),
    "port": int(os.getenv("POSTGRES_PORT", 5432)),
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD")
}

# Date range for simulation (18 months of data)
START_DATE = "2024-01-01"
END_DATE = "2025-06-30"

# Volume settings
NUM_CUSTOMERS = 10000
NUM_PRODUCTS = 200

# Customer persona distribution (must sum to 1.0)
PERSONAS = {
    "loyal": 0.20,
    "gradual_churner": 0.25,
    "sudden_churner": 0.15,
    "casual": 0.25,
    "one_and_done": 0.15
}

# Product categories with relative weights
PRODUCT_CATEGORIES = {
    "electronics": 0.15,
    "clothing": 0.25,
    "home": 0.175,
    "beauty": 0.125,
    "sports": 0.10,
    "books": 0.075,
    "food": 0.06,
    "accessories": 0.065
}

# Acquisition channels with weights
ACQUISITION_CHANNELS = {
    "organic": 0.25,
    "paid_ad": 0.30,
    "referral": 0.15,
    "social_media": 0.20,
    "email_campaign": 0.10
}

# Regions
REGIONS = ["AU", "US", "UK", "EU", "APAC"]