from database import add_subscriber, get_subscribers, init_db
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse



app = FastAPI()
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