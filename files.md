## gmail.py: 
        This file contains the code to interact with the Gmail API. It fetches emails from a Gmail account and stores them in a MongoDB database. It uses OAuth2 for authentication.

## parse.py: 
        This file contains functions to process the emails stored in the MongoDB database. 

        1. The emails_to_df function retrieves all emails from the database and converts them into a pandas DataFrame. 
        2. The sort_emails function sorts the emails into important and non-important based on the 'labelIds' field. 
        3. The unsubscribe function is intended to unsubscribe from emails based on a keyword in the body, but it's not implemented yet.

## credentials.json: 
        This file contains the OAuth2 client ID credentials used to authenticate the application with the Gmail API.

