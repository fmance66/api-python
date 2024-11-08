from pymongo import MongoClient

# conexión a base de datos local en localhost
# db_client = MongoClient().local

connstring = "mongodb+srv://fmancevich:mega08ne@cluster0.zwyqo.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# conexión a servidor de base de datos remota en Atlas
db_client = MongoClient(connstring).curso                 # base de datos curso