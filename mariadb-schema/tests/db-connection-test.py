import mariadb
from dotenv import load_dotenv
import os

load_dotenv()

mysql_user = os.getenv('mysql_user')
mysql_password = os.getenv('mysql_password')
mysql_database = os.getenv('mysql_database')

try:
    conn = mariadb.connect(
        user=mysql_user,
        password=mysql_password,
        host="127.0.0.1",
        port=3306,
        database=mysql_database  
    )
    print("Connected to MariaDB successfully!")
    
    # Perform a simple query
    cur = conn.cursor()
    cur.execute("SHOW TABLES;")
    for table in cur:
        print(table)

    # Close the connection
    conn.close()

except mariadb.Error as e:
    print(f"Error connecting to MariaDB: {e}")