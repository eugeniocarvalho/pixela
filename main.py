from crypt import methods
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from forms import CreatePixel, DeletePixel, UpdatePixel
from datetime import datetime
from dotenv import load_dotenv
import pytz, requests, os

app = Flask(__name__)
Bootstrap(app)

app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6boboniqued'


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



@app.route('/')
def home():
  return render_template('index.html')


@app.route('/create-graph')
def create_graph():
  return render_template('index.html')


@app.route('/create-pixel', methods=['GET', 'POST'])
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

    return render_template('index.html', message=response.json()["message"])

  return render_template('create-pixel.html', form=form)


@app.route('/update-pixel', methods=['GET', 'POST'])
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

    return render_template('index.html', message=response.json()["message"])

  return render_template('update-pixel.html', form=form)


@app.route('/delete-pixel', methods=['GET', 'POST'])
def delete_pixel():
  form = DeletePixel()

  if form.validate_on_submit():
    date = str(form.date.data).replace('-', '')

    pixel_day = f"{pixela_endpoint}/{USERNAME}/graphs/{GRAPH_ID}/{date}"
    print(pixel_day)
    response = requests.delete(url=pixel_day, headers=headers)

    print(response)

    return render_template('index.html', message=response.json()["message"])

  return render_template('delete-pixel.html', form=form)


if __name__ == '__main__':
  app.run(debug=True)