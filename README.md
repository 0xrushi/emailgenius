## Introduction
EmailGenius is an AI-driven email categorization tool that automates the process of sorting and labeling emails using the Opensource LLAMA API. It connects to an IMAP server, fetches emails, and categorizes them based on user-defined criteria. The project also includes a Streamlit interface for an interactive user experience.

## Requirements
- Python 3.x
- LLAMA API Key (I used https://deepinfra.com, needs `openai==0.28`)
- IMAP Server Credentials (refer [accessing-gmail-inbox-using-python-imaplib-module](https://pythoncircle.com/post/727/accessing-gmail-inbox-using-python-imaplib-module/) to create your gmail python app password)
- Streamlit

## Installation
1. Clone the repository:
   ```
   git clone [repository URL]
   ```
2. Navigate to the project directory:
   ```
   cd email-genius
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

## Email Ingestion
The `ingest_emails` function connects to an IMAP server and fetches emails, storing them in a JSON file after cleaning the text.

## Streamlit Interface
The `run_streamlit` function uses Streamlit to create an interactive UI, allowing users to input categories and view categorized emails.

## Contributing
Contributions to EmailGenius are welcome. Please follow the standard fork, branch, and pull request workflow.

## License
MIT
