from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import sessionmaker
from typing import List
from pydantic import BaseModel

# Importing my database and model
from day_6_database import engine
from item_model import Item

# Creating the app
day_8app = FastAPI(title="Day 8 - DTO Example")

# Optional CORS
day_8app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Database session factory
Session = sessionmaker(bind=engine)

# --- DTO Models ---
class ItemOut(BaseModel):
    id: int
    name: str
    price: float

    model_config = {
        "from_attributes": True # Allows creation from SQLAlchemy model
    }

class ItemsOut(BaseModel):
    status: str
    message: str
    data: List[ItemOut]
    count: int

# --- Endpoint ---
@day_8app.get("/items", response_model=ItemsOut)
async def get_all_items():
    session = Session()
    try:
        items = session.query(Item).all()
        # Convert each Item to ItemOut (only id, name, price)
        items_out = [ItemOut.model_validate(item) for item in items]
        return {
            "status": "success",
            "message": f"Retrieved {len(items_out)} items",
            "data": items_out,
            "count": len(items_out)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()

# Optional: root endpoint
@day_8app.get("/")
async def root():
    return {"message": "Day 8: DTO Example – GET /items returns only id, name, price"}