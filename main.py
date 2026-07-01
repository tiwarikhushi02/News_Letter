from sched import scheduler
from contextlib import asynccontextmanager
import random

from fastapi.responses import RedirectResponse
from send_email import send_otp_email
from postgres_database.database import (
    add_subscriber,
    get_latest_subscribers,
    get_subscribers,
    get_total_subscribers,
    get_total_pending,
    init_db,
    remove_subscriber,
    save_otp,
    verify_otp,
    delete_pending_verification,
    subscriber_exists,
)
from postgres_database.database import admin_remove_subscriber
import re
from starlette.middleware.sessions import SessionMiddleware
import os
from postgres_database.database import search_subscriber

from postgres_database.database import (
    add_subscriber,
    get_subscribers,
    init_db,
    remove_subscriber
)
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from send_news import run_daily_newsletter


scheduler = AsyncIOScheduler()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ensure database tables exist
    init_db()
    
    # Schedule sending daily newsletter email at 6:00 AM local time
    scheduler.add_job(
        run_daily_newsletter,
        CronTrigger(hour=6, minute=0),
        id="daily_newsletter_job",
        replace_existing=True
    )
    scheduler.start()
    print("Scheduler started. Daily newsletter job scheduled for 6:00 AM.")
    yield
    scheduler.shutdown()
    print("Scheduler shut down.")

app = FastAPI(lifespan=lifespan)
templates = Jinja2Templates(directory="templates")

app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SECRET_KEY")
)



@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )

def is_valid_email(email):

    email_pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'

    return re.match(email_pattern, email)

@app.post("/subscribe")
def subscribe(request: Request, email: str = Form(...)):
    email = email.strip().lower()
    if not is_valid_email(email):
        return templates.TemplateResponse(
            request=request,
            name="invalid_email.html"
        )

    if subscriber_exists(email):
        return templates.TemplateResponse(
            request=request,
            name="user_exist.html"
        )

    otp = str(random.randint(100000, 999999))

    save_otp(email, otp)

    send_otp_email(email, otp)

    return templates.TemplateResponse(
        request=request,
        name="verify.html",
        context={
            "email": email
        }
    )

@app.post("/verify")
def verify(
    request: Request,
    email: str = Form(...),
    otp: str = Form(...)
):

    user = verify_otp(email, otp)

    if user:

        add_subscriber(email)

        delete_pending_verification(email)

        return templates.TemplateResponse(
            request=request,
            name="success.html"
        )

    return templates.TemplateResponse(
    request=request,
    name="verify.html",
    context={
        "email": email,
        "error": "Invalid or expired OTP. Please try again."
    }
)

@app.post("/resend-otp")
def resend_otp(
    request: Request,
    email: str = Form(...)
):

    otp = str(random.randint(100000, 999999))

    save_otp(email, otp)

    send_otp_email(email, otp)

    return templates.TemplateResponse(
    request=request,
    name="verify.html",
    context={
        "email": email,
        "message": "A new OTP has been sent to your email."
    }
)
    
@app.get("/unsubscribe")
def unsubscribe(request:Request):
    return templates.TemplateResponse(
        request=request,
        name="unsubscribe.html",
    )    
    
@app.post("/unsubscribe")
def unsubscribe(request:Request, email:str=Form(...)):
    success=remove_subscriber(email)
    if success:
        return templates.TemplateResponse(
            request=request,
            name="unsubscribe_success.html"
        )
    else:
        return templates.TemplateResponse(
            request=request,
            name="unsubscribe_failure.html"
        )

@app.get("/dashboard")
def dashboard(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "total_subscribers": get_total_subscribers(),
            "pending": get_total_pending(),
            "latest_subscribers": get_latest_subscribers(),
            "status": "Running",
            "schedule": "Every Day - 6:00 AM"
        }
    )

@app.get("/admin")
def admin(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="admin_login.html"
    )

@app.post("/admin/login")
def admin_login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):

    if (
        username == os.getenv("ADMIN_USERNAME")
        and
        password == os.getenv("ADMIN_PASSWORD")
    ):

        request.session["admin"] = True

        return RedirectResponse(
            url="/dashboard",
            status_code=303
        )

    return templates.TemplateResponse(
        request=request,
        name="admin_login.html",
        context={
            "error": "Invalid username or password."
        }
    )
@app.get("/dashboard")
def dashboard(request: Request):

    if not request.session.get("admin"):

        return RedirectResponse(
            url="/admin",
            status_code=303
        )

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "total_subscribers": get_total_subscribers(),
            "pending": get_total_pending(),
            "latest_subscribers": get_latest_subscribers(),
            "status": "Running",
            "schedule": "Every Day - 6:00 AM"
        }
    )
@app.post("/search-subscriber")
def search_subscriber_route(
    request: Request,
    email: str = Form(...)
):

    if not request.session.get("admin"):
        return RedirectResponse(url="/admin", status_code=303)

    user = search_subscriber(email.strip().lower())

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "total_subscribers": get_total_subscribers(),
            "pending": get_total_pending(),
            "latest_subscribers": get_latest_subscribers(),
            "status": "Running",
            "schedule": "Every Day - 6:00 AM",
            "search_result": user,
            "searched": True
        }
    )

@app.post("/remove-subscriber")
def remove_subscriber_route(
    request: Request,
    email: str = Form(...)
):

    if not request.session.get("admin"):
        return RedirectResponse(url="/admin", status_code=303)

    success = admin_remove_subscriber(email.strip().lower())

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "total_subscribers": get_total_subscribers(),
            "pending": get_total_pending(),
            "latest_subscribers": get_latest_subscribers(),
            "status": "Running",
            "schedule": "Every Day - 6:00 AM",
            "removed": success,
            "searched": False
        }
    )