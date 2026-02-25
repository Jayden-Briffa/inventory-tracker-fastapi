from fastapi import FastAPI, Depends, Request
import models
from db import get_db
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
apiRoute = "/api/"
viewRoute = "/"

templates = Jinja2Templates(directory="templates")
@app.get(f"{viewRoute}", response_class=HTMLResponse)
async def page_home(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "message": "Hello, world!",
    })

@app.post(f"{apiRoute}items/", response_model=models.ItemResponse)
async def create_item(item: models.ItemCreate, db: Session = Depends(get_db)):
    db_item = models.Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

