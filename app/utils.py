from flask import flash

from app.models import Item


def is_valid_quantity_ordered(item, quantity_ordered):
    if quantity_ordered < 1:
        flash(f"Item # {item.id} quantity ordered must be >= 1")
        return False

    if quantity_ordered > item.quantity:
        flash(
            f"You ordered Item # {item.id} x {quantity_ordered} but there are only {item.quantity} available"
        )
        return False
    return True
