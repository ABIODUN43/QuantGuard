"""Seed QuantGuard AI demo data.

Usage:
    python scripts/seed_data.py
"""

from app.db.init_db import seed_demo_data


if __name__ == "__main__":
    seed_demo_data()
    print("Seeded QuantGuard AI demo data.")
