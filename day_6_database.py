from sqlalchemy import create_engine

#this creates a file called items.db in the folder
DATABASE_URL = "sqlite:///Items.db"

engine = create_engine(DATABASE_URL, echo=True)

print("Connection  Created")