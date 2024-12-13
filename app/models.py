from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class Employee(db.Model, UserMixin):
    __tablename__ = "employees"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    employee_number = db.Column(db.Integer, unique=True, nullable=False)
    hashed_password = db.Column(db.String(255), nullable=False)
    admin = db.Column(db.Boolean, nullable=False)

    orders = db.relationship("Order", back_populates="employee")

    @property
    def password(self):
        return self.hashed_password

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_open_order_qty(self):
        return sum(1 for order in self.orders if order.finished == False)


# Menu has a one-to-many relationship with named items to the MenuItem objects
# A menu can have many items, but each item is assigned to a particular menu
class Menu(db.Model):
    __tablename__ = "menus"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)

    items = db.relationship("MenuItem", back_populates="menu", cascade="all, delete-orphan")


# MenuItem has a many-to-one relationship with Menu, and a many-to-one relationship with MenuItemType
# Many menu items can be part of a particular menu
# There are many menu items, but each item has one particular menu item type
class MenuItem(db.Model):
    __tablename__ = "menu_items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    menu_id = db.Column(db.Integer, db.ForeignKey("menus.id"), nullable=False)
    menu_type_id = db.Column(db.Integer, db.ForeignKey("menu_item_types.id"), nullable=False)

    menu = db.relationship("Menu", back_populates="items")
    type = db.relationship("MenuItemType", back_populates="menu_item")

    order_details = db.relationship("OrderDetail", back_populates="menu_item")


# MenuItemType has a many-to-one relationship with MenuItem
# Many menu items have a type (read: all menu items have a type), but each menu item can have only one type
class MenuItemType(db.Model):
    __tablename__ = "menu_item_types"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    sort_order = db.Column(db.Integer, nullable=False)

    menu_item = db.relationship("MenuItem", back_populates="type", cascade="all, delete-orphan")


class Table(db.Model):
    __tablename__ = "tables"

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, unique=True, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)

    orders = db.relationship("Order", back_populates="table")


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey("employees.id"), nullable=False)
    table_id = db.Column(db.Integer, db.ForeignKey("tables.id"), nullable=False)
    finished = db.Column(db.Boolean, nullable=False)

    employee = db.relationship("Employee", back_populates="orders")
    table = db.relationship("Table", back_populates="orders")
    order_details = db.relationship("OrderDetail", back_populates="order")

class OrderDetail(db.Model):
    __tablename__ = "order_details"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
    menu_item_id = db.Column(db.Integer, db.ForeignKey("menu_items.id"), nullable=False)

    order = db.relationship("Order", back_populates="order_details")
    menu_item = db.relationship("MenuItem", back_populates="order_details")
