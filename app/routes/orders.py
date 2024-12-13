from decimal import Decimal
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, current_user
from ..forms import TableAssignmentForm, MenuItemAssignmentForm
from ..models import db, Employee, Table, MenuItem, MenuItemType, Order, OrderDetail

bp = Blueprint("orders", __name__, url_prefix="")


@bp.route("/")
@login_required
def index():
    # ---------------------------------------------
    # Assignment
    # ---------------------------------------------
    # Get all tables and open orders
    # (if using list comprehension syntax to determine occupied table ids, do not execute the query with .all())
    tables = Table.query.order_by(Table.number).all()
    all_open_orders = Order.query.filter(Order.finished == False).all()
    # test_tables = Table.query.join(Order).filter(Order.finished == True).all()
    # print(test_tables)

    # Determine occupied tables
    occupied_table_ids = [order.table_id for order in all_open_orders]
    # # A list comprehension can be used in order to execute queries and then loop over the rows returned as it is iterable
    # occupied_table_ids = [order.table_id for order in all_open_orders]

    # Determine open tables
    open_tables = [table for table in tables if table.id not in occupied_table_ids]

    servers = Employee.query.order_by(Employee.name).all()
    open_order_qtys = [server.get_open_order_qty() for server in servers]

    # Generate assignment form
    table_assign_form = TableAssignmentForm()
    table_assign_form.tables.choices = [(table.id, f"Table {table.number}") for table in open_tables]
    table_assign_form.servers.choices = [(server.id, f"{server.name} ({order_qty})") for server, order_qty in zip(servers, open_order_qtys) if not server.admin]

    # ---------------------------------------------
    # Open Orders
    # ---------------------------------------------
    # Get open orders for current user
    if current_user.admin:
        curr_user_open_orders = Order.query.join(Employee).filter(Order.finished == False).all()
    else:
        curr_user_open_orders = Order.query.join(Employee).filter(Employee.id == current_user.id, Order.finished == False).all()

    curr_user_open_order_details = {}
    for order in curr_user_open_orders:
        curr_user_open_order_details[order.id] = {
                                                    "order": order,
                                                    "total": Decimal(sum([item.price for item in MenuItem.query.join(OrderDetail).filter(OrderDetail.order_id == order.id)])).quantize(Decimal('0.01'))
                                                 }

    # ---------------------------------------------
    # Menu
    # ---------------------------------------------
    # Get menu item types
    menu_item_types = MenuItemType.query.order_by(MenuItemType.sort_order).all()
    menu = {type.name: MenuItem.query.join(MenuItemType).filter(MenuItem.menu_type_id == type.id).order_by(MenuItem.name).all() for type in menu_item_types}
    menu_items = MenuItem.query.join(MenuItemType).order_by(MenuItemType.name, MenuItem.name).all()

    menu_item_form = MenuItemAssignmentForm()
    menu_item_form.menu_item_ids.choices = [(item.id, item.name) for item in menu_items]

    return render_template("orders.html",
                           table_assign_form=table_assign_form,
                           open_orders=curr_user_open_order_details,
                           menu_item_types=menu_item_types,
                           menu_item_form=menu_item_form,
                           menu=menu,
                           title="Order Up!")


@bp.route("/assign_table", methods=["POST"])
@login_required
def assign_table():
    table_id = request.form.get("tables")
    employee_id = request.form.get("servers")

    if not table_id or not employee_id:
        flash("Please select a table and server")
    else:
        new_order = Order(employee_id=employee_id, table_id=table_id, finished=False)
        db.session.add(new_order)
        db.session.commit()

    return redirect(url_for('.index'))


@bp.route("/close_table/<int:order_id>", methods=["POST"])
@login_required
def close_table(order_id):
    order_to_close = Order.query.get(order_id)
    order_to_close.finished = True

    db.session.add(order_to_close)
    db.session.commit()

    return redirect(url_for('.index'))


@bp.route("/add_to_order/<int:order_id>/items", methods=["POST"])
@login_required
def add_to_order(order_id):
    # order = Order.query.get(order_id)

    selected_item_ids = request.form.getlist("menu_items")

    for item_id in selected_item_ids:
        added_item = OrderDetail(order_id = order_id, menu_item_id = item_id)
        db.session.add(added_item)

    # item_prices = [item.price for item in MenuItem.query.filter(MenuItem.id.in_(selected_item_ids))]
    # print("\nTotal:", Decimal(sum(item_prices)).quantize(Decimal('0.01')))

    db.session.commit()

    return redirect(url_for('.index'))


@bp.route("/remove_from_order/<int:order_detail_id>", methods=["POST"])
@login_required
def remove_from_order(order_detail_id):
    item_to_delete = OrderDetail.query.get(order_detail_id)

    db.session.delete(item_to_delete)
    db.session.commit()

    return redirect(url_for('.index'))

@bp.route("/edit_menu")
@login_required
def edit_menu():
    return redirect(url_for('menu.edit_menu'))
