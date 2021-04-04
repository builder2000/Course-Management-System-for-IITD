import psycopg2
conn= psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="") #gitignore
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS course_student")
cur.execute("CREATE TABLE course_student (uid text NOT NULL, name text, course text, CONSTRAINT p_key PRIMARY KEY(uid,course))")
cur.execute(
    "copy course_student from '/home/pratik/Documents/COL362/COL362-Project/Project/course_student.csv' delimiter ',' csv header")  # gitignore
cur.execute("DROP TABLE IF EXISTS courses")
cur.execute("CREATE TABLE courses (Sl bigint, Course_Name text, Slot_Name text, Units text, Type text, Instructor text, Instructor_Email text, Lecture_Time text, Tutorial_Time text, Practical_Time text, Vacancy bigint, Current_Strength bigint, Courseid text, CONSTRAINT c_key PRIMARY KEY(Courseid, Slot_Name))")
cur.execute(
    "copy courses from '/home/pratik/Documents/COL362/COL362-Project/Project/courses.csv' delimiter ',' csv header")
#cur.execute("copy (SELECT distinct uid, name from  course_student order by uid) TO 'D:/DBMS_Project/COL362-Project/Project/studentInfo.csv' DELIMITER ',' CSV HEADER") #gitignore
cur.execute("DROP TABLE IF EXISTS ngu")
cur.execute(
     "CREATE TABLE ngu (userid text PRIMARY KEY, first_name text, second_name text, PESR float,Communication float,DPE float,PESR_copy float,NCC_NSO_NSS float,Programme float,Writing float)")
# gitignore
cur.execute(
    "copy ngu from '/home/pratik/Documents/COL362/COL362-Project/Project/ngu.csv' delimiter ',' csv header")
cur.execute("DROP TABLE IF EXISTS studentInfo")
cur.execute("CREATE TABLE studentInfo (uid text PRIMARY KEY, name text)")
cur.execute(
    "copy studentInfo from '/home/pratik/Documents/COL362/COL362-Project/Project/studentInfo.csv' delimiter ',' csv header")  # gitignore
cur.execute("DROP TABLE IF EXISTS  admintable")
cur.execute("CREATE TABLE admintable (uid text PRIMARY KEY, password text)")
cur.execute("INSERT INTO admintable VALUES('cs5180415','cs5180415')")
cur.execute("INSERT INTO admintable VALUES('cs5180417','cs5180417')")
cur.execute("INSERT INTO admintable VALUES('cs1180641','cs1180641')")
cur.execute("ALTER TABLE course_student ADD COLUMN feedback text")
cur.execute("ALTER TABLE studentInfo ADD COLUMN password text")
cur.execute("UPDATE studentInfo SET password = uid")
cur.execute("ALTER TABLE course_student ADD COLUMN status text DEFAULT 'C' ")
cur.execute("DROP TABLE IF EXISTS course_student_request")
cur.execute("CREATE TABLE course_student_request(uid text, course_id text, status_request text)")

cur.execute("DROP TABLE IF EXISTS prof_pass")
cur.execute("CREATE TABLE prof_pass (prof_id text PRIMARY KEY,password text)")
cur.execute("INSERT INTO prof_pass select distinct Instructor_Email, Instructor_Email from courses")
cur.execute("DROP TABLE IF EXISTS student_request")
cur.execute("CREATE TABLE student_request (uid text,request text,req_id text PRIMARY KEY,status text DEFAULT 'UR')")
cur.execute("DROP TABLE IF EXISTS dues_table")
cur.execute("CREATE TABLE dues_table (Sl bigint,hostname text, amtdue bigint, amtrcv bigint, name text,uid text PRIMARY KEY)")
cur.execute(
    "copy dues_table from '/home/pratik/Documents/COL362/COL362-Project/Project/Dues_List-converted.csv' delimiter ',' csv header")  # gitignore
cur.execute("DROP TABLE IF EXISTS course_student_assn")
cur.execute(
    "CREATE TABLE course_student_assn (uid text, student text, course text, assignment_id text, assignment text, submission text, grade text)")



