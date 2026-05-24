import os
import sys
from datetime import datetime

def main():
    # 1. Safely extract the 3 new fields sent from Make via GitHub Actions inputs
    user_rant = os.environ.get("INPUT_USER_RANT", "").strip()
    location = os.environ.get("INPUT_LOCATION", "Unknown Location").strip()
    category = os.environ.get("INPUT_CATEGORY", "General").strip()

    # Fallback: check sys.argv if environment variables aren't populated
    if not user_rant and len(sys.argv) > 1:
        user_rant = sys.argv[1]

    # If everything is completely empty, don't write blank data
    if not user_rant:
        print("Error: No user rant content received. Exiting.")
        sys.exit(1)

    # 2. Generate the current date formatted nicely (e.g., "24 May 2026")
    current_date = datetime.now().strftime("%d %b %Y")

    # 3. Design the precise HTML table row matching your new multi-field layout
    new_html_row = f"""          <tr>
            <td>{current_date}</td>
            <td><span class="badge">{category}</span></td>
            <td><strong>{location}</strong></td>
            <td>"{user_rant}"</td>
          </tr>\n"""

    html_filename = "index.html"

    # 4. Read the existing index.html file
    if os.path.exists(html_filename):
        with open(html_filename, "r", encoding="utf-8") as f:
            html_content = f.read()
    else:
        print(f"Error: {html_filename} not found in root directory!")
        sys.exit(1)

    # 5. Locate your table body tag to insert the fresh entry at the top
    target_marker = "<tbody>"
    
    if target_marker in html_content:
        # Injecting right after <tbody> so newest entries show first
        updated_html = html_content.replace(target_marker, f"{target_marker}\n{new_html_row}")
        print("Successfully injected new row into the ledger table!")
    else:
        # Fallback if <tbody> tag isn't explicitly found
        print("Warning: <tbody> tag not found. Appending to end of file.")
        updated_html = html_content + f"\n\n<table>{new_html_row}</table>"

    # 6. Save the modifications back to index.html
    with open(html_filename, "w", encoding="utf-8") as f:
        f.write(updated_html)

if __name__ == "__main__":
    main()
