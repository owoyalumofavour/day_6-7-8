from sqlalchemy import Column, Integer, String, Text, Numeric, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

#creating a base class for the item models
Base = declarative_base()

#defining class and schema for the item models 
class Item(Base):
    __tablename__ = 'Items'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name= Column(String(100), nullable=False)
    description= Column(Text)
    price=Column(Numeric(10,2))
    created_at=Column(DateTime, default=datetime.now)

def __repr__(self):
    """Reprsentation of the Item models"""
    return f"<Item(id={self.id}, name={self.name}, price={self.price}, description={self.description}, created_at={self.created_at})>"
