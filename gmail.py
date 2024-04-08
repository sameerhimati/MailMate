import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.service_account import Credentials
import pymongo

# Load the credentials from the 'credentials.json' file
# This is necessary to authenticate the application with Google's servers
flow = InstalledAppFlow.from_client_secrets_file(
    '/Users/sameer/Desktop/ML/MailMate/credentials.json',
    ['https://www.googleapis.com/auth/gmail.modify']  # Scopes define the level of access the application has
)

# Run the OAuth2 flow to authenticate the application
creds = flow.run_local_server(port=0)

# Build the service that will interact with the Gmail API
service = build('gmail', 'v1', credentials=creds)

# Define the scopes for the Gmail API
SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]

def initialize_connection():
  """Initialize the connection to the Gmail API.
  
  This function checks if there are valid credentials stored in 'token.json'.
  If not, it runs the OAuth2 flow to authenticate the application and stores the credentials for future use.
  """
  creds = None
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    with open("token.json", "w") as token:
      token.write(creds.to_json())
    return creds

def get_labels():
    """Prints the names of all labels in the user's Gmail account."""
    try:
        service = build("gmail", "v1", credentials=creds)
        results = service.users().labels().list(userId="me").execute()
        labels = results.get("labels", [])

        print("Labels:")
        for label in labels:
            print(label["name"])
    except HttpError as error:
        print(f"An error occurred: {error}")

def get_emails():
    """Prints the snippets of all emails in the user's Gmail inbox."""
    try:
        service = build("gmail", "v1", credentials=creds)
        results = (
            service.users()
            .messages()
            .list(userId="me", labelIds=["INBOX"])
            .execute()
        )
        messages = results.get("messages", [])
        for message in messages:
            msg = (
                service.users()
                .messages()
                .get(userId="me", id=message["id"])
                .execute()
            )
            print(msg["snippet"])
    except HttpError as error:
        print(f"An error occurred: {error}")

def get_emails_to_mongodb(count=5, label=None):
    """Stores emails from the user's Gmail account in a MongoDB database.
    
    The function connects to a MongoDB database, retrieves emails from the Gmail API, and stores them in the database.
    The number of emails retrieved and the label from which to retrieve them can be specified.
    """
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["mailmate-gmail"]
    collection = db["emails"]

    try:
        service = build("gmail", "v1", credentials=creds)
        query = {
            "userId": "me",
            "labelIds": ["INBOX"] if label is None else [label],
            "maxResults": 5,
        }
        results = service.users().messages().list(**query).execute()
        messages = results.get("messages", [])
        for message in messages:
            msg = (
                service.users()
                .messages()
                .get(userId="me", id=message["id"])
                .execute()
            )
            if collection.find_one({"id": msg["id"]}) is None:
                collection.insert_one(msg)
    except HttpError as error:
        print(f"An error occurred: {error}")

# Call the functions to print labels and store emails in MongoDB
get_labels()
get_emails_to_mongodb(label="STARRED")