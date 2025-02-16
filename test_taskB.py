from tasksB import B3, B5, B6, B7, B9
from PIL import Image
import os

# Ensure the /data directory exists
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

# Ensure sample.md exists before testing B9
sample_md_path = os.path.join(DATA_DIR, "sample.md")
if not os.path.exists(sample_md_path):
    with open(sample_md_path, "w", encoding="utf-8") as f:
        f.write("# Sample Markdown\nThis is a test markdown file for B9 conversion.")

# Ensure sample_image.png exists before testing B7
sample_image_path = os.path.join(DATA_DIR, "sample_image.png")
if not os.path.exists(sample_image_path):
    img = Image.new("RGB", (500, 500), (255, 0, 0))  # Create a red image
    img.save(sample_image_path)

# Test B3: Fetch API Data
B3("https://jsonplaceholder.typicode.com/posts", os.path.join(DATA_DIR, "test_api.json"))

# Test B5: Run SQL Query
B5(os.path.join(DATA_DIR, "ticket-sales.db"), "SELECT * FROM tickets LIMIT 5;", os.path.join(DATA_DIR, "query_result.txt"))

# Test B6: Web Scraping
B6("https://example.com", os.path.join(DATA_DIR, "example_page.html"))

# Test B7: Image Processing (Resizing)
B7(sample_image_path, os.path.join(DATA_DIR, "resized_image.png"), resize=(300, 300))

# Test B9: Markdown to HTML
B9(sample_md_path, os.path.join(DATA_DIR, "sample.html"))

print("✅ All functions executed successfully!")
