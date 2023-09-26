from dotenv import load_dotenv
from app.models import Menu, MenuItem, MenuItemType, Table

load_dotenv()

from app import app, db
from app.models import Employee

with app.app_context():
    db.drop_all()
    db.create_all()

    # Seeding employee
    employee = Employee(name="Margot", employee_number=1234, password="password")
    db.session.add(employee)
    db.session.commit()

    # MenuItemType
    beverages = MenuItemType(name="Beverages")
    entrees = MenuItemType(name="Entrees")
    sides = MenuItemType(name="Sides")

    db.session.add_all([beverages, entrees, sides])

    # Menu
    dinner = Menu(name="Dinner")

    db.session.add(dinner)
    db.session.commit()

    # MenuItem
    fries = MenuItem(name="French fries", price=3.50, type=sides, menu=dinner)
    drp = MenuItem(name="Dr. Pepper", price=1.0, type=beverages, menu=dinner)
    jambalaya = MenuItem(name="Jambalaya", price=21.98, type=entrees, menu=dinner)

    db.session.add_all([fries, drp, jambalaya])
    db.session.commit()

    # Tables
    for i in range(1, 11):
        table = Table(number=i, capacity=4)
        db.session.add(table)

    db.session.commit()
