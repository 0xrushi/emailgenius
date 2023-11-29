import os
from dotenv import load_dotenv
import json
from html import unescape
import re
import pandas as pd
import numpy as np
import time
import streamlit as st
import pandas as pd
import numpy as np
import time
import streamlit as st
import pandas as pd
import numpy as np
import time
import streamlit as st
import openai
import re
from langchain import PromptTemplate
from utils import remove_long_urls
from imap_tools import MailBox, AND
import argparse
from utils import create_gmail_label_if_not_exists, move_email_to_label, clean_text, read_json_file, highlight_rows, clean_html

load_dotenv()

parser = argparse.ArgumentParser(description="EmailGenius")
parser.add_argument('--approve', type=bool, default=False, help='Approve creating labels')
parser.add_argument('--ingest', type=bool, default=False, help='Ingest emails into data/email_data.json')
args = parser.parse_args()


# Point OpenAI client to our endpoint
openai.api_key = os.environ.get("OPENAI_API_KEY")
openai.api_base = os.environ.get("OPENAI_API_BASE")
# model at https://deepinfra.com
MODEL_DI = "meta-llama/Llama-2-70b-chat-hf"

def ingest_emails():
    """
    Ingests emails from an IMAP server and saves them to a JSON file.

    This function connects to an IMAP server using the provided login credentials and fetches all emails from the INBOX folder. It then cleans the email text and saves the email data to a JSON file.

    Parameters:
    - None

    Returns:
    - None
    """
    json_file = 'data/email_data.json'
    with open(json_file, 'a') as file:
        with MailBox('imap.gmail.com').login(os.environ['USERNAME'], os.environ["PASSWORD"], initial_folder='INBOX') as mailbox:
            # Fetch all emails from the INBOX folder
            for msg in mailbox.fetch(mark_seen=False):  # mark_seen=False to leave messages as unread
                email_body = msg.text or clean_html(msg.html)  # Use text if available, otherwise clean the HTML
                cleaned_body = clean_text(email_body)

                specified_label = "Important"

                email_data = {
                    'id': msg.uid,
                    'date': msg.date_str,
                    'from': msg.from_,
                    'to': msg.to,
                    'subject': msg.subject,
                    'body': cleaned_body,
                    'label': specified_label
                }

                file.write(json.dumps(email_data) + '\n')
    
def run_streamlit(st):
    """
    Runs the Streamlit application for EmailGenius: AI-Driven Email Categorization.
    
    Parameters:
        - st: Streamlit object for building the user interface.
        
    Returns:
        None
    """
    
    emails = read_json_file('data/email_data.json')

    st.title('EmailGenius: AI-Driven Email Categorization')
    input1 = st.text_input('Category', placeholder='Enter your category here')
    prompt_template = """###Objective: Assess whether the email falls under the '{input1}' category. 
    ###Email Details: ```{email}```.

    - If the email is associated with the '{input1}' category, Respond in JSON format {{"Output": 1}}.
    - If the email does not belong to the '{input1}' category, Respond in JSON format {{"Output": 0}}.
    - Respond only in JSON nothing else, no explaination needed.

    ###Response: 
    """

    if st.button('Submit'):
        # initialize empty df
        df = pd.DataFrame(columns=['From', 'Subject', 'Label'])
        col1, col2 = st.columns(2)
        placeholder_df = col1.empty()
        placeholder_logs = col2.empty()
        live_logs = ""
        i=0
        for msg in emails:
            txt = ""
            from_email = msg['from']
            subject = msg['subject']
            body = msg['body']
            txt += from_email + "\n"
            txt += subject + "\n"
            txt += body + "\n"
            email_content = txt
            i+=1

            prompt = PromptTemplate(template=prompt_template, input_variables=["input1", "email"])
            input_data = {'input1':input1, 'email':email_content}
            generated_prompt = prompt.format(**input_data)
            generated_prompt = remove_long_urls(generated_prompt).replace('( )', '')
            generated_prompt = clean_text(generated_prompt)

            print(generated_prompt)

            chat_completion = openai.ChatCompletion.create(
                model=MODEL_DI,
                messages=[{"role": "user", "content": generated_prompt}],
                stream=False,
                max_tokens=256,
            )
            response = chat_completion.choices[0].message.content
            response = response.replace("'", '"')
            print(response)
            try:
                label = str(json.loads(response.strip())['Output'])
            except json.JSONDecodeError as e:
                print(e)
                try:
                    response = response.split('\n')[0].strip()
                    label = str(json.loads(response.strip())['Output'])
                except json.JSONDecodeError as e:
                    print(e)
                    label = "N/A"
            if args.approve and label == "1":
                create_gmail_label_if_not_exists(input1)
                move_email_to_label(msg['id'], input1)
            new_row = pd.DataFrame({'From': [from_email], 'Subject': [subject], 'Label': [label]})
            df = pd.concat([df, new_row], ignore_index=True)

            placeholder_df.dataframe(df.style.apply(highlight_rows, subset=['Label']))
            live_logs += f"{i+1} - {from_email} - {subject} \n"
            placeholder_logs.text(live_logs)
            time.sleep(1)

        st.write(df['Label'].sum())

if __name__ == '__main__':
    if args.ingest:
        ingest_emails()
    else:
        run_streamlit(st)