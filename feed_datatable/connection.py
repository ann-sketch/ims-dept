import mysql.connector

ims_db_dept = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="ims_db_dept_gh"
)

ims_db_gh = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="ims_db_gh"
)

ims_db_dept_cursor = ims_db_dept.cursor(buffered=True)
ims_cursor = ims_db_gh.cursor(buffered=True)
