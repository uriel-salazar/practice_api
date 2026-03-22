from pydantic import BaseModel,Field,EmailStr


class Create_User(BaseModel):
    """ A Pydantic model that check users email, age
    and validate if their name is above 15.

    Args:
        BaseModel (class): A base class for creating pydantic models. 
    """
    name : str 
    age : int = Field(..., gt=15)
    email : EmailStr
    
    
class User_Response(BaseModel):
    id : int
    age:int
    name : str
    email : str
    
class Update_User(BaseModel):
    name:str
    age:int = Field(..., gt=15)
    email:EmailStr
    