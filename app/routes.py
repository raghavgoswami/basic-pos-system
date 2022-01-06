from flask import flash, redirect, render_template, url_for

from app import app, db
from app.forms import (CreateMenuItemForm, CreateOrderForm, DeleteMenuItemForm,
                       UpdateMenuItemForm)
from app.models import Item, Order


@app.route("/")
@app.route("/index")
def index():
    items = db.session.query(Item).all()
    orders = db.session.query(Order).all()
    return render_template("index.html", items=items, orders=orders)


@app.route("/item", methods=["GET", "POST"])
def create_menu_item():
    form = CreateMenuItemForm()
    if form.validate_on_submit():
        item = Item(
            description=form.description.data,
            quantity=form.quantity.data,
            price="{:.2f}".format(float(form.price.data)),
        )
        db.session.add(item)
        db.session.commit()
        flash(f"Successfully Added Menu Item: {form.description.data}")
        return redirect(url_for("index"))
    return render_template("create-menu-item.html", form=form)


@app.route("/item/<item_id>/update", methods=["GET", "POST"])
def update_menu_item(item_id):
    item = Item.query.filter_by(id=item_id).first()
    form = UpdateMenuItemForm()
    if form.validate_on_submit():
        item = Item.query.filter_by(id=item_id).first()
        if item:
            item.description = (
                form.description.data
                if form.description.data != None
                else item.description
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
            flash(f"Successfully Updated Menu Item: {form.description.data}")
            return redirect(url_for("index"))

    return render_template("update-menu-item.html", form=form, item=item)


@app.route("/item/<item_id>/delete", methods=["GET", "POST"])
def delete_menu_item(item_id):
    item = Item.query.filter_by(id=item_id).first()
    form = DeleteMenuItemForm()
    if form.validate_on_submit():
        if item:
            db.session.delete(item)
            db.session.commit()
            flash(f"Successfully Deleted Menu Item: {item.description}")
            return redirect(url_for("index"))
    return render_template("delete-menu-item.html", form=form, item=item)


@app.route("/order", methods=["GET", "POST"])
def create_order():
    form = CreateOrderForm()
    if form.validate_on_submit():
        payment_amount = 0
        item_id_and_quantity_list = []

        for item_id_and_quantity in str(form.item_id_and_quantity_str.data).split(","):
            item_id, quantity_ordered = item_id_and_quantity.split(":")
            item_id = item_id.strip()
            quantity_ordered = int(quantity_ordered.strip())

            item = Item.query.get(item_id)
            if item is None:
                flash(f"Item # {item_id} does not exist")
                return render_template("create-order.html", form=form)

            if quantity_ordered < 1:
                flash(f"Item # {item_id} quantity ordered must be >= 1")
                return render_template("create-order.html", form=form)

            if quantity_ordered > item.quantity:
                flash(
                    f"You ordered Item # {item_id} x {quantity_ordered} but there are only {item.quantity} available"
                )
                return render_template("create-order.html", form=form)

            item_id_and_quantity_list.append(f"Item #{item_id} x {quantity_ordered}")
            item.quantity -= quantity_ordered
            payment_amount += float(item.price) * float(quantity_ordered)

        order = Order(
            note=form.note.data,
            payment_amount="{:.2f}".format(float(payment_amount)),
            item_id_and_quantity_str=(", ").join(item_id_and_quantity_list),
        )

        db.session.add(order)
        db.session.commit()
        flash(f"Successfully Added Order #{order.id} and Updated Menu")

        return redirect(url_for("index"))

    return render_template("create-order.html", form=form)