conn.commit()

cur.execute("SELECT * FROM course_student")
# print(cur.fetchall())
cur.fetchall()
cur.close()
conn.close()

def connect():
    c= psycopg2.connect(
    host="localhost",
    database="postgres",
        user="postgres",
    password="")
    return c


def get_all_students():
  conn = connect()
  cur = conn.cursor()
  cur.execute("SELECT cs.uid, cs.name, c.Courseid, c.Units, c.Slot_Name FROM course_student cs inner join courses c on (c.Courseid=cs.course and cs.uid='cs5180415') order by Courseid")
  details = cur.fetchall()
  cur.close()
  conn.close()
  return details
def get_all_coursesOf_id(id): #courses of a student with student id, id
  conn = connect()
  cur = conn.cursor()
  SQL = "SELECT cs.uid, cs.name, c.Courseid, c.Units, c.Slot_Name, cs.status FROM course_student cs inner join courses c on (c.Courseid=cs.course and cs.uid=%s) order by Courseid"
  data = (id, )
  cur.execute(SQL, data)
  details = cur.fetchall()
  cols = list(map(lambda x: x[0], cur.description))
  cur.close()
  conn.close()
  return (cols, details)


def get_all_studentsOf_courseid(id): #students with course id, id
  conn = connect()
  cur = conn.cursor()
  SQL = "select cs.uid, cs.name, cs.status, cs.Feedback from course_student cs where cs.course=%s order by cs.uid"
  data = (id, )
  cur.execute(SQL, data)
  details = cur.fetchall()
  cols = list(map(lambda x: x[0], cur.description))
  cur.close()
  conn.close()
  return (cols, details)


def get_all_courses_of_prof(id):  # students with course id, id
  conn = connect()
  cur = conn.cursor()
  SQL = "select c.Courseid, c.Course_Name, c.Slot_Name, c.Units, c.Lecture_Time from courses c where c.Instructor_Email=%s order by c.Courseid"
  data = (id, )
  cur.execute(SQL, data)
  details = cur.fetchall()
  cols = list(map(lambda x: x[0], cur.description))
  cur.close()
  conn.close()
  return (cols, details)


def get_ngu_details(id):  # students with course id, id
  conn = connect()
  cur = conn.cursor()
  SQL = "select n.PESR, n.Communication, n.DPE, n.NCC_NSO_NSS, n.Programme, n.Writing from ngu n where n.userid=%s "
  data = (id, )
  cur.execute(SQL, data)
  details = cur.fetchall()
  #cols = list(map(lambda x: x[0], cur.description))
  #print(len(cols))
  #details.insert(0, cols)
  cols = list(map(lambda x: x[0], cur.description))
  cur.close()
  conn.close()
  return (cols, details)

def add_feedback(fb, user, course):
  conn = connect()
  cur = conn.cursor()
  SQL = "UPDATE course_student SET Feedback = %s WHERE uid = %s AND course = %s"
  data = (fb, user, course, )
  cur.execute(SQL, data)
  # details = cur.fetchall()
  # cols = list(map(lambda x: x[0], cur.description))
  conn.commit()
  cur.close()
  conn.close()
def change_status(fb, user, course):
  conn = connect()
  cur = conn.cursor()
  SQL = "UPDATE course_student SET status = %s WHERE uid = %s AND course = %s"
  data = (fb, user, course, )
  cur.execute(SQL, data)
  # details = cur.fetchall()
  # cols = list(map(lambda x: x[0], cur.description))
  conn.commit()
  cur.close()
  conn.close()

def update_course_req_table(user,course,val):
  conn = connect() 
  cur = conn.cursor()
  SQL = "INSERT INTO course_student_request SELECT uid, course, %(a3)s from course_student where uid = %(a1)s and course = %(a2)s"
  data = {'a1':user,'a2':course,'a3':val}
  cur.execute(SQL, data)
  # details = cur.fetchall()
  # cols = list(map(lambda x: x[0], cur.description))
  conn.commit()
  cur.close()
  conn.close()

