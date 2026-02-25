from sqlalchemy.orm import sessionmaker
from day_6_database import engine
from item_model import item

def insert_records():
    """Insert 5 sample records"""
    
    # Creating a session
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Create 5 sample items
        items = [
            item(
                name="360 Office Chair",
                description="Ergonomic office chair with wheels, S-curve",
                price=7500.00
            ),
            item(
                name="API England Extension box",
                description="20V extension box with five ports and surge protection",
                price=12000.00
            ),
            item(
                name="Hisense Standing Fan",
                description="Solar chargeable, eco-friendly",
                price=100500.00
            ),
            item(
                name="Stylish Pen",
                description="Good grip",
                price=500.00
            ),
            item(
                name="Beauty Water Bottle",
                description="3-in-1, comes with handle",
                price=8000.00
            )
        ]
        
        # Add all items to session
        session.add_all(items)
        
        # Commit the transaction
        session.commit()
        
        print("="*50)
        print("You have successfully inserted records!")
        print("="*50)
        
        # Count and display total records
        count = session.query(item).count()
        print(f"Total records in the database: {count}")
        
    except Exception as e:
        print(f"Error inserting records: {e}")
        session.rollback()
        
    finally:
        session.close()
        print("Database session closed")

# Call the function
if __name__ == "__main__":
    insert_records()
