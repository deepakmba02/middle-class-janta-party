import os
import urllib.parse
import xml.etree.ElementTree as ET
import google.generativeai as genai
import requests
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

# 1. Initialize Gemini
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

def fetch_latest_bangalore_news():
    """Scrapes Google News RSS feed for live Bengaluru middle-class pain points"""
    query = "Bangalore rent inflation food fuel price hike"
    encoded_query = urllib.parse.quote(query)
    url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en-IN&gl=IN&ceid=IN:en"
    
    try:
        response = requests.get(url, timeout=10)
        root = ET.fromstring(response.content)
        headlines = []
        for item in root.findall('.//item')[:5]:
            title = item.find('title').text
            headlines.append(title)
        return "\n".join(headlines)
    except Exception as e:
        print(f"Error fetching news: {e}")
        return "High rents, hotel food price hikes, 5% GST burdens, electricity tariff jumps."

def wrap_text(text, font, max_width, draw):
    """Helper to wrap long text into lines so it fits beautifully on the image"""
    words = text.split(' ')
    lines = []
    current_line = []
    
    for word in words:
        current_line.append(word)
        # Check size of line with the new word
        line_str = ' '.join(current_line)
        bbox = draw.textbbox((0, 0), line_str, font=font)
        width = bbox[2] - bbox[0]
        
        if width > max_width:
            current_line.pop()
            lines.append(' '.join(current_line))
            current_line = [word]
            
    if current_line:
        lines.append(' '.join(current_line))
    return lines

# 2. Collect Real-Time Data Context
today_news = fetch_latest_bangalore_news()
date_str = datetime.now().strftime("%d %b %Y")

# 3. Ask Gemini to write a custom, dynamic tweet based on reality
prompt = f"""
You are the voice of the Middle Class Janta Party (MCJP). Today is {date_str}.
Here are the latest trending issues and news regarding the cost of living squeeze in Bengaluru:
{today_news}

Write a raw, intense, punchy message (under 160 characters) expressing middle class anger about high prices, bills, or taxes. 
Make it short, clear, and direct. Do not include any links or hashtags inside this raw text block.
"""

response = model.generate_content(prompt)
raw_ai_tweet = response.text.strip()

# Create the full X social post text with tracking links & hashtags
full_tweet_post = f"{raw_ai_tweet}\n\n#Bangalore #GST\n\n📊 Track the math live & report today's loot:\n👉 https://bit.ly/4fBg9JB"

# 4. Save Text Asset to Launchpad Folder
os.makedirs("launchpad", exist_ok=True)
with open("launchpad/today_tweet.txt", "w", encoding="utf-8") as f:
    f.write(full_tweet_post)

# 5. DYNAMIC GRAPHIC UPGRADE: Render the AI generated tweet directly onto the image
try:
    # Open the master branding banner you uploaded
    img = Image.open("mcjp_graphic.png").convert("RGBA")
    draw = ImageDraw.Draw(img)
    
    # Try using standard system fonts, fallback to basic default if not found
    try:
        font_title = ImageFont.truetype("DejaVuSans-Bold.ttf", 28)
        font_body = ImageFont.truetype("DejaVuSans.ttf", 24)
    except IOError:
        font_title = ImageFont.load_default()
        font_body = ImageFont.load_default()
        
    # Draw a visual container box on the canvas for the dynamic text
    # [X_start, Y_start, X_end, Y_end]
    card_coords = [50, 180, 750, 450]
    draw.rectangle(card_coords, fill=(0, 0, 0, 190), outline=(255, 215, 0), width=3)
    
    # Stamp Section Header
    draw.text((75, 200), f"TODAY'S VOICE // {date_str.upper()}", fill=(255, 215, 0), font=font_title)
    
    # Wrap and stamp the AI's custom generated text inside the box boundaries
    wrapped_lines = wrap_text(raw_ai_tweet, font_body, 650, draw)
    
    y_offset = 250
    for line in wrapped_lines[:5]:  # Safety cap at 5 lines maximum to prevent box spill
        draw.text((75, y_offset), line, fill=(255, 255, 255), font=font_body)
        y_offset += 35
        
    # Flatten image layers and save final copy to launchpad
    final_img = img.convert("RGB")
    final_img.save("launchpad/today_graphic.png", "PNG")
    print("Successfully cooked and rendered today's dynamic graphic!")
    
except Exception as e:
    print(f"Dynamic Image generation error: {e}")
