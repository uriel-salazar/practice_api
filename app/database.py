from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from models import Session
import os

load_dotenv()
"""loads all my environment va"""

# Gets database URL. 
url = os.environ.get("DATABASE_URL")

if url:
    #database connection
    engine = create_engine(url, echo=True)

else:
    print("Naoo")


class Base(DeclarativeBase):
    pass

# Function for -dependency injection -
def get_db():
    """ Dependency injection for database 

    Yields:
        db: Session()
    """
    db=Session() # A database session created.
    
    try: 
        yield db # It's injected to whoever needs it.
        
    finally: #Then, we close the database session.
        db.close()