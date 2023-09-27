from flask import Flask
from .config import Configuration
from .models import db, Employee
from .routes import orders, session, table_orders
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Configuration)

app.register_blueprint(orders.bp)
app.register_blueprint(session.bp)
app.register_blueprint(table_orders.bp)

db.init_app(app)

login = LoginManager(app)
login.login_view = "session.login"

@login.user_loader
def load_user(id):
    return Employee.query.get(int(id))
