import pandas as pd
from pymongo import MongoClient

def emails_to_df():
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017')
    db = client['mailmate-gmail']
    collection = db['emails']
    
    # Retrieve all emails from MongoDB
    all_emails = list(collection.find())
    
    # Convert emails to DataFrame
    df_emails = pd.DataFrame(all_emails)
    
    return df_emails

# Example usage
df_all_emails = emails_to_df()

def sort_emails(emails):
    # Sort emails into important and non-important
    important_emails = []
    non_important_emails = []
    
    for _, email in emails.iterrows():
        # Your sorting logic here
        if 'IMPORTANT' in email['labelIds']:
            important_emails.append(email)
        else:
            non_important_emails.append(email)
    
    return important_emails, non_important_emails

def unsubscribe(emails, keyword):
    # Unsubscribe emails based on keyword in body
    unsubscribed_emails = {}
    
    for _, email in emails.iterrows():
        for label in range(len(email['payload']['headers'])):
            if keyword in email['payload']['headers'][label]['name'].lower():
                print(email['payload']['headers'][label])
            # Unsubscribe logic here
                unsubscribed_emails[email['id']] = email['payload']['headers'][label]
    
    return unsubscribed_emails

def clean_emails(emails):
    # Clean emails in various ways
    cleaned_emails = []
    
    for _, email in emails.iterrows():
        # Your cleaning logic here
        cleaned_email = email  # Placeholder, replace with actual cleaning logic
        cleaned_emails.append(cleaned_email)
    
    return cleaned_emails

# Example usage
important_emails, non_important_emails = sort_emails(df_all_emails)
unsubscribed_emails = unsubscribe(df_all_emails, 'unsubscribe')
cleaned_emails = clean_emails(df_all_emails)

# Convert to DataFrame objects
df_important_emails = pd.DataFrame(important_emails)
df_non_important_emails = pd.DataFrame(non_important_emails)
df_unsubscribed_emails = pd.DataFrame(unsubscribed_emails)
df_cleaned_emails = pd.DataFrame(cleaned_emails)


for _, email in df_non_important_emails.iterrows():
    for label in range(len(email['payload']['headers'])):
        if 'unsubscribe' in email['payload']['headers'][label]['name'].lower():
            print(email['payload']['headers'][label])


