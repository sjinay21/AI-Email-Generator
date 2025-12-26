import os
import time
import openai
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

SPREADSHEET_ID = "1pN8aTz1BJCsuS3faPweuHx-Cm8_AvPtMM_lcSPvuu2s"
INPUT_SHEET = "leads"
OUTPUT_SHEET = "ai_email_output"

openai.api_key = os.getenv("OPENAI_API_KEY")

SENDERS = [
    {"name": "abc", "email": "abc@gmail.com"},
    {"name": "abc", "email": "abc@gmail.com"},
    {"name": "abc", "email": "abc@gmail.com"},
]

def connect_to_sheets():
    creds = Credentials.from_service_account_file(
        "service_account.json",
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    return build("sheets", "v4", credentials=creds)

def get_value(row, idx):
    return row[idx].strip() if len(row) > idx and row[idx] else ""

def fetch_leads(service):
    res = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=f"{INPUT_SHEET}!A2:BF"
    ).execute()
    return res.get("values", [])

def ensure_header(service):
    header = [[
        "First Name",
        "Title",
        "Company",
        "Industry",
        "Website",
        "LinkedIn",
        "Twitter",
        "Email Variant 1",
        "Email Variant 2",
        "Email Variant 3"
    ]]

    service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=f"{OUTPUT_SHEET}!A1:J1",
        valueInputOption="RAW",
        body={"values": header}
    ).execute()

def generate_emails(first_name, title, company, industry, website, sender):

    prompt = f"""
You are an expert B2B sales copywriter working for Seven Nodes.

MANDATORY RULES:
- You are writing ONLY for Seven Nodes
- DO NOT invent sender details
- DO NOT invent company names
- NO placeholders
- Emails must be ready to send
- Professional, human, consultative tone

Recipient details:
Name: {first_name}
Title: {title}
Company: {company}
Industry: {industry}
Website: {website}

Sender details (USE EXACTLY):
Name: {sender['name']}
Company: xyz
Email: {sender['email']}

Write THREE email variants.

FORMAT STRICTLY:

---VARIANT 1---
Subject: ...
Body:
Hi {first_name},

...

Best regards,
{sender['name']}
Seven Nodes
{sender['email']}

---VARIANT 2---
...

---VARIANT 3---
...
"""

    while True:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.6,
                max_tokens=900
            )
            return response.choices[0].message.content.strip()

        except openai.error.RateLimitError:
            print("Rate limit hit. Waiting 25 seconds...")
            time.sleep(25)   
            
def split_variants(text):
    parts = text.split("---VARIANT")
    variants = [p.strip() for p in parts[1:]]
    return variants if len(variants) == 3 else ["ERROR", "ERROR", "ERROR"]

def write_output(service, row):
    service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range="A1",
        valueInputOption="RAW",
        insertDataOption="INSERT_ROWS",
        body={"values": [row]}
    ).execute()

def main():
    service = connect_to_sheets()
    ensure_header(service)

    leads = fetch_leads(service)

    for lead in leads:
        first_name = get_value(lead, 0)
        title      = get_value(lead, 31)
        company    = get_value(lead, 7)
        industry   = get_value(lead, 28)
        website    = get_value(lead, 56)
        linkedin   = get_value(lead, 11)
        twitter    = get_value(lead, 55)

        if not first_name or not company:
            continue

        sender = SENDERS[hash(first_name) % len(SENDERS)]

        print(f"Generating emails for {first_name} ({sender['name']})...")

        email_text = generate_emails(
            first_name,
            title,
            company,
            industry,
            website,
            sender
        )

        v1, v2, v3 = split_variants(email_text)

        row = [
            first_name,
            title,
            company,
            industry,
            website,
            linkedin,
            twitter,
            v1,
            v2,
            v3
        ]

        write_output(service, row)
        time.sleep(20)

    print("ALL EMAIL VARIANTS GENERATED SUCCESSFULLY")
    
if __name__ == "__main__":
    main()

    
    

    
