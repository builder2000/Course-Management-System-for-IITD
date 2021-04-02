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

@app.route("/admin", methods=["POST"])
def admin():
    return render_template('admin_login.html')

@app.route('/admin_id', methods=["POST"])
def i1():
    id = request.form['admin_id']
    headings, details = db.check_admin(id)
    if(len(details) == 0):
        return render_template('no_user_found.html')
    return render_template('adminactions.html')

@app.route('/add_to_course', methods=["POST"])
def i2():
    return render_template('add_to_courses.html')

@app.route('/add_course', methods=["POST"])
def i4():
    return render_template('add_course.html')

@app.route('/add_student', methods=["POST"])
def i6():
    return render_template('add_student.html')

@app.route('/delete_from_course', methods=["POST"])
def i8():
    return render_template('delete_students_from_course.html')

@app.route('/delete_course', methods=["POST"])
def i10():
    return render_template('delete_course.html')

@app.route('/delete_student', methods=["POST"])
def i12():
    return render_template('delete_student.html')

@app.route('/abcd', methods=["POST"])
def i3():
    s_id = request.form['user_id']
    c_id = request.form['course_id']
    db.add_student_to_course(s_id,c_id)
    return render_template('Success.html')

@app.route('/new_course', methods=["POST"])
def i5():
    sl = request.form['sl']
    c_id = request.form['course_id']
    c_name = request.form['course_name']
    s_name = request.form['slot_name'] or None
    units = request.form['units'] or None
    t = request.form['type'] or None
    i_name = request.form['Instructor_name'] or None
    i_email = request.form['Instructor_Email'] or None
    l_time = request.form['Lecture_Time'] or None
    t_time = request.form['Tutorial_Time'] or None
    p_time = request.form['Practical_Time'] or None
    vac = request.form['Vacancy'] or None
    cur = request.form['current_strength'] or None
    db.add_course(sl,c_id,c_name,s_name,units,t,i_name,i_email,l_time,t_time,p_time,vac,cur)
    return render_template('Success.html')

@app.route('/new_student', methods=["POST"])
def i7():
    s_id = request.form['user_id']
    c_id = request.form['name']
    db.add_student(s_id,c_id)
    return render_template('Success.html')

@app.route('/remove_from_course', methods=["POST"])
def i9():
    s_id = request.form['user_id']
    c_id = request.form['course_id']
    headings, details = db.check_delete_from_course(s_id,c_id)
    if(len(details) == 0):
        return "no such student in the course"
    db.del_student_from_course(s_id,c_id)
    return render_template('Success.html')

@app.route('/remove_course', methods=["POST"])
def i11():
    c_id = request.form['course_id']
    headings, details = db.check_delete_course(c_id)
    if(len(details) == 0):
        return "course not found"
    db.del_course(c_id)
    return render_template('Success.html')

@app.route('/remove_student', methods=["POST"])
def i13():
    s_id = request.form['user_id']
    headings, details = db.check_delete_student(s_id)
    if(len(details) == 0):
        return "student not found"
    db.del_student(s_id)
    return render_template('Success.html')



@app.route('/<id>', methods=["POST"])
def index2(id):
    id = request.form['user_id']
    headings, details = db.get_all_coursesOf_id(id)
    if(len(details) == 0):
        return render_template('no_user_found.html')
    return render_template('studentdetails.html', headings=headings,
      details=details)


@app.route('/courses', methods=["POST"])
def index4():
    id = request.form['user_id']
    headings, details = db.get_all_courses_of_prof(id)
    if(len(details) == 0):
        return render_template('no_user_found.html')
    return render_template('profdetails.html', headings=headings,
    details=details)


@app.route('/ngu/<id>', methods=["GET"])
def index5(id):
    # id = request.form['user_id']
    # print(id)
    headings, details = db.get_ngu_details(id)
    return render_template('ngu.html', headings=headings, details=details)



@app.route('/courses/<id>', methods=["GET"])
def index3(id):
    headings, details = db.get_all_studentsOf_courseid(id)
    return render_template('ngu.html', headings= headings, details=details)


@app.route('/student_id/feedback/<user>/<course>', methods=["GET", "POST"])
def index6(user, course):
    return render_template('feedback.html', user=user, course=course)


@app.route('/student_id/feedback/<user>/<course>/ty', methods=["GET", "PUT", "POST"])
def index7(user, course):
    feedb = request.form["paragraph_text"]
    db.add_feedback(feedb, user, course)
    # update the database, call a function, input student id and courseid
    return render_template("ty.html")
@app.route('/student_id/audit-withdraw-request/<user>', methods=["GET", "POST"])
def index8(user):
    return render_template("au-request.html", user=user)

@app.route('/aw-request/<user>/success', methods=["GET", "PUT", "POST"])
def index9(user):
    course=request.form["course_id"]
    db.update_course_req_table(user,course,"A")
    #db.change_status("A",user,course)
    return render_template("ty.html")

@app.route('/awrequest/<course>', methods=["GET", "PUT","POST"])
def func(course):
    headings, details=db.get_course_req(course)
    return render_template("aud_req_view.html", details=details, headings=headings)

@app.route('/awrequest/success/<user>/<course>', methods=["GET", "PUT","POST"])
def func2(user,course):
    db.change_status("A",user,course)
    return render_template("ty.html")

@app.errorhandler(500)
def internal_error(error):

    return "The given info cannot be added, removed or updated"

if __name__ == "__main__":
    app.run()
