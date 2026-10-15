"""Shared product data for Brew & Bite CEC.

TODO (group): replace the placeholder prices with your real selling prices
from the Business Analytics feasibility study.
"""

STUDENT_DISCOUNT = 0.10  # 10% off for CEC students (placeholder business rule)

PRODUCTS = [
    {"id": "cafe-latte", "name": "Café Latte", "category": "Drinks", "price": 70,
     "desc": "Smooth iced latte with fresh milk over espresso."},
    {"id": "spanish-latte", "name": "Spanish Latte", "category": "Drinks", "price": 80,
     "desc": "Iced latte sweetened with condensed milk."},
    {"id": "matcha-latte", "name": "Matcha Latte", "category": "Drinks", "price": 85,
     "desc": "Iced matcha with milk. The non-coffee pick."},
    {"id": "choc-chip-cookie", "name": "Chocolate Chip Cookie", "category": "Cookies", "price": 35,
     "desc": "Soft-baked cookie with chocolate chips."},
    {"id": "combo", "name": "Latte + Cookie Combo", "category": "Combos", "price": 95,
     "desc": "Any one latte with a cookie. Cheaper than buying both."},
]


def peso(amount):
    """Format a number as Philippine pesos, e.g. ₱70.00"""
    return f"₱{amount:,.2f}"
