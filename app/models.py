from datetime import datetime

from app import db


class Order_Item_Association(db.Model):
    __tablename__ = "order_item_association"

    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"), primary_key=True)

    quantity_in_order = db.Column(db.Integer)

    item = db.relationship("Item", back_populates="orders")
    order = db.relationship("Order", back_populates="items")

    def __init__(self, order=None, item=None, quantity_in_order=None):
        self.order = order
        self.item = item
        self.quantity_in_order = quantity_in_order

    def __repr__(self):
        return "<Order{}Item{}Quant{}".format(
            self.order_id, self.item, self.quantity_in_order
        )


class Item(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(140))
    price = db.Column(db.String(140))
    quantity = db.Column(db.Integer)
    orders = db.relationship("Order_Item_Association", back_populates="item")

    def __init__(self, description=None, price=None, quantity=None):
        self.description = description
        self.price = price
        self.quantity = quantity

    def __repr__(self):
        return "<Item{}>".format(self.id)


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    payment_amount = db.Column(db.String(140))
    note = db.Column(db.String(140))
    item_id_and_quantity_str = db.Column(db.String(140))
    items = db.relationship("Order_Item_Association", back_populates="order")

    def __init__(self, note=None, payment_amount=None, item_id_and_quantity_str=None):
        self.note = note
        self.payment_amount = payment_amount
        self.item_id_and_quantity_str = item_id_and_quantity_str

    def __repr__(self):
        return "<Order{}>".format(self.id)

    def add_items(self, item_and_quantity_list):
        for item, quantity in item_and_quantity_list:
            self.items.append(
                Order_Item_Association(
                    item=item, order=self, quantity_in_order=quantity
                )
            )
        db.session.commit()
