import mariadb
import sys

# Connect to MariaDB Platform
try:
    conn = mariadb.connect(
        user="USER_NAME",
        password="DB_PASSWORD",
        host="localhost_or_remote_IP",
        port=3306,
        database="DB_NAME"
    )
    cursor = conn.cursor()
    cursor.execute("INSERT INTO test_table VALUES (456)")
    cursor.execute("select * from test_table")
    resultset = cursor.fetchall() # get result set
    print(resultset) 
    conn.commit() # commit 안하면 실제 데이터 베이스에서는 반영 안됨

    # for firstname, lastname in resultset:
    #     print(f"First name: {firstname}, Last name: {lastname}")
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Get Cursor
cur = conn.cursor()
