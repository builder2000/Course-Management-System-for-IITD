import psycopg2
import numpy as np
conn= psycopg2.connect(
    host="localhost",
    database="postgres",
    user="project",
    password="papamummy03") #gitignore
cur = conn.cursor()
cur.execute("DROP TABLE course_student")
cur.execute("CREATE TABLE course_student (uid text NOT NULL, name text, course text, CONSTRAINT p_key PRIMARY KEY(uid,course))")
cur.execute(
    "copy course_student from '/home/pratik/Documents/COL362/COL362-Project/Project/course_student.csv' delimiter ',' csv header") #gitignore
cur.execute("DROP TABLE courses")
cur.execute("CREATE TABLE courses (Sl bigint PRIMARY KEY, Course_Name text, Slot_Name text, Units text, Type text, Instructor text, Instructor_Email text, Lecture_Time text, Tutorial_Time text, Practical_Time text, Vacancy bigint, Current_Strength bigint, Courseid text)")
cur.execute(
    "copy courses from '/home/pratik/Documents/COL362/COL362-Project/Project/courses.csv' delimiter ',' csv header")
#cur.execute("copy (SELECT distinct uid, name from  course_student order by uid) TO 'D:/DBMS_Project/COL362-Project/Project/studentInfo.csv' DELIMITER ',' CSV HEADER") #gitignore
cur.execute("DROP TABLE ngu")
cur.execute(
     "CREATE TABLE ngu (userid text PRIMARY KEY, first_name text, second_name text, PESR float,Communication float,DPE float,PESR_copy float,NCC_NSO_NSS float,Programme float,Writing float)")
cur.execute("copy ngu from '/home/pratik/Documents/COL362/COL362-Project/Project/ngu.csv' delimiter ',' csv header") #gitignore
cur.execute("DROP TABLE studentInfo")
cur.execute("CREATE TABLE studentInfo (uid text PRIMARY KEY, name text)")
cur.execute(
    "copy studentInfo from '/home/pratik/Documents/COL362/COL362-Project/Project/studentInfo.csv' delimiter ',' csv header") #gitignore
# cur.execute("DROP TABLE toys")
# cur.execute("CREATE TABLE toys (id serial PRIMARY KEY, name text);")
# # let's add some starter data
# cur.execute("INSERT INTO toys (name) VALUES (%s)", ("duplo",))
# cur.execute("INSERT INTO toys (name) VALUES (%s)", ("lego",))
# cur.execute("INSERT INTO toys (name) VALUES (%s)", ("knex",))
conn.commit()

# make sure data was saved
# cur.execute("SELECT * FROM toys")
# cur.fetchall() # should get [(1, 'duplo'), (2, 'lego'), (3, 'knex')]

cur.execute("SELECT * FROM course_student")
# print(cur.fetchall())
cur.fetchall()
cur.close()
conn.close()

def connect():
    c= psycopg2.connect(
    host="localhost",
    database="postgres",
    user="project",
    password="papamummy03")
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
  SQL = "SELECT cs.uid, cs.name, c.Courseid, c.Units, c.Slot_Name FROM course_student cs inner join courses c on (c.Courseid=cs.course and cs.uid=%s) order by Courseid"
  data = (id, )
  cur.execute(SQL, data)
  details = cur.fetchall()
  cols = list(map(lambda x: x[0], cur.description))
  cur.close()
  conn.close()
  return (cols, details)

# def get_all_coursesOf_id_cols(id): #columns of table of courses of a student with student id, id
#   conn = connect()
#   cur = conn.cursor()
#   SQL = "SELECT cs.uid, cs.name, c.Courseid, c.Units, c.Slot_Name FROM course_student cs inner join courses c on (c.Courseid=cs.course and cs.uid=%s) order by Courseid"
#   data = (id, )
#   cur.execute(SQL, data)
#   details = cur.fetchall()
#   cols = list(map(lambda x: x[0], cur.description))
#   cur.close()
#   conn.close()
#   return cols


def get_all_studentsOf_courseid(id): #students with course id, id
  conn = connect()
  cur = conn.cursor()
  SQL = "select cs.uid, cs.name, cs.Feedback from course_student cs where cs.course=%s order by cs.uid"
  data = (id, )
  cur.execute(SQL, data)
  details = cur.fetchall()
  cols = list(map(lambda x: x[0], cur.description))
  cur.close()
  conn.close()
  return (cols, details)


# def get_all_studentsOf_courseid_cols(id): #students with course id, id
#   conn = connect()
#   cur = conn.cursor()
#   SQL = "select cs.uid, cs.name from course_student cs where cs.course=%s order by cs.uid"
#   data = (id, )
#   cur.execute(SQL, data)
#   details = cur.fetchall()
#   cols = list(map(lambda x: x[0], cur.description))
#   cur.close()
#   conn.close()
#   return cols


def get_all_courses_of_prof(id):  # students with course id, id
  conn = connect()
  cur = conn.cursor()
  SQL = "select c.Courseid, c.Course_Name, c.Slot_Name, c.Units, c.Lecture_Time, c.Current_Strength from courses c where c.Instructor_Email=%s order by c.Courseid"
  data = (id, )
  cur.execute(SQL, data)
  details = cur.fetchall()
  cols = list(map(lambda x: x[0], cur.description))
  cur.close()
  conn.close()
  return (cols, details)

# def get_all_courses_of_prof_cols(id):  # students with course id, id
#   conn = connect()
#   cur = conn.cursor()
#   SQL = "select c.Courseid, c.Course_Name, c.Slot_Name, c.Units, c.Lecture_Time, c.Current_Strength from courses c where c.Instructor_Email=%s order by c.Courseid"
#   data = (id, )
#   cur.execute(SQL, data)
#   details = cur.fetchall()
#   cols = list(map(lambda x: x[0], cur.description))
#   cur.close()
#   conn.close()
#   return cols


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

# def get_ngu_cols(id):  # students with course id, id
#   conn = connect()
#   cur = conn.cursor()
#   SQL = "select n.PESR, n.Communication, n.DPE, n.NCC_NSO_NSS, n.Programme, n.Writing from ngu n where n.userid=%s "
#   data = (id, )
#   cur.execute(SQL, data)
#   details = cur.fetchall()
#   cols = list(map(lambda x: x[0], cur.description))
#   cur.close()
#   conn.close()
#   return cols


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