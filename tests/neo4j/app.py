import os
import dotenv
from py2neo import Graph

dotenv.load_dotenv()

# connect to db
graph = Graph(os.environ['NEO4J_URL'])

# ... use graph in your app to build queries ...
