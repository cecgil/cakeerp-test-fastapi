from sqlalchemy.orm import Session

from fastapi import FastAPI, Depends, HTTPException

from models import Base
from typing import List
from schemas import SchemaItem, SchemaItemCreate, UpdateItem
from database import get_db, engine
from crud import delete_item, get_items, get_item, create_item, update_item

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/status")
def status():
    return {"message": "ok"}

@app.get("/items", response_model = List[SchemaItem])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = get_items(db, skip=skip, limit=limit)
    if items is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return items

@app.get("/items/{item_id}", response_model = SchemaItem)
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = get_item(db=db, item_id = item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


@app.post("/items", response_model=SchemaItem)
def post_item(item:SchemaItemCreate, db:Session=Depends(get_db)):
    return create_item(db=db, item=item)

@app.put("/items/{item_id}", response_model=SchemaItem)
def update_item_1(item_id: int, update_param: UpdateItem, db: Session = Depends(get_db)):
    items =  get_item(db=db, item_id = item_id)
    if not items:
        raise HTTPException(status_code = 400, detail="No record found to update")
    return update_item(db=db, details=update_param, item_id = item_id)


@app.delete("/items/{item_id}", response_model=SchemaItem)
def delete_item_1(item_id: int, db: Session = Depends(get_db)):
     return delete_item(db=db, item_id=item_id)

    