def check_update_course_req_table(user,course):
  conn = connect() 
  cur = conn.cursor()
  SQL = "select * from course_student where uid = %(a1)s and course = %(a2)s"
  data = {'a1':user,'a2':course}
  cur.execute(SQL, data)
  details = cur.fetchall()
  cols = list(map(lambda x: x[0], cur.description))
  conn.commit()
  cur.close()
  conn.close()
  return (cols, details)

def check_update_course_req_table2(user,course):
  conn = connect() 
  cur = conn.cursor()
  SQL = "select * from course_student_request where uid = %(a1)s and course_id = %(a2)s"
  data = {'a1':user,'a2':course}
  cur.execute(SQL, data)
  details = cur.fetchall()
  cols = list(map(lambda x: x[0], cur.description))
  conn.commit()
  cur.close()
  conn.close()
  return (cols, details)

def get_course_req(id): #students with course id, id
  conn = connect()
  cur = conn.cursor()
  SQL = "select cs.uid, cs.course_id, cs.status_request from course_student_request cs where cs.course_id=%s order by cs.uid"
  data = (id, )
  cur.execute(SQL, data)
  details = cur.fetchall()
  cols = list(map(lambda x: x[0], cur.description))
  cur.close()
  conn.close()
  return (cols, details)

def add_student_to_course(s_id,c_id):
  conn = connect()
  cur = conn.cursor()
  SQL = "INSERT INTO course_student SELECT uid, name, %(a2)s from (SELECT * from studentInfo where uid = %(a1)s) as foo"
  data = {'a1': s_id, "a2": c_id}
  cur.execute(SQL, data)
  conn.commit()
  cur.close()
  conn.close()

def add_course(sl,c_id,name,slot_name,units,t,instructor,Instructor_Email,Lecture_Time,Tutorial_Time,Practical_Time,Vacancy, Current_Strength):
  conn = connect()
  cur = conn.cursor()
  SQL = "INSERT INTO courses VALUES (%(a0)s,%(a2)s,%(a3)s,%(a4)s,%(a5)s,%(a6)s,%(a7)s,%(a8)s,%(a9)s,%(a10)s,%(a11)s,%(a12)s,%(a1)s)"
  data = {"a0":sl,'a1': c_id, "a2": name, "a3":slot_name,"a4":units,"a5":t, "a6":instructor, "a7":Instructor_Email,"a8":Lecture_Time,"a9":Tutorial_Time,"a10":Practical_Time,"a11":Vacancy,"a12":Current_Strength}
  cur.execute(SQL, data)
  conn.commit()
  cur.close()
  conn.close()

def add_student(uid, name):
  conn = connect()
  cur = conn.cursor()
  SQL = "INSERT INTO studentInfo VALUES (%(a1)s,%(a2)s)"
  data = {'a1': uid, "a2": name}
  cur.execute(SQL, data)
  conn.commit()
  cur.close()
  conn.close()

def del_student_from_course(s_id,c_id):
  conn = connect()
  cur = conn.cursor()
  SQL = "DELETE FROM course_student WHERE uid = %(a1)s and course = %(a2)s"
  data = {'a1': s_id, "a2": c_id}
  cur.execute(SQL, data)
  conn.commit()
  cur.close()
  conn.close()

def del_course(c_id):
  conn = connect()
  cur = conn.cursor()
  SQL = "DELETE FROM courses WHERE Courseid = %(a1)s"
  data = {'a1': c_id}
  cur.execute(SQL, data)
  conn.commit()
  cur.close()
  conn.close()

def del_student(s_id):
  conn = connect()
  cur = conn.cursor()
  SQL = "DELETE FROM studentInfo WHERE uid = %(a1)s"
  data = {'a1': s_id}
  cur.execute(SQL, data)
  conn.commit()
  cur.close()
  conn.close()

