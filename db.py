import psycopg2

conn= psycopg2.connect(
    host="localhost",
    #database="hello",
    user="postgres",
    password="Nandita@1804")
cur = conn.cursor()
cur.execute("DROP TABLE course_student")
cur.execute("CREATE TABLE course_student (uid text NOT NULL, name text, course text)")
cur.execute("copy course_student from 'D:\Courses\Sem 6 2020-21\COL362\Project\course_student.csv' delimiter ',' csv header")
cur.execute("DROP TABLE courses")
cur.execute("CREATE TABLE courses (Sl bigint NOT NULL, Course_Name text, Slot_Name text, Units text, Type text, Instructor text, Instructor_Email text, Lecture_Time text, Tutorial_Time text, Practical_Time text, Vacancy bigint, Current_Strength bigint, Courseid text)")
cur.execute("copy courses from 'D:\Courses\Sem 6 2020-21\COL362\Project\courses.csv' delimiter ',' csv header")
cur.execute("copy (SELECT distinct uid, name from  course_student order by uid) TO 'D:\Courses\Sem 6 2020-21\COL362\Project\studentInfo.csv' DELIMITER ',' CSV HEADER")
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
    password="Nandita@1804")
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
def get_all_coursesOf_id(id):
  conn = connect()
  cur = conn.cursor()
  SQL = "SELECT cs.uid, cs.name, c.Courseid, c.Units, c.Slot_Name FROM course_student cs inner join courses c on (c.Courseid=cs.course and cs.uid=%s) order by Courseid"
  data = (id, )
  cur.execute(SQL, data)
  details = cur.fetchall()
  cur.close()
  conn.close()
  return details