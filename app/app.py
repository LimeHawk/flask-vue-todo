from flask import Flask
from flask import render_template
from flask import jsonify

from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

from config import Config
import models


load_dotenv('./.flaskenv')

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

@app.route('/')
def index():
  tasks = models.Task.query.all()
  #return render_template('index.html')
  return jsonify(tasks)

if __name__ == '__main__':
  app.run() 