import sqlite3
import subprocess
from dateutil.parser import parse
from datetime import datetime
import json
from pathlib import Path
import os
import requests
from scipy.spatial.distance import cosine
from dotenv import load_dotenv

load_dotenv()

AIPROXY_TOKEN = os.getenv('AIPROXY_TOKEN')


def A1(email="22f2000526@ds.study.iitm.ac.in"):
    try:
        process = subprocess.Popen(
            ["uv", "run", "https://raw.githubusercontent.com/sanand0/tools-in-data-science-public/tds-2025-01/project-1/datagen.py", email],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        stdout, stderr = process.communicate()
        if process.returncode != 0:
            raise HTTPException(status_code=500, detail=f"Error: {stderr}")
        return stdout
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Error: {e.stderr}")
# A1()
# def A2(prettier_version="prettier@3.4.2", filename="/data/format.md"):
#     # Read the markdown file
#     with open(filename, "r", encoding="utf-8") as file:
#         content = file.read()

#     # Fix list formatting issues before running Prettier
#     content = content.replace("+Third item", "  - Third item")
#     content = content.replace("    *    Fourth item", "  - Fourth item")

#     # Write back the corrected content
#     with open(filename, "w", encoding="utf-8") as file:
#         file.write(content)

#     # Run Prettier for final formatting
#     command = [r"C:\Program Files\nodejs\npx.cmd", prettier_version, "--write", filename]
#     try:
#         subprocess.run(command, check=True)
#         print("Prettier executed successfully.")
#     except subprocess.CalledProcessError as e:
#         print(f"An error occurred: {e}")
def A2(prettier_version="prettier@3.4.2", filename="/data/format.md"):
    command = [r"C:\Program Files\nodejs\npx.cmd", prettier_version, "--write", filename]
    try:
        subprocess.run(command, check=True)
        print("Prettier executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")


def A3(filename='/data/dates.txt', targetfile='/data/dates-wednesdays.txt', weekday=2):
    input_file = filename
    output_file = targetfile
    weekday = weekday
    weekday_count = 0

    with open(input_file, 'r') as file:
        weekday_count = sum(1 for date in file if parse(date).weekday() == int(weekday)-1)


    with open(output_file, 'w') as file:
        file.write(str(weekday_count))

def A4(filename="/data/contacts.json", targetfile="/data/contacts-sorted.json"):
    # Load the contacts from the JSON file
    with open(filename, 'r') as file:
        contacts = json.load(file)

    # Sort the contacts by last_name and then by first_name
    sorted_contacts = sorted(contacts, key=lambda x: (x['last_name'], x['first_name']))

    # Write the sorted contacts to the new JSON file
    with open(targetfile, 'w') as file:
        json.dump(sorted_contacts, file, indent=4)

def A5(log_dir_path='/data/logs', output_file_path='/data/logs-recent.txt', num_files=10):
    log_dir = Path(log_dir_path)
    output_file = Path(output_file_path)

    # Get list of .log files sorted by modification time (most recent first)
    log_files = sorted(log_dir.glob('*.log'), key=os.path.getmtime, reverse=True)[:num_files]

    # Read first line of each file and write to the output file
    with output_file.open('w') as f_out:
        for log_file in log_files:
            with log_file.open('r') as f_in:
                first_line = f_in.readline().strip()
                f_out.write(f"{first_line}\n")

def A6(doc_dir_path='/data/docs', output_file_path='/data/docs/index.json'):
    docs_dir = doc_dir_path
    output_file = output_file_path
    index_data = {}

    # Walk through all files in the docs directory
    for root, _, files in os.walk(docs_dir):
        for file in files:
            if file.endswith('.md'):
                # print(file)
                file_path = os.path.join(root, file)
                # Read the file and find the first occurrence of an H1
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        if line.startswith('# '):
                            # Extract the title text after '# '
                            title = line[2:].strip()
                            # Get the relative path without the prefix
                            relative_path = os.path.relpath(file_path, docs_dir).replace('\\', '/')
                            index_data[relative_path] = title
                            break  # Stop after the first H1
    # Write the index data to index.json
    # print(index_data)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(index_data, f, indent=4)

def A7(filename='/data/email.txt', output_file='/data/email-sender.txt'):
    # Read the content of the email
    with open(filename, 'r') as file:
        email_content = file.readlines()

    sender_email = "sujay@gmail.com"
    for line in email_content:
        if "From" == line[:4]:
            sender_email = (line.strip().split(" ")[-1]).replace("<", "").replace(">", "")
            break

    # Get the extracted email address

    # Write the email address to the output file
    with open(output_file, 'w') as file:
        file.write(sender_email)

import base64
def png_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        base64_string = base64.b64encode(image_file.read()).decode('utf-8')
    return base64_string


import time
import pytesseract
import re
from PIL import Image, ImageDraw, ImageFont
import os

DATA_DIR = Path("/data")

def A8(filename=DATA_DIR / "credit-card.txt", image_path=DATA_DIR / "credit_card.png"):
    try:
        # Ensure image exists
        if not image_path.exists():
            print(f"❌ Error: Image file '{image_path}' not found.")
            return "Error: Credit Card image not found."

        # Load image and perform OCR
        image = Image.open(image_path)
        extracted_text = pytesseract.image_to_string(image)

        # Extract only 16-digit numbers
        extracted_numbers = re.findall(r"\b\d{4} \d{4} \d{4} \d{4}\b", extracted_text)

        if extracted_numbers:
            card_number = extracted_numbers[0].replace(" ", "")  # Remove spaces

            # Ensure extracted number is 16 digits
            if len(card_number) == 16:
                print(f"✅ Extracted Credit Card Number: {card_number}")

                # Ensure the directory exists before writing
                filename.parent.mkdir(parents=True, exist_ok=True)

                # Write to file
                with open(filename, "w") as f:
                    f.write(card_number)

                # Give time for the file to be written before evaluation
                time.sleep(2)

                print(f"✅ Credit Card Number Saved in: {filename}")
            else:
                print("❌ Error: Extracted card number is not 16 digits.")
                return "Error: Invalid card number length."
        else:
            print("❌ Error: No valid credit card number detected.")
            return "Error: No card number found."

    except Exception as e:
        print(f"❌ Error during credit card extraction: {str(e)}")
        return f"Error during OCR extraction: {str(e)}"


# def get_embedding(text):
#     if not AIPROXY_TOKEN:
#         raise ValueError("Error: Missing AIPROXY_TOKEN.")

#     headers = {
#         "Content-Type": "application/json",
#         "Authorization": f"Bearer {AIPROXY_TOKEN}"
#     }
#     data = {
#         "model": "text-embedding-3-small",
#         "input": [text]
#     }

#     response = requests.post("http://aiproxy.sanand.workers.dev/openai/v1/embeddings", headers=headers, data=json.dumps(data))

#     if response.status_code == 401:
#         raise ValueError("Error: Unauthorized API request. Check AIPROXY_TOKEN.")

#     response.raise_for_status()
#     return response.json()["data"][0]["embedding"]

# def A9(filename='/data/comments.txt', output_filename='/data/comments-similar.txt'):
#     # Read comments
#     with open(filename, 'r') as f:
#         comments = [line.strip() for line in f.readlines()]

#     # Get embeddings for all comments
#     embeddings = [get_embedding(comment) for comment in comments]

#     # Find the most similar pair
#     min_distance = float('inf')
#     most_similar = (None, None)

#     for i in range(len(comments)):
#         for j in range(i + 1, len(comments)):
#             distance = cosine(embeddings[i], embeddings[j])
#             if distance < min_distance:
#                 min_distance = distance
#                 most_similar = (comments[i], comments[j])

#     # Write the most similar pair to file
#     with open(output_filename, 'w') as f:
#         f.write(most_similar[0] + '\n')
#         f.write(most_similar[1] + '\n')

def get_embedding(text):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {AIPROXY_TOKEN}"
    }
    data = {
        "model": "text-embedding-3-small",
        "input": [text]
    }
    response = requests.post("http://aiproxy.sanand.workers.dev/openai/v1/embeddings", headers=headers, data=json.dumps(data))
    response.raise_for_status()
    return response.json()["data"][0]["embedding"]