def check_admin(a_id):
  conn = connect()
  cur = conn.cursor()
  SQL = "select * from admintable where uid = %s"
  data = (a_id, )
  cur.execute(SQL, data)
  details = cur.fetchall()
  cols = list(map(lambda x: x[0], cur.description))
  cur.close()
  conn.close()
  return (cols, details)

def check_delete_from_course(s_id,c_id):
  conn = connect()
  cur = conn.cursor()
  SQL = "select * from course_student where uid = %(a1)s and course = %(a2)s"
  data = {'a1': s_id, "a2": c_id}
  cur.execute(SQL, data)
  details = cur.fetchall()
  cols = list(map(lambda x: x[0], cur.description))
  cur.close()
  conn.close()
  return (cols, details)

def check_delete_course(c_id):
  conn = connect()
  cur = conn.cursor()
  SQL = "select * from courses where Courseid = %s"
  data = (c_id, )
  cur.execute(SQL, data)
  details = cur.fetchall()
  cols = list(map(lambda x: x[0], cur.description))
  cur.close()
  conn.close()
  return (cols, details)

def check_delete_student(s_id):
  conn = connect()
  cur = conn.cursor()
  SQL = "select * from studentInfo where uid = %s"
  data = (s_id, )
  cur.execute(SQL, data)
  details = cur.fetchall()
  cols = list(map(lambda x: x[0], cur.description))
  cur.close()
  conn.close()
  return (cols, details)
def del_course_aud_request(course, user):
  conn = connect()
  cur = conn.cursor()
  SQL = "DELETE FROM course_student_request WHERE uid = %s and course_id=%s"
  data = (user,course)
  cur.execute(SQL, data)
  conn.commit()
  cur.close()
  conn.close()

def check_stud_password(s_id,password):
  conn = connect()
  cur = conn.cursor()
  SQL = "select * from studentInfo where uid = %s and password = %s"
  data = (s_id, password)
  cur.execute(SQL, data)
  details = cur.fetchall()
  cols = list(map(lambda x: x[0], cur.description))
  cur.close()
  conn.close()
  return (cols, details)

def check_admin_password(s_id,password):
  conn = connect()
  cur = conn.cursor()
  SQL = "select * from admintable where uid = %s and password = %s"
  data = (s_id, password)
  cur.execute(SQL, data)
  details = cur.fetchall()
  cols = list(map(lambda x: x[0], cur.description))
  cur.close()
  conn.close()
  return (cols, details)

def check_prof_password(s_id,password):
  conn = connect()
  cur = conn.cursor()
  SQL = "select * from prof_pass where prof_id = %s and password = %s"
  data = (s_id, password)
  cur.execute(SQL, data)
  details = cur.fetchall()
  cols = list(map(lambda x: x[0], cur.description))
  cur.close()
  conn.close()
  return (cols, details)

def change_stud_password(u_id,password):
  conn = connect()
  cur = conn.cursor()
  SQL = "UPDATE studentInfo set password = %(a2)s where uid = %(a1)s"
  data = {'a1': u_id, 'a2': password}
  cur.execute(SQL, data)
  conn.commit()
  cur.close()
  conn.close()

def check_old_stud_pass(u_id,password):
  conn = connect()
  cur = conn.cursor()
  SQL = "select * from studentInfo where password = %(a2)s and uid = %(a1)s"
  data = {'a1': u_id, 'a2': password}
  cur.execute(SQL, data)
  details = cur.fetchall()
  cols = list(map(lambda x: x[0], cur.description))
  cur.close()
  conn.close()
  return (cols, details)

def change_prof_password(u_id,password):
  conn = connect()
  cur = conn.cursor()
  SQL = "UPDATE prof_pass set password = %(a2)s where prof_id = %(a1)s"
  data = {'a1': u_id, 'a2': password}
  cur.execute(SQL, data)
  conn.commit()
  cur.close()
  conn.close()

def check_old_prof_pass(u_id,password):
  conn = connect()
  cur = conn.cursor()
  SQL = "select * from prof_pass where password = %(a2)s and prof_id = %(a1)s"
  data = {'a1': u_id, 'a2': password}
  cur.execute(SQL, data)
  details = cur.fetchall()
  cols = list(map(lambda x: x[0], cur.description))
  cur.close()
  conn.close()
  return (cols, details)

