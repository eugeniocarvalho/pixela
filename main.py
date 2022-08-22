from crypt import methods
from flask import Flask, render_template, redirect, url_for, abort, flash
from flask_bootstrap import Bootstrap
from forms import CreatePixel, DeletePixel, UpdatePixel, LoginForm, SignUpForm
from datetime import datetime
from dotenv import load_dotenv
import pytz, requests, os
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
Bootstrap(app)

app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6boboniqued'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))

load_dotenv()

TOKEN = os.environ.get("TOKEN")
USERNAME = "eugeniocarvalho"  
GRAPH_ID = "graph1"
pixela_endpoint = "https://pixe.la/v1/users"

user_params = {
  "token": TOKEN,
  "username": USERNAME,
  "agreeTermsOfService": "yes",
  "notMinor": "yes"
}

headers = {
    "X-USER-TOKEN": TOKEN
  }

# CREATE A GRAPH
def create_graph(graph_name):
  graph_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs"
  
  graph_config = {
    "id": graph_name,
    "name": "Reading Graph",
    "unit": "pages",
    "type": "int",
    "timezone": "America/Fortaleza",
    "color": "sora"
  }
  
  response = requests.post(url=graph_endpoint, json=graph_config, headers=headers)
  print(response.text)


class User(db.Model, UserMixin):
  __tablname__ = 'users'
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(100), unique=True)
  name = db.Column(db.String(100))
  password = db.Column(db.String(100))


db.create_all()


def admin_only(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):
    if current_user.id != 1:
        return abort(403)

    return f(*args, **kwargs)
      
  return decorated_function



@app.route('/')
def home():
  return render_template('dashboard.html', user=current_user)


@app.route('/login', methods=['GET', 'POST'])
def login():
  form = LoginForm()

  if form.validate_on_submit():
    email = form.email.data
    password = form.password.data
    user = User.query.filter_by(email=email).first()

    if not user:
      flash('That email does not exist, please try again.')

      return redirect(url_for('login'))
    elif not check_password_hash(user.password, password):
      flash('Password incorrect, try again.')
    else:
      login_user(user)

      return render_template('dashboard.html', user=current_user)

  return render_template('login.html', form=form, user=current_user)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
  pass
  # form = SignUpForm()

  # if form.validate_on_submit():
  #   if User.query.filter_by(email=form.email.data).first():
  #     flash("You've already signed up with that email, login inteast")

  #     return redirect(url_for('login'))
  #   else:
  #     password_hash = generate_password_hash(password=form.password.data, method="pbkdf2:sha256", salt_length=8)
      
  #     user = User (
  #         name = form.name.data,
  #         email = form.email.data,
  #         password = password_hash
  #     )

  #     db.session.add(user)
  #     db.session.commit()

  #     login_user(user)

  #     return redirect(url_for("dashboard"))

  # return render_template("signup.html", form=form, user=current_user)

@app.route('/dashboard')
def dashboard():
  return render_template('dashboard.html', user=current_user)

@app.route('/create-graph')
@login_required
def create_graph():
  return render_template('dashboard.html', user=current_user)


@app.route('/create-pixel', methods=['GET', 'POST'])
@login_required
def create_pixel():
  form = CreatePixel()

  if form.validate_on_submit():
    graph_pixel = f"{pixela_endpoint}/{USERNAME}/graphs/{GRAPH_ID}"
  
    today = datetime.now(pytz.timezone("America/Fortaleza"))
    #today = datetime(year=2022, month=6, day=10)
    
    print(today)

    pixel_config = {
      "date": today.strftime("%Y%m%d"),
      "quantity": str(form.pixel.data)
    }

    response = requests.post(url=graph_pixel, json=pixel_config, headers=headers)
    print(response.json()["message"])

    return render_template('dashboard.html', message=response.json()["message"], user=current_user)

  return render_template('create-pixel.html', form=form, user=current_user)


@app.route('/update-pixel', methods=['GET', 'POST'])
@login_required
def update_pixel():
  form = UpdatePixel()

  if form.validate_on_submit():
    date = str(form.date.data).replace('-', '')

    pixel_day = f"{pixela_endpoint}/{USERNAME}/graphs/{GRAPH_ID}/{date}"
  
    pixel_update = {
      "quantity": str(form.pixel.data)
    }

    response = requests.put(url=pixel_day, json=pixel_update, headers=headers)
    
    print(response.json())

    return render_template('dashboard.html', message=response.json()["message"], user=current_user)

  return render_template('update-pixel.html', form=form, user=current_user)


@app.route('/delete-pixel', methods=['GET', 'POST'])
@login_required
def delete_pixel():
  form = DeletePixel()

  if form.validate_on_submit():
    date = str(form.date.data).replace('-', '')

    pixel_day = f"{pixela_endpoint}/{USERNAME}/graphs/{GRAPH_ID}/{date}"
    print(pixel_day)
    response = requests.delete(url=pixel_day, headers=headers)

    print(response)

    return render_template('dashboard.html', message=response.json()["message"], user=current_user)

  return render_template('delete-pixel.html', form=form, user=current_user)



@app.route('/logout')
@login_required
def logout():
  logout_user()

  return redirect(url_for('home'))


if __name__ == '__main__':
  app.run(debug=True)