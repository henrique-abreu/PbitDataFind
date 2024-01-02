'''
from pymongo.mongo_client import MongoClient

# Replace the placeholder with your Atlas connection string
uri = "mongodb://localhost:27017/"

# Create a new client and connect to the server
client = MongoClient(uri, username='admin', password='admin')

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")

    db = client["dog"] 

    coll = db["Output"] 

    record = {"Test": "lapis", "Funciona": "Ah pois é!"}

    coll.insert_one(record)


except Exception as e:
    print(e)
    '''

my_dict = {"Key1": "Dog", "Key2": "Cat"}


for key, items in my_dict.items():
    new_dict = {}
    new_dict[key] = items
    print(new_dict)
    print(type(new_dict))
    print("\n")
