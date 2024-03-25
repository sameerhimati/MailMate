from pymongo import MongoClient

# Create a MongoClient object
client = MongoClient('mongodb://localhost:27017/')

# Access the database
db = client['mailmate']

# Access the collection
collection = db['emails']

# Test if connected
if 'mailmate' in client.list_database_names():
    print("Connected to MongoDB")
else:
    print("Failed to connect to MongoDB")

# Close the connection
client.close()