#AI Email Generator

This project automates the generation of personalized cold emails using OpenAI and the Google Sheets API.
It is designed to streamline outbound communication by generating multiple, ready-to-send email variants based on lead data.

##Features
⦁	Reads structured lead data from Google Sheets.
⦁	Generates three personalized email variants per lead using AI.
⦁	Uses static sender identities to maintain brand consistency.
⦁	Handles API rate limits gracefully.
⦁	Writes generated emails back to Google Sheets automatically.

##How It Works
1.	Lead data is fetched from a Google Sheets worksheet.
2.	Relevant fields (name, company, role, etc.) are passed to the OpenAI model.
3.	The model generates three well-formatted, professional email variants.
4.	The output is written to a separate Google Sheets worksheet for review or use.

##Tech Stack
⦁	Python 3.x
⦁	OpenAI API
⦁	Google Sheets API
⦁	Google Service Account authentication

##Setup & Configuration
To run this project locally:
⦁	Set your OpenAI API key as an environment variable.
⦁	Create a Google Service Account with access to Google Sheets.
⦁	Provide the service account credentials locally.

Note: Sensitive files such as service_account.json and API keys are intentionally excluded from this repository for security reasons.
A template file and setup instructions are provided instead.

##Security Note

All sensitive credentials and sender details are anonymized or excluded in this repository.
In a production environment, real credentials and sender information are used securely.

##Use Case
This project is useful for:
⦁	Sales and marketing automation.
⦁	AI-assisted outbound email campaigns.
⦁	Demonstrating AI + API integration in real-world workflows.
