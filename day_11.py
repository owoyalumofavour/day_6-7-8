from fastapi import FastAPI, HTTPException, status
from sqlalchemy.orm import sessionmaker
from day_6_database import engine
from item_model import Item
from pydantic import BaseModel
from typing import Optional, List

day_11app = FastAPI(title="Day 11 Challenge - DELETE Endpoint")


Session = sessionmaker(bind=engine)


@day_11app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int):
    """
    Delete an item by its ID.
    Returns 204 No Content on success, 404 if not found.
    """
    session = Session()
    try:
        # locate the record by ID
        item = session.query(Item).filter(Item.id == item_id).first()
        
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        
        # perform hard delete
        session.delete(item)
        session.commit()
        
        # no content returned – just 204 status
        return
        
    except HTTPException:
        session.rollback()
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()

class ItemOut(BaseModel):
    id: int
    name: str
    price: float
    
    model_config = {"from_attributes": True}

# used to get the item by id to confirm it exixts before deleting
@day_11app.get("/items/{item_id}", response_model=ItemOut)
async def get_item(item_id: int):
    session = Session()
    try:
        item = session.query(Item).filter(Item.id == item_id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        return item
    finally:
        session.close()