from flask import Flask, render_template, redirect, url_for, request
#from flask_modus import Modus
import db

app = Flask(__name__)
#modus = Modus(app)

@app.route('/')
def index():
    return render_template('home.html')


@app.route("/student", methods=["POST"])
def stud():
    return render_template('stud_login.html')


@app.route("/prof", methods=["POST"])
def prof():
    return render_template('prof_login.html')


@app.route('/<id>', methods=["POST"])
def index2(id):
    id = request.form['user_id']
    return render_template('studentdetails.html', headings=db.get_all_coursesOf_id_cols(id),
      details=db.get_all_coursesOf_id(id))


@app.route('/courses', methods=["POST"])
def index4():
    id = request.form['user_id']
    return render_template('profdetails.html', headings=db.get_all_courses_of_prof_cols(id),
    details=db.get_all_courses_of_prof(id))


@app.route('/ngu/<id>', methods=["GET"])
def index5(id):
    # id = request.form['user_id']
    # print(id)
    headings=db.get_ngu_cols(id)
    return render_template('ngu.html', headings=headings, details=db.get_ngu_details(id))



@app.route('/courses/<id>', methods=["GET"])
def index3(id):
    headings = db.get_all_studentsOf_courseid_cols(id)
    return render_template('ngu.html', headings= headings, details=db.get_all_studentsOf_courseid(id))


if __name__ == "__main__":
    app.run()
