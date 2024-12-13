from flask import Flask
from flask_login import LoginManager
from .config import Configuration
from .models import db, Employee
from .routes import orders, session, menu

app = Flask(__name__)
app.config.from_object(Configuration)

app.register_blueprint(orders.bp)
app.register_blueprint(session.bp)
app.register_blueprint(menu.bp)

db.init_app(app)  # Configure the application with SQLAlchemy

login = LoginManager(app)               # Create the login manager for the app to protect routes
login.login_view = "session.login"      # Instruct the login manager to use the "session.login" blueprint function. This defines the route for @login_required to direct to if user is not logged in

# Configure LoginManager to use the load_user function to get Employee objects from the database
@login.user_loader
def load_user(id):
    return Employee.query.get(int(id))
