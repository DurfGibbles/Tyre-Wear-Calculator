import pymysql
pymysql.install_as_MySQLdb()

import MySQLdb

# Connect to MySQL
conn = MySQLdb.connect(
    host="localhost",
    user="root",
    password="",
    db="tyre_wear_calculator"
)

print("✅ Connected to the database!")

# Create a cursor object
cursor = conn.cursor()

# Run a test query
cursor.execute("SHOW TABLES")

# Fetch the results
tables = cursor.fetchall()

print("📋 Tables in the database:")
for table in tables:
    print(f" - {table[0]}")

conn.commit()

print("✅ Test table created successfully!")

# Close the connection
conn.close()