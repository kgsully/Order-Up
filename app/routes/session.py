from flask import Blueprint, flash, redirect, url_for, render_template
from flask_login import current_user, login_user, logout_user
from ..forms import LoginForm
from ..models import Employee

bp = Blueprint("session", __name__, url_prefix="/session")

# The use of @bp, here, assumes you named the variable "bp"
# that holds your Blueprint object for this routing module
@bp.route("/", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("orders.index"))

    form = LoginForm()
    if form.validate_on_submit():
        empl_number = form.employee_number.data
        try:
            empl_number = int(empl_number)
        except:
            flash("Employee number must be numeric")
            return redirect(url_for(".login"))

        employee = Employee.query.filter(Employee.employee_number == empl_number).first()
        if not employee or not employee.check_password(form.password.data):
            flash("Invalid login - Please try again")
            return redirect(url_for(".login"))
        login_user(employee)
        return redirect(url_for("orders.index"))
    return render_template("login.html", form=form, title="Login - Order Up!")

@bp.route("/logout", methods=["POST"])
def logout():
    logout_user()
    return redirect(url_for(".login"))