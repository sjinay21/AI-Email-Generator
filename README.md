# AI-Email-Generator
This project automates personalized cold email generation using OpenAI and Google Sheets API.

## How it works
1. Reads lead data from Google Sheets
2. Uses OpenAI to generate 3 email variants
3. Uses static sender identities (Seven Nodes)
4. Writes generated emails back to Google Sheets

## Setup
- Python 3.x
- OpenAI API key (via environment variable)
- Google Service Account credentials

> Note: Sensitive files like `service_account.json` are excluded from the repository for security reasons.
