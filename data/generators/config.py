# data/generators/config.py

# Database connection
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "shopsense",
    "user": "shopsense",
    "password": "shopsense123"
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

# Product categories with relative weights (some categories have more products)
PRODUCT_CATEGORIES = {
    "electronics": 0.15,
    "clothing": 0.20,
    "home": 0.15,
    "beauty": 0.12,
    "sports": 0.10,
    "books": 0.13,
    "food": 0.08,
    "accessories": 0.07
}

# Price ranges per category (min, max)
PRICE_RANGES = {
    "electronics": (29.99, 899.99),
    "clothing": (14.99, 149.99),
    "home": (9.99, 299.99),
    "beauty": (7.99, 89.99),
    "sports": (12.99, 199.99),
    "books": (4.99, 39.99),
    "food": (2.99, 49.99),
    "accessories": (5.99, 79.99)
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