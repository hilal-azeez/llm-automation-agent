# Phase B: LLM-based Automation Agent for DataWorks Solutions
import os
import requests
import sqlite3
import duckdb
from PIL import Image
import markdown

# Ensure the `/data` directory exists
DATA_DIR = os.path.abspath("data")  # Corrected for Windows/Linux compatibility
os.makedirs(DATA_DIR, exist_ok=True)  # Ensure the directory exists


# B1 & B2: Security Checks
# B1 & B2: Security Checks
def B12(filepath):
    """Ensure the file is inside `/data` and prevent deletion."""
    filepath = os.path.abspath(filepath)  # Convert to absolute path
    data_dir = os.path.abspath(DATA_DIR)  # Get absolute path of /data
    
    if not filepath.startswith(data_dir):
        raise PermissionError(f"Access denied: `{filepath}` is outside `{DATA_DIR}`.")
    
    return True


# B3: Fetch Data from an API and Save It
def B3(url, save_path):
    """Fetches data from a given API URL and saves it."""
    if B12(save_path):
        response = requests.get(url)
        if response.status_code == 200:
            with open(save_path, "w", encoding="utf-8") as file:
                file.write(response.text)
        else:
            raise Exception(f"Failed to fetch data: {response.status_code}")

# B4: Clone a Git Repo and Make a Commit
def B4(repo_url, commit_message):
    """Clones a GitHub repository and commits changes."""
    if B12("/data/repo"):
        import subprocess
        subprocess.run(["git", "clone", repo_url, "/data/repo"], check=True)
        subprocess.run(["git", "-C", "/data/repo", "commit", "-m", commit_message], check=True)

# B5: Run a SQL Query on a SQLite or DuckDB Database
def B5(db_path, query, output_filename):
    """Executes an SQL query on SQLite or DuckDB and saves the results."""
    if B12(db_path) and B12(output_filename):
        conn = sqlite3.connect(db_path) if db_path.endswith(".db") else duckdb.connect(database=":memory:")
        cur = conn.cursor()
        cur.execute(query)
        result = cur.fetchall()
        conn.close()
        with open(output_filename, "w", encoding="utf-8") as file:
            file.write(str(result))
        return result

# B6: Extract Data from a Website (Web Scraping)
def B6(url, output_filename):
    """Scrapes a webpage and saves the HTML content."""
    if B12(output_filename):
        response = requests.get(url)
        if response.status_code == 200:
            with open(output_filename, "w", encoding="utf-8") as file:
                file.write(response.text)
        else:
            raise Exception(f"Failed to fetch page: {response.status_code}")

# B7: Compress or Resize an Image
def B7(image_path, output_path, resize=None):
    """Resizes or compresses an image."""
    if B12(image_path) and B12(output_path):
        img = Image.open(image_path)
        if resize:
            img = img.resize(resize)
        img.save(output_path)

# B8: Transcribe Audio from an MP3 File
def B8(audio_path, output_path):
    """Transcribes audio using OpenAI Whisper."""
    if B12(audio_path) and B12(output_path):
        import openai
        AIPROXY_TOKEN = os.environ.get("AIPROXY_TOKEN")
        if not AIPROXY_TOKEN:
            raise Exception("AIPROXY_TOKEN environment variable is not set.")
        with open(audio_path, "rb") as audio_file:
            response = openai.Audio.transcribe("whisper-1", audio_file)
            with open(output_path, "w", encoding="utf-8") as file:
                file.write(response["text"])

# B9: Convert Markdown to HTML
def B9(md_path, output_path):
    """Converts Markdown to HTML."""
    if B12(md_path) and B12(output_path):
        with open(md_path, "r", encoding="utf-8") as file:
            html = markdown.markdown(file.read())
        with open(output_path, "w", encoding="utf-8") as file:
            file.write(html)

# B10: Write an API Endpoint That Filters a CSV File and Returns JSON Data
from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

@app.route("/filter_csv", methods=["POST"])
def filter_csv():
    """Filters a CSV file based on a column value."""
    data = request.json
    csv_path = data["csv_path"]
    filter_column = data["filter_column"]
    filter_value = data["filter_value"]

    if B12(csv_path):
        df = pd.read_csv(csv_path)
        filtered = df[df[filter_column] == filter_value]
        return jsonify(filtered.to_dict(orient="records"))

if __name__ == "__main__":
    print("API Running at http://localhost:8000")
    app.run(host="0.0.0.0", port=8000)
