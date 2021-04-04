from flask import Flask, render_template, redirect, url_for, request
#from flask_modus import Modus
import db
import time
import os
from time import time,ctime

template_dir = os.path.abspath('./FRONT_END')
app = Flask(__name__, template_folder = template_dir)
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
    password = request.form['Password']
    headings, details = db.check_admin(id)
    if(len(details) == 0):
        return render_template('no_user_found.html')
    headings, details = db.check_admin_password(id,password)
    if(len(details) == 0):
        return "Wrong Password"
    return render_template('adminactions.html', user = id)

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

@app.route('/update_student', methods=["POST"])
def i14():
    return render_template('update_student.html')

@app.route('/update_dues', methods=["POST"])
def i16():
    return render_template('update_dues.html')

@app.route('/update_ngu', methods=["POST"])
def i18():
    return render_template('update_ngu.html')

@app.route('/view_course', methods=["POST"])
def i20():
    return render_template('view_course_input.html')

@app.route('/view_student', methods=["POST"])
def i22():
    return render_template('view_student_credentials.html')

@app.route('/view_prof', methods=["POST"])
def i24():
    return render_template('view_professor_input.html')

@app.route('/view_allprof', methods=["GET",])
def profunc():
    headings,details=db.get_all_prof()
    return render_template('view_all_prof.html', details=details, headings=headings)

@app.route('/view_prof/<id>', methods=["GET"])
def prfunc2(id):
    headings,details=db.get_all_courses_of_prof(id)
    return render_template('view_courses.html', details=details, headings=headings)

@app.route('/view_allstudents', methods=["GET"])
def stufunc():
    headings,details=db.get_all_students()
    return render_template('view_all_students.html', details=details, headings=headings)

@app.route('/view_student/<id>', methods=["GET"])
def stufunc1(id):
    headings,details=db.get_all_coursesOf_id(id)
    return render_template('view_courses.html', details=details, headings=headings)


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

@app.route('/change_student', methods=["POST"])
def i15():
    s_id = request.form['user_id']
    name = request.form['name']
    headings, details = db.check_delete_student(s_id)
    if(len(details) == 0):
        return "student not found"
    db.update_student(s_id,name)
    return render_template('Success.html')

@app.route('/change_dues', methods=["POST"])
def i17():
    s_id = request.form['user_id']
    dues = request.form['dues']
    headings, details = db.check_update_dues(s_id)
    if(len(details) == 0):
        db.update_dues2(s_id,dues)
        return render_template('Success.html')
    db.update_dues(s_id,dues)
    return render_template('Success.html')

@app.route('/change_ngu', methods=["POST"])
def i19():
    s_id = request.form['user_id']
    hours = request.form['hours']
    headings, details = db.check_update_ngu(s_id)
    if(len(details) == 0):
        return "student not found"
    db.update_ngu(s_id,hours)
    return render_template('Success.html')

@app.route('/view_this_course', methods=["POST"])
def i21():
    c_id = request.form['course_id']
    headings, details = db.get_all_studentsOf_courseid(c_id)
    if(len(details) == 0):
        return "Course Not Found"
    return render_template('view_courses.html',headings = headings, details = details)

@app.route('/view_this_professor', methods=["POST"])
def i23():
    p_id = request.form['prof_id']
    headings, details = db.get_all_courses_of_prof(p_id)
    if(len(details) == 0):
        return "Professor Not Found"
    return render_template('view_courses.html',headings = headings, details = details)

@app.route('/view_this_student', methods=["POST"])
def i25():
    s_id = request.form['user_id']
    headings, details = db.get_all_coursesOf_id(s_id)
    if(len(details) == 0):
        return "Student Not Found"
    return render_template('view_courses.html',headings = headings, details = details)

@app.route('/<id>', methods=["POST"])
def index2(id):
    id = request.form['user_id']
    password = request.form['Password']

    h, p = db.check_stud_password(id, password)
    if(len(p) == 0):
        return render_template('no_user_found.html')
    headings, details = db.get_all_coursesOf_id(id)
    
    return render_template('studentdetails.html', headings=headings,
      details=details)


@app.route('/courses', methods=["POST"])
def index4():
    id = request.form['user_id']
    password = request.form['Password']
    headings, details = db.check_prof_password(id,password)
    if(len(details)==0):
        return "Wrong Password"
    headings, details = db.get_all_courses_of_prof(id)
    if(len(details) == 0):
        return render_template('no_user_found.html')
    return render_template('profdetails.html', headings=headings,
    details=details, user = id)


@app.route('/ngu/<id>', methods=["GET"])
def index5(id):
    # id = request.form['user_id']
    # print(id)
    headings, details = db.get_ngu_details(id)
    return render_template('ngu.html', headings=headings, details=details)


