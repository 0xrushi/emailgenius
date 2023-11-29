import httplib2
import os
from oauth2client import client, tools
from oauth2client.file import Storage

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from apiclient import errors, discovery
import imaplib
from bs4 import BeautifulSoup 
import re
import json

def get_credentials():
    SCOPES = 'https://www.googleapis.com/auth/gmail.modify'
    CLIENT_SECRET_FILE = 'data/credentials.json'
    APPLICATION_NAME = 'Gmail API Python Label Email'
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'gmail-python-email-send.json')
    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run_flow(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


credentials = get_credentials()
http = credentials.authorize(httplib2.Http())
service = discovery.build('gmail', 'v1', http=http)
user_id = 'me' 



def remove_long_urls(text):
    # Keep only ASCII characters, and replace all other characters with a space
    ascii_text = re.sub(r'https?:\/\/(www\.)?([a-zA-Z0-9.-]+).*?(\s|$)', '', text)
    # Collapse all whitespace into single spaces
    ascii_text = ' '.join(ascii_text.split())
    return ascii_text.replace('( )', '')

def clean_text(text):
    """
    Clean the given text by keeping only ASCII characters and replacing all other characters with a space.
    
    Parameters:
        text (str): The text to be cleaned.
        
    Returns:
        str: The cleaned text with collapsed whitespace.
    """
    ascii_text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    ascii_text = ' '.join(ascii_text.split())
    return ascii_text

def read_json_file(file_path):
    """
    Reads a JSON file and returns a list of email entries.

    Parameters:
        file_path (str): The path to the JSON file.

    Returns:
        list: A list of email entries parsed from the JSON file.
    """
    email_entries = []
    with open(file_path, 'r') as file:
        for line in file:
            # Each line is a JSON object
            try:
                email_data = json.loads(line)
                email_entries.append(email_data)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
    return email_entries

def highlight_rows(s):
    # Function to highlight the rows
    return ['background-color: yellow' if v else '' for v in s == 1]

def clean_html(html_content):
    """
    Convert HTML to text and remove style and script tags.

    Parameters:
        html_content (str): The HTML content to be cleaned.

    Returns:
        str: The cleaned text without style and script tags.
    """
    # Convert HTML to text and remove style and script tags
    soup = BeautifulSoup(html_content, 'html.parser')
    for script_or_style in soup(['script', 'style']):
        script_or_style.decompose()
    text = soup.get_text(separator='\n')
    return text

def create_gmail_label_if_not_exists(label_name, service=service, user_id=user_id):
    """
    Creates a Gmail label if it does not already exist.

    Args:
        label_name (str): The name of the label to create.
        service (googleapiclient.discovery.Resource): An instance of the Gmail API service.
            Defaults to the global `service` variable.
        user_id (str): The ID of the user for whom the label should be created.
            Defaults to the global `user_id` variable.

    Returns:
        None

    Raises:
        Exception: If an error occurs while creating the label.
    """
    try:
        existing_labels = service.users().labels().list(userId=user_id).execute()

        # Check if the label already exists
        if any(label['name'] == label_name for label in existing_labels.get('labels', [])):
            print(f"Label '{label_name}' already exists.")
        else:
            # Create the label if it doesn't exist
            service.users().labels().create(userId=user_id, body={'name': label_name}).execute()
            print('Label created successfully.')

    except Exception as e:
        print('An error occurred:', e)



def move_email_to_label(email_id, new_label):
    """
    Move an email to a specified label.

    Parameters:
        email_id (str): The ID of the email to be moved.
        new_label (str): The label to which the email should be moved.

    Returns:
        None
    """
    # Connect to the IMAP server
    mail = imaplib.IMAP4_SSL('imap.gmail.com')

    mail.login(os.environ['USERNAME'], os.environ["PASSWORD"])

    mail.select('INBOX')
    
    # Search for the email with the specific ID
    typ, email_data = mail.uid('search', None, 'ALL')
    email_ids = email_data[0].split()
    
    if email_id.encode() not in email_ids:
        print(f"No email found with ID: {email_id}")
        return
    
    # Apply the label to the email with the specific ID
    result, _ = mail.uid('STORE', email_id, '+X-GM-LABELS', new_label)
    
    if result == 'OK':
        print(f"Email with ID {email_id} has been moved to {new_label}")
    else:
        print(f"Failed to move email with ID {email_id}")
    
    # Close the mailbox
    mail.close()
    
    # Logout from the server
    mail.logout()
    