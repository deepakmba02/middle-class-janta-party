import os
import sys
from google import genai

client = genai.Client()

def generate_satirical_row(user_submission):
    """
    AI Agent that reviews live citizen complaints and structures them into a clean HTML table row.
    """
    prompt = f"""
    You are the automated chief creative satirist for the Middle Class Janta Party website.
    Take this user submission regarding rising inflation or daily expenses and format it into exactly ONE <tr> table row.
    
    User Submission: "{user_submission}"
    
    Output exactly this structure and nothing else (do not include markdown ticks like ```html or system logs):
    <tr>
        <td><strong>Category Name</strong></td>
        <td>Extracted or Estimated Price/Cost (in ₹)</td>
        <td>A highly relatable, respectful, deeply sharp sarcastic punchline about the tax/rent/GST burden</td>
    </tr>
    """
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt
    )
    return response.text.strip()

def update_website(new_html_row):
    file_path = "index.html"
    
    with open(file_path, "r", encoding="utf-8") as f:
        html_content = f.read()
        
    target_tag = '<tbody id="ledger-body">'
    
    if target_tag in html_content:
        updated_content = html_content.replace(target_tag, f"{target_tag}\n                    {new_html_row}")
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(updated_content)
        print("Successfully updated the MCJP live ledger with new AI content!")
    else:
        print("Error: Could not locate <tbody id='ledger-body'> marker in index.html")

if __name__ == "__main__":
    # 💥 DYNAMIC UPDATE: Read the input text sent over by Make.com via the workflow argument
    # If no argument is found, it falls back to a default testing value.
    if len(sys.argv) > 1:
        live_submission = sys.argv[1]
    else:
        live_submission = "Paid premium price for basic city amenities again."
        
    print(f"Processing Live Submission: {live_submission}")
    html_row = generate_satirical_row(live_submission)
    update_website(html_row)
