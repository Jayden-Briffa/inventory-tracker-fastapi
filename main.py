from fastapi import FastAPI, Depends
import models
from db import get_db
from sqlalchemy.orm import Session

app = FastAPI()

@app.post("/items/", response_model=models.ItemResponse)
async def create_item(item: models.ItemCreate, db: Session = Depends(get_db)):
    db_item = models.Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

