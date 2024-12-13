from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, current_user
from ..models import db, Employee, Table, MenuItem, MenuItemType, Order, OrderDetail
from ..forms import MenuItemEditForm

bp = Blueprint("menu", __name__, url_prefix="/menu")

@bp.route("/edit")
@login_required
def edit_menu():
    if not current_user.admin:
        return redirect(url_for("orders.index"))

    menu_item_types = MenuItemType.query.order_by(MenuItemType.sort_order).all()
    menu = {type.name: MenuItem.query.join(MenuItemType).filter(MenuItem.menu_type_id == type.id).order_by(MenuItem.name).all() for type in menu_item_types}

    return render_template("menu.html",
                           menu_item_types=menu_item_types,
                           menu=menu,
                           title="Edit Menu - Order Up!")


@bp.route("/cancel")
@login_required
def cancel_edit():
    return redirect(url_for("orders.index"))

@bp.route("/add_item", methods=["POST"])
@login_required
def add_item():
    name = request.form.get("new_name")
    price = request.form.get("new_price")
    type = request.form.get("new_type")

    if not name:
        flash("Please enter a name for the item")
        return redirect(url_for(".edit_menu"))
    try:
        price = float(price)
    except:
        flash("Price must be a number value in $")
        return redirect(url_for(".edit_menu"))

    new_item = MenuItem(name=name, price=price, menu_type_id=type, menu_id=1)
    db.session.add(new_item)
    db.session.commit()

    return redirect(url_for(".edit_menu"))


@bp.route("/delete_item/<int:item_id>", methods=["POST"])
@login_required
def delete_item(item_id):
    item_to_delete = MenuItem.query.get(item_id)
    db.session.delete(item_to_delete)
    db.session.commit()
    return redirect(url_for('.edit_menu'))


@bp.route("/edit_item/<int:item_id>", methods=["POST"])
@login_required
def edit_item(item_id):
    item_to_update = MenuItem.query.get(item_id)

    name = request.form.get(f"edit_name_{item_id}")
    price = request.form.get(f"edit_price_{item_id}")
    type = request.form.get(f"edit_type_{item_id}")

    if not name:
        flash("Please enter a name for the item")
        return redirect(url_for(".edit_menu"))
    try:
        price = float(price)
    except:
        flash("Price must be a number value in $")
        return redirect(url_for(".edit_menu"))

    try:
        type = int(type)
    except:
        flash("Invalid item type")
        return redirect(url_for(".edit_menu"))

    item_to_update.name = name
    item_to_update.price = price
    item_to_update.menu_type_id = type

    db.session.commit()

    return redirect(url_for(".edit_menu"))
