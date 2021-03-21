from flask import Flask, render_template, redirect, url_for, request
#from flask_modus import Modus
import db

app = Flask(__name__)
#modus = Modus(app)

@app.route('/details', methods=["GET"])
def index():
    return render_template('index.html', details=db.get_all_students())

@app.route('/<id>', methods=["GET"])
def index2(id):
    return render_template('studentdetails.html', details=db.get_all_coursesOf_id(id))