from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@tiny.db.elephantsql.com/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.route('/')
def hello():
    return 'Hello World'