def change_admin_password(u_id,password):
  conn = connect()
  cur = conn.cursor()
  SQL = "UPDATE admintable set password = %(a2)s where uid = %(a1)s"
  data = {'a1': u_id, 'a2': password}
  cur.execute(SQL, data)
  conn.commit()
  cur.close()
  conn.close()

def check_old_admin_pass(u_id,password):
  conn = connect()
  cur = conn.cursor()
  SQL = "select * from admintable where password = %(a2)s and uid = %(a1)s"
  data = {'a1': u_id, 'a2': password}
  cur.execute(SQL, data)
  details = cur.fetchall()
  cols = list(map(lambda x: x[0], cur.description))
  cur.close()
  conn.close()
  return (cols, details)


def adding_gen_req(u_id, req_id, request):
  conn = connect()
  cur = conn.cursor()
  SQL = "INSERT INTO student_request(uid, request, req_id ) VALUES(%(a1)s, %(a2)s, %(a3)s)"
  data = {'a1': u_id, 'a2': request, 'a3':req_id}
  cur.execute(SQL, data)
  conn.commit()
  cur.close()
  conn.close()

def get_gen_req(status):
  conn=connect()
  cur=conn.cursor()
  SQL="SELECT * from student_request where status=%(a1)s"
  data={'a1':status}
  cur.execute(SQL,data)
  details=cur.fetchall()
  cols= list(map(lambda x: x[0], cur.description))
  cur.close()
  conn.close()
  return (cols,details)

def del_gen_req(req_id):
  conn = connect()
  cur = conn.cursor()
  SQL = "DELETE FROM student_request WHERE req_id=%s"
  data = (req_id)
  cur.execute(SQL, data)
  conn.commit()
  cur.close()
  conn.close()

def change_genreq_status(status,req_id):
  conn = connect()
  cur = conn.cursor()
  SQL = "UPDATE student_request SET status = %s WHERE req_id=%s"
  data = (status, req_id)
  cur.execute(SQL, data)
  conn.commit()
  cur.close()
  conn.close()

def view_req(user):
  conn=connect()
  cur=conn.cursor()
  SQL="SELECT * from student_request where uid=%(a1)s"
  data={'a1': user}
  cur.execute(SQL,data)
  details=cur.fetchall()
  cols= list(map(lambda x: x[0], cur.description))
  cur.close()
  conn.close()
  return (cols,details)


def add_assignment_for_course(course_id, assgn_id, assgn):

  d, l = get_all_studentsOf_courseid(course_id)
  conn = connect()
  cur = conn.cursor()

  for i in range(len(l)):
    SQL = "INSERT INTO course_student_assn(uid, student, course, assignment_id, assignment) VALUES(%s, %s, %s, %s, %s)"
    data = (l[i][0], l[i][1], course_id,assgn_id, assgn)
    cur.execute(SQL, data)
  conn.commit()
  cur.close()
  conn.close()
  return


def get_assgn(user, course, ass_id):
  conn = connect()
  cur = conn.cursor()
  SQL = "SELECT assignment from course_student_assn where uid = %s AND course=%s AND assignment_id=%s"
  data = (user, course, ass_id)
  cur.execute(SQL, data)
  details = cur.fetchall()
  # cols = list(map(lambda x: x[0], cur.description))
  cur.close()
  conn.close()
  return details


def add_submission_to_table(user, course, ass_id, assgn):
  conn = connect()
  cur = conn.cursor()
  SQL = "UPDATE course_student_assn SET submission = %s WHERE uid=%s AND course=%s AND assignment_id=%s"
  data = (assgn, user, course, ass_id, )
  cur.execute(SQL, data)
  conn.commit()
  cur.close()
  conn.close()


