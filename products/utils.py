from .models import Products
from collections import Counter
from decimal import Decimal

def calculate_total(product_codes):
    """
    Given a list of product codes (e.g. ["GR1", "GR1", "CF1"]),
    apply pricing rules and return the final total with discounts.
    """
    total = Decimal("0.00")
    counts = Counter(product_codes)  # counts each product code

    for code, quantity in counts.items():
        try:
            product = Products.objects.get(product_code=code)
        except Products.DoesNotExist:
            continue  # skip invalid codes

        if code == "GR1":
            # Buy one, get one free: only pay for half (rounded up)
            total += product.price * (quantity // 2 + quantity % 2)

        elif code == "SR1":
            # If 3 or more, price drops to 4.50
            unit_price = Decimal("4.50") if quantity >= 3 else product.price
            total += unit_price * quantity

        elif code == "CF1":
            # If 3 or more, price drops to 2/3 of original
            unit_price = product.price * Decimal("2") / Decimal("3") if quantity >= 3 else product.price
            total += unit_price * quantity

        else:
            # No special rule
            total += product.price * quantity

    return float(round(total, 2))