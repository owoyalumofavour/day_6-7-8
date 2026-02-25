from day_6_database import engine
from item_model import Base

def migration():
    """Create the tables in the database"""
    print("Running migration")
    Base.metadata.create_all(bind=engine) # creates the tables whose schema is defined in the item_models using the engine 
    print("Table created sucessfully")

if __name__ =="__main__":
    migration()