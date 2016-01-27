from flask import Flask
from flask import render_template

from models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.debug = True
db.init_app(app)


@app.before_first_request
def create_database():
    print("attempting database creation")


@app.route("/")
def hello():
    return render_template("index.html")

if __name__ == "__main__":
    app.run()