@app.route('/courses/add_grade/<ass_id>/<user>/<course>/success', methods=["GET", "POST"])
def index16(user, course, ass_id):
    # headings, details = db.get_all_studentsOf_courseid(id)
    grade = request.form["paragraph_text"]
    db.add_grade(user, course, grade, ass_id)

    return render_template('add_grade_success.html', user=user)


@app.route('/courses/add_grade/<ass_id>/<user>/<course>', methods=["GET", "POST"])
def index24(user, course, ass_id):
    return render_template('add_grade_text.html', user=user, course=course, ass_id=ass_id)


@app.route('/courses/add_grade/<user>/<course>', methods=["GET", "POST"])
def index17(user, course):
    assgn = db.get_all_assgn(user, course)
    if(len(assgn)==0):
        return render_template('no_assgn_added.html')
    return render_template('add_grade_textlist.html', user=user, course=course, assgn=assgn)


@app.route('/courses/v_submission/<ass_id>/<user>/<course>', methods=["GET", "POST"])
def index23(user, course, ass_id):
    assgn = db.get_student_submission(user, course, ass_id)
    if(len(assgn) == 0):
        return render_template('no_assgn_student.html', user=user)
    return render_template('v_assgn.html', text=assgn[0][0])

@app.route('/courses/v_submission/<user>/<course>', methods=["GET", "POST"])
def index18(user, course):
    assgn = db.get_all_assgn(user, course)
    # if(len(assgn) == 0):
    #     return render_template('no_assgn_student.html', user=user)
    return render_template('v_assgn_sublist.html', user=user, course=course, assgn=assgn)


@app.route('/courses/<id>', methods=["GET"])
def index3(id):
    headings, details = db.get_all_studentsOf_courseid(id)
    return render_template('add_grade.html', headings= headings, details=details, id=id)


@app.route('/student_id/audit-withdraw-request/<user>', methods=["GET", "POST"])
def index8(user):
    return render_template("au-request.html", user=user)

@app.route('/aw-request/<user>/success', methods=["GET", "PUT", "POST"])
def index9(user):
    course=request.form["course_id"]
    option=request.form["option"]
    headings, details = db.check_update_course_req_table(user,course)
    if(len(details)==0):
        return "You do not belong to this course. Kindly enter a course you are registered in"
    headings, details = db.check_update_course_req_table2(user,course)
    if(len(details)!=0):
        return "You have already requested for this course"
    db.update_course_req_table(user,course, option)
    #db.change_status("A",user,course)
    return render_template("ty.html")

@app.route('/awrequest/<course>', methods=["GET", "PUT","POST"])
def func(course):
    headings, details=db.get_course_req(course)
    return render_template("aud_req_view.html", details=details, headings=headings)

@app.route('/awrequest/success/<user>/<course>/<option>', methods=["GET", "PUT","POST"])
def func2(user,course,option):
    db.change_status(option,user,course)
    db.del_course_aud_request(course,user)
    return render_template("ty.html")

@app.route("/student_id/<user>/password_change", methods = ["GET","POST"])
def pass1(user):
    return render_template("change_stud_pass.html",user = user)

@app.route("/student_id/<user>/change_stud_pass",methods = ["GET","PUT","POST"])
def pass2(user):
    o_pw = request.form["o_pass"]
    n_pw = request.form["n_pass"]
    headings,details = db.check_old_stud_pass(user,o_pw)
    if(len(details)==0):
        return "Old Password Incorrect"
    db.change_stud_password(user,n_pw)
    return render_template("Success.html")

@app.route("/prof_id/<user>/password_change", methods = ["GET","POST"])
def pass3(user):
    return render_template("change_prof_password.html",user = user)

@app.route("/prof_id/<user>/change_prof_pass",methods = ["GET","PUT","POST"])
def pass4(user):
    o_pw = request.form["o_pass"]
    n_pw = request.form["n_pass"]
    headings,details = db.check_old_prof_pass(user,o_pw)
    if(len(details)==0):
        return "Old Password Incorrect"
    db.change_prof_password(user,n_pw)
    return render_template("Success.html")

@app.route("/admin_id/<user>/password_change", methods = ["GET","POST"])
def pass5(user):
    return render_template("change_admin_pass.html",user = user)

@app.route("/admin_id/<user>/change_admin_pass",methods = ["GET","PUT","POST"])
def pass6(user):
    o_pw = request.form["o_pass"]
    n_pw = request.form["n_pass"]
    headings,details = db.check_old_admin_pass(user,o_pw)
    if(len(details)==0):
        return "Old Password Incorrect"
    db.change_admin_password(user,n_pw)
    return render_template("Success.html")


@app.route('/student_id/feedback/<user>/<course>', methods=["GET", "POST"])
def index6(user, course):
    return render_template('feedback.html', user=user, course=course)


