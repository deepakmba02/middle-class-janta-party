import os
import urllib.parse
import xml.etree.ElementTree as ET
import google.generativeai as genai
import requests
from datetime import datetime
from PIL import Image

# 1. Initialize Gemini
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

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

# 2. Get today's real context
today_news = fetch_latest_bangalore_news()

# 3. Ask Gemini to write a completely custom tweet based on reality
date_str = datetime.now().strftime("%d %B %Y")
prompt = f"""
You are the voice of the Middle Class Janta Party (MCJP). Today is {date_str}.
Here are the latest trending issues and news regarding the cost of living squeeze in Bengaluru:
{today_news}

Write a raw, intense, punchy X tweet (under 190 characters) reacting to these frustrations (rent hikes, eating out costs, 5% GST on bills, or daily expense stress). 
Do not look corporate or repetitive. Sound like a real citizen who has had enough.
Include the hashtags #Bangalore #GST. Do not include any links.
"""

response = model.generate_content(prompt)
tweet_content = f"{response.text}\n\n📊 Track the math live & report today's loot:\n👉 https://bit.ly/4fBg9JB"

# 4. Save to your launchpad folder
os.makedirs("launchpad", exist_ok=True)
with open("launchpad/today_tweet.txt", "w", encoding="utf-8") as f:
    f.write(tweet_content)

# 5. Handle the image template copy
try:
    img = Image.open("mcjp_graphic.png") # Make sure your master graphic is saved in your root folder!
    img.save("launchpad/today_graphic.png")
    print("Successfully cooked today's post in the launchpad!")
except Exception as e:
    print(f"Image error: {e}")
