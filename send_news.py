from langchain.chat_models import init_chat_model
import os
import requests
from send_email import send_email
import database
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
gmail_app_password = os.getenv("gmail_app_password")




def fetch_news():
    url = (
    "https://newsapi.org/v2/everything?"
    "q=world OR politics OR technology OR business&"
    "language=en&"
    "pageSize=20&"
    "sortBy=publishedAt&apiKey=" + NEWS_API_KEY)

    # Make request
    request = requests.get(url)

    # Get a dictionary with data
    content = request.json()
   
    if "articles" not in content:
        print("API Error:", content)
        exit()
    articles = content["articles"]
    return articles


# AI summarizing the news
def summarize_news(headlines):
    model = init_chat_model(
    model="gemini-2.5-flash",
    model_provider="google-genai",
    api_key=GOOGLE_API_KEY
    )

    prompt = f"""
You are a news analyst.

Summarize today's major news headlines in 2 short paragraphs.

In the second paragraph explain the possible impact on business, markets, and society.

Headlines:
{headlines}
"""
    response = model.invoke(prompt)
    response_str = response.content
    headlines_text = "• " + "\n• ".join(headlines)

    body = f"""
TOP HEADLINES

{headlines_text}

--------------------------------

AI SUMMARY

{response_str}

--------------------------------

To unsubscribe:
http://127.0.0.1:8000/unsubscribe
"""

    
    return body



def send_newsletter(body):
    subscribers = database.get_subscribers()

    for subscriber in subscribers:
     email = subscriber[1]
     send_email(
             receiver=email,
            message=body
        )
     print(f"Sent to {email}")

articles = fetch_news()

headlines = []

for article in articles:
    headlines.append(article["title"])

print(headlines)
headlines_text = "• " + "\n• ".join(headlines)

print(headlines_text)
body = summarize_news(headlines)

send_newsletter(body)
        