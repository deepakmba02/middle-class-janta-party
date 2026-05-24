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

def fetch_broad_middle_class_issues():
    """Scrapes Google News RSS using an expanded matrix of Bengaluru middle class issues"""
    # Expanded query to capture school fees, property tax, water, power, and transit
    query = "Bengaluru inflation OR property tax OR school fees OR water tariff OR fuel price"
    encoded_query = urllib.parse.quote(query)
    url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en-IN&gl=IN&ceid=IN:en"
    
    try:
        response = requests.get(url, timeout=10)
        root = ET.fromstring(response.content)
        headlines = []
        for item in root.findall('.//item')[:6]:
            headlines.append(item.find('title').text)
        return " | ".join(headlines)
    except Exception as e:
        print(f"Scraper error: {e}")
        return "Bengaluru property tax stress, surging school admission fees, auto/cab fare hikes, and local cost-of-living burdens."

def wrap_text(text, font, max_width, draw):
    """Helper to wrap dynamically generated text accurately into paragraphs"""
    words = text.split(' ')
    lines = []
    current_line = []
    for word in words:
        current_line.append(word)
        line_str = ' '.join(current_line)
        bbox = draw.textbbox((0, 0), line_str, font=font)
        if (bbox[2] - bbox[0]) > max_width:
            current_line.pop()
            lines.append(' '.join(current_line))
            current_line = [word]
    if current_line:
        lines.append(' '.join(current_line))
    return lines

# 2. Extract context dynamically
live_news_bulletin = fetch_broad_middle_class_issues()
date_str = datetime.now().strftime("%d %b %Y")

print("--- AGENT SEARCH RADAR ---")
print(live_news_bulletin)

# 3. Prompt Gemini to write a specific, hard-hitting localized citizen tweet
prompt = f"""
You are the voice of the Middle Class Janta Party (MCJP). Today is {date_str}.
Here is the real-world news context regarding middle-class issues in Bengaluru scraped right now:
"{live_news_bulletin}"

INSTRUCTIONS:
- Identify one or two key issues from the text (could be tax, fees, transport, utility bills, or general cost increases).
- Write a raw, highly specific, angry reaction post from a stressed salary earning resident.
- Call out how the system squeezes common citizens. Keep it punchy and sharp.
- Ensure the text block is under 150 characters. Do not use hashtags or links inside this specific block of text.
"""

response = model.generate_content(prompt)
raw_ai_voice = response.text.strip().replace('"', '')

# Compile final full package for X platform distribution
full_twitter_post = f"{raw_ai_voice}\n\n#Bangalore #MiddleClass\n\n📊 Track the math live & report today's loot:\n👉 https://bit.ly/4fBg9JB"

# 4. Save Text Asset
os.makedirs("launchpad", exist_ok=True)
with open("launchpad/today_tweet.txt", "w", encoding="utf-8") as f:
    f.write(full_twitter_post)

# 5. NEW GENERATIVE IMAGE CREATION FROM SCRATCH (No Template Required)
try:
    # Creating a 1080x1080 Square Image layout - perfect for X (Twitter) feeds!
    canvas_w, canvas_h = 1080, 1080
    img = Image.new("RGBA", (canvas_w, canvas_h), color=(18, 18, 18, 255)) # Sleek Matte Charcoal Base
    draw = ImageDraw.Draw(img)
    
    try:
        font_header = ImageFont.truetype("DejaVuSans-Bold.ttf", 42)
        font_sub = ImageFont.truetype("DejaVuSans.ttf", 30)
        font_body = ImageFont.truetype("DejaVuSans-Bold.ttf", 36)
        font_footer = ImageFont.truetype("DejaVuSans.ttf", 26)
    except IOError:
        font_header = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        font_body = ImageFont.load_default()
        font_footer = ImageFont.load_default()
        
    # Brand Accents: Red Left Border Strip (MCJP Branding)
    draw.rectangle([0, 0, 35, canvas_h], fill=(220, 40, 40, 255))
    
    # Graphic Header Elements
    draw.text((70, 70), "MIDDLE CLASS JANTA PARTY", fill=(220, 40, 40, 255), font=font_header) # Brand Crimson
    draw.text((70, 125), f"BENGALURU REALITY RADAR • {date_str.upper()}", fill=(160, 160, 160, 255), font=font_sub)
    
    # Decorative Divider Line
    draw.line([70, 185, canvas_w - 70, 185], fill=(255, 215, 0, 255), width=3) # Gold Accents
    
    # Central Content Display Card
    card_margin = 70
    draw.rectangle([card_margin, 240, canvas_w - card_margin, 900], fill=(28, 28, 28, 255), outline=(255, 215, 0, 255), width=2)
    
    # Word Wrapping Math focused into the 1080 box frame
    wrapped_lines = wrap_text(raw_ai_voice, font_body, canvas_w - (card_margin * 3), draw)
    
    # Centered Vertical Rendering Sequence for content text
    line_height = 54
    total_text_h = len(wrapped_lines) * line_height
    start_y = 240 + ((660 - total_text_h) // 2) # Perfectly centers the generated text block inside the frame box
    
    for line in wrapped_lines[:10]:
        # Center horizontally inside the text container card
        bbox = draw.textbbox((0, 0), line, font=font_body)
        line_w = bbox[2] - bbox[0]
        line_x = card_margin + ((canvas_w - (card_margin * 2) - line_w) // 2)
        
        draw.text((line_x, start_y), line, fill=(255, 255, 255, 255), font=font_body)
        start_y += line_height
        
    # Branded Footer Core Call-To-Action
    draw.text((70, 950), "📢 VOICE YOUR GRIPES", fill=(255, 215, 0, 255), font=font_footer)
    draw.text((70, 990), "Log on to report daily financial loot: bit.ly/4fBg9JB", fill=(200, 200, 200, 255), font=font_footer)
    
    # Compile and output clean asset file
    final_img = img.convert("RGB")
    final_img.save("launchpad/today_graphic.png", "PNG")
    print("Successfully built and saved a brand-new social media graphic canvas completely from scratch!")
    
except Exception as e:
    print(f"Generative graphics architecture error: {e}")
