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

print("NEWS_API_KEY:", NEWS_API_KEY)
print(type(NEWS_API_KEY))


def fetch_news():
    url = (
    "https://newsapi.org/v2/top-headlines?"
    "category=business&"
    "language=en&"
    "pageSize=8&"
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

articles = fetch_news()



# AI summarizing the news
def summarize_news(articles):
    model = init_chat_model(
    model="gemini-2.5-flash",
    model_provider="google-genai",
    api_key=GOOGLE_API_KEY
    )

    prompt = f"""
    You're a news summarizer.
    Write a short paragraph analyzing those news.
    Add another second paragraph to tell me
    how they affect the stock market.
    Here are the news articles:
    {articles}
    """
    response = model.invoke(prompt)
    response_str = response.content

    body = "Subject: News Summary\n\n" + response_str + "\n\n"

    body = body.encode("utf-8")
    return body

body = summarize_news(articles)

def send_newsletter(body):
    subscribers = database.get_subscribers()

    for subscriber in subscribers:
     email = subscriber[1]
     send_email(
             receiver=email,
            message=body
        )
     print(f"Sent to {email}")
send_newsletter(body)
        