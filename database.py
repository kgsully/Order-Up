from dotenv import load_dotenv
load_dotenv()

# Regardless of the lint error you receive, load_dotenv must run before running this
# so that the environment variables are properly loaded.
from app import app, db
from app.models import Employee, Menu, MenuItem, MenuItemType, Order, Table


with app.app_context():
    # Drop and create all tables
    db.drop_all()
    db.create_all()

    # Handle seed data for "employees" table
    employee1 = Employee(name="Margot", employee_number=123, password="password", admin=False)
    employee2 = Employee(name="Steve", employee_number=456, password="password", admin=False)
    employee3 = Employee(name="Laura", employee_number=789, password="password", admin=False)
    employee4 = Employee(name="Admin", employee_number=999, password="password", admin=True)

    # Handle seed data for "menus", "menu_items", and "menu_item_types" tables
    beverages = MenuItemType(name="Beverages", sort_order=1)
    entrees = MenuItemType(name="Entrees", sort_order=2)
    sides = MenuItemType(name="Sides", sort_order=3)

    dinner = Menu(name="Dinner")

    fries = MenuItem(name="French fries", price=3.50, type=sides, menu=dinner)
    tots  = MenuItem(name="Tater Tots", price=2.75, type=sides, menu=dinner)

    drp = MenuItem(name="Dr. Pepper", price=1.0, type=beverages, menu=dinner)
    coke = MenuItem(name="Coca Cola", price=1.0, type=beverages, menu=dinner)
    iced_tea = MenuItem(name="Iced Tea", price=1.25, type=beverages, menu=dinner)

    jambalaya = MenuItem(name="Jambalaya", price=21.98, type=entrees, menu=dinner)
    chic_kiev = MenuItem(name="Chicken Kiev", price=23.98, type=entrees, menu=dinner)
    epp = MenuItem(name="Eggplant Parmesean", price=18.65, type=entrees, menu=dinner)


    # Handle seed data for "tables"
    table1 = Table(number=1, capacity=2)
    table2 = Table(number=2, capacity=2)
    table3 = Table(number=3, capacity=4)
    table4 = Table(number=4, capacity=4)
    table5 = Table(number=5, capacity=4)
    table6 = Table(number=6, capacity=6)
    table7 = Table(number=7, capacity=6)
    table8 = Table(number=8, capacity=8)
    table9 = Table(number=9, capacity=8)
    table10 = Table(number=10, capacity=12)

    # Handle seed data for Order
    order1 = Order(employee_id=1, table_id=1, finished=False)
    order2 = Order(employee_id=1, table_id=5, finished=True)
    order3 = Order(employee_id=2, table_id=9, finished=True)
    order4 = Order(employee_id=1, table_id=3, finished=False)


    # Add data to sessions before committing
    db.session.add_all(
        [
            employee1,
            employee2,
            employee3,
            employee4
        ]
    )
    db.session.add(beverages)
    db.session.add(entrees)
    db.session.add(sides)
    db.session.add(dinner)
    db.session.add(fries)
    db.session.add(tots)
    db.session.add(drp)
    db.session.add(coke)
    db.session.add(iced_tea)
    db.session.add(jambalaya)
    db.session.add(chic_kiev)
    db.session.add(epp)

    db.session.add_all(
        [
            table1,
            table2,
            table3,
            table4,
            table5,
            table6,
            table7,
            table8,
            table9,
            table10
        ]
    )

    db.session.add_all(
        [
            order1,
            order2,
            order3,
            order4
        ]
    )

    # Commit data from session
    db.session.commit()
