# 🤖 AI News Summarizer

This project automatically collects the latest AI news, summarizes it using Google's Gemini API, and sends a daily email newsletter to subscribed users.

I built this project to learn how AI APIs can be integrated into a real-world web application. Along the way, I also explored email automation, user authentication with OTP, PostgreSQL, and FastAPI deployment.

---

## ✨ Features

- Fetches the latest AI news
- Generates AI-powered summaries using Gemini
- Sends daily newsletters via email
- Email verification using OTP
- Resend OTP support
- Email validation
- Subscribe & Unsubscribe functionality
- PostgreSQL database
- Admin login with session authentication
- Admin dashboard
- Search subscribers
- Remove subscribers
- Daily newsletter automation using APScheduler

---

## 🛠 Tech Stack

- **Backend:** FastAPI
- **Database:** PostgreSQL
- **AI:** Google Gemini API
- **Scheduler:** APScheduler
- **Frontend:** HTML, CSS, Jinja2
- **Email:** Gmail SMTP
- **Deployment:** Render

---

## 📂 Project Structure

```
AI_News_Summarizer/

├── postgres_database/
├── templates/
├── main.py
├── send_news.py
├── send_email.py
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

Clone the repository

```bash
git clone <your-repo-url>
```

Move into the project

```bash
cd AI_News_Summarizer
```

Create a virtual environment

```bash
python -m venv venv
```

Activate it

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the project

```bash
uvicorn main:app --reload
```

---

## 🔑 Environment Variables

Create a `.env` file and add:

```env
DATABASE_URL=

EMAIL_ADDRESS=

gmail_app_password=

GEMINI_API_KEY=

SECRET_KEY=

ADMIN_USERNAME=

ADMIN_PASSWORD=
```

---

## 📸 Screenshots

I'll be adding screenshots of the application here.

- Home Page
- OTP Verification
- Admin Login
- Admin Dashboard
- Newsletter Email

---

## 💡 What I Learned

While building this project, I learned:

- Building REST APIs with FastAPI
- Working with PostgreSQL
- Sending emails using SMTP
- OTP-based email verification
- Session-based authentication
- Integrating Google's Gemini API
- Scheduling background jobs with APScheduler
- Deploying a FastAPI application on Render

---

## 🔮 Future Improvements

Some ideas I'd like to explore in the future:

- Newsletter history
- Analytics dashboard
- Category-wise AI news
- Better admin analytics

---

## 👨‍💻 About

This project was built as part of my journey into AI-powered web applications. The goal was not only to use an LLM API, but also to understand how AI features fit into a complete production-style application.
