from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Regexp


class CreateMenuItemForm(FlaskForm):
    description = StringField("Description", validators=[DataRequired()])
    price = StringField(
        "Price",
        validators=[
            DataRequired(),
            Regexp("^(\d+(\.\d{0,2})?|\.?\d{1,2})$"),
        ],
    )
    quantity = IntegerField(
        "Quantity",
        validators=[DataRequired(), NumberRange(min=1, message="Quantity must be >=1")],
    )
    submit = SubmitField("Submit Menu Item")


class UpdateMenuItemForm(FlaskForm):
    description = StringField("Description", validators=[DataRequired()])
    price = StringField(
        "Price",
        validators=[
            DataRequired(),
            Regexp("^(\d+(\.\d{0,2})?|\.?\d{1,2})$"),
        ],
    )
    quantity = IntegerField(
        "Quantity",
        validators=[DataRequired(), NumberRange(min=1, message="Quantity must be >=1")],
    )
    submit = SubmitField("Update Menu Item")


class DeleteMenuItemForm(FlaskForm):
    submit = SubmitField("Delete")


class CreateOrderForm(FlaskForm):
    note = StringField("Note", validators=[DataRequired()])
    item_id_and_quantity_str = StringField(
        "Item Id and Quantity String", validators=[DataRequired()]
    )
    submit = SubmitField("Submit Order")
