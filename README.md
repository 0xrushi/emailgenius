## Introduction
EmailGenius is an AI-driven email categorization tool that automates the process of sorting and labeling emails using the Opensource LLAMA API. It connects to an IMAP server, fetches emails, and categorizes them based on user-defined criteria. The project also includes a Streamlit interface for an interactive user experience.

## Purpose 
The market offers various proprietary email categorization and management tools, including:
- [SaneBox](https://www.sanebox.com/): This tool automatically organizes incoming emails into different folders based on user behavior.
- [Clean Email](https://clean.email/): A management tool designed to help users declutter their inboxes from unnecessary emails.

However, these tools have limitations, such as not being opensource and requiring payment and often adopting a pricing model based on each email account. With the ongoing democratization of AI, it's expected that even standard servers will be capable of running similar processes more affordably, accommodating any number of accounts within the next five years.

In contrast, widely-used email services like Microsoft Outlook, Gmail, and Zoho Mail can be cumbersome in setting up email filter rules, often involving numerous steps. Moreover, users frequently encounter issues where emails from unsubscribed websites persist in appearing in their inboxes.


## Requirements
- Python 3.x
- LLAMA API Key (I used https://deepinfra.com, needs `openai==0.28`)
- IMAP Server Credentials (refer [accessing-gmail-inbox-using-python-imaplib-module](https://pythoncircle.com/post/727/accessing-gmail-inbox-using-python-imaplib-module/) to create your gmail python app password)
- Streamlit

## Installation
1. Clone the repository:
   ```
   git clone https://github.com/0xrushi/emailgenius.git
   ```
2. Navigate to the project directory:
   ```
   cd emailgenius
   ```
3. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

## Configuration
1. Create a `.env` file in the project root with the following variables:
   - `OPENAI_API_KEY` - Your OpenAI API key.
   - `OPENAI_API_BASE` - OpenAI API base URL.
   - `USERNAME` - IMAP server username.
   - `PASSWORD` - IMAP server password.
2. Load environment variables:
   ```python
   load_dotenv()
   ```

## Usage
1. To ingest emails from your IMAP server to a `data/email_data.json` file:
   ```
   streamlit run src/main.py -- --ingest true
   ```
2. To run the Streamlit app for categorization:
   ```
    streamlit run src/main.py
   ```
3. To use it in production:
   ```
    streamlit run src/main.py -- --approve true
   ```

### Streamlit App
- Launch the app and enter a category in the text input field.
- Click 'Submit' to categorize emails based on the specified category.
- The app displays the processed emails along with their categorization.
- In production mode (using the --approve flag), labels are generated and the actual sorting of emails into these labels occurs.

## Screenshots
![Screenshot 2023-11-28 at 9 44 10 PM](https://github.com/0xrushi/emailgenius/assets/6279035/e94d70f1-6ba2-43a3-915b-6d4b8eb29e79)
![Screenshot 2023-11-28 at 9 49 00 PM](https://github.com/0xrushi/emailgenius/assets/6279035/4c6370f4-abca-4b50-bdd0-11ecfb11cb4a)
![Screenshot 2023-11-28 at 10 12 53 PM](https://github.com/0xrushi/emailgenius/assets/6279035/4dfa487c-ff54-45e1-92b6-0feba8fb62e5)
![Screenshot 2023-11-28 at 10 13 08 PM](https://github.com/0xrushi/emailgenius/assets/6279035/024cda90-eff3-4e7e-b595-614e7da4b6d6)

## Limitations
- As of now, the existing code template is compatible exclusively with Gmail.

## Contributing
Contributions to EmailGenius are welcome. Please follow the standard fork, branch, and pull request workflow.


<a href="https://www.buymeacoffee.com/rushic24" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: 41px !important;width: 174px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" ></a>

