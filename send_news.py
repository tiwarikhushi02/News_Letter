
from langchain.chat_models import init_chat_model
import os
import requests
from send_email import send_email
from postgres_database import database
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

    # Plain text headlines
    headlines_text = "• " + "\n• ".join(headlines)

    # HTML headlines
    headlines_html = ""

    for headline in headlines:
        headlines_html += f"<li>{headline}</li>"

    # Plain text email
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

    # HTML email
    html_body = f"""
<html>
<body style="
font-family: Arial, sans-serif;
max-width:700px;
margin:auto;
padding:20px;
background-color:#f8fafc;
">

<h1 style="color:#2563eb;">
📰 AI-Powered Daily News Digest
</h1>

<p style="color:#666;">
Your daily AI-generated news briefing
</p>

<hr>

<h2>Top Headlines</h2>

<div style="
background:white;
padding:15px;
border-radius:10px;
box-shadow:0 2px 5px rgba(0,0,0,0.1);
">
<ul>
{headlines_html}
</ul>
</div>

<br>

<h2>AI Summary</h2>

<div style="
background:#eef6ff;
padding:15px;
border-radius:10px;
line-height:1.6;
">
{response_str}
</div>

<br>

<hr>

<p>
<a
href="http://127.0.0.1:8000/unsubscribe"
style="
background:#ef4444;
color:white;
padding:10px 16px;
text-decoration:none;
border-radius:6px;
">
Unsubscribe
</a>
</p>

</body>
</html>
"""

    return body, html_body



def send_newsletter(body, html_body):
    subscribers = database.get_subscribers()

    for subscriber in subscribers:
        email = subscriber[1]

        send_email(
            receiver=email,
            message=body,
            html=html_body
        )

        print(f"Sent to {email}")

def run_daily_newsletter():
    articles = fetch_news()

    with open("task_log.txt", "a") as f:
        f.write("News Fetched\n")

    headlines = []

    for article in articles:
        headlines.append(article["title"])

    print(headlines)
    headlines_text = "• " + "\n• ".join(headlines)

    print(headlines_text)
    body, html_body = summarize_news(headlines)

    send_newsletter(body, html_body)

if __name__ == "__main__":
    run_daily_newsletter()


        