from pymongo import MongoClient

# Create a MongoClient object
client = MongoClient('mongodb://localhost:27017/')

# Access the database
db = client['mailmate']

# Access the collection
emails_collection = db['emails']
users_collection = db['users']

def find_all_emails():
    emails = emails_collection.find()
    for email in emails:
        print(email)

find_all_emails()

def find_all_users():
    users = users_collection.find()
    for user in users:
        print(user)

find_all_users()

def create_user_if_not_exists():
    emails = emails_collection.find()
    for email in emails:
        sender_id = email['sender_email']
        recipient_id = email['recipient_email']
        
        # Check if sender_id exists in users collection
        sender = users_collection.find_one({'email_id': sender_id})
        if sender is None:
            # Create new document in users collection for sender
            users_collection.insert_one({'email_id': sender_id})
        
        # Check if recipient_id exists in users collection
        recipient = users_collection.find_one({'email_id': recipient_id})
        if recipient is None:
            # Create new document in users collection for recipient
            users_collection.insert_one({'email_id': recipient_id})

create_user_if_not_exists()

def update_email_sender_recipient_ids():
    emails = emails_collection.find()
    for email in emails:
        sender_email = email['sender_email']
        recipient_email = email['recipient_email']
        
        # Find the corresponding sender document in the users collection
        sender = users_collection.find_one({'email_id': sender_email})
        if sender is not None:
            # Update the sender_id in the email document
            emails_collection.update_one({'_id': email['_id']}, {'$set': {'sender_id': sender['_id']}})
        
        # Find the corresponding recipient document in the users collection
        recipient = users_collection.find_one({'email_id': recipient_email})
        if recipient is not None:
            # Update the recipient_id in the email document
            emails_collection.update_one({'_id': email['_id']}, {'$set': {'recipient_id': recipient['_id']}})

update_email_sender_recipient_ids()

def project_columns():
    emails = emails_collection.find({}, {"subject": 1, "sender": 1, "recipient": 1, "status": 1, "_id": 0, "sender_email": 1, "recipient_email": 1, "sender_id": 1, "recipient_id": 1})
    for email in emails:
        print(email)

project_columns()


# Test if connected
if 'mailmate' in client.list_database_names():
    print("Connected to MongoDB")
else:
    print("Failed to connect to MongoDB")





client.close()