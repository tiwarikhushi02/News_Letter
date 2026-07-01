from sched import scheduler
from contextlib import asynccontextmanager

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



@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )

@app.post("/subscribe")
def subscribe(request:Request, email:str=Form(...)):
    success = add_subscriber(email)
    if success:
        return templates.TemplateResponse(
            request=request,
            name="success.html"
        )
    else:
        return templates.TemplateResponse(
            request=request,
            name="user_exist.html"
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
