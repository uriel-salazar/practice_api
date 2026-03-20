from sqlalchemy.orm import Session
from models import User,Post


def get_users(db:Session,user_id=User.id):
    """ Makes a query to the datbase get the user's id. 

    Args:
        db (Session): A database session.
        user_id (int)): An id from the User's table. 

    Returns:
        _type_: A query to get id.
    """
    return db.query(User).filter(User.id == user_id).first()
    
    