from sqlalchemy.orm import Session
from models import User,Post
from schemas import Create_User,Update_User


def get_user(db:Session,user_id=User.id):
    """ Makes a query to the datbase get the user's id. 

    Args:
        db (Session): A database session.
        user_id (int)): An id from the User's table. 

    Returns:
        _type_: A query to database
    """
    return db.query(User).filter(User.id == user_id).first()
    
def get_users(db:Session, skip: int, limit: int):
    """ Makes a query to get all user by passing 
    query parameters (skip and limit)

    Args:
        db (Session): Database session
        skip (int): Starts from n items
        limit (int): Returns n items 

    Returns:
        _type_: A query to database.
    """
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db:Session,Create_User):
    """ Creates an user
        If the user have less than 15 years old, it will raise an
        exception.

    Args:
        db (Session): Database session
        Create_User (class): Schema's response to create an user.

    Returns:
        _type_: Returns a query to database.
    """
    user=User(name = Create_User.name,age = Create_User.age,
           email = Create_User.email)
    
    if user.age < 15:
        return None
    else:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

def update_user(db:Session,update_u:Update_User,id:int):
    user=db.query(User).filter(User.id==id).first()
    
    if user is None:
        return None
    
    user.name = update_u.name
    user.age = update_u.age
    user.email = update_u.email
    
    db.commit()
    db.refresh(user)
    
    
    
    