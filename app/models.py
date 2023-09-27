from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class Employee(db.Model, UserMixin):
    __tablename__ = "employees"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    employee_number = db.Column(db.Integer, nullable=False, unique=True)
    hashed_password = db.Column(db.String(255), nullable=False)

    orders = relationship("Order", back_populates="employee")

    @property
    def password(self):
        return self.hashed_password

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Menu(db.Model):
    __tablename__ = 'menus'

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)

    items = relationship("MenuItem", back_populates="menu")


class MenuItem(db.Model):
    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    price = Column(Float, nullable=False)
    menu_id = Column(Integer, ForeignKey('menus.id'), nullable=False)
    menu_type_id = Column(Integer, ForeignKey('menu_item_types.id'), nullable=False)

    menu = relationship("Menu", back_populates="items")
    type = relationship("MenuItemType", back_populates="items")


class MenuItemType(db.Model):
    __tablename__ = "menu_item_types"

    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)

    items = relationship("MenuItem", back_populates="type")


class Table(db.Model):
    __tablename__ = 'tables'

    id = Column(Integer, primary_key=True)
    number = Column(Integer, nullable=False, unique=True)
    capacity = Column(Integer, nullable=False)

class Order(db.Model):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    table_id = Column(Integer, ForeignKey('tables.id'), nullable=False)
    finished = Column(Boolean, nullable=False, default=False)

    employee = relationship("Employee", back_populates="orders")
    table = relationship("Table", backref="orders")
    details = relationship("OrderDetail", back_populates="order")

class OrderDetail(db.Model):
    __tablename__ = 'order_details'

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    menu_item_id = Column(Integer, ForeignKey('menu_items.id'), nullable=False)

    order = relationship("Order", back_populates="details")
    menu_item = relationship("MenuItem", backref="order_details")