@app.route('/student_id/feedback/<user>/<course>/ty', methods=["GET", "PUT", "POST"])
def index7(user, course):
    feedb = request.form["paragraph_text"]
    db.add_feedback(feedb, user, course)
    # update the database, call a function, input student id and courseid
    return render_template("ty.html")

@app.route("/add_assignment/<id>", methods=["GET", "POST"])
def index10(id):
    return render_template("assignment.html", id = id)


@app.route("/add_assignment/<id>/success", methods=["GET", "PUT", "POST"])
def index11(id):
    assgn_id = request.form["assgn_id"]
    assgn = request.form["paragraph_text"]
    # some work to do with database
    db.add_assignment_for_course(id, assgn_id, assgn)
    # assignment addition successful
    # add a button to go to the page of prof
    return render_template("assignment_success.html")


@app.route('/student_id/v_assgn/<ass_id>/<user>/<course>', methods=["GET", "POST"])
def index21(user, course, ass_id):
    assgn = db.get_assgn(user, course, ass_id)
    # if(len(assgn) == 0):
    #     return render_template('no_assgn.html')
    return render_template('v_assgn.html', text=assgn[0][0])

@app.route('/student_id/v_assgn/<user>/<course>', methods=["GET", "POST"])
def index12(user, course):
    assgn = db.get_all_assgn(user, course)
    if(len(assgn) == 0):
        return render_template('no_assgn.html')
    return render_template('v_assgn_list.html', user=user, course=course, assgn=assgn)


@app.route('/student_id/s_assgn/<ass_id>/<user>/<course>', methods=["GET", "POST"])
def index22(user, course, ass_id):
    return render_template("s_assignment.html", user=user, course=course, ass_id=ass_id)


@app.route('/student_id/s_assgn/<user>/<course>', methods=["GET", "POST"])
def index13(user, course):
    assgn = db.get_all_assgn(user, course)
    return render_template("s_assgn_list.html", user=user, course=course, assgn=assgn)


@app.route('/student_id/s_assgn/<ass_id>/<user>/<course>/success', methods=["GET", "POST"])
def index14(user, course, ass_id):
    assgn = request.form["paragraph_text"]
    # some work to do with database
    db.add_submission_to_table(user, course, ass_id, assgn)
    # assignment addition successful
    # add a button to go to the page of prof
    return render_template("assignment_s_success.html")


@app.route('/student_id/view_grade/<ass_id>/<user>/<course>', methods=["GET", "POST"])
def index25(user, course, ass_id):
    grade = db.get_grade(user, course, ass_id)

    if(len(grade) == 0):
        return render_template("not_graded_yet.html", grade=grade)

    return render_template("grade.html", grade=grade[0])

@app.route('/student_id/view_grade/<user>/<course>', methods=["GET", "POST"])
def index15(user, course):
    assgn = db.get_all_assgn(user, course)

    # if(len(grade) == 0):
    #     return render_template("not_graded_yet.html", grade=grade)

    return render_template("grade_list.html", user=user, course=course, assgn=assgn)




@app.route('/student_id/view-gen-req/<user>', methods=["GET", "POST"])
def view_genrq(user):
    user=str(user)
    headings, details=db.view_req(user)
    return render_template("view-gen_req.html", user=user, details=details, headings=headings)

@app.route('/student_id/gen-req/<user>', methods=["GET", "POST"])
def genrq(user):
    return render_template("gen_req.html", user=user)

@app.route('/student_id/gen-req/<user>/success', methods=["GET", "PUT", "POST"])
def genreqsucc(user):
    req=request.form["request"]
    t=time()
    req_id=user+"-"+ ctime(t)
    print("%s")
    db.adding_gen_req(user,req_id,req)
    # if(len(details)==0):
    #     return "You do not belong to this course. Kindly enter a course you are registered in"
    # headings, details = db.check_update_course_req_table2(user,course)
    # if(len(details)!=0):
    #     return "You have already requested for this course"

    #db.change_status("A",user,course)
    return render_template("ty.html")

@app.route('/admin/gen_req', methods=["GET", "PUT","POST"])
def rqfunc():
    
    headings, details=db.get_gen_req("UR")
    return render_template("gen_req_view.html", details=details, headings=headings)

@app.route('/admin/gen_req/processed/<req_id>', methods=["GET", "PUT","POST"])
def reqfunc2(req_id):
    db.change_genreq_status("R", req_id)
    return render_template("ty.html")

@app.route('/student_id/<user>/dues_details', methods = ["GET", "PUT", "POST"])
def dues1(user):
    headings, details = db.get_dues(user)
    return render_template("dues.html",details = details, headings = headings)

@app.errorhandler(500)
def internal_error(error):
    return "The given info cannot be added, removed or updated"

if __name__ == "__main__":
    app.run()
