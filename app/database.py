from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,DeclarativeBase
import os


load_dotenv()
"""loads all my environment variables"""

# Gets database URL. 
url = os.environ.get("DATABASE_URL")


if url:
    #database connection
    engine = create_engine(url, echo=True)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
else:
    print("NO DATABASE")


class Base(DeclarativeBase):
    pass

# Function for -dependency injection -
def get_db():
    """ Dependency injection for database 

    Yields:
        db: Session()
    """
    db=SessionLocal() # A database session created.
    
    try: 
        yield db # It's injected to whoever needs it.
        
    finally: #Then, we close the database session.
        db.close()