from flask import flash, redirect, render_template, url_for

from app import app, db
from app.forms import (CreateMenuItemForm, CreateOrderForm, DeleteMenuItemForm,
                       UpdateMenuItemForm)
from app.helpers import is_valid_quantity_ordered
from app.models import Item, Order


@app.route("/")
@app.route("/index")
def index():
    items = db.session.query(Item).all()
    orders = db.session.query(Order).all()
    return render_template("index.html", items=items, orders=orders), 200


@app.route("/item", methods=["GET", "POST"])
def create_menu_item():
    form = CreateMenuItemForm()
    if not form.validate_on_submit():
        return render_template("create-menu-item.html", form=form), 200

    item = Item(
        description=form.description.data,
        quantity=form.quantity.data,
        price="{:.2f}".format(float(form.price.data)),
    )
    db.session.add(item)
    db.session.commit()
    flash(f"Successfully Added Menu Item: {form.description.data}")
    return redirect(url_for("index")), 302


@app.route("/item/<item_id>/update", methods=["GET", "POST"])
def update_menu_item(item_id):
    item = Item.query.filter_by(id=item_id).first()
    form = UpdateMenuItemForm()
    if not form.validate_on_submit():
        return render_template("update-menu-item.html", form=form, item=item), 200

    item = Item.query.filter_by(id=item_id).first()
    if item:
        item.description = (
            form.description.data if form.description.data != None else item.description
        )
        item.quantity = (
            form.quantity.data if form.quantity.data != None else item.quantity
        )
        item.price = (
            "{:.2f}".format(float(form.price.data))
            if form.price.data != None
            else item.price
        )
        db.session.commit()
        flash(f"Successfully Updated Menu Item: {form.description.data}"),
        return redirect(url_for("index")), 302


@app.route("/item/<item_id>/delete", methods=["GET", "POST"])
def delete_menu_item(item_id):
    item = Item.query.filter_by(id=item_id).first()
    form = DeleteMenuItemForm()
    if not form.validate_on_submit():
        return render_template("delete-menu-item.html", form=form, item=item), 200

    if item:
        db.session.delete(item)
        db.session.commit()
        flash(f"Successfully Deleted Menu Item: {item.description}")
        return redirect(url_for("index")), 302


@app.route("/order", methods=["GET", "POST"])
def create_order():
    try:
        form = CreateOrderForm()
        if not form.validate_on_submit():
            return render_template("create-order.html", form=form), 200

        payment_amount = 0
        item_id_and_quantity_list = []
        order = Order(note=form.note.data)

        for item_id_and_quantity in str(form.item_id_and_quantity_str.data).split(","):
            item_id, quantity_ordered = item_id_and_quantity.split("x")
            item_id, quantity_ordered = int(item_id), int(quantity_ordered)

            item = Item.query.get(item_id)
            if item is None:
                flash(f"Item # '{item_id}' is not a valid Item Id")
                return render_template("create-order.html", form=form)

            if not is_valid_quantity_ordered(item, quantity_ordered):
                return render_template("create-order.html", form=form)
            item.quantity -= quantity_ordered
            payment_amount += float(item.price) * float(quantity_ordered)

            order.add_items([(item, quantity_ordered)])
            item_id_and_quantity_list.append(f"Item #{item.id} x {quantity_ordered}")

        order.payment_amount = "{:.2f}".format(float(payment_amount))
        order.item_id_and_quantity_str = (", ").join(item_id_and_quantity_list)

        db.session.add(order)
        db.session.commit()
        flash(f"Successfully Added Order #{order.id} and Updated Menu")
        return redirect(url_for("index")), 302

    except Exception as e:
        flash(f"Something went wrong while creating order. Error message: {e}")
        db.session.rollback()
        return render_template("create-order.html", form=form), 400