def add_grade(user, course, grade, ass_id):
  conn = connect()
  cur = conn.cursor()
  SQL = "UPDATE course_student_assn SET grade = %s WHERE uid=%s AND course=%s AND assignment_id=%s"
  data = (grade, user, course, ass_id, )
  cur.execute(SQL, data)
  conn.commit()
  cur.close()
  conn.close()


def get_dues(user):
  conn=connect()
  cur=conn.cursor()
  SQL="SELECT uid,amtdue from dues_table where uid=%(a1)s"
  data={'a1': user}
  cur.execute(SQL,data)
  details=cur.fetchall()
  cols= list(map(lambda x: x[0], cur.description))
  cur.close()
  conn.close()
  return (cols,details)

def update_student(s_id,name):
  conn = connect()
  cur = conn.cursor()
  SQL = "UPDATE studentInfo SET name= %(a2)s WHERE uid = %(a1)s"
  data = {'a1': s_id, 'a2': name}
  cur.execute(SQL, data)
  SQL = "UPDATE course_student SET name= %(a2)s WHERE uid = %(a1)s"
  cur.execute(SQL,data)
  conn.commit()
  cur.close()
  conn.close()

def update_dues(s_id, amtdue):
  conn = connect()
  cur = conn.cursor()
  SQL = "UPDATE dues_table SET amtdue= %(a2)s WHERE uid = %(a1)s"
  data = {'a1': s_id, 'a2': amtdue}
  cur.execute(SQL,data)
  conn.commit()
  cur.close()
  conn.close()
 
def check_update_dues(s_id):
  conn = connect()
  cur = conn.cursor()
  SQL = "select * from dues_table where uid = %(a1)s"
  data = {'a1': s_id}
  cur.execute(SQL, data)
  details = cur.fetchall()
  cols = list(map(lambda x: x[0], cur.description))
  cur.close()
  conn.close()
  return (cols, details)

def update_dues2(s_id, amtdue):
  conn = connect()
  cur = conn.cursor()
  SQL = "INSERT into dues_table(uid,amtdue) VALUES(%(a1)s,%(a2)s) "
  data = {'a1': s_id, 'a2': amtdue}
  cur.execute(SQL,data)
  conn.commit()
  cur.close()
  conn.close()


def get_student_submission(user, course, ass_id):
  conn = connect()
  cur = conn.cursor()
  SQL = "SELECT submission from course_student_assn where course=%s AND uid=%s AND assignment_id=%s"
  data = (course, user, ass_id, )
  cur.execute(SQL, data)
  details = cur.fetchall()
  # cols = list(map(lambda x: x[0], cur.description))
  cur.close()
  conn.close()
  return details
def update_ngu(s_id, hours):
  conn = connect()
  cur = conn.cursor()
  SQL = "UPDATE ngu SET ncc_nso_nss= %(a2)s WHERE userid = %(a1)s"
  data = {'a1': s_id, 'a2': hours}
  cur.execute(SQL,data)
  conn.commit()
  cur.close()
  conn.close()

def check_update_ngu(s_id):
  conn = connect()
  cur = conn.cursor()
  SQL = "select * from ngu where userid = %(a1)s"
  data = {'a1': s_id}
  cur.execute(SQL, data)
  details = cur.fetchall()
  cols = list(map(lambda x: x[0], cur.description))
  cur.close()
  conn.close()
  return (cols, details)


def get_grade(user, course, ass_id):
  conn = connect()
  cur = conn.cursor()
  SQL = "SELECT grade from course_student_assn where course=%s AND uid=%s AND assignment_id=%s"
  data = (course, user, ass_id, )
  cur.execute(SQL, data)
  details = cur.fetchall()
  # cols = list(map(lambda x: x[0], cur.description))
  cur.close()
  conn.close()
  return details


def get_all_assgn(user, course):
  conn = connect()
  cur = conn.cursor()
  SQL = "SELECT assignment_id from course_student_assn where uid = %s AND course=%s"
  data = (user, course, )
  cur.execute(SQL, data)
  details = cur.fetchall()
  # cols = list(map(lambda x: x[0], cur.description))
  cur.close()
  conn.close()
  return details
