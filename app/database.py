from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
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

