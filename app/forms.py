from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SelectField, SelectMultipleField, SubmitField # add import for widges if using the class MultiCheckboxField
from wtforms.validators import DataRequired, ValidationError

class LoginForm(FlaskForm):
    employee_number = StringField("Employee Number", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

class TableAssignmentForm(FlaskForm):
    tables = SelectField("Open Tables", coerce=int)
    servers = SelectField("Servers", coerce=int)
    assign = SubmitField("Assign")

# class MultiCheckboxField(SelectMultipleField):
#     widget = widgets.ListWidget(prefix_label=False)
#     option_widget = widgets.CheckboxInput()

class MenuItemAssignmentForm(FlaskForm):
    menu_item_ids = SelectMultipleField("Menu Items", coerce=int)

class MenuItemEditForm(FlaskForm):
    name = StringField("Item Name", validators=[DataRequired()])
    price = StringField("Item Name", validators=[DataRequired()])
    menu_id = SelectField("Menu", validators=[DataRequired()])
    menu_type_id = SelectField("Category", validators=[DataRequired()])
