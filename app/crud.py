from http.client import HTTPException
from shutil import ExecError
from sqlalchemy.orm import Session



from models import Item 
from schemas import SchemaItem, SchemaItemCreate, UpdateItem



def get_items(db: Session, skip: int = 0, limit: int = 100):
    try:
        db.query(Item).offset(skip).limit(limit).all()
    except Exception as e:
        raise(e)
    return db.query(Item).offset(skip).limit(limit).all()

def get_item(db: Session, item_id: int):
    try:
        db.query(Item).filter(Item.id == item_id).first()
    except Exception as e:
        raise(e)
        
    return db.query(Item).filter(Item.id == item_id).first()

def create_item(db: Session, item: SchemaItemCreate):
    db_item = Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    return db_item

def update_item(db: Session, item_id: int, details: UpdateItem):

    item = db.query(Item).filter(Item.id == item_id).first()

    if item is None:
        return None

    db.query(Item).filter(Item.id == item_id).update(vars(details))
    db.commit()
    return db.query(Item).filter(Item.id == item_id).first()
        

def delete_item(db: Session, item_id: int):
    try:
        db.query(Item).filter(Item.id == item_id).delete()
        db.commit()
    except Exception as e:
        raise(e)
    return{"delete status": "Sucess"}
