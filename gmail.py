import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.service_account import Credentials
import pymongo

# Load the credentials from the 'credentials.json' file
flow = InstalledAppFlow.from_client_secrets_file(
    '/Users/sameer/Desktop/ML/MailMate/credentials.json',
    ['https://www.googleapis.com/auth/gmail.modify']  # Or any other scopes you need
)

# Run the OAuth2 flow
creds = flow.run_local_server(port=0)

# Build the service
service = build('gmail', 'v1', credentials=creds)

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]



def initialize_connection():
  """Shows basic usage of the Gmail API.
  Lists the user's Gmail labels.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())
    return creds

#creds = initialize_connection()

def get_labels():
    try:
    # Call the Gmail API
        service = build("gmail", "v1", credentials=creds)
        results = service.users().labels().list(userId="me").execute()
        labels = results.get("labels", [])

        print("Labels:")
        for label in labels:
            print(label["name"])

    

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f"An error occurred: {error}")

def get_emails():
    try:
    # Call the Gmail API
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
        # TODO(developer) - Handle errors from gmail API.
        print(f"An error occurred: {error}")

def get_emails_to_mongodb(count=5, label=None):
    # Connect to MongoDB
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    # Select the database
    db = client["mailmate-gmail"]
    # Select the collection
    collection = db["emails"]

    try:
        # Call the Gmail API
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
            # Check if email already exists in the database
            if collection.find_one({"id": msg["id"]}) is None:
                # Store the email in MongoDB
                collection.insert_one(msg)

    except HttpError as error:
        # TODO(developer) - Handle errors from Gmail API.
        print(f"An error occurred: {error}")

get_labels()
get_emails_to_mongodb(label="STARRED")
