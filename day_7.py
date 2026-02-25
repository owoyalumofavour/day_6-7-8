from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import sessionmaker
from day_6_database import engine
from item_model import item 
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

# Create FastAPI app
day_7app = FastAPI(title="API for items")

# Enable CORS
day_7app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Database session
Session = sessionmaker(bind=engine)

# Pydantic models for response
class ItemResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    created_at: Optional[datetime] = None

    # Enable ORM mode for Pydantic v2
    model_config = {
        "from_attributes": True
    }

class ItemsResponse(BaseModel):
    status: str
    message: str
    data: List[ItemResponse]
    count: int

# Root endpoint
@day_7app.get("/", tags=["Root"])
async def home():
    return {
        "message": "Welcome to the Items API",
        "endpoints": {
            "/items": "GET - Retrieve all items",
            "/items/{id}": "GET - Retrieve single item",
            "/docs": "Swagger UI Documentation"
        }
    }

# GET all items
@day_7app.get("/items", response_model=ItemsResponse, tags=["Items"])
async def get_all_items():
    session = Session()
    try:
        # Query all items using the model class 'item'
        db_items = session.query(item).all()
        items_list = []
        for it in db_items: # use 'it' instead of 'item' to avoid shadowing
            items_list.append(ItemResponse(
                id=it.id,
                name=it.name,
                description=it.description,
                price=float(it.price),
                created_at=it.created_at
            ))
        return {
            "status": "success",
            "message": f"Retrieved {len(items_list)} items",
            "data": items_list,
            "count": len(items_list)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()

# GET single item by ID
@day_7app.get("/items/{item_id}", response_model=ItemResponse, tags=["Items"])
async def get_single_item(item_id: int):
    session = Session()
    try:
        # Use a different variable name for the result
        db_item = session.query(item).filter(item.id == item_id).first()
        if db_item:
            return ItemResponse(
                id=db_item.id,
                name=db_item.name,
                description=db_item.description,
                price=float(db_item.price),
                created_at=db_item.created_at
            )
        else:
            raise HTTPException(status_code=404, detail=f"Item with id {item_id} not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()