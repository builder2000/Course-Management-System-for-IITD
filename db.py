import psycopg2

conn= psycopg2.connect(
    host="localhost",
    #database="hello",
    user="postgres",
    password="p9TUnVkM")
cur = conn.cursor()
cur.execute("DROP TABLE course_student")
cur.execute("CREATE TABLE course_student (uid text NOT NULL, name text, course text)")
cur.execute("copy course_student from 'D:/DBMS_Project/COL362-Project/Project/course_student.csv' delimiter ',' csv header")
cur.execute("DROP TABLE courses")
cur.execute("CREATE TABLE courses (Sl bigint NOT NULL, Course_Name text, Slot_Name text, Units text, Type text, Instructor text, Instructor_Email text, Lecture_Time text, Tutorial_Time text, Practical_Time text, Vacancy bigint, Current_Strength bigint, Courseid text)")
cur.execute("copy courses from 'D:/DBMS_Project/COL362-Project/Project/courses.csv' delimiter ',' csv header")
cur.execute("copy (SELECT distinct uid, name from  course_student order by uid) TO 'D:/DBMS_Project/COL362-Project/Project/studentInfo.csv' DELIMITER ',' CSV HEADER")
cur.execute("DROP TABLE ngu")
cur.execute(
    "CREATE TABLE ngu (userid text NOT NULL, first_name text, second_name text, PESR float,Communication float,DPE float,PESR_copy float,NCC_NSO_NSS float,Programme float,Writing float)")
cur.execute("copy ngu from 'D:/DBMS_Project/COL362-Project/Project/ngu.csv' delimiter ',' csv header")
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
cur.fetchall()
cur.close()
conn.close()

def connect():
    c= psycopg2.connect(
    host="localhost",
    #database="hello",
    user="postgres",
    password="p9TUnVkM")
    return c

def get_all_toys():
  conn = connect()
  cur = conn.cursor()
  cur.execute("SELECT * FROM toys")
  toys = cur.fetchall()
  cur.close()
  conn.close()
  return toys
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
  cur.close()
  conn.close()
  return details
def get_all_studentsOf_courseid(id): #students with course id, id
  conn = connect()
  cur = conn.cursor()
  SQL = "select cs.uid, cs.name from course_student cs where cs.course=%s order by cs.uid"
  data = (id, )
  cur.execute(SQL, data)
  details = cur.fetchall()
  cur.close()
  conn.close()
  return details


def get_all_courses_of_prof(id):  # students with course id, id
  conn = connect()
  cur = conn.cursor()
  SQL = "select c.Courseid, c.Course_Name, c.Slot_Name, c.Units, c.Lecture_Time, c.Current_Strength from courses c where c.Instructor_Email=%s order by c.Courseid"
  data = (id, )
  cur.execute(SQL, data)
  details = cur.fetchall()
  cur.close()
  conn.close()
  return details


def get_ngu_details(id):  # students with course id, id
  conn = connect()
  cur = conn.cursor()
  SQL = "select n.PESR, n.Communication, n.DPE, n.NCC_NSO_NSS, n.Programme, n.Writing from ngu n where n.userid=%s "
  data = (id, )
  cur.execute(SQL, data)
  details = cur.fetchall()
  cur.close()
  conn.close()
  return details
