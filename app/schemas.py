from pydantic import BaseModel,Field,EmailStr
from pydantic import BaseModel,Field,EmailStr



class Create_User(BaseModel):
    """ A Pydantic model that check users email, age and email. 
    
    Attributes:
        id (int): Unique identifier of the user.
        age (int): Age of the user. Must be greater than 15 and less than 120.
        name (str): Full name of the user.
        email (str): Email address of the user.
    
    """
    
    name : str =Field(...,min_length=3,max_length=40)
    # An age greater between 15 and 120 years old 
    age : int = Field(..., gt=15,le=120)
    password: str=Field(...,min_length=8)
    email : EmailStr
       
    
class UserPublic(BaseModel):
    """
    Represents a user in API responses.

    Attributes:
        id (int): Unique identifier of the user.
        age (int): Age of the user. Must be greater than 15 and less than 120.
        name (str): Full name of the user.
        email (str): Email address of the user.
    """
    """
    Represents a user in API responses.

    Attributes:
        id (int): Unique identifier of the user.
        age (int): Age of the user. Must be greater than 15 and less than 120.
        name (str): Full name of the user.
        email (str): Email address of the user.
    """
    id : int
    age:int
    name : str
    email : str

class UserPrivate(UserPublic):
    email:EmailStr
    
class Update_User(BaseModel):
    """ Pydantic model for updating.

    Args:
        BaseModel (class): A base class for creating pydantic models. 
    """
    name:str = Field(...,min_length=3,max_length=30)
    age:int = Field(..., gt=15,le=120)
    email:EmailStr

class Create_Post(BaseModel):
      description:str
      user_id:int

class Response_Post(BaseModel):
    id : int
    description : str | None = None
    user_id : int
    class Config():
        from_attributes = True
        
class Token(BaseModel):
    access_token: str
    token_type: str
    
