from app.models import Employee, Table, Order
from flask import Blueprint, request, render_template, redirect, url_for
from app import db
from app.models import MenuItem, OrderDetail

bp = Blueprint("table_order", __name__, url_prefix="/table_order")

@bp.route("/assign", methods=["GET", "POST"])
def assign_employee_to_table():
    if request.method == 'POST':
        employee_id = request.form.get('employee_id')
        table_id = request.form.get('table_id')
        order = Order(employee_id=employee_id, table_id=table_id, finished=False)

        db.session.add(order)
        db.session.commit()

        return redirect(url_for('index'))

    employees = Employee.query.all()
    tables = Table.query.all()
    return render_template('assign.html', employees=employees, tables=tables)


@bp.route("/close_table", methods=["GET", "POST"])
def close_table():
     if request.method == 'POST':
        order_id = request.form.get('order_id')
        order = Order.session.get(order_id)
        order.finished = True
        db.session.commit()
        return redirect(url_for('index'))

     open_orders = Order.query.filter_by(finished=False).all()
     return render_template('close_table.html', open_orders=open_orders)


@bp.route('/add_items', methods=["GET", "POST"])
def add_items_to_order():
    if request.method == 'POST':
        order_id = request.form.get('order_id')
        menu_item_id = request.form.get('menu_item_id')
        order_detail = OrderDetail(order_id=order_id, menu_item_id=menu_item_id)

        db.session.add(order_detail)
        db.session.commit()
        return redirect(url_for('index'))

    open_orders = Order.query.filter_by(finished=False).all()
    menu_items = MenuItem.query.all()
    return render_template('add_items.html', open_orders=open_orders, menu_items=menu_items)
