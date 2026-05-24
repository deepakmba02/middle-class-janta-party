import os
import re
from google import genai

# 1. Initialize the Gemini AI Client using the cloud environment key
# The new google-genai SDK automatically initializes via the GEMINI_API_KEY env variable.
client = genai.Client()

def generate_satirical_row(user_submission):
    """
    AI Agent that reviews citizen complaints and structures them into a clean HTML table row.
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
    """
    Locates the structural marker in index.html and injects the AI row at the top of the ledger.
    """
    file_path = "index.html"
    
    # Read the current layout file
    with open(file_path, "r", encoding="utf-8") as f:
        html_content = f.read()
        
    # Look for our special HTML identifier tag
    target_tag = '<tbody id="ledger-body">'
    
    if target_tag in html_content:
        # Inject the fresh automated row immediately below the table body start
        updated_content = html_content.replace(target_tag, f"{target_tag}\n                    {new_html_row}")
        
        # Overwrite the file on GitHub
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(updated_content)
        print("Successfully updated the MCJP live ledger with new AI content!")
    else:
        print("Error: Could not locate <tbody id='ledger-body'> marker in index.html")

if __name__ == "__main__":
    # Test sample simulating an anonymous form entry from Bangalore
    sample_input = "Paid 42,000 rupees rent for a 1BHK in Outer Ring Road plus 18 percent GST on my onboarding platform fee."
    
    # Run the automation loop
    html_row = generate_satirical_row(sample_input)
    update_website(html_row)
