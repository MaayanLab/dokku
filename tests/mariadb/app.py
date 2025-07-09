import os
import dotenv
import mysql.connector

dotenv.load_dotenv()

# connect to db
conn = mysql.connector.connect(os.environ['DATABASE_URL'])

# ... use conn in your app to build queries ...

conn.close()