def A9(filename='/data/comments.txt', output_filename='/data/comments-similar.txt'):
    # Read comments
    with open(filename, 'r') as f:
        comments = [line.strip() for line in f.readlines()]

    # Get embeddings for all comments
    embeddings = [get_embedding(comment) for comment in comments]

    # Find the most similar pair
    min_distance = float('inf')
    most_similar = (None, None)

    for i in range(len(comments)):
        for j in range(i + 1, len(comments)):
            distance = cosine(embeddings[i], embeddings[j])
            if distance < min_distance:
                min_distance = distance
                most_similar = (comments[i], comments[j])

    # Write the most similar pair to file
    with open(output_filename, 'w') as f:
        f.write(most_similar[0] + '\n')
        f.write(most_similar[1] + '\n')

def A10(filename='/data/ticket-sales.db', output_filename='/data/ticket-sales-gold.txt', query="SELECT SUM(units * price) FROM tickets WHERE type = 'Gold'"):
    # Connect to the SQLite database
    conn = sqlite3.connect(filename)
    cursor = conn.cursor()

    # Calculate the total sales for the "Gold" ticket type
    cursor.execute(query)
    total_sales = cursor.fetchone()[0]

    # If there are no sales, set total_sales to 0
    total_sales = total_sales if total_sales else 0

    # Write the total sales to the file
    with open(output_filename, 'w') as file:
        file.write(str(total_sales))

    # Close the database connection
    conn.close()
