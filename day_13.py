from fastapi import FastAPI, HTTPException, status, Query
from sqlalchemy.orm import sessionmaker
from day_6_database import engine
from item_model import Item
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

day_13app=FastAPI(title="Day 13 Challenge: Pagination and Filtering")

Session = sessionmaker(bind=engine)
session = Session()
items=[]
#adding  more items to the existing databas4
class ItemOut(BaseModel):
    id: int
    name: str
    price: float
    
    model_config = {"from_attributes": True}

#pagination
class Pagination(BaseModel):
    status: str
    message: str
    data: List[ItemOut]
    total: int
    page: int
    limit: int
    pages: int

@day_13app.get("/items", response_model=Pagination)
async def get_items(
    
    page: int = Query(1, ge=1, description="Page number (starts at 1)"),
    limit: int = Query(10, ge=1, le=10, description="Items per page")
):
    """
    Retrieve all items with pagination.
    
    This endpoint returns a paginated list of all items in the database.
    Use the page and limit parameters to control how many items are returned.
    
    Parameters:
    - **page**: Page number (default: 1, starts at 1)
    - **limit**: Number of items per page (default: 10, maximum: 100)
    
    Returns:
    - **200 OK**: Success with paginated list of items
    - **500 Internal Server Error**: Database error occurred
    
    The response includes metadata:
    - total: Total number of items in database
    - page: Current page number
    - limit: Items per page
    - pages: Total number of pages
    - data: Array of items for this page
    """
    session = Session()
    try:
        # Calculate offset
        offset = (page - 1) * limit
        
        # Get total count for metadata
        total = session.query(Item).count()
        
        # Get paginated items
        items = session.query(Item).offset(offset).limit(limit).all()
        
        # Calculate total pages
        pages = (total + limit - 1) // limit # Ceiling division
        
        # Convert to DTOs
        items_out = [ItemOut.model_validate(item) for item in items]
        
        return {
            "status": "success",
            "message": f"Retrieved {len(items_out)} items",
            "data": items_out,
            "total": total,
            "page": page,
            "limit": limit,
            "pages": pages
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()

@day_13app.get("/items/filter", response_model=Pagination)
async def filter_items(
    # Pagination parameters
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    
    # Filter parameters
    min_price: Optional[float] = Query(None, ge=0, description="Minimum price"),
    max_price: Optional[float] = Query(None, ge=0, description="Maximum price"),
    name_contains: Optional[str] = Query(None, description="Search in name"),
    category: Optional[str] = Query(None, description="Filter by category")
):  
   
    """
    Filter items by various criteria with pagination.
    
    This endpoint allows searching and filtering items based on price and name.
    All filter parameters are optional and can be combined.
    
    Parameters:
    - **min_price** (query): Minimum price (inclusive)
    - **max_price** (query): Maximum price (inclusive)
    - **name_contains** (query): Text to search for in item names
    - **page** (query): Page number (default: 1)
    - **limit** (query): Items per page (default: 10, max: 100)
    
    Returns:
    - **200 OK**: Success with filtered and paginated items
    - **500 Internal Server Error**: Database error occurred
    
    Example:
    GET /items/filter?min_price=2000&max_price=5000&page=2&limit=5
    Returns first 5 items priced between 2000 and 5000
    """
    session = Session()
    try:
        # Start with base query
        query = session.query(Item)
        
        # Apply filters
        if min_price is not None:
            query = query.filter(Item.price >= min_price)
        
        if max_price is not None:
            query = query.filter(Item.price <= max_price)
        
        if name_contains:
            query = query.filter(Item.name.contains(name_contains))
        
        if category:
            # Assuming category is part of the name for demo purposes
            # In a real app, you'd have a category field
            query = query.filter(Item.name.contains(category))
        
        # Get total count after filters
        total = query.count()
        
        # Apply pagination
        offset = (page - 1) * limit
        items = query.offset(offset).limit(limit).all()
        
        pages = (total + limit - 1) // limit
        
        items_out = [ItemOut.model_validate(item) for item in items]
        
        return {
            "status": "success",
            "message": f"Retrieved {len(items_out)} items",
            "data": items_out,
            "total": total,
            "page": page,
            "limit": limit,
            "pages": pages,
            "filters_applied": {
                "min_price": min_price,
                "max_price": max_price,
                "name_contains": name_contains,
                "category": category
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()