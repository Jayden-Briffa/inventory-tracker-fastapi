from fastapi import FastAPI, Depends, Request
import schemas
import models
from db import get_db
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
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

@app.post(f"{apiRoute}items/", response_model=schemas.ItemResponse)
async def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    db_item = models.Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

