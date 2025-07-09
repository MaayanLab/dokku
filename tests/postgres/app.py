import os
import dotenv
import psycopg2

dotenv.load_dotenv()

# connect to db
conn = psycopg2.connect(os.environ['DATABASE_URL'])

# ... use conn in your app to build queries ...

conn.close()
