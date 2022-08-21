from sqlite3 import Date
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, IntegerField, PasswordField, EmailField
from wtforms.validators import DataRequired

class CreatePixel(FlaskForm):
  pixel = IntegerField('Pixel Quantity: ', validators=[DataRequired()])
  submit = SubmitField('Send')

class UpdatePixel(FlaskForm):
  pixel = IntegerField('Pixel Update Quantity: ', validators=[DataRequired()])
  date = DateField('Date: ', validators=[DataRequired()])
  submit = SubmitField('Submit')

class DeletePixel(FlaskForm):
  date = DateField('Pixel Date', validators=[DataRequired()])
  submit = SubmitField('Submit')

class LoginForm(FlaskForm):
  email = StringField("Email", validators=[DataRequired()])
  password = PasswordField("Password", validators=[DataRequired()])
  submit = SubmitField("Login")

class SignUpForm(FlaskForm):
  email = EmailField("Email", validators=[DataRequired()])
  name = StringField("Name", validators=[DataRequired()])
  password = PasswordField("Password", validators=[DataRequired()])
  submit = SubmitField("Sign up")