from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models, app, db
from app.models import Item, Order, Order_Item_Association


@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        "Order": Order,
        "Item": Item,
        "Order_Item_Association": Order_Item_Association,
    }


db.drop_all()
db.create_all()
pizza, burger, salad = [
    Item(description="pizza", price="9.99", quantity=5),
    Item(description="burger", price="5.00", quantity=3),
    Item(description="salad", price="3.50", quantity=10),
]

pizza_order, burger_order = [
    Order(
        note="With some dipping sauce, thanks",
        payment_amount=9.99,
        item_id_and_quantity_str="Item #1 x 1",
    ),
    Order(
        note="Some fries with that, please",
        payment_amount=10.00,
        item_id_and_quantity_str="Item #2 x 2",
    ),
]
db.session.add_all([pizza, burger, salad, pizza_order, burger_order])
db.session.commit()
