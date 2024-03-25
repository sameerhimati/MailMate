from pymongo import MongoClient

# Create a MongoClient object
client = MongoClient('mongodb://localhost:27017/')

# Access the database
db = client['mailmate']

# Access the collection
collection = db['emails']

# Update the date column type from string to date
collection.update_many({}, [{"$set": {"date": {"$toDate": "$date"}}}])

# Test if connected
if 'mailmate' in client.list_database_names():
    print("Connected to MongoDB")
else:
    print("Failed to connect to MongoDB")

def insert_test_doc():
    collection = db['emails']
    test_document = {
        "subject": "Test Email",
        "sender": "Ameer",
        "recipient": "Sameer",
        "message": "This is a test email",
        "date": "2021-09-01",
        "time": "12:00",
        "sender_email": "test@ameer.com",
        "recipient_email": "test@sameer.com",
        "status": "unread",
        "sender_id": "1",
        "recipient_id": "2"
    }
    inserted_id = collection.insert_one(test_document).inserted_id
    print(f"Inserted document with ID: {inserted_id}")

def create_documents():
    emails = [
        {
            "subject": "Fake Email 1",
            "sender": "John Doe",
            "recipient": "Jane Smith",
            "message": "This is a fake email 1",
            "date": "2021-09-01",
            "time": "12:00",
            "sender_email": "john.doe@example.com",
            "recipient_email": "jane.smith@example.com",
            "status": "unread",
            "sender_id": "3",
            "recipient_id": "4"
        },
        {
            "subject": "Fake Email 2",
            "sender": "Alice Johnson",
            "recipient": "Bob Williams",
            "message": "This is a fake email 2",
            "date": "2021-09-02",
            "time": "13:00",
            "sender_email": "alice.johnson@example.com",
            "recipient_email": "bob.williams@example.com",
            "status": "unread",
            "sender_id": "5",
            "recipient_id": "6"
        },
        {
            "subject": "Fake Email 3",
            "sender": "Emily Davis",
            "recipient": "Michael Brown",
            "message": "This is a fake email 3",
            "date": "2021-09-03",
            "time": "14:00",
            "sender_email": "emily.davis@example.com",
            "recipient_email": "michael.brown@example.com",
            "status": "unread",
            "sender_id": "7",
            "recipient_id": "8"
        },
        {
            "subject": "Fake Email 4",
            "sender": "Sarah Wilson",
            "recipient": "David Taylor",
            "message": "This is a fake email 4",
            "date": "2021-09-04",
            "time": "15:00",
            "sender_email": "sarah.wilson@example.com",
            "recipient_email": "david.taylor@example.com",
            "status": "unread",
            "sender_id": "9",
            "recipient_id": "10"
        },
        {
            "subject": "Fake Email 5",
            "sender": "Olivia Martinez",
            "recipient": "James Anderson",
            "message": "This is a fake email 5",
            "date": "2021-09-05",
            "time": "16:00",
            "sender_email": "olivia.martinez@example.com",
            "recipient_email": "james.anderson@example.com",
            "status": "unread",
            "sender_id": "11",
            "recipient_id": "12"
        }
        ]
    collection.insert_many(emails)

def find_all_emails():
    emails = collection.find()
    for email in emails:
        print(email)

def find_email_by_sender(sender):
    emails = collection.find({"sender": sender})
    count = collection.count_documents({"sender": {"$eq": sender}})
    if count == 0:
        print("No emails from sender")
    else:
        for email in emails:
            print(email)

# find_email_by_sender("Ameer")
# find_email_by_sender("Sameer")

def get_email_by_id(email_id):
    from bson.objectid import ObjectId

    _id = ObjectId(email_id)
    email = collection.find_one({"_id": _id})
    print(email)

#get_email_by_id("66016cc77d72944d71b261e2")

def get_date_range(start_date, end_date):
    emails = collection.find({"date": {"$gte": start_date, "$lte": end_date}}).sort("sender")
    for email in emails:
        print(email)

# get_date_range("2021-09-01", "2021-09-02")

def project_columns():
    emails = collection.find({}, {"subject": 1, "sender": 1, "recipient": 1, "status": 1, "_id": 0, "date": 2})
    for email in emails:
        print(email)

project_columns()

def update_email_status(email_id, status):
    from bson.objectid import ObjectId

    _id = ObjectId(email_id)
    collection.update_one({"_id": _id}, {"$set": {"status": status}})
    print("Email status updated")

    collection.update_many({"date" : { "$exists" : True } },
  [{ "$set": { "date": { "$subtract": ["$date", 24*60*60000] } } }]
)



update_email_status("66016cc77d72944d71b261e2", "unread")
project_columns()
# Close the connection
client.close()