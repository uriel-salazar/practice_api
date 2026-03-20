from sqlalchemy.orm import Session
from models import User,Post


def get_user(db:Session,user_id=User.id):
    """ Makes a query to the datbase get the user's id. 

    Args:
        db (Session): A database session.
        user_id (int)): An id from the User's table. 

    Returns:
        _type_: A query to get id.
    """
    return db.query(User).filter(User.id == user_id).first()
    
def get_users(db:Session, skip: int=0, limit: int=10):
    return db.query(User).offset(skip).limit(limit).all()
    pass
