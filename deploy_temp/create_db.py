import mysql.connector

try:
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="2003"
    )

    mycursor = mydb.cursor()
    mycursor.execute("CREATE DATABASE IF NOT EXISTS enrollment_db")
    print("Database 'enrollment_db' created or already exists.")
except Exception as e:
    print(f"Error creating database: {e}")
