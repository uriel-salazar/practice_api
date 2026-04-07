from sqlalchemy.orm import Session
from .models import User,Post
from .schemas import Create_User,Update_User,Create_Post,Response_Post
from .auth import hash_password

def get_user(db: Session, user_id=User.id):
    """Gets a single user by their ID.

    Args:
        db (Session): A database session.
        user_id (int): The user's ID.

    Returns:
        User: The matching user, or None if not found.
    """
    return db.query(User).filter(User.id == user_id).first()


def get_users(db: Session, skip: int, limit: int):
    """Gets a list of users with pagination.

    Args:
        db (Session): A database session.
        skip (int): Number of records to skip.
        limit (int): Maximum number of records to return.

    Returns:
        list[User]: A list of users.
    """
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, Create_User):
    """Creates a new user. Users under 15 years old will not be created.

    Args:
        db (Session): A database session.
        Create_User (CreateUser): The schema containing the user's data.

    Returns:
        User: The newly created user, or None if the age requirement isn't met.
    """
    user = User(
        name=Create_User.name, 
        age=Create_User.age ,
        email=Create_User.email.lower(), # lowers email to lowercase 
        hashed_password=hash_password(Create_User.password)
        )

    if user.age < 15:
        return None
    else:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user


def update_user(db: Session, update_u: Update_User, id: int):
    """Updates an existing user by their ID.

    Args:
        db (Session): A database session.
        update_u (Update_User): The schema containing the updated data.
        id (int): The ID of the user to update.

    Returns:
        User: The updated user, or None if the user wasn't found.
    """
    user = db.query(User).filter(User.id == id).first()

    if user is None:
        return None

    user.name = update_u.name
    user.age = update_u.age
    user.email = update_u.email

    db.commit()
    db.refresh(user)
    return user

def delete_user(db:Session,id:int):
    delete=db.query(User).filter(User.id==id).first()
    if delete is None:
        return None
    
    if delete:
        db.delete(delete)
        db.commit()
        db.refresh
    return delete

def create_post(db: Session,description:str,image_url:str,
    user_id:int) -> Post:
    new_post = Post(
        description=description,
        image_url=image_url,
        user_id=user_id
    )
   
    

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

def get_post(db:Session,id:int):
    
    get=db.query(Post).filter(Post.user_id==id).first()
    return get


def get_posts(db:Session,skip:int,limit:int):
    posts=db.query(Post).offset(skip).limit(limit).all()

    return posts
